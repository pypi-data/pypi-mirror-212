import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np 
from collections import OrderedDict
from lung_analysis_pipeline.utils import util
from lung_analysis_pipeline.utils import patch as patch_util
import os 
import pkg_resources
from skimage.transform import resize
import logging
logger = logging.getLogger('base')


class double_conv(nn.Module):
    '''(conv => BN => ReLU) * 2'''
    def __init__(self, in_ch, out_ch):
        super(double_conv, self).__init__()
        self.conv = nn.Sequential(
            nn.Conv3d(in_ch, out_ch, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm3d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv3d(out_ch, out_ch, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm3d(out_ch),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        x = self.conv(x)
        return x


class inconv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(inconv, self).__init__()
        self.conv = double_conv(in_ch, out_ch)

    def forward(self, x):
        x = self.conv(x)
        return x


class down(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(down, self).__init__()
        self.mpconv = nn.Sequential(
            nn.MaxPool3d(2),
            double_conv(in_ch, out_ch)
        )

    def forward(self, x):
        x = self.mpconv(x)
        return x


class up(nn.Module):
    def __init__(self, in_ch, out_ch, bilinear=True):
        super(up, self).__init__()
        if bilinear:
            # self.up = nn.UpsamplingBilinear2d(scale_factor=2)
            self.up = nn.Upsample(scale_factor=2)
        else:
            self.up = nn.ConvTranspose3d(in_ch//2, in_ch//2, 2, stride=2)

        self.conv = double_conv(in_ch, out_ch)

    def forward(self, x1, x2):
        x1 = self.up(x1)
        diffX = x1.size()[2] - x2.size()[2]
        diffY = x1.size()[3] - x2.size()[3]
        x2 = F.pad(x2, (diffX // 2, int(diffX / 2),
                        diffY // 2, int(diffY / 2)))
        x = torch.cat([x2, x1], dim=1)
        x = self.conv(x)
        return x
        

class outconv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super(outconv, self).__init__()
        self.conv = nn.Conv3d(in_ch, out_ch, 1)

    def forward(self, x):
        x = self.conv(x)
        return x


class UNet(nn.Module):
    def __init__(self, in_nc, out_nc, nf):
        super(UNet, self).__init__()
        self.inc = inconv(in_nc, nf)
        self.down1 = down(nf, 128)
        self.down2 = down(128, 256)
        self.down3 = down(256, 512)
        self.down4 = down(512, 512)
        self.up1 = up(1024, 256)
        self.up2 = up(512, 128)
        self.up3 = up(256, nf)
        self.up4 = up(128, nf)
        self.outc = outconv(nf, out_nc)
        self.Dropout = nn.Dropout(0.2)

    def forward(self, x):
        # print('======== forward method called ========')
        # print('incoming x shape:', x.shape)
        x1 = self.inc(x)
        # print('x1 - shape after first inc:', x1.shape)
        x2 = self.down1(x1)
        # print('x2 - shape after first down1:', x2.shape)
        x3 = self.down2(x2)
        # print('x3 - shape after first down2:', x3.shape)
        x3 = self.Dropout(x3)
        # print('shape after first dropout:', x3.shape)
        x4 = self.down3(x3)
        # print('x4 - shape after first down3:', x4.shape)
        x5 = self.down4(x4)
        # print('x5 - shape after first down4:', x5.shape)
        # print('-'*40)
        # print('upsampling x5 to match with x4')
        x = self.up1(x5, x4)
        # print('shape after first up1:', x.shape)
        x = self.up2(x, x3)
        # print('shape after first up2:', x.shape)
        x = self.up3(x, x2)
        # print('shape after first up3:', x.shape)
        x = self.up4(x, x1)
        # print('shape after first up4:', x.shape)
        x = self.outc(x)
        # print('final output:', x.shape)
        return x
    
    def run_test(self, input_data, opt):
        if opt['segmentation']['use_decetion_bbox']:
            return self.run_test_rois(input_data) 
        else:
            return self.run_test_entire_vol(input_data)
    
    def run_test_rois(self, input_data): 
        with torch.no_grad(): 
            self.eval()
            image = input_data['volume'][0][0].cpu().numpy().astype(np.float32)
            uid = input_data['uid'][0]
            detection_bboxes = input_data['detection_bboxes'][0].cpu().numpy()

            preds = []
            for i, bbox in enumerate(detection_bboxes): 
                bbox = bbox.astype(int)
                _, z, y, x, d, _ = bbox 
                # Calculate starting and ending indices for each dimension
                start_z = max(0, z - d // 2)
                end_z = min(image.shape[0], z + d // 2 + 1)
                start_y = max(0, y - d // 2)
                end_y = min(image.shape[1], y + d // 2 + 1)
                start_x = max(0, x - d // 2)
                end_x = min(image.shape[2], x + d // 2 + 1)

                patch_size = (end_z - start_z, end_y - start_y, end_x - start_x)
                # print('original input size: {}'.format(patch_size))
                if any(element < 0 for element in patch_size):
                    # print('start_z: {}'.format(start_z))
                    # print('end_z: {}'.format(end_z))
                    # print('start_y: {}'.format(start_y))
                    # print('end_y: {}'.format(end_y))
                    # print('start_x: {}'.format(start_x))
                    # print('end_x: {}'.format(end_x))
                    continue 
                roi = image[start_z:end_z, start_y:end_y, start_x:end_x]
                roi = util.resize_image(roi, size=(32,64,64))
                roi = torch.from_numpy(roi)[None,None].cuda()
                out_mask = self.forward(roi)[0,0] # remove batch and ch dims 

                # resizing to original roi size and thresholding 
                out_mask = torch.from_numpy(util.resize_image(out_mask.cpu(), size=patch_size)).cuda()
                prob = torch.sigmoid(out_mask) 
                pred = (prob > 0.5) * 1 

                preds.append(pred)
            input_data['seg_masks'] = preds 
            return input_data 

    def run_test_entire_vol(self, input_data): 
        with torch.no_grad(): 
            self.eval()

            volume = input_data['volume'][0][0].cpu() # this is the whole 3D volume 
            volume = (volume - volume.mean()) / volume.std()
            patch_size = (32,64,64) #(D,H,W)
            patch_stride = (16,32,32)
            pad_volume = patch_util.zero_padding(volume, patch_size)
            pad_result = np.zeros_like(pad_volume)
            pad_add = np.zeros_like(pad_volume)
            count = 0 
            prob_max = 0 
            for z in range(0, pad_volume.shape[0], patch_stride[0]):
                for y in range(0, pad_volume.shape[1], patch_stride[1]):
                    for x in range(0, pad_volume.shape[2], patch_stride[2]):
                        # print('Processing patch {}'.format(count))
                        count += 1 
                        patch = pad_volume[z:z+patch_size[0], y:y+patch_size[1], x:x+patch_size[2]]
                        patch = torch.from_numpy(patch[None,None]).type(torch.FloatTensor).cuda()
                        # print(patch.shape)
                        out_masks = self.forward(patch)[0,0] # remove batch and ch dims 
                        probs = torch.sigmoid(out_masks).detach().cpu().numpy() #[0,1]
                        pad_result[z:z+patch_size[0], y:y+patch_size[1], x:x+patch_size[2]] += probs
                        pad_add[z:z+patch_size[0], y:y+patch_size[1], x:x+patch_size[2]] += 1

            
            pad_result = pad_result / pad_add
            result = patch_util.remove_padding(pad_result, volume)
            result = (result > 0.5) * 1 # threshold = 0.5 
            # result = torch.from_numpy(result[None,None]).type(torch.FloatTensor).cuda()
            result = torch.from_numpy(result[None]).type(torch.FloatTensor).cuda()
        input_data['seg_mask'] = result
        return input_data

def create_seg_model(opt, in_nc=1, out_nc=1, nf=64): 
    ## from opt to create segmentation options  

    ## create segmentation model    
    model = UNet(in_nc=in_nc, out_nc=out_nc, nf=nf).cuda()
    model = nn.DataParallel(model)
    # path_to_weight = 'trails_UNet/models/UNet_epoch_106_best_weight_0.646983.pth.tar'
    # path_to_weight = os.path.abspath(os.path.join(os.path.dirname(__file__), path_to_weight))
    # path_to_weight = os.path.join(module_path, path_to_weight)
    # path_to_weight = pkg_resources.resource_filename(__name__, path_to_weight)
    path_to_weight = opt['segmentation']['weights']
    checkpoint = torch.load(path_to_weight)
    model.load_state_dict(checkpoint['state_dict'])

    # Extract the original model from the DataParallel wrapper
    if isinstance(model, nn.DataParallel):
        model = model.module

    logger.info('Segmentation model {:s} is created.'.format(model.__class__.__name__)) 
    # logger.info(util.dict2str(option)) # or other function to conver segmentation option format to string 
    return model 

