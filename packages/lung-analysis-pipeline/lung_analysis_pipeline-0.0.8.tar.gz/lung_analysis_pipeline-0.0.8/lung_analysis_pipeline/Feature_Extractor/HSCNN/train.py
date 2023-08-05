from torch.utils.data import DataLoader, random_split
import torch.optim as optim
import matplotlib.pyplot as plt
from dataloader import HscnnDataset
import pickle
import os
import torch
import pandas as pd
import logging
import torch.nn as nn
import numpy as np
from model import HSCNN
from keras.utils import np_utils # Used only for converting true vectors to one-hot for AUC calculations
from itertools import cycle
import torch.nn.functional as F
from sklearn.metrics import confusion_matrix, precision_score, accuracy_score, recall_score, \
    roc_curve, roc_auc_score, auc
from scipy import interp
# Transforms
from torchio.transforms import (
    RandomFlip,
    RandomAffine,
    RandomMotion,
    RescaleIntensity,
    Compose,
)

LOG_FILENAME = 'HSCNN_LOG_FOLDS_01_23_2023.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO,
                    format='%(levelname)s: %(message)s')


class TrainModel:

    def __init__(self, input_channel=1, num_low_level_tasks=3, low_level_outputs=[2, 2, 2], loss_weights=[0.1, 0.1, 0.1], malignancy_class=2, num_epochs=300, batch_size=6, val_per=0.2):
        self.in_channel = input_channel
        self.num_low_level_tasks = num_low_level_tasks
        self.low_level_outputs = low_level_outputs
        self.malignancy_class = malignancy_class
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.loss_weights = loss_weights
        self.val_per = val_per
        self.device = self._get_device()
        self.thresh = 0.5

    def _get_device(self):
        train_on_gpu = torch.cuda.is_available()
        if not train_on_gpu:
            device = torch.device("cpu")
            logging.info("Running on {}".format(device))
        else:
            device = torch.device("cuda:0")
            logging.info("Running on {}".format(torch.cuda.get_device_name(0)))
        return device
	
    # make sure input data is clipped in range [-1000, 500] HU
    def _get_default_transforms(self):
        io_transforms = Compose([
            RescaleIntensity((0, 1)),  # so that there are no negative values for RandomMotion
            # RandomMotion(),
            RandomFlip(axes=(1,)),
            # RandomAffine(scales=(0.9, 1.2), degrees=(10), isotropic=False, default_pad_value='otsu', image_interpolation='bspline')
        ])
        return io_transforms

    def _weights_init(self, model):
        classname = model.__class__.__name__
        if classname.find('Conv3d') != -1:
            # model.weight.data.normal_(0.0, 0.02)
            nn.init.xavier_uniform_(model.weight,  gain=nn.init.calculate_gain('relu'))
            model.bias.data.fill_(0)
        # elif classname.find('BatchNorm3d') != -1:
            # model.weight.data.normal_(1.0, 0.02)
            # model.bias.data.fill_(0)

    def _get_HSCNN(self, in_channel, num_low_level_tasks, low_level_outputs, malignancy_class, initialize_weights=True):
        # Get the Model
        model = HSCNN(in_channel, num_low_level_tasks, low_level_outputs, malignancy_class).to(self.device)
        if initialize_weights:
            model.apply(self._weights_init)
        return model

    """
    Calculate class weights over dataset
    """
    def _class_weights(self, path_to_label, pos_weight=False):
        data = pd.read_csv(path_to_label)
        weights = {}
        for i in range(self.num_low_level_tasks + 1):
            lbl = data.iloc[:, i].value_counts()
            if pos_weight:
                pos_sample_ratio = lbl[0]/lbl[1]
                weights['task_{}_weights'.format(i + 1)] = [pos_sample_ratio]
            else:
                weight_0 = lbl[1]/(lbl[0]+lbl[1])
                weight_1 = lbl[0] / (lbl[0] + lbl[1])
                weights['task_{}_weights'.format(i+1)] = [weight_0, weight_1]
        return weights

    def _get_evaluation_metric(self, y_truth_dict, y_predicted_dict, scores_dict, each_class=False):
        label = ["Sphericity", "Texture", "Margin", "Subtlety", "Calcification", "Malignancy"]
        class_outputs = self.low_level_outputs.copy()
        class_outputs.append(self.malignancy_class)
        evaluations = {}
        for i in range(self.num_low_level_tasks+1):
            y_true = y_truth_dict['label_{}'.format(i+1)]
            one_hot_true = np_utils.to_categorical(y_true, num_classes=class_outputs[i])
            y_pred = y_predicted_dict['label_{}'.format(i+1)]
            score = np.array(scores_dict['label_{}'.format(i+1)])
            # Calculate the metrics
            t_n, f_p, f_n, t_p = confusion_matrix(y_true, y_pred).ravel()
            recall_sensitivity = recall_score(y_true, y_pred)
            #recall_sensitivity = t_p / (t_p + f_n)
            specificity = t_n / (t_n + f_p)
            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred)
            #precision = t_p / (t_p + f_p)
            #f1_score = (2 * precision * recall_sensitivity) / (precision + recall_sensitivity)
            model_auc = roc_auc_score(one_hot_true, score, average='weighted')
            evaluations[label[i]] = [accuracy, precision, recall_sensitivity, specificity, model_auc]
        return evaluations

    def _start_model(self, model, optimizer, criterions, scheduler, lbl_weights, loss_weights, train_loader=None, val_loader=None, test_loader=None, fold=0):
        if train_loader:
            train_losses, val_losses, accuracy_list, specificity_list, recall_list, f1_score_list = [], [], [], [], [], []
            valid_loss_min = np.Inf
            # Start with inital weights
            best_model_wts = False
            best_epch_at = 0
            aucs_across_folds = []
            for epoch in range(self.num_epochs):
                # Keep track of lossess
                running_train_loss, running_val_loss = 0.0, 0.0
                epoch_loss = []
                # Training loop
                for index, data in enumerate(train_loader):
                    images, labels = data['img'].to(self.device), data['label']
                    per_label_for_each_image = [labels[:, i].to(self.device, dtype=torch.long) for i in range(self.num_low_level_tasks + 1)]
                    optimizer.zero_grad()
                    output = model(images)
                    running_loss_subtask = 0
                    # Calculate loss for each sub-network
                    for i in range(self.num_low_level_tasks+1):
                        criterion = criterions['criterion_{}'.format(i+1)]
                        running_loss_subtask += criterion(output[i], per_label_for_each_image[i]) * loss_weights[i]

                    loss = running_loss_subtask / (self.num_low_level_tasks+1)
                    loss.backward()
                    optimizer.step()
                    epoch_loss.append(float(loss.item() * images.size(0)))
                    running_train_loss += float(loss.item()) * images.size(0)

                scheduler.step(np.mean(epoch_loss))
                # Validation loop
                with torch.no_grad():
                    model.eval()
                    # Store the predictions and scores
                    predicted_labels_dict = {'label_1': [], 'label_2': [], 'label_3': [], 'label_4': [], 'label_5': [], 'label_6': []}
                    true_labels_dict = {'label_1': [], 'label_2': [], 'label_3': [], 'label_4': [], 'label_5': [], 'label_6': []}
                    scores_dict = {'label_1': [], 'label_2': [], 'label_3': [], 'label_4': [], 'label_5': [], 'label_6': []}

                    for index, data in enumerate(val_loader):
                        images, labels = data['img'].to(self.device), data['label']
                        per_label_for_each_image = [labels[:, i].to(self.device, dtype=torch.long) for i in range(self.num_low_level_tasks + 1)]
                        output = model(images)
                        val_loss_subtask = 0
                        for i in range(self.num_low_level_tasks+1):
                            criterion = criterions['criterion_{}'.format(i+1)]
                            val_loss_subtask += criterion(output[i], per_label_for_each_image[i]) * loss_weights[i]
                            per_task_out = F.softmax(output[i].cpu(), dim=1)
                            top_ps, top_class = per_task_out.topk(1, dim=1)
                            predicted_labels_dict['label_{}'.format(i + 1)].extend(list(top_class.flatten().numpy()))
                            true_labels_dict['label_{}'.format(i + 1)].extend(list(per_label_for_each_image[i].cpu().numpy()))
                            scores_dict['label_{}'.format(i + 1)].extend(per_task_out.numpy().tolist())
                        loss = val_loss_subtask / (self.num_low_level_tasks + 1)
                        running_val_loss += float(loss.item()) * images.size(0)

                model.train()
                train_loss = running_train_loss/len(train_loader)
                val_loss = running_val_loss / len(val_loader)
                metrics = self._get_evaluation_metric(true_labels_dict, predicted_labels_dict, scores_dict)
                # Appedning the losses
                train_losses.append(train_loss)
                val_losses.append(val_loss)

                print("Epoch:{}/{} - Training Loss:{:.6f} | Validation Loss: {:.6f}".format(
                    epoch+1, self.num_epochs, train_loss, val_loss))
                logging.info("Epoch:{}/{} - Training Loss:{:.6f} | Validation Loss: {:.6f}".format(
                    epoch+1, self.num_epochs, train_loss, val_loss))
                print("\tAccuracy | Precision | Sensitivity | Specificity | AUC")
                logging.info("\tAccuracy | Precision | Sensitivity | Specificity | AUC")
                for arg in metrics:
                    print("{}: {}".format(arg, metrics[arg]))
                    logging.info("{}: {}".format(arg, metrics[arg]))
                print("-" * 40)
                logging.info("-" * 40)

                # SAVE MODEL IF VALIDATION LOSS HAS DECREASED
                if val_loss <= valid_loss_min:
                    print("Validation loss decreased ({:.6f} --> {:.6f}).  Saving model ...".format(valid_loss_min, val_loss))
                    print("-"*40)
                    # Copy new weights
                    best_model_wts = True
                    # Save models
                    fold_wgt_path = "checkpoints/HSCNN_Fold-{}_Epoch-{}.pth".format(fold+1, epoch+1)
                    torch.save(model.state_dict(), fold_wgt_path)
                    best_epch_at = epoch+1
                    # Update minimum loss
                    valid_loss_min = val_loss
                else:
                    if best_model_wts:
                        # Update best weights
                        weights = torch.load("checkpoints/HSCNN_Fold-{}_Epoch-{}.pth".format(fold+1, best_epch_at))
                        model.load_state_dict(weights)
                        del weights

                # Delete to save memory
                del metrics, true_labels_dict, predicted_labels_dict, scores_dict, \
                    running_train_loss, running_val_loss

            # External test-set loop
            with torch.no_grad():
                runnning_test_loss = 0.0
                model.eval()
                predicted_labels_dict = {'label_1': [], 'label_2': [], 'label_3': [], 'label_4': [], 'label_5': [],
                                         'label_6': []}
                true_labels_dict = {'label_1': [], 'label_2': [], 'label_3': [], 'label_4': [], 'label_5': [],
                                    'label_6': []}
                scores_dict = {'label_1': [], 'label_2': [], 'label_3': [], 'label_4': [], 'label_5': [], 'label_6': []}

                for index, data in enumerate(test_loader):
                    images, labels = data['img'].to(self.device), data['label']
                    per_label_for_each_image = [labels[:, i].to(self.device, dtype=torch.long) for i in range(self.num_low_level_tasks + 1)]
                    output = model(images)
                    test_loss_subtask = 0
                    for i in range(self.num_low_level_tasks + 1):
                        criterion = criterions['criterion_{}'.format(i + 1)]
                        test_loss_subtask += criterion(output[i], per_label_for_each_image[i]) * loss_weights[i]
                        per_task_out = F.softmax(output[i].cpu(), dim=1)
                        top_ps, top_class = per_task_out.topk(1, dim=1)
                        predicted_labels_dict['label_{}'.format(i + 1)].extend(list(top_class.flatten().numpy()))
                        true_labels_dict['label_{}'.format(i + 1)].extend(list(per_label_for_each_image[i].cpu().numpy()))
                        scores_dict['label_{}'.format(i + 1)].extend(per_task_out.numpy().tolist())
                    loss = test_loss_subtask / (self.num_low_level_tasks + 1)
                    runnning_test_loss += float(loss.item()) * images.size(0)

            test_loss = runnning_test_loss / len(test_loader)
            metrics = self._get_evaluation_metric(true_labels_dict, predicted_labels_dict, scores_dict)
            aucs_across_folds.append(metrics["Malignancy"][-1])

            print("="*40)
            print("Test loss:", test_loss)
            logging.info("Test loss: {}".format(test_loss))
            print("-" * 40)
            print("\tAccuracy | Precision | Sensitivity | Specificity | AUC")
            logging.info("\tAccuracy | Precision | Sensitivity | Specificity | AUC")
            for arg in metrics:
                print("{}: {}".format(arg, metrics[arg]))
                logging.info("{}: {}".format(arg, metrics[arg]))
            print("=" * 40)

            plt.plot(train_losses, label='Training loss')
            plt.plot(val_losses, label='Validation loss')
            plt.xlabel('Loss')
            plt.ylabel('Epoch')
            plt.legend(frameon=False)
            plt.savefig('metrics_fold_{}_losses.png'.format(fold+1))
            plt.clf()

            fpr = dict()
            tpr = dict()
            roc_auc = dict()
            one_hot_true_lbls = np_utils.to_categorical(true_labels_dict['label_6'], num_classes=self.malignancy_class)
            y_scores = np.array(scores_dict['label_6'])
            # Computer FPR, TPR for two classes
            for i in range(self.malignancy_class):
                fpr[i], tpr[i], _ = roc_curve(one_hot_true_lbls[:, i], y_scores[:, i])
                roc_auc[i] = auc(fpr[i], tpr[i])
            """
            # Computer Micro FPR, TPR
            fpr["micro"], tpr["micro"], _ = roc_curve(one_hot_true_lbls.ravel(), y_scores.ravel())
            roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
            """
            # Computer Macro FPR, TPR
            all_fpr = np.unique(np.concatenate([fpr[i] for i in range(self.malignancy_class)]))
            # Then interpolate all ROC curves at this points
            mean_tpr = np.zeros_like(all_fpr)
            for i in range(self.malignancy_class):
                mean_tpr += interp(all_fpr, fpr[i], tpr[i])
            mean_tpr /= self.malignancy_class
            fpr["macro"] = all_fpr
            tpr["macro"] = mean_tpr
            roc_auc["macro"] = auc(fpr["macro"], tpr["macro"])

            plt.figure()
            plt.plot(fpr["macro"], tpr["macro"],
                     label='Average AUC Curve (area = {0:0.2f})'
                           ''.format(roc_auc["macro"]),
                     color='deeppink', linestyle=':', linewidth=4)
            colors = cycle(['aqua', 'darkorange'])
            for i, color in zip(range(self.malignancy_class), colors):
                plt.plot(fpr[i], tpr[i], color=color, lw=2,
                         label='ROC curve of class {0} (area = {1:0.2f})'
                               ''.format(i, roc_auc[i]))

            plt.plot([0, 1], [0, 1], 'k--', lw=2)
            plt.xlim([0.0, 1.0])
            plt.ylim([0.0, 1.05])
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC - Malignancy')
            plt.legend(loc="lower right")
            plt.savefig('metrics_fold_{}_auc.png'.format(fold + 1))
            plt.clf()
            del train_losses, val_losses, accuracy_list, specificity_list, recall_list, f1_score_list, metrics, \
                true_labels_dict, predicted_labels_dict, scores_dict, runnning_test_loss, epoch_loss
        else:
            raise ValueError('Model must be instantiated and Trainloader/Validation loader cannot be empty!')

    def _get_index(self, input_index, num_fold):
        return input_index % num_fold

    def _load_pickle(self, input_file):
        with open(input_file, "rb") as f:
            pkl_file = pickle._Unpickler(f)
            pkl_file.encoding = 'latin1'
            pkl_file = pkl_file.load()
            return pkl_file

    def _merge_training_folds(self, path_to_training_fold, train_1_idx, train_2_idx):
        path_to_save = os.path.join(path_to_training_fold, "folds_merged")
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)
        # Set up paths to training folds
        path_to_train_1 = path_to_training_fold+"fold_{}\\fold_{}_img.pkl".format(train_1_idx, train_1_idx)
        path_to_lbl_1 = path_to_training_fold + "fold_{}\\labels.csv".format(train_1_idx)
        path_to_train_2 = path_to_training_fold + "fold_{}\\fold_{}_img.pkl".format(train_2_idx, train_2_idx)
        path_to_lbl_2 = path_to_training_fold + "fold_{}\\labels.csv".format(train_2_idx)
        # Merge data and label
        img_1 = self._load_pickle(path_to_train_1)
        img_2 = self._load_pickle(path_to_train_2)
        new_img = np.concatenate((img_1, img_2), axis=0)
        lbl_1 = pd.read_csv(path_to_lbl_1)
        lbl_2 = pd.read_csv(path_to_lbl_2)
        frames = [lbl_1, lbl_2]
        df_concatenated = pd.concat(frames)

        # Save merged file and label
        pkl_name = "fold_{}_{}.pkl".format(train_1_idx, train_2_idx)
        full_path_lbl = os.path.join(path_to_save, "labels.csv")
        full_path_pkl = os.path.join(path_to_save, pkl_name)
        # Save Pickle file
        with open(full_path_pkl, 'wb') as file:
            pickle.dump(new_img, file)
        # Save csv file
        df_concatenated.to_csv(full_path_lbl, encoding='utf-8', index=False)
        return full_path_pkl, full_path_lbl

    def start_training(self, path_to_training_folds=None, num_folds=(3, 7)):
        if path_to_training_folds and num_folds:
            fold = 0
            for index in range(num_folds[0], num_folds[1]):
                # Set up path for folds
                test_idx, train_1_idx, train_2_idx, val_idx = self._get_index(index, 4), self._get_index(index+1, 4),\
                                                              self._get_index(index+2, 4), self._get_index(index+3, 4)

                print("Training fold: {}".format(fold+1))
                logging.info("Training fold: {}".format(fold+1))
                logging.info("Test Index: {}, Train Index:{}, Val Index:{}".format(test_idx, (train_1_idx, train_2_idx), val_idx))
                # Test set and labels
                path_to_test_fold = os.path.join(path_to_training_folds, 'fold_{}\\fold_{}_img.pkl'.format(test_idx, test_idx))
                path_to_test_lbl = os.path.join(path_to_training_folds, 'fold_{}\\labels.csv'.format(test_idx))
                # Val set and label
                path_to_val_fold = os.path.join(path_to_training_folds, 'fold_{}\\fold_{}_img.pkl'.format(val_idx, val_idx))
                path_to_val_lbl = os.path.join(path_to_training_folds, 'fold_{}\\labels.csv'.format(val_idx))
                # Get the merged training set with labels
                path_to_train_fold, path_to_train_lbl = self._merge_training_folds(path_to_training_folds,
                                                                 train_1_idx, train_2_idx)

                # Set up Dataset
                train_dataset = HscnnDataset(path_to_train_fold, path_to_train_lbl, num_low_level_tasks=3, transform=self._get_default_transforms())
                val_dataset = HscnnDataset(path_to_val_fold, path_to_val_lbl, num_low_level_tasks=3, transform=self._get_default_transforms())
                test_dataset = HscnnDataset(path_to_test_fold, path_to_test_lbl, num_low_level_tasks=3, transform=None)
                # Set up Dataloader
                train_loader = DataLoader(train_dataset, batch_size=self.batch_size, shuffle=True, drop_last=True)
                lbl_weights = self._class_weights(path_to_train_lbl)
                val_loader = DataLoader(val_dataset, batch_size=self.batch_size, shuffle=True, drop_last=True)
                test_loader = DataLoader(test_dataset, batch_size=self.batch_size, shuffle=True, drop_last=True)

                # Instantiate the model
                model = self._get_HSCNN(self.in_channel, self.num_low_level_tasks, self.low_level_outputs,
                                        self.malignancy_class, True)

                optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-6)
                scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=3, verbose=True)
                # Define criterions depending upon the number of tasks
                criterions = {}
                for i in range(self.num_low_level_tasks + 1):
                    weights = lbl_weights["task_{}_weights".format(i + 1)]
                    weights_tensor = torch.FloatTensor(weights).to(self.device)
                    #criterions['criterion_{}'.format(i + 1)] = nn.BCEWithLogitsLoss(pos_weight=weights_tensor)
                    criterions['criterion_{}'.format(i + 1)] = nn.CrossEntropyLoss(weight=weights_tensor)

                self._start_model(model, optimizer, criterions, scheduler, lbl_weights, self.loss_weights,
                                  train_loader, val_loader, test_loader, fold)
                fold += 1
                del train_loader, val_loader, test_loader, model, optimizer, scheduler, criterions
                # Delete the merged files
                os.remove(path_to_train_fold)
                os.remove(path_to_train_lbl)
                logging.info("Finished Fold {}".format(fold+1))
                return None
        else:
            return "Path to Training Fold is required!"


if __name__ == "__main__":
    # Hyper-param
    number_folds = (3, 7)
    in_channel = 1
    low_level_tasks = 5
    low_level_outputs = [2, 2, 2, 2, 2]
    loss_weights_each_task = [0.2, 0.1, 0.1, 0.2, 0.1, 1]
    malignancy_class = 2
    num_epochs = 200
    batch_size = 20
    val_per = 0.2

    # Call for Training
    path_to_folds = "training_fold"
    train_obj = TrainModel(in_channel, low_level_tasks, low_level_outputs, loss_weights_each_task, malignancy_class, num_epochs, batch_size, val_per)
    train_obj.start_training(path_to_folds, number_folds)

