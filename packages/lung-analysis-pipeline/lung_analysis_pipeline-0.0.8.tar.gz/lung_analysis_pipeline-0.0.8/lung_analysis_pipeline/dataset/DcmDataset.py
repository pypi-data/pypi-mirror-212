import numpy as np
import torch.utils.data as data
import SimpleITK as sitk
import pydicom
import lung_analysis_pipeline.utils.util as util
import random
import os, glob
import torch
import nrrd 

class dcmDataset(data.Dataset):
    def __init__(self, dataset_opt):
        super(dcmDataset, self).__init__()
        self.FILL_RATIO_THRESHOLD = 0.8
        self.opt = dataset_opt
        self.in_folder = self.opt['dataroot_LR']

        # 3d voxel size
        if self.opt['phase'] == 'train' or (self.opt['phase'] =='val' and self.opt['need_voxels']):
            self.ps = (self.opt['LR_slice_size'], self.opt['LR_size'], self.opt['LR_size'])
         
        self.paths = []
        for dirpath, dirnames, filenames in os.walk(self.in_folder):
            if any(f.endswith('.dcm') for f in filenames) and 'Contours' not in dirpath:
                self.paths.append(dirpath)
       
        # feature extraction ROI 
        if opt['feature_roi_centroid']:
            with open(opt['feature_roi_centroid'], 'r') as json_file:
                self.feature_roi = json.load(json_file)
        if opt['feature_mask']:
            with open(opt['feature_mask'], 'r') as json_file: 
                self.img_to_mask_path = json.load(json_file)


        self.scale = self.opt['scale']
        self.ToTensor = util.ImgToTensor()

    def __len__(self):
        return len(self.paths)

    def __getitem__(self, index):
        volume_path = self.paths[index]
        dcm_files = [os.path.join(volume_path, f) for f in os.listdir(volume_path) if f.endswith('.dcm')]
        dcm_files.sort(key=lambda x: int(pydicom.dcmread(x).InstanceNumber))
        slices = [pydicom.dcmread(f) for f in dcm_files]
        volume = np.stack([slice.pixel_array for slice in slices], axis=0).astype(np.float16)

        # creates an extra dimension. e.g. 32x64x64 becomes 1x32x64x64
        volume = np.expand_dims(volume, axis=0)

        # convert to tensors and also within a certain range of values as defined in 'self.ToTensor()' class
        transformed_vol = self.ToTensor(volume, clip=True, raw_data_range=1500.)

        # generate a volume id 
        patient_id = slices[0].PatientID.replace("_", "-")
        timepoint = slices[0].StudyDate
        series_instance_uid = slices[0].SeriesInstanceUID
        modality = slices[0].Modality 
        volume_id = f"{patient_id}_{timepoint}_{series_instance_uid}_{modality}"

        # HR and mask are not allowed to be None. Passing vol_in. 
        out_dict = {'original_vol_in': torch.from_numpy(original_vol_in), 'LR': transformed_vol, 'spacings': [], 'uid': volume_id}

        # load ROI centroids for feature extraction if provided 
        feature_rois = []
        if hasattr(self, 'feature_roi'): 
            feature_rois = self.feature_roi[data_dir_path]
            feature_rois = torch.tensor(feature_rois)
            out_dict['feature_roi_centroids'] = feature_rois
        # if hasattr(self, 'img_to_mask_path'): 
        #     gt_mask = self.load_masks(mask_dir_path)
        #     out_dict['gt_mask'] = gt_mask 

        return out_dict