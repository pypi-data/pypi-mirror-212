import os, os.path
import glob
import math
import argparse
import random
import logging
import torch
import options.options as option
from utils import util
from data import create_dataloader, create_dataset
from models import create_model
import numpy as np
from collections import OrderedDict


def main():
    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-opt', type=str, required=True, help='Path to option JSON file.')
    opt = option.parse(parser.parse_args().opt, is_train=True)
    # convert to a dictionary with 'None' for missing key
    opt = option.dict_to_nonedict(opt)
    torch.backends.cudnn.benchmark = True
 
    if opt['path']['resume_state']:
        resume_state = torch.load(opt['path']['resume_state'])
    else:
        resume_state = None
        util.mkdir_and_rename(opt['path']['experiments_root'])
        util.mkdirs((path for key, path in opt['path'].items() if not key == 'experiments_root'
                     and 'pretrain_model' not in key and 'resume' not in key))

    # config loggers. without it, logger will not work
    util.setup_logger('base', opt['path']['log'], 'train', level=logging.INFO, screen=True)
    util.setup_logger('val', opt['path']['log'], 'val', level=logging.INFO)
    logger = logging.getLogger('base') # get the 'base' logger which records training data
    
    # if 'resume_state' is not None, start training from the end state of weights
    if resume_state:
        logger.info('Resuming training from epoch: {}, iter: {}.'.format(
            resume_state['epoch'], resume_state['iter']))
        # check resume options and paths for model weights are available
        option.check_resume(opt)  
    
    # print the parsed dictionary into readable form and print on screen
    logger.info(option.dict2str(opt))

    # set up tensorboard logger if path specified and 'debug' not in name
    if opt['use_tb_logger'] and 'debug' not in opt['name']:
        from torch.utils.tensorboard import SummaryWriter
        # create summary writer
        tb_logger = SummaryWriter(log_dir='../tb_logger/' + opt['name'])
    seed = opt['train']['manual_seed']
    if seed is None:
        seed = random.randint(1, 10000)
    logger.info('Random seed: {}'.format(seed))
    util.set_random_seed(seed)

    need_label, data_merged = opt['need_label'], opt['data_merged'] 
    need_atten = opt['network_G']['use_attention']
    if need_atten:
        need_candidate_atten = opt['network_G']['use_attention']['generate_candidate']
    else:
        need_candidate_atten = opt['network_G']['use_attention']
        
    # 'train' and 'val' keys in opt['datasets'] with parameters for their respective phase
    for phase, dataset_opt in opt['datasets'].items():
        dataset_opt['need_label'] = need_label
        dataset_opt['data_merged'] = data_merged
        dataset_opt['use_candidate_atten'] = need_candidate_atten
        if phase == 'train':
            train_set = create_dataset(dataset_opt)
            train_size = int(math.floor(len(train_set) / dataset_opt['batch_size']))
            logger.info('Number of train cases: {:,d}, iters required: total cases/batch size = {}/{}={}'.format(
                len(train_set), len(train_set), dataset_opt['batch_size'], train_size))
            total_iters = int(opt['train']['niter'])
            print("Total training iterations:", total_iters)
            total_epochs = int(math.ceil(total_iters / train_size))
            logger.info('Total epochs needed: {:,d}/{:,d} = {:,d} for iters {:,d}'.format(
                total_iters, train_size, total_epochs, total_iters))
            train_loader = create_dataloader(train_set, dataset_opt)
        elif phase == 'val':
            val_set = create_dataset(dataset_opt)
            val_loader = create_dataloader(val_set, dataset_opt)
            logger.info('Number of val cases in [{:s}]: {:d}'.format(dataset_opt['name'],
                                                                      len(val_set)))
        else:
            raise NotImplementedError('Phase [{:s}] is not recognized.'.format(phase))
    assert train_loader is not None

    """
    data = iter(train_loader).next()
    print("batch data keys:", data.keys())
    print('LR shape:', data['LR'].shape)
    print('HR shape:', data['HR'].shape)
    print('Mask shape:', data['mask'].shape)
    print('Candidates shape:', data['Cand'].shape)
    print('uid:', data['uid'])
    print('kernel:', data['kernel'])
    print('dose:', data['dose'])
    print('-'*40)
    data = iter(val_loader).next()
    print("batch data keys:", data.keys())
    print('LR shape:', data['LR'].shape)
    print('HR shape:', data['HR'].shape)
    print('Mask shape:', data['mask'].shape)
    print('Candidates shape:', data['Cand'].shape)
    """

    # create model (by default, model is already fp32)
    model = create_model(opt)
    # initialize amp for mixed precision training, determines best precision for each layer
    model.initialize_amp()

    if resume_state:
        start_epoch = resume_state['epoch'] # get last epoch training was stopped on, which becomes start epoch
        current_step = resume_state['iter'] # get number of iterations from last training
        model.resume_training(resume_state)  # handle optimizers and schedulers
    else:
        current_step = 0 
        start_epoch = 0

    print('Model Instantiated!')
    ## =====================
    ## START TRAINING
    ## =====================
    logger.info('Start training from epoch: {:d}, iter: {:d}'.format(start_epoch, current_step))
    for epoch in range(start_epoch, total_epochs):
        # print("Epoch:", epoch)
        for _, train_data in enumerate(train_loader):
            current_step += 1
            if current_step > total_iters:
                break
            # set up attributes: 'self.var_L' & 'self.real_H' for 'LR' &  'HR' image respectively
            model.feed_train_data(train_data)
            model.optimize_parameters(current_step)
            # update learning rate, called after .step() after pytorch 1.1
            model.update_learning_rate()
            # print("check for logging: {} % {} == 0 = {}".format(current_step, opt['logger']['print_freq'],
            # current_step % opt['logger']['print_freq'] == 0))
            # log : opt['logger']['print_freq'] == 10, so logger will print every 10 step
            
            if current_step % opt['logger']['print_freq'] == 0:
                logs = model.get_current_log() # gets dictionary that contains gan losses
                # 'get_current_learning_rate()' returns current lr for generator
                message = '<epoch:{:5d}, iter:{:8,d}, lr:{:.6e}> '.format(
                    epoch, current_step, model.get_current_learning_rate())
                
                # 'logs.items()' give (key, value) pairs, we add that to the initial message we set up above
                for k, v in logs.items():
                    message += '{:s}: {:.4e} '.format(k, v)
                    # add log items (losses) to tensorboard logger and print message on screen
                    if opt['use_tb_logger'] and 'debug' not in opt['name']:
                        tb_logger.add_scalar(k, v, current_step)
                logger.info(message)

            # save models and training states at every that step
            if current_step % opt['logger']['save_checkpoint_freq'] == 0:
                logger.info('Saving models and training states.')
                model.save(current_step) # save 'state_dict' of both G & D at given step
                # save 'epoch', 'current_step', 'optimizer', 'scheduler'
                model.save_training_state(epoch, current_step) 

            # validation loop
            # print("checking to run validation: {} % {} = {}".format(current_step, opt['train']['val_freq'],
            if current_step % opt['train']['val_freq'] == 0:
                # copy net and convert to fp16 if necessary, according to json
                model.half()
                # create pdist model (PNetLin - based on vgg16)
                pdist_model = util.create_pdist_model()
                # 'OrderedDictionary' to store evaluation metrics
                pnsr_results = OrderedDict()
                ssim_results = OrderedDict()
                pdist_results = OrderedDict()
                for val_data in val_loader:
                    logger.info('start inference...')
                    model.feed_test_data(val_data)
                    model.test(val_data)  # test
                    # get cpu numpy from cuda tensor
                    has_mask = False if val_loader.dataset.opt['maskroot_HR'] is None else True
                    visuals = model.get_current_visuals(val_data, maskOn=has_mask)
                    # save volume data
                    patient_id = val_data['uid'][0]
                    util.mkdir(os.path.join(opt['path']['val_images'], str(current_step)))
                    vol_path = os.path.join(opt['path']['val_images'], str(current_step), patient_id)
                    LR_spacings = [x.item() for x in val_data['spacings']] if val_data['spacings'] else None
                    if opt['result_format'] == 'nrrd':
                        logger.info('saving nnrd...')
                        sr_vol = util.tensor2img(visuals['SR'], out_type=np.uint16) 
                        util.save_vol(opt, LR_spacings, vol_path + '.nrrd', sr_vol)
                    elif opt['result_format'] == 'dicom':
                        logger.info('saving dicoms...') 
                        sr_vol = util.tensor2img(visuals['SR'], out_type=np.int16, intercept = -1000) 
                        util.save_dicoms(opt, LR_spacings, vol_path, sr_vol)
                    else: 
                        raise NotImplementedError('supported output format: nrrd or dicom')

                    # initialize dictionary with empty {}
                    pnsr_results[patient_id] = {}
                    ssim_results[patient_id] = {}
                    pdist_results[patient_id] = {}

                    def _calculate_metrics(sr_vol, gt_vol, view='xy'):
                        sum_psnr = 0.
                        sum_ssim = 0.
                        sum_pdist = 0.
                        # [D,H,W]
                        num_val = 0  # psnr could be inf at xz or yz (near edges), will not calculate
                        for i, vol in enumerate(zip(sr_vol, gt_vol)):
                            sr_img, gt_img = vol[0], vol[1]
                            # calculate PSNR and SSIM
                            # range is assume to be [0,255] so  have to scale back from 1500 to 255 float64
                            crop_size = round(opt['scale'])
                            cropped_sr_img = sr_img[crop_size:-crop_size, crop_size:-crop_size] \
                                                 .astype(np.float64) / 1500. * 255.
                            cropped_gt_img = gt_img[crop_size:-crop_size, crop_size:-crop_size] \
                                                 .astype(np.float64) / 1500. * 255.

                            psnr = util.calculate_psnr(cropped_sr_img, cropped_gt_img)
                            ssim = util.calculate_ssim(cropped_sr_img, cropped_gt_img)
                            pdist = util.calculate_pdist(pdist_model, cropped_sr_img, cropped_gt_img)

                            if psnr != float('inf'):
                                num_val += 1
                                sum_psnr += psnr
                                sum_ssim += ssim
                                sum_pdist += pdist
                            logger.info('{:20s} - {:3d}- PSNR: {:.6f} dB; SSIM: {:.6f}; pdist: {:.6f}.' \
                                        .format(patient_id, i + 1, psnr, ssim, pdist))

                        pnsr_results[patient_id][view] = sum_psnr / num_val
                        ssim_results[patient_id][view] = sum_ssim / num_val
                        pdist_results[patient_id][view] = sum_pdist / num_val
                        return pnsr_results, ssim_results, pdist_results

                    sr_vol = util.tensor2img(visuals['SR'], out_type=np.uint16) 
                    gt_vol = util.tensor2img(visuals['HR'], out_type=np.uint16) # uint16 range [0,1500]
                    # [H W] axial view
                    _calculate_metrics(sr_vol, gt_vol, view='xy')
                    # [D W] coronal view
                    _calculate_metrics(sr_vol.transpose(1, 0, 2), gt_vol.transpose(1, 0, 2), view='xz')
                    # [D H] sagittal view
                    _calculate_metrics(sr_vol.transpose(2, 0, 1), gt_vol.transpose(2, 0, 1), view='yz')

                logger_val = logging.getLogger('val')  # validation logger
                logger_val.info('<epoch:{:5d}, iter:{:8,d} > '.format(epoch, current_step))
                # prints the metrics to screen
                avg_psnr = util.print_metrics(logger_val, 'val PSNR', pnsr_results)
                avg_ssim = util.print_metrics(logger_val, 'val SSIM', ssim_results)
                avg_pdist = util.print_metrics(logger_val, 'val pdist', pdist_results)

                # record evluation metrics on tensorboard
                if opt['use_tb_logger'] and 'debug' not in opt['name']:
                    tb_logger.add_scalars('psnr', avg_psnr, current_step)
                    tb_logger.add_scalars('ssim', avg_ssim, current_step)
                    tb_logger.add_scalars('pdist', avg_pdist, current_step)

    logger.info('Saving the final model.')
    model.save('latest')
    logger.info('End of training.')


if __name__ == '__main__':
    main()
