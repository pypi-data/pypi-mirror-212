import numpy as np
import h5py
import torch.utils.data as data
import utils.util as util
import random
import os
import torch


class h5Dataset(data.Dataset):
    def __init__(self, opt):
        super(h5Dataset, self).__init__()
        # useful when extracting 3D mask cube from the input masks
        self.FILL_RATIO_THRESHOLD = 0.8
        self.opt = opt # 'opt' is dictionary of parameters for either training/validation
        self.in_folder = opt['dataroot_LR']
        # print("-"*40)
        # print("input folder is:", self.in_folder)
        self.tar_folder = opt['dataroot_HR']
        # print("target folder is:", self.tar_folder)
        self.mask_folder = opt['maskroot_HR']
        # print("mask folder is:", self.mask_folder)
        # print("phase:", self.opt['phase'])

        # 3d voxel size
        if self.opt['phase'] == 'train' or self.opt['need_voxels']:
            self.ps = (opt['LR_slice_size'], opt['LR_size'], opt['LR_size'])
            # print("ps:", self.ps)        
        self.uids = opt['uids'] # list of uids
        # get only a subset of uids if provided
        if opt['subset'] is not None:
           self.uids = self.uids[:opt['subset']]
        self.scale = opt['scale']
        # print("scale:", self.scale)
        self.ToTensor = util.ImgToTensor()
        # print("-"*40)

    def __getitem__(self, index):
        uid = self.uids[index]
        # print("selected uid {}: {}".format(index, uid))
        # body mask - first we look at if the random voxel contain 80% of the body mask
        vol_mask = None
        if self.mask_folder:
            with h5py.File(os.path.join(self.mask_folder, uid+'.h5'), 'r') as file:
                IMG_THICKNESS, IMG_WIDTH, IMG_HEIGHT = file['data'].shape
                # random index of the 3D voxel for each patient
                if self.opt['phase'] == 'train' or (self.opt['need_voxels'] and not self.opt['need_voxels']['tile_x_y']):
                    t, w, h = self.ps
                    # print("t, w, h = {}, {}, {}".format(t, w, h))
                    # randomly search the voxel until 80% filled with ones
                    fill_ratio = 0.
                    """
                    randomly search for a 3D mask cube of size specified in t,w,h. 80% of the mask
                    must be filled with ones
                    """
                    # print("checking for fill ratio")
                    # print("*"*40)
                    while fill_ratio < self.FILL_RATIO_THRESHOLD:
                        rnd_t_HR = random.randint(0, IMG_THICKNESS - int(t * self.scale))
                        rnd_h = random.randint(0, IMG_HEIGHT - h)
                        rnd_w = random.randint(0, IMG_WIDTH - w)
                        extracted_cube = file['data'][rnd_t_HR:rnd_t_HR+int(t*self.scale), rnd_h:rnd_h+h, rnd_w:rnd_w+w].sum()
                        total_required = (self.scale * t * w * h)
                        fill_ratio = extracted_cube/total_required
                    vol_mask = None # mask not used for training, only for extracting LR and HR volume

                # get vol_mask during validation
                if self.opt['phase'] == 'val':
                    if self.mask_folder and self.opt['need_voxels'] and not self.opt['need_voxels']['tile_x_y']:
                        vol_mask = file['data'][rnd_t_HR:rnd_t_HR+int(t*self.scale), rnd_h:rnd_h+h, rnd_w:rnd_w+w]
                    else:
                        vol_mask = file['data'][()]

        # LR
        with h5py.File(os.path.join(self.in_folder, uid+'.h5'), 'r') as file:
            # print("LR data shape:", file['data'].shape) # same shape as mask 
            # extract volume cube during training, else return entire volume during validation
            if self.opt['phase'] == 'train':
                # print("LR z -> {}/{}:({}/{})+{}".format(rnd_t_HR, self.scale, rnd_t_HR, self.scale, t))
                # print("LR h -> {}:{}+{}".format(rnd_h, rnd_h, h))
                # print("LR w -> {}:{}+{}".format(rnd_w, rnd_w, w))
                vol_in = file['data'][round(rnd_t_HR/self.scale):round(rnd_t_HR/self.scale)+t,
                                      rnd_h:rnd_h+h, rnd_w:rnd_w+w]
            else:
                if self.mask_folder and self.opt['need_voxels'] and not self.opt['need_voxels']['tile_x_y']:
                    vol_in = file['data'][round(rnd_t_HR/self.scale):round(rnd_t_HR/self.scale)+t,
                                          rnd_h:rnd_h+h, rnd_w:rnd_w+w]
                else:
                    vol_in = file['data'][()]
        
        # HR (note: HR cube indexes will be same as mask cube indexes since the masks are for HR images)
        vol_tar = None
        if self.tar_folder:
            with h5py.File(os.path.join(self.tar_folder, uid+'.h5'), 'r') as file:
                # extract volume cube during training, else return entire volume during validation
                if self.opt['phase'] == 'train':
                    # print("HR z -> {}:{}+({}*{})".format(rnd_t_HR, rnd_t_HR, t, self.scale))
                    # print("HR h -> {}:{}+{}".format(rnd_h, rnd_h, h))
                    # print("HR w -> {}:{}+{}".format(rnd_w, rnd_w, w))
                    vol_tar = file['data'][rnd_t_HR:rnd_t_HR+int(t*self.scale), rnd_h:rnd_h+h, rnd_w:rnd_w+w]
                else:
                    if self.mask_folder and self.opt['need_voxels'] and not self.opt['need_voxels']['tile_x_y']:
                        vol_tar = file['data'][rnd_t_HR:rnd_t_HR+int(t*self.scale), rnd_h:rnd_h+h, rnd_w:rnd_w+w]
                    else:
                        vol_tar = file['data'][()]

        # creates an extra dimension. e.g. 32x64x64 becomes 1x32x64x64
        vol_in = np.expand_dims(vol_in, axis=0)
        vol_tar = np.expand_dims(vol_tar, axis=0)
        vol_mask = np.expand_dims(vol_mask, axis=0)
        # convert to tensors and also within a certain range of values as defined in 'self.ToTensor()' class
        vol_in, vol_tar = self.ToTensor(vol_in), self.ToTensor(vol_tar)
        vol_mask = self.ToTensor(vol_mask, raw_data_range = 1)

        # read LR spacings
        spacings = [] 
        if self.opt['phase'] == 'val':
            config_path = os.path.join(self.in_folder, uid + '.json')
            # we only need spacing information for the configuration file
            meta_data = util.read_config(config_path)
            spacings = meta_data['Spacing']

        # store information in dictionary 
        out_dict = {'LR': vol_in, 'HR': vol_tar, 'mask': vol_mask, 
                    'spacings': spacings, 'uid': uid
                    }
        return out_dict

    def __len__(self):
        return len(self.uids)
