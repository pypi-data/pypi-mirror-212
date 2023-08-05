from setting import parse_opts 
from model import generate_model
import torch
from torch import nn
import numpy as np
from torch.utils.data import DataLoader
import torch.nn.functional as F
import sys
import os
import numpy as np
from tqdm import tqdm
from utils.logger import log
from build_unet_model import UNet
import nrrd


def getIoU(y_true, y_pred):
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.logical_and(y_true_f, y_pred_f).sum()
    union = np.logical_or(y_true_f, y_pred_f).sum()
    return (intersection + 1) * 1. / (union + 1)

def rescale_img_to_rgb(img):
    img = (img - img.min()) / (img.max() - img.min())
    img *= 255.0
    img = img.astype(np.uint8)
    return img


if __name__ == '__main__':
    # settting
    sets = parse_opts()
    path_to_data = '/datasets'
    save_output = '/datasets/Unet_Predictions'

    os.environ["CUDA_VISIBLE_DEVICES"]=str(sets.gpu_id[0])
    # ---------------------------------------------------   
    model = UNet(in_nc=1, out_nc=1, nf=64).cuda()
    model = nn.DataParallel(model)
    path_to_weight = './trails_UNET/models/UNet_epoch_106_best_weight_0.646983.pth.tar'
    checkpoint = torch.load(path_to_weight)
    model.load_state_dict(checkpoint['state_dict'])
    print('UNet weights loaded!')

    # run inference
    with torch.no_grad():
        model.eval()
        norm_models = [norm for norm in os.listdir(path_to_data) if norm != 'Unet_Predictions']
        print('norm models:', norm_models)

        for norm_model in norm_models:
            print('Loading Normalization:', norm_model)
            save_model_predictions = os.path.join(save_output, norm_model)
            print(save_model_predictions)
            if not os.path.exists(save_model_predictions):
                os.makedirs(save_model_predictions)

            cur_path = os.path.join(path_to_data, norm_model)
            cnds =  os.listdir(cur_path)
            for each_cnd in cnds:
                save_model_cnd = os.path.join(save_model_predictions, each_cnd)
                if not os.path.exists(save_model_cnd):
                    os.makedirs(save_model_cnd)
                volumes = os.path.join(cur_path, each_cnd)

                for vol in os.listdir(volumes):
                    path_to_vol = os.path.join(volumes, vol)
                    data, header = nrrd.read(path_to_vol)
                    mask_header = {'units': ['mm', 'mm', 'mm'], 'spacings': header['spacings']}
                    rescaled_vol = rescale_img_to_rgb(data)
                    rescaled_vol = (rescaled_vol - rescaled_vol.mean()) / rescaled_vol.std()
                    rescaled_vol = torch.from_numpy(np.expand_dims(np.expand_dims(rescaled_vol.transpose(2,0,1), axis=0), axis=0)).type(torch.FloatTensor)

                    # get prediction
                    rescaled_vol = rescaled_vol.cuda() 
                    out_masks = model(rescaled_vol)
                    output_prob = torch.sigmoid(out_masks).detach().cpu().numpy()
                    output_prob_thresh = (output_prob > 0.5) * 1
                    vol_to_save = output_prob_thresh[0,0,:,:,:]
                    vol_to_save = vol_to_save*255.0
                    vol_to_save = vol_to_save.astype(np.uint8)
                    vol_save_path = os.path.join(save_model_cnd, vol)
                    nrrd.write(vol_save_path, vol_to_save, mask_header, index_order='C')
            
    print('All Normalization Prediction Complete!')




