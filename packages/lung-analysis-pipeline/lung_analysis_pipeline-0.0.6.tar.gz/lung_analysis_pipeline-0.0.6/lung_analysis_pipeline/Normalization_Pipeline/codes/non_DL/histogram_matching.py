import h5py
import SimpleITK as sitk
import os
import json
import nrrd
import numpy as np


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

"""
Histogram matching following the method developed on
Nyul et al 2001 (ITK implementation)
inputs:
- mov_scan: np.array containing the image to normalize
- ref_scan np.array containing the reference image
- histogram levels
- number of matched points
- Threshold Mean setting
outputs:
- histogram matched image
"""
def histogram_matching(lr_scan_path, ref_scan_path, UID, save_path, histogram_levels=2048, match_points=100, set_th_mean=True, split_uid_for_ref=True):
    with open(UID, 'r') as f:
        lines = f.readlines()
        uids = [l.rstrip() for l in lines]
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # read each uid
    for uid in uids:
        if split_uid_for_ref:
            uid_for_ref = uid.split('_')[0]
        else:
            uid_for_ref = uid
        print('Reading UID:', uid)
        LR_path = os.path.join(lr_scan_path, '{}.h5'.format(uid))
        HR_path = os.path.join(ref_scan_path, '{}.h5'.format(uid_for_ref))
        with h5py.File(LR_path, 'r') as file:
            mov_scan = file['data'][()]
        with h5py.File(HR_path, 'r') as file:
            ref_scan = file['data'][()]

        header = os.path.join(ref_scan_path, '{}.json'.format(uid_for_ref))
        volume_save_path = os.path.join(save_path, '{}.nrrd'.format(uid))
        spacing_info = read_config(header)
 
        # convert np arrays into itk image objects
        ref = sitk.GetImageFromArray(ref_scan.astype('float32'))
        mov = sitk.GetImageFromArray(mov_scan.astype('float32'))
        # perform histogram matching
        caster = sitk.CastImageFilter()
        caster.SetOutputPixelType(ref.GetPixelID())
        matcher = sitk.HistogramMatchingImageFilter()
        matcher.SetNumberOfHistogramLevels(histogram_levels)
        matcher.SetNumberOfMatchPoints(match_points)
        matcher.SetThresholdAtMeanIntensity(set_th_mean)
        matched_vol = matcher.Execute(mov, ref)
        nda = sitk.GetArrayFromImage(matched_vol)
        # clip to desired range
        nda = nda.astype(np.int16)
        nda_clipped = np.clip(nda, 0, 1500)
        nda_clipped = nda_clipped.astype(np.int16)
        # nrrd.write(volume_save_path, nda, spacing_info, index_order='C')
        nrrd.write(volume_save_path, nda_clipped, spacing_info, index_order='C')
    print('HM DONE!')


if __name__ == '__main__':
    dataroot_LR = '/datasets/data_st1.0_merged' # '/dingo_data_leihaowei/nastaran_test_h5/k2_d10_st1.0'
    dataroot_HR = '/datasets/reference/k2_d100_st1' # '/dingo_data_leihaowei/nastaran_test_h5/k2_d100_st1.0'
    UID = '/datasets/uids/70-30_split/ucla_testUID_70_30_split.txt' # '/datasets/nodule_annotations/ucla_nastaran_subset_32_test_uid.txt'
    save_path = '../../results/test_HM-70-30-Split_tileStitch-32x64x64_Ref-k2d100/merged_cases/test_st1.0_norm' # train_CNN-SRResNet-EQMergedData_tileStitch-32x64x64_Ref-k2d100
    histogram_matching(dataroot_LR, dataroot_HR, UID, save_path)



