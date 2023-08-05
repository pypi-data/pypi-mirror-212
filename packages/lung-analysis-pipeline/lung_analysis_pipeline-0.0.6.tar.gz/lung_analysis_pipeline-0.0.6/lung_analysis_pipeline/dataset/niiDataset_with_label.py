import numpy as np
import h5py
import torch.utils.data as data
import lung_analysis_pipeline.utils.util as util
import random
import os
import re
import torch
import nibabel as nib


class NIIDataset(data.Dataset):
    def __init__(self, opt):
        super(NIIDataset, self).__init__()
        # useful when extracting 3D mask cube from the input masks
        self.FILL_RATIO_THRESHOLD = 0.8
        self.opt = opt
        self.in_folder = opt['dataroot_LR']
        self.tar_folder = opt['dataroot_HR']
        self.mask_folder = opt['maskroot_HR']
        # 3d voxel size
        if self.opt['phase'] == 'train' or (self.opt['phase'] =='val' and self.opt['need_voxels']):
            self.ps = (opt['LR_slice_size'], opt['LR_size'], opt['LR_size'])       
        self.uids = opt['uids'] # list of uids
        # print('uids:', self.uids)
        # get only a subset of uids if provided
        if opt['subset'] is not None:
           self.uids = self.uids[:opt['subset']]
        self.scale = opt['scale']
        self.ToTensor = util.ImgToTensor()
        # print("-"*40)

    def _cvt_int(self, inputString):
        find_digit = re.search(r'\d', inputString)
        reformat_num = int(float(inputString[find_digit.start():]))
        reformat_str = inputString[:find_digit.start()] + str(reformat_num)
        return reformat_str

    def __getitem__(self, index):
        uid = self.uids[index]
        if self.opt['data_merged']:
            uid_to_open_for_mask_target = uid.split('_')[0]
        else:
            uid_to_open_for_mask_target = uid

        # body mask - first we look at if the random voxel contain 80% of the body mask
        vol_mask = None
        if self.mask_folder:
            with h5py.File(os.path.join(self.mask_folder, uid_to_open_for_mask_target+'.h5'), 'r') as file:
                IMG_THICKNESS, IMG_WIDTH, IMG_HEIGHT = file['data'].shape
                # random index of the 3D voxel for each patient
                if self.opt['phase'] == 'train' or (self.opt['phase'] =='val' and self.opt['need_voxels'] and not self.opt['need_voxels']['tile_x_y']):
                    # print('Getting mask volume')
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
        uid = '/'.join(uid.split('\\'))
        file = nib.load(os.path.join(self.in_folder, uid)).get_fdata()
        file = file.transpose((2, 1, 0))
        file = np.clip(file, -1000, None)
        file += 1000
        file = file.astype(np.int16)
        if self.opt['phase'] == 'train':
            vol_in = file[round(rnd_t_HR/self.scale):round(rnd_t_HR/self.scale)+t,
                                    rnd_h:rnd_h+h, rnd_w:rnd_w+w]
        else:
            if self.mask_folder and self.opt['need_voxels'] and not self.opt['need_voxels']['tile_x_y']:
                vol_in = file[round(rnd_t_HR/self.scale):round(rnd_t_HR/self.scale)+t,
                                        rnd_h:rnd_h+h, rnd_w:rnd_w+w]
            else:
                vol_in = file
    
        # HR (note: HR cube indexes will be same as mask cube indexes since the masks are for HR images)
        vol_tar = None
        if self.tar_folder:
            with h5py.File(os.path.join(self.tar_folder, uid_to_open_for_mask_target+'.h5'), 'r') as file:
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
        if self.opt['use_candidate_atten']:
            vol_in_cp = vol_in.copy()
            vol_in_cp[vol_in_cp < 604] = 0
            vol_in_candidates = self.ToTensor(vol_in_cp)

        vol_tar = np.expand_dims(vol_tar, axis=0)
        vol_mask = np.expand_dims(vol_mask, axis=0)
        # convert to tensors and also within a certain range of values as defined in 'self.ToTensor()' class
        # print('vol in min-max:', vol_in.min(), vol_in.max())
        # print('vol tar min-max:', vol_tar.min(), vol_tar.max())
        vol_in, vol_tar = self.ToTensor(vol_in, raw_data_range=vol_in.max()), self.ToTensor(vol_tar)
        vol_mask = self.ToTensor(vol_mask, raw_data_range = 1)
                
        # print('vol in after transf min-max:', vol_in.min(), vol_in.max())
        # print('vol tar after transf min-max:', vol_tar.min(), vol_tar.max())
        # print('vol tar afer norm min-max:', vol_mask.min(), vol_mask.max())

        # read LR spacings
        spacings = [] 
        
        # set up labels if needed
        if self.opt['need_label']:
            class_label = {'d10':0, 'd25':1, 'd100': 2, 'k1':0, 'k2':1, 'k3':2, 'st1':0, 'st0.6':1, 'st2':2}
            # generate label from path if data is not merged
            if not self.opt['data_merged']:
                kernel_lbl, dose_lbl, st_lbl = self.opt['dataroot_LR'].split('/')[-1].split('_')
                kernel_lbl_to_assign, dose_lbl_to_assign, st_lbl_to_assign = self._cvt_int(kernel_lbl),\
                                                                                        self._cvt_int(dose_lbl), self._cvt_int(st_lbl)
                kernel_lbl = np.expand_dims(class_label[kernel_lbl_to_assign], axis=0)
                dose_lbl = np.expand_dims(class_label[dose_lbl_to_assign], axis=0)
            else:
                kernel_lbl = np.expand_dims(class_label[uid.split('_')[1:][0]], axis=0)
                dose_lbl = np.expand_dims(class_label[uid.split('_')[1:][1]], axis=0)
            
            # store information in dictionary
            out_dict = {'LR': vol_in, 'HR': vol_tar, 'mask': vol_mask, 'spacings': spacings, 'uid': uid,
                        'kernel': kernel_lbl, 'dose': dose_lbl}
        else:
            out_dict = {'LR': vol_in, 'HR': vol_tar, 'mask': vol_mask, 'spacings': spacings, 'uid': uid}        
        
        # candidate attention
        if self.opt['use_candidate_atten']:
            out_dict['Cand'] = vol_in_candidates
        return out_dict

    def __len__(self):
        return len(self.uids)
