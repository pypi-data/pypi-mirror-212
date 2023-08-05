import numpy as np
import h5py
import torch.utils.data as data
import lung_analysis_pipeline.utils.util as util
import random
import os
import re
import torch


class h5Dataset(data.Dataset):
    def __init__(self, dataset_opt):
        super(h5Dataset, self).__init__()
        # useful when extracting 3D mask cube from the input masks
        self.FILL_RATIO_THRESHOLD = 0.8
        self.opt = dataset_opt
        self.in_folder = dataset_opt['dataroot_LR']
        self.tar_folder = dataset_opt['dataroot_HR']
        self.mask_folder = dataset_opt['maskroot_HR']
        # self.ps = (32, 64, 64)
        with open(dataset_opt['uids_location']) as f:
            self.uids = [x.rstrip() for x in f.readlines()]
        self.scale = 1.
        self.ToTensor = util.ImgToTensor()

    def _cvt_int(self, inputString):
        find_digit = re.search(r'\d', inputString)
        reformat_num = int(float(inputString[find_digit.start():]))
        reformat_str = inputString[:find_digit.start()] + str(reformat_num)
        return reformat_str

    def __getitem__(self, index):
        uid = self.uids[index]
        uid_to_open_for_mask_target = uid.split('_')[0]

        # body mask - first we look at if the random voxel contain 80% of the body mask
        vol_mask = None
        if self.mask_folder:
            with h5py.File(os.path.join(self.mask_folder, uid_to_open_for_mask_target+'.h5'), 'r') as file:
                IMG_THICKNESS, IMG_WIDTH, IMG_HEIGHT = file['data'].shape
                vol_mask = file['data'][()]
        
        # LR
        with h5py.File(os.path.join(self.in_folder, uid+'.h5'), 'r') as file:
            vol_in = file['data'][()]
        
        # HR (note: HR cube indexes will be same as mask cube indexes since the masks are for HR images)
        vol_tar = None
        if self.tar_folder:
            with h5py.File(os.path.join(self.tar_folder, uid_to_open_for_mask_target+'.h5'), 'r') as file:
                vol_tar = file['data'][()]

        # creates an extra dimension. e.g. 32x64x64 becomes 1x32x64x64
        vol_in = np.expand_dims(vol_in, axis=0)
        vol_tar = np.expand_dims(vol_tar, axis=0)
        vol_mask = np.expand_dims(vol_mask, axis=0)

        # convert to tensors and also within a certain range of values as defined in 'self.ToTensor()' class
      
        vol_in, vol_tar = self.ToTensor(vol_in, clip=True, raw_data_range=1500.), self.ToTensor(vol_tar, clip=True, raw_data_range=1500.)
        vol_mask = self.ToTensor(vol_mask, clip=False, raw_data_range = 1)

        # read LR spacings
        spacings = [] 
        config_path = os.path.join(self.in_folder, uid + '.json')
        meta_data = util.read_config(config_path) # we only need spacing information for the configuration file
        spacings = meta_data['Spacing']

        out_dict = {'LR': vol_in, 'HR': vol_tar, 'mask': vol_mask, 'spacings': spacings, 'uid': uid}        

        return out_dict

    def __len__(self):
        return len(self.uids)
