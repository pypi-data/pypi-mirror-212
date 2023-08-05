import SimpleITK as sitk
import torch.utils.data as data
import random
import os, glob
import json 
import torch
import numpy as np 
import nibabel as nib
import nrrd
import nibabel
import pydicom
from lung_analysis_pipeline.utils import util

class dcmDataset(data.Dataset):
    def __init__(self, opt): 
        super(dcmDataset, self).__init__()
        self.FILL_RATIO_THRESHOLD = 0.8
        self.opt = opt
        self.in_folder = opt['dataroot_LR']

        # feature extraction ROI 
        if opt['feature_roi_centroid']:
            with open(opt['feature_roi_centroid'], 'r') as json_file:
                self.feature_roi = json.load(json_file)
        if opt['feature_mask']:
            with open(opt['feature_mask'], 'r') as json_file: 
                self.img_to_mask_path = json.load(json_file)
        
        # 3d voxel size
        if self.opt['phase'] == 'train' or (self.opt['phase'] =='val' and self.opt['need_voxels']):
            self.ps = (opt['LR_slice_size'], opt['LR_size'], opt['LR_size'])

        self.paths, self.uids = self.get_instance_paths(opt['dataroot_LR'])

        self.scale = opt['scale']
        self.ToTensor = util.ImgToTensor()

    def __len__(self): 
        return len(self.paths)
    
    def __getitem__(self, index):
        ## load dicoms 
        # data_dir_path = os.path.join(self.paths[index], 'DICOM')
        # mask_dir_path = os.path.join(self.paths[index], 'Contours', 'NIFTI')
        # splits = os.path.normpath(data_dir_path).split(os.sep)
        # LR: extract volume cube during training, else return volume during validation 
        # dcm_files = [os.path.join(data_dir_path, f) for f in os.listdir(data_dir_path) if f.endswith('.dcm')]
        # dcm_files.sort(key=lambda x: int(pydicom.dcmread(x).InstanceNumber))
        # slices = [pydicom.dcmread(f) for f in dcm_files]
        # vol_in = np.stack([slice.pixel_array for slice in slices], axis=0).astype(np.float16)

        ## load NIFTI 
        data_dir_path = self.paths[index]
        data_file_path = os.path.join(data_dir_path, 'Contours', 'NIFTI', 'image.nii.gz')
        # mask_dir_path = os.path.join(data_dir_path, 'Contours', 'NIFTI')
        mask_dir_path = self.img_to_mask_path[data_dir_path]
        image_data = nib.load(data_file_path)
        vol_in = image_data.get_fdata()
        vol_in = np.transpose(vol_in, (2,1,0)) # onvert from WHD format to DHW format
        # Optional: Print the image shape and data type
        # print('Image Shape:', vol_in.shape)
        # print('Data Type:', vol_in.dtype)
        gt_mask = self.load_masks(mask_dir_path)
        # gt_mask = np.expand_dims(gt_mask, axis=0)
        # print('gt_mask Shape:', gt_mask.shape)
        # print('gt_mask Type:', gt_mask.dtype)

        # creates an extra dimension. e.g. (156, 512, 512) becomes (1, 156, 512, 512)
        vol_in = np.expand_dims(vol_in, axis=0)

        # convert to tensors and also within a certain range of values as defined in 'self.ToTensor()' class
        vol_in = self.ToTensor(vol_in, clip=True, raw_data_range=1500.)
        # vol_in = torch.from_numpy(np.array(vol_in, np.float32, copy=False))

        # generate a volume id 
        # patient_id = slices[0].PatientID.replace("_", "-")
        # timepoint = slices[0].StudyDate
        # series_instance_uid = slices[0].SeriesInstanceUID
        # modality = slices[0].Modality 
        # volume_id = f"{patient_id}_{timepoint}_{series_instance_uid}_{modality}"

        # # some info needed when saving results 
        # spacings = [slices[0].PixelSpacing[0], slices[0].PixelSpacing[1], abs(slices[1].SliceLocation - slices[0].SliceLocation)]
        # input_info = {'patient_id': splits[3], 'time': splits[4], 'name': splits[5]}
        # input_info['spacings'] = spacings
        # input_info['image_position'] = slices[0].ImagePositionPatient

        # load ROI centroids for feature extraction if provided 
        feature_rois = []
        if hasattr(self, 'feature_roi'): 
            feature_rois = self.feature_roi[data_dir_path]
            feature_rois = torch.tensor(feature_rois)
        # out_dict = {'LR': vol_in, 'spacings': [], 'uid': volume_id, 'feature_roi_centroids': feature_rois}
        out_dict = {'LR': vol_in, 'spacings': [], 'uid': self.uids[index], 'feature_roi_centroids': feature_rois, 'gt_mask': gt_mask}
        return out_dict
    
    def load_masks(self, mask_root): 
        combined_mask = None 
        for filename in os.listdir(mask_root): 
            if filename.startswith("Lesion"):
                file_path = os.path.join(mask_root, filename)
                mask = nib.load(file_path).get_fdata().astype(np.uint8)
                mask = np.transpose(mask, (2,1,0))
                if combined_mask is None:
                    combined_mask = mask
                else:
                    combined_mask = np.logical_or(combined_mask, mask).astype(np.uint8)

        return combined_mask
    """
    Returns a list of paths of instances. Assumes file structure to be the same as NLST_CT_annotation. 
    """
    def get_instance_paths(self, data_root): 
        paths = [] 
        ids = [] 
        for patient in os.listdir(data_root): 
            id = ''
            patient_path = os.path.join(data_root, patient)
            patient_id = patient.replace("_", "-") + '_'
            if not os.path.isdir(patient_path): 
                continue 
            for timepoint in os.listdir(patient_path): 
                timepoint_id = patient_id + "".join(timepoint.split("-")) + '_'
                time_path = os.path.join(patient_path, timepoint)
                for f in os.listdir(time_path): 
                    instance_id = timepoint_id + f.split('-')[-1] + '_CT'
                    paths.append( os.path.join(time_path, f) )
                    ids.append(instance_id) # [-1]
        return paths, ids