from setting import parse_opts 
from datasets.brains18 import BrainS18Dataset
import albumentations as A
from datasets.lungCT import LIDC_CT
from model import generate_model
import torch
import numpy as np
from torch import nn
from torch import optim
import pickle
from torch.optim import lr_scheduler
from torch.utils.data import DataLoader
import time
from utils.logger import log
from scipy import ndimage
import os
from tqdm import tqdm
from models.custom_loss import *
from build_unet_model import UNet


"""
Returns Intersection over Union score for ground truth and predicted masks
"""
def getIoU(y_true, y_pred):
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.logical_and(y_true_f, y_pred_f).sum()
    union = np.logical_or(y_true_f, y_pred_f).sum()
    return (intersection + 1) * 1. / (union + 1)


"""
Training and Validation of Segmentation Model
"""
def train_and_validate(train_loader, val_loader, model, optimizer, scheduler, total_epochs, save_interval, save_folder, sets):
    # settings
    batches_per_epoch_train = len(train_loader)
    batches_per_epoch_val = len(val_loader)
    log.info('Train: {} epochs in total, {} batches per epoch'.format(total_epochs, batches_per_epoch_train))
    log.info('Val: {} epochs in total, {} batches per epoch'.format(total_epochs, batches_per_epoch_val))
    loss_dict = {'bce':[], 'dice':[], 'invt_dice':[]}

    # criteria to save best weight
    best_iou, total_ious = 0.0, []
    
    # define losses
    criterion1 = nn.BCEWithLogitsLoss()
    criterion2 = SoftDiceLoss()
    criterion3 = InvSoftDiceLoss()
    if not sets.no_cuda:
        criterion1 = nn.BCEWithLogitsLoss().cuda()
        criterion2 = SoftDiceLoss().cuda()
        criterion3 = InvSoftDiceLoss().cuda()
    
    # ------------------ #
    #     Training       #
    # ------------------ #
    model.train()
    train_time_sp = time.time()
    for epoch in range(total_epochs):
        log.info('Start epoch {}'.format(epoch))
        log.info('lr = {}'.format(scheduler.get_last_lr()))
        # running_total_loss = []

        bce_loss_over_epoch, dice_loss_over_epoch, ivt_loss_over_epoch = 0, 0, 0
        for batch_id, batch_data in enumerate(train_loader):
            batch_id_sp = epoch * batches_per_epoch_train
            volumes, label_masks = batch_data
            if not sets.no_cuda: 
                volumes = volumes.cuda()
                label_masks = label_masks.cuda()

            optimizer.zero_grad()
            out_masks = model(volumes)

            """
            # resize GT label
            [n, _, d, h, w] = out_masks.shape
            new_label_masks = np.zeros([n, _, d, h, w])
            for label_id in range(n):
                label_mask = label_masks[label_id]
                [ori_c, ori_d, ori_h, ori_w] = label_mask.shape
                label_mask = np.reshape(label_mask, [ori_d, ori_h, ori_w])
                scale = [d*1.0/ori_d, h*1.0/ori_h, w*1.0/ori_w]
                label_mask = ndimage.interpolation.zoom(label_mask, scale, order=0)
                new_label_masks[label_id, 0] = label_mask
            new_label_masks = torch.tensor(new_label_masks).type(torch.FloatTensor)
            if not sets.no_cuda:
                new_label_masks = new_label_masks.cuda()
            """
            
            # calculate loss
            # bce_loss, dice_loss, invt_dice_loss = criterion1(out_masks, new_label_masks), criterion2(out_masks, new_label_masks),\
            #                                     criterion3(out_masks, new_label_masks)

            bce_loss, dice_loss, invt_dice_loss = criterion1(out_masks, label_masks), criterion2(out_masks, label_masks),\
                                                criterion3(out_masks, label_masks)

            bce_loss_over_epoch += bce_loss.item()
            dice_loss_over_epoch += dice_loss.item()
            ivt_loss_over_epoch += invt_dice_loss.item()
            # running_total_loss.append(float(loss.item() * volumes.size(0)))
            loss = bce_loss + dice_loss + invt_dice_loss
            loss.backward()
            optimizer.step()

            # log metrics
            avg_batch_time = (time.time() - train_time_sp) / (1 + batch_id_sp)
            log.info(
                    'Batch: {}-{} ({}), loss_bce = {:.3f}, loss_dice = {:.3f}, loss_invt_dice = {:.3f}, total_loss = {:.3f}, avg_batch_time = {:.3f}'\
                    .format(epoch+1, batch_id, batch_id_sp, bce_loss.item(), dice_loss.item(), invt_dice_loss.item(), loss.item(), avg_batch_time))
            
        # append losses
        loss_dict['bce'].append(bce_loss_over_epoch/len(train_loader))
        loss_dict['dice'].append(dice_loss_over_epoch/len(train_loader))
        loss_dict['invt_dice'].append(ivt_loss_over_epoch/len(train_loader))

        if (epoch+1)%5 == 0:
            model_save_path = '{}_epoch_{}.pth.tar'.format(save_folder, epoch+1)
            model_save_dir = os.path.dirname(model_save_path)
            if not os.path.exists(model_save_dir):
                os.makedirs(model_save_dir)
            log.info('Save checkpoint: epoch = {}, batch_id = {}'.format(epoch+1, batch_id)) 
            torch.save({'epoch': epoch+1,
                        'batch_id': batch_id,
                        'state_dict': model.state_dict(),
                        'optimizer': optimizer.state_dict()},
                        model_save_path)
            loss_dict_path = '{}_loss_dict_epoch_{}.pkl'.format(save_folder, epoch+1)
            loss_save_dir = os.path.dirname(loss_dict_path)
            if not os.path.exists(loss_save_dir):
                os.makedirs(loss_save_dir)
            with open(loss_dict_path, 'wb') as f:
                pickle.dump(loss_dict, f)

        scheduler.step()
        # scheduler.step(np.mean(running_total_loss))
        # ------------------ #
        #     Validation     #
        # ------------------ #
        iou_over_epoch = 0
        with torch.no_grad():
            model.eval()
            for volumes, label_masks in tqdm(val_loader):
                if not sets.no_cuda:
                    volumes = volumes.cuda()
                
                out_masks = model(volumes)
                output_prob = torch.sigmoid(out_masks).detach().cpu().numpy()
                output_prob_thresh = (output_prob > 0.5) * 1

                """
                # resize GT label
                [n, _, d, h, w] = out_masks.shape
                new_label_masks = np.zeros([n, _, d, h, w])
                for label_id in range(n):
                    label_mask = label_masks[label_id]
                    [ori_c, ori_d, ori_h, ori_w] = label_mask.shape 
                    label_mask = np.reshape(label_mask, [ori_d, ori_h, ori_w])
                    scale = [d*1.0/ori_d, h*1.0/ori_h, w*1.0/ori_w]
                    label_mask = ndimage.interpolation.zoom(label_mask, scale, order=0)
                    new_label_masks[label_id, 0] = label_mask
                new_label_masks = torch.tensor(new_label_masks).to(torch.int64)
                """

                # iou = getIoU(new_label_masks, output_prob_thresh)
                iou = getIoU(label_masks, output_prob_thresh)
                iou_over_epoch += iou

            avg_iou = iou_over_epoch/len(val_loader)
            total_ious.append(avg_iou)
            log.info('Average IoU: {:.6f}'.format(avg_iou))

            # save model if average iou increases
            if avg_iou > best_iou:
                log.info("Average mask IoU increased: ({:.6f} --> {:.6f}).  Saving model ...".format(best_iou,\
                                                                                                  avg_iou))
                model_save_path = '{}_epoch_{}_best_weight_{:.6f}.pth.tar'.format(save_folder, epoch+1, avg_iou)
                model_save_dir = os.path.dirname(model_save_path)
                if not os.path.exists(model_save_dir):
                    os.makedirs(model_save_dir)
                torch.save({'epoch': epoch+1,
                            'batch_id': batch_id,
                            'state_dict': model.state_dict(),
                            'optimizer': optimizer.state_dict()},
                            model_save_path)
                best_iou = avg_iou


    print('Finished training')
    total_epochs_path = '{}_iou_over_{}_epochs.pkl'.format(save_folder, total_epochs)
    total_epochs_dir = os.path.dirname(total_epochs_path)
    if not os.path.exists(total_epochs_dir ):
        os.makedirs(total_epochs_dir)
    with open(total_epochs_path, 'wb') as f:
        pickle.dump(total_ious, f)
    exit()


if __name__ == '__main__':
    # settting
    sets = parse_opts()

    os.environ["CUDA_VISIBLE_DEVICES"]=str(sets.gpu_id[0])   
    model = UNet(in_nc=1, out_nc=1, nf=64).cuda()
    model = nn.DataParallel(model)

    # getting model
    torch.manual_seed(sets.manual_seed)
    # model, parameters = generate_model(sets) 

    # optimizer
    # if sets.ci_test:
    #     params = [{'params': parameters, 'lr': sets.learning_rate}]
    # else:
    #     params = [
    #             { 'params': parameters['base_parameters'], 'lr': sets.learning_rate }, 
    #             { 'params': parameters['new_parameters'], 'lr': sets.learning_rate*100 }
    #             ]

    # params = [{'params': parameters, 'lr': 1e-4}]
    # optimizer = torch.optim.SGD(params, momentum=0.9, weight_decay=1e-3)   
    # scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.99)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
    scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.99)

    # getting data
    sets.phase = 'train'
    if sets.no_cuda:
        sets.pin_memory = False
    else:
        sets.pin_memory = True  

    # training transforms
    train_transform = A.Compose([
        A.HorizontalFlip(p=0.6),
        A.VerticalFlip(p=0.6),
        A.Transpose(p=0.6),
        A.RandomRotate90(p=0.6),
        A.OneOf([
            A.GaussNoise(p=0.6),
            A.RandomBrightnessContrast(p=0.5)
        ])
        # A.RandomCrop(width=64, height=64),
        # A.Resize(width=224, height=224),
    ])

    training_dataset = LIDC_CT('train', sets.data_root, sets.img_train_list, sets, transforms=train_transform)
    val_dataset = LIDC_CT('validation', sets.data_root, sets.img_val_list, sets, transforms=None)

    train_loader = DataLoader(training_dataset, batch_size=sets.batch_size, shuffle=True, num_workers=sets.num_workers, pin_memory=sets.pin_memory)
    val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=sets.num_workers, pin_memory=sets.pin_memory)
    
    # data, label = iter(train_loader).next()
    # print('data shape:', data.shape)
    # print('label shape:', label.shape)

    # start training
    train_and_validate(train_loader, val_loader, model, optimizer, scheduler, total_epochs=sets.n_epochs, save_interval=sets.save_intervals, save_folder=sets.save_folder, sets=sets) 
