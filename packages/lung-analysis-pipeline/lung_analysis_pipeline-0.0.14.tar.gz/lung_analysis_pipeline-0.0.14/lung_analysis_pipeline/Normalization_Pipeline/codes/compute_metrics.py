import os
import nrrd
import h5py 
import numpy as np
import torch
import logging
from collections import OrderedDict
from utils.util import calculate_psnr, calculate_ssim, calculate_pdist
from utils.util import setup_logger, print_metrics
from utils.util import create_pdist_model


def clip_to_range(sample, raw_data_range=1500):
    img = np.clip(np.array(sample, np.float32, copy=False), 0, raw_data_range)
    return img.astype(np.int16)

def read_file(file_path, ext):
    if ext == '.h5':
        with h5py.File(file_path, 'r') as file:
            data = file['data'][()]
    elif ext == '.nrrd':
        data, _ = nrrd.read(file_path)
        data = data.transpose((2, 1, 0))
    else:
        raise ValueError('Input file extension not supported!')
    return data


def main():
    if UID_file:
        with open(UID_file, 'r') as f:
            lines = f.readlines()
            uids = [l.rstrip()+LR_datatype for l in lines]
    else:
        uids = [file for file in os.listdir(path_to_LR) if file.endswith(LR_datatype)]
    # dict for metrics
    pnsr_results = OrderedDict()
    ssim_results = OrderedDict()
    pdist_results = OrderedDict()
    # create pdist model vgg
    pdist_model = create_pdist_model(use_gpu=True)
    # iterate for each cases
    for uid in uids:
        patient_id = uid.split(LR_datatype)[0]
        pnsr_results[patient_id] = {}
        ssim_results[patient_id] = {}
        pdist_results[patient_id] = {}

        # set-up data paths
        LR_case_path = os.path.join(path_to_LR, uid)
        if split_uid_for_ref:
            HR_case_path = os.path.join(path_to_HR, uid.split('_')[0]+HR_datatype)
        else:
            HR_case_path = os.path.join(path_to_HR, uid.split(LR_datatype)[0]+HR_datatype)

        # read LR-HR pair
        LR_data = read_file(LR_case_path, LR_datatype)
        HR_data = read_file(HR_case_path, HR_datatype)
        assert LR_data.shape == HR_data.shape

        sr_vol = clip_to_range(LR_data, raw_data_range=1500.)
        gt_vol = clip_to_range(HR_data, raw_data_range=1500.)
        min_depth = min(sr_vol.shape[0], gt_vol.shape[0])
        sr_vol = sr_vol[:min_depth,...]
        gt_vol = gt_vol[:min_depth,...] # make sure they have the same depth

        # compute metric
        def _calculate_metrics(sr_vol, gt_vol, view='xy'):
            sum_psnr = 0.
            sum_ssim = 0.
            sum_pdist = 0.
            # [D,H,W]
            num_val = 0 # psnr could be inf at xz or yz (near edges), will not calculate
            for i, vol in enumerate(zip(sr_vol, gt_vol)):
                sr_img, gt_img = vol[0], vol[1] # shape: [823, 512, 512] of type numpy.ndarray
                # print('i is {}, sr_img shape is {} and gt_img shape is {}'.format(i, sr_img.shape, gt_img.shape))
                # range is assume to be [0,255] so  have to scale back from 1500 to 255 float64
                crop_size = round(1.0)
                # shape [510, 510]
                cropped_sr_img = sr_img[crop_size:-crop_size, crop_size:-crop_size]\
                                    .astype(np.float64) / 1500. * 255.
                cropped_gt_img = gt_img[crop_size:-crop_size, crop_size:-crop_size]\
                                    .astype(np.float64) / 1500. * 255.
                psnr = calculate_psnr(cropped_sr_img, cropped_gt_img)
                ssim = calculate_ssim(cropped_sr_img, cropped_gt_img)
                pdist = calculate_pdist(pdist_model, cropped_sr_img, cropped_gt_img)
                if psnr != float('inf'):
                    num_val += 1
                    sum_psnr += psnr
                    sum_ssim += ssim
                    sum_pdist += pdist
                logger.info('{:20s} - {:3d}- PSNR: {:.6f} dB; SSIM: {:.6f}; pdist: {:.6f}'\
                                .format(patient_id, i+1, psnr, ssim, pdist))

            pnsr_results[patient_id][view] = sum_psnr / num_val
            ssim_results[patient_id][view] = sum_ssim / num_val
            pdist_results[patient_id][view] = sum_pdist / num_val
            return pnsr_results, ssim_results, pdist_results

        # [H W] axial view
        _calculate_metrics(sr_vol, gt_vol, view='xy')
        # [D W] coronal view
        _calculate_metrics(sr_vol.transpose(1, 0, 2), gt_vol.transpose(1, 0, 2), view='xz')
        # [D H] sagittal view
        _calculate_metrics(sr_vol.transpose(2, 0, 1), gt_vol.transpose(2, 0, 1), view='yz')

    print_metrics(logger, 'test PSNR', pnsr_results)
    print_metrics(logger, 'test SSIM', ssim_results)
    print_metrics(logger, 'test pdist', pdist_results)    
    logger.info('All metrics computed!')



if __name__ == '__main__':
    # set-up data types
    path_to_LR = '/datasets/data_st1.0_merged'
    LR_datatype = '.h5'
    UID_file = '/datasets/uids/70-30_split/ucla_testUID_70_30_split.txt' # if UID provided, read only specific cases

    path_to_HR = '/datasets/reference/k2_d100_st1'
    HR_datatype = '.h5'
    split_uid_for_ref = True

    # set-up logger
    path_to_save_metric = '/workspace/cNormGAN-AC-LT/results/test_Unnorm-70-30-Split_tileStitch-32x64x64_Ref-k2d100/merged_cases'
    setup_logger(None, path_to_save_metric, 'test.log', level=logging.INFO, screen=True)
    logger = logging.getLogger('base')

    main()


