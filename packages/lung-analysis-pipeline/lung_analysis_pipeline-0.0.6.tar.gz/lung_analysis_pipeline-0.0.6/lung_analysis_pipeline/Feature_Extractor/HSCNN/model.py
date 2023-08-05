import torch
import torch.nn as nn
from scipy import ndimage
from skimage import measure
import pkg_resources
import numpy as np 
import torch.nn.functional as F
from lung_analysis_pipeline.utils import util 
import logging
logger = logging.getLogger('base')

class HSCNN(nn.Module):
    """
    This is a Pytorch version of the HSCNN used in the paper https://doi.org/10.1117/12.2551220
    """
    def __init__(self, input_channel=1, num_low_level_tasks=3, low_level_outputs=[2, 2, 2], malignancy_class=2):
        super(HSCNN, self).__init__()
        self.num_low_level_tasks = num_low_level_tasks
        # Feature module
        self.feature_module = self._make_feature_layers(in_channel=input_channel, num_filters=[16, 32], repeat_each_layer=1)
        self.feature_output_size = 32 * 13 * 13 * 13
        # Low-level module
        self.low_level_tasks = self._make_low_level_layers(num_tasks=self.num_low_level_tasks, output_neurons=low_level_outputs)
        self.low_level_1 = self.low_level_tasks['task_1']
        self.low_level_2 = self.low_level_tasks['task_2']
        self.low_level_3 = self.low_level_tasks['task_3']
        self.low_level_4 = self.low_level_tasks['task_4']
        self.low_level_5 = self.low_level_tasks['task_5']
        self.final_layer_input_size = self.feature_output_size + 256 * self.num_low_level_tasks
        # High-level task module
        self.final_layer = nn.Sequential(nn.Linear(self.final_layer_input_size, 256),
                                         nn.ReLU(),
                                         nn.BatchNorm1d(256),
                                         nn.Linear(256, malignancy_class)
                                         )

    def _conv_layer(self, in_channel, out_channel, final_layers=[], repeat=1):
        """
        :param in_channel: input number of channels
        :param out_channel: output number of channels
        :param final_layers: number of channnels for CNN
        :param repeat: number of times to repeat each layer
        :return: a conv network
        """
        for i in range(repeat + 1):
            final_layers += [
                nn.Conv3d(in_channels=in_channel, out_channels=out_channel, kernel_size=(3, 3, 3), stride=(1, 1, 1),
                          padding=(1, 1, 1)),
                nn.ReLU(),
                nn.BatchNorm3d(out_channel)
                ]
            in_channel = out_channel
        return final_layers

    def _make_feature_layers(self, in_channel, num_filters, repeat_each_layer):
        """
        :param in_channel: input number of channel for feature layers
        :param num_filters: number of filters for each layers
        :param repeat_each_layer: number of times each layer is repeateds
        :return: a CNN module
        """
        if isinstance(num_filters, list):
            if len(num_filters) == 0:
                raise ValueError('Number of filters cannot be empty')
            else:
                feature_layers = []
                in_channel = in_channel
                for arg in num_filters:
                    feature_layers = self._conv_layer(in_channel, arg, feature_layers, repeat_each_layer)
                    feature_layers += [nn.MaxPool3d(kernel_size=(2, 2, 2), stride=(2, 2, 2)), nn.Dropout3d(p=0.6)]
                    in_channel = arg
            return nn.Sequential(*feature_layers)
        else:
            raise ValueError('Number of filters must be passed as list')

    def _sub_tasks(self, num_filters):
        """
        :param num_filters: number of filters for a given low-level task
        :return: a low-level sub-network
        """
        if isinstance(num_filters, list):
            if len(num_filters) == 0:
                raise ValueError('Number of filters cannot be empty')
            else:
                task_layer = []
                input_neurons = self.feature_output_size
                for index, arg in enumerate(num_filters):
                    # If its last layer, one add linear layer
                    if index == len(num_filters)-1:
                        task_layer += [nn.Linear(input_neurons, arg)]
                    else:
                        task_layer += [nn.Linear(input_neurons, arg), nn.ReLU(), nn.BatchNorm1d(arg), nn.Dropout(p=0.2)]
                        #task_layer += [nn.Linear(input_neurons, arg), nn.ReLU(), nn.BatchNorm1d(arg)]
                    input_neurons = arg
                return nn.Sequential(*task_layer)
        else:
            raise ValueError('Number of filters must be passed as list')

    def _make_low_level_layers(self, num_tasks, output_neurons):
        """
        :param num_tasks: number of low-level tasks
        :param output_neurons: output neurons for each sub-task
        :return: three low-level sub-networks
        """
        low_level_tasks = {}
        if isinstance(output_neurons, list):
            if len(output_neurons) != num_tasks:
                raise ValueError('Number of tasks and number of neurons does not match')
            else:
                for index, each_neuron in enumerate(output_neurons):
                    low_level_tasks['task_{}'.format(index+1)] = self._sub_tasks([256, 64, each_neuron])
                return low_level_tasks
        else:
            raise ValueError('Output neurons must be in a list')

    def forward(self, x):
        if len(x.shape) != 5:
            raise ValueError('Expect input of shape B x C x Z x H x W')
        # Feature module
        # print('Running through model')
        # print('image shape:', x.shape)
        out = self.feature_module(x)
        # print('out after feature_model:', out.shape)
        out = out.view(x.shape[0], -1)
        # print('out reshaped:', out.shape)
        out_concat_list = [out]

        # Passing networks through low-level tasks
        low_level_out_1 = self.low_level_1(out)
        # print('out after ll1:', low_level_out_1.shape)
        low_level_out_2 = self.low_level_2(out)
        # print('out after ll2:', low_level_out_2.shape)
        low_level_out_3 = self.low_level_3(out)
        # print('out after ll3:', low_level_out_3.shape)
        low_level_out_4 = self.low_level_4(out)
        # print('out after ll4:', low_level_out_4.shape)
        low_level_out_5 = self.low_level_5(out)
        # print('out after ll5:', low_level_out_5.shape)

        # print('Intermediate out')
        # Get Intermediate output from Sub-Networks
        for sub_network in self.low_level_tasks:
            feature_out = out.clone()
            for arg in list(self.low_level_tasks[sub_network].modules())[1:5]:
                feature_out = arg(feature_out)
            out_concat_list.append(feature_out)
            del feature_out # delete the variable from memory

        # Concatanate all the intermediate outputs
        output_concat = torch.cat(out_concat_list, dim=1)
        final_output = self.final_layer(output_concat)
        sub_networks_output = [low_level_out_1, low_level_out_2, low_level_out_3, low_level_out_4, low_level_out_5, final_output]
        return sub_networks_output
    
    def _extract_features(self, x): 
        '''
        param x: input volume of size B x C x Z x H x W
        returns: extracted feature of size [1,256]
        '''
        if len(x.shape) != 5:
            raise ValueError('Expect input of shape B x C x Z x H x W')
        # HSCNN takes in patches with values in [0,1]
        x = (x - x.min()) / (x.max() - x.min()) 

        # Feature module
        out = self.feature_module(x)
        out = out.view(x.shape[0], -1)
        out_concat_list = [out]

        # Passing networks through low-level tasks
        low_level_out_1 = self.low_level_1(out)
        low_level_out_2 = self.low_level_2(out)
        low_level_out_3 = self.low_level_3(out)
        low_level_out_4 = self.low_level_4(out)
        low_level_out_5 = self.low_level_5(out)

        # Get Intermediate output from Sub-Networks
        for sub_network in self.low_level_tasks:
            feature_out = out.clone()
            for arg in list(self.low_level_tasks[sub_network].modules())[1:5]:
                feature_out = arg(feature_out)
            out_concat_list.append(feature_out)
            del feature_out # delete the variable from memory
        
        # Concatanate all the intermediate outputs
        final_layer_input = torch.cat(out_concat_list, dim=1)
        feature = self.final_layer[0](final_layer_input) 
        return feature

    def run_test(self, input_data, roi, threshold_size=0): 
        
        with torch.no_grad():
            self.eval()
            if roi == 'user' or roi == 'segmentation': 
                if roi == 'segmentation': 
                    mask = input_data['seg_mask'][0].cpu()
                else: 
                    mask = input_data['gt_mask'][0].cpu()
                
                image = input_data['volume'][0][0].cpu()
                labeled_mask, num_components = measure.label(mask, return_num=True)

                features = []
                # Iterate over each labeled component
                for i in range(1, num_components + 1):
                    # Extract the binary mask for the current component
                    component_mask = (labeled_mask == i)
                    # Check if the size of the current component is larger than the threshold
                    if np.sum(component_mask) < threshold_size:
                        continue
                    # Calculate the centroid of the current component
                    z, y, x = np.round(np.array(ndimage.center_of_mass(component_mask))).astype(int)
                    centroid = np.array([z, y, x])
                    roi = torch.from_numpy(util.extract_roi(image, centroid)).cuda()
                    roi = roi[None,None]
                    # Extract features from the ROI 
                    features.append(self._extract_features(roi))

                # concatenate features into numpy array 
                features = torch.cat(features, axis=0)
                
                input_data['deep_feature'] = features
                return input_data
            
            elif roi == 'detection': 
 
                image, detection_bboxes = input_data['volume'][0][0].cpu().numpy(), input_data['detection_bboxes'][0].cpu().numpy()

                features = [] 
                for bbox in detection_bboxes: 
                    bbox = bbox.astype(int)
                    
                    _, z, y, x, d, _ = bbox # do not need probability here 
                    # Calculate starting and ending indices for each dimension
                    start_z = max(0, z - d // 2)
                    end_z = min(image.shape[0], z + d // 2 + 1)
                    start_y = max(0, y - d // 2)
                    end_y = min(image.shape[1], y + d // 2 + 1)
                    start_x = max(0, x - d // 2)
                    end_x = min(image.shape[2], x + d // 2 + 1)
                    
                    roi = image[start_z:end_z, start_y:end_y, start_x:end_x]
                    # Resize ROI 
                    roi = util.resize_image(roi, size=(52,52,52))
                    roi = torch.from_numpy(roi)[None,None].cuda()

                    # Extract features from the ROI 
                    feature = self._extract_features(roi) 
                    features.append(feature)

                # roi_centroids = detection_bboxes[:,1:4] # z, y, x
                
                # features = []
                # for roi_centroid in roi_centroids:
                #     roi = torch.from_numpy(util.extract_roi(image, roi_centroid)).cuda()
                    
                #     # Extract features from the ROI 
                #     feature = self._extract_features(roi)
                #     features.append(feature)
                features = torch.cat(features, axis=0)
                input_data['deep_feature'] = features
                return input_data

def create_feat_extractor(opt): 
    # check if the specified model is supported 
    if opt['feature_extraction']['deep_feature']['model'] != 'hscnn': 
        raise NotImplementedError('Model [{:s}] not implemented.'.format(opt['feature_extraction']['deep_models']['model']))
    # hyperparams (copied from train.py)
    in_channel = 1
    low_level_tasks = 5
    low_level_outputs = [2, 2, 2, 2, 2]
    malignancy_class = 2


    # instantiate HSCNN model 
    model = HSCNN(in_channel, low_level_tasks, low_level_outputs, malignancy_class).cuda()
    # load pre-trained weights 
    # path_to_weight = 'checkpoints/HSCNN_Fold-1_Epoch-86.pth'
    # path_to_weight = pkg_resources.resource_filename(__name__, path_to_weight)
    path_to_weight = opt['feature_extraction']['deep_feature']['weights']
    checkpoint = torch.load(path_to_weight)
    model.load_state_dict(checkpoint)

    logger.info('Feature extraction model {:s} is created.'.format(model.__class__.__name__)) 
    # logger.info(util.dict2str(option)) # or other function to conver segmentation option format to string 
    return model 