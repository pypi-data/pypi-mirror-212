import nrrd
import bm3d
import numpy as np
from skimage.restoration import estimate_sigma
import os
import h5py
import json
from tqdm import tqdm
import torch 


def rescale_intensity(img):
    img = (img - img.min()) / (img.max() - img.min())
    return img

def rescale_img(img, clip=None, max_val=255.0):
    if clip:
        img = np.clip(img, clip[0], clip[1])
    img = rescale_intensity(img)
    img *= max_val
    img = img.astype(np.float32)
    # img = img.type(torch.float32)
    return img

def read_config(config_path):
    config_path = os.path.join(config_path) 
    with open(config_path, 'r') as f:
        config = json.load(f)
    meta_data = {}
    meta_data['Spacing'] = [float(i) for i in config['Spacing'].split()]
    meta_data['Orientation'] = [float(i) for i in config['Orientation'].split()] 
    meta_data['Origin'] = [float(i) for i in config['Origin'].split()]
    header = {'units': ['mm', 'mm', 'mm'], 'spacings': meta_data['Spacing']} 
    return header


def calculate_bm3d(lr_scan_path, UID, save_path, split_uid_for_ref=False):
    with open(UID, 'r') as f:
        lines = f.readlines()
        uids = [l.rstrip() for l in lines]
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    for uid in uids:
        print('Reading UID:', uid)
        LR_path = os.path.join(lr_scan_path, '{}.h5'.format(uid))
        with h5py.File(LR_path, 'r') as file:
            lr_scan = file['data'][()]

        lr_bm3d_norm = np.empty(lr_scan.shape)
        header = os.path.join(lr_scan_path, '{}.json'.format(uid))
        volume_save_path = os.path.join(save_path, '{}.nrrd'.format(uid))
        spacing_info = read_config(header)

        for index, slice_ in enumerate(tqdm(lr_scan)):
            # +1000 to input images 
            # 
            img_slice = rescale_img(slice_, clip=None, max_val=255.0)
            sigma_est = np.mean(estimate_sigma(img_slice, multichannel=False))
            BM3D_denoised_image = bm3d.bm3d(img_slice, sigma_psd=sigma_est, stage_arg=bm3d.BM3DStages.ALL_STAGES) # bm3d.BM3DStages.HARD_THRESHOLDING
            bm3d_clipped = rescale_img(BM3D_denoised_image, clip=(0.0, 255.0), max_val=slice_.max())
            lr_bm3d_norm[index] = bm3d_clipped
        
        lr_bm3d_norm = lr_bm3d_norm.astype(np.int16)
        lr_bm3d_norm_clipped = np.clip(lr_bm3d_norm, 0, 1500)
        lr_bm3d_norm_clipped = lr_bm3d_norm_clipped.round()
        lr_bm3d_norm_clipped = lr_bm3d_norm_clipped.astype(np.int16)
        nrrd.write(volume_save_path, lr_bm3d_norm_clipped, spacing_info, index_order='C')

"""
Apply bm3d denoising to data['LR'] of shape 3D(D,H,W) and value [0,1]
data: dictionary from dataloader 
"""
def calculate_scan_bm3d(data):
    lr_scan = data['LR'][0,0].numpy()
    lr_bm3d_norm = np.empty(lr_scan.shape)
    for index, slice_ in enumerate(lr_scan):
        img_slice = rescale_img(slice_, clip=None, max_val=255.0)
        sigma_est = np.mean(estimate_sigma(img_slice, multichannel=False))
        BM3D_denoised_image = bm3d.bm3d(img_slice, sigma_psd=sigma_est, stage_arg=bm3d.BM3DStages.ALL_STAGES) # bm3d.BM3DStages.HARD_THRESHOLDING
        # bm3d_clipped = rescale_img(BM3D_denoised_image, clip=(0.0, 255.0), max_val=slice_.max())
        bm3d_clipped = rescale_img(BM3D_denoised_image, clip=(0.0, 255.0), max_val=1500)
        lr_bm3d_norm[index] = bm3d_clipped
    
    # lr_bm3d_norm = lr_bm3d_norm.astype(np.int16)
    lr_bm3d_norm_clipped = np.clip(lr_bm3d_norm, 0, 1500)
    lr_bm3d_norm_clipped = lr_bm3d_norm_clipped.round()
    # lr_bm3d_norm_clipped = lr_bm3d_norm_clipped.astype(np.int16)
    data['volume'] = torch.from_numpy(lr_bm3d_norm_clipped)
    print(lr_bm3d_norm[10])
    return data

if __name__ == '__main__':
    dataroot_LR = '/datasets/data_st1.0_merged'
    UID = '/datasets/uids/70-30_split/ucla_testUID_70_30_split.txt'
    save_path = '../../results/BM3D-70-30-Split_tileStitch-32x64x64_Ref-k2d100/merged_cases/test_st1.0_norm'
    calculate_bm3d(dataroot_LR, UID, save_path)