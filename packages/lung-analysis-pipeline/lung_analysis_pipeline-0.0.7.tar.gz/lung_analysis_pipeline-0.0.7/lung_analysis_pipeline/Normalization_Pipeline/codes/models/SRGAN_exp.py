import logging
from collections import OrderedDict
import torch
import torch.nn as nn
import models.lr_scheduler as lr_scheduler
import models.networks as networks
from .base_model import BaseModel
from models.modules.loss import GANLoss, GradientPenaltyLoss
from tqdm import tqdm
"""
Amp allows users to easily experiment with different pure and mixed precision modes. 
Commonly-used default modes are chosen by selecting an “optimization level” or opt_level; each opt_level 
establishes a set of properties that govern Amp’s implementation of pure or mixed precision training.
- opt_level: 01 = Mixed Precision (recommended for typical use)
"""
# from apex import amp
# import apex
from torch.cuda import amp
logger = logging.getLogger('base')


"""
Instantiates both generator and discriminator, put models in training, define losses, optimizers and schedulers
"""
class SRGANModel(BaseModel):
    def __init__(self, opt):
        super(SRGANModel, self).__init__(opt)
        train_opt = opt['train']
        if self.is_train:
            self.scaler = amp.GradScaler()
            self.netD = networks.define_D(opt).to(self.device)

        # define losses, optimizer and scheduler for training mode
        if self.is_train:
            # pixel loss
            if train_opt['pixel_weight'] > 0:
                l_pix_type = train_opt['pixel_criterion']
                if l_pix_type == 'l1':
                    self.cri_pix = nn.L1Loss().to(self.device)
                elif l_pix_type == 'l2':
                    self.cri_pix = nn.MSELoss().to(self.device)
                else:
                    raise NotImplementedError('Loss type [{:s}] not recognized.'.format(l_pix_type))
                self.l_pix_w = train_opt['pixel_weight'] # get pixel weight
            else:
                logger.info('Skipping pixel loss ...')
                self.cri_pix = None

            # set perceptual loss
            if train_opt['feature_criterion']:
                l_fea_type = train_opt['feature_criterion']['model_type']
                self.cri_fea = networks.define_PL(opt, l_fea_type).to(self.device)
                self.l_fea_w = train_opt['feature_criterion']['feature_weight'] # get feature weight
            else:
                logger.info('Skipping feature loss ...')
                self.cri_fea = None
        
            # set adversarial loss loss
            self.cri_adv = nn.BCEWithLogitsLoss().to(self.device)
            self.adv_w = train_opt['gan_weight']
            
            # D_update_ratio (how many times discriminator should be train after each generator training) 
            self.D_update_ratio = train_opt['D_update_ratio'] if train_opt['D_update_ratio'] else 1
            print("D update ratio:", self.D_update_ratio)
            self.D_init_iters = train_opt['D_init_iters'] if train_opt['D_init_iters'] else 0
            print("D init iters:", self.D_init_iters)

            # initialize gradient penality
            if "wgan" in train_opt['gan_type']:
                if train_opt['gan_type'] == "wgan-gp":
                    self.cri_gp = GradientPenaltyLoss(center=1.).to(self.device)
                elif train_opt['gan_type'] == "wgan-gp0":
                    self.cri_gp = GradientPenaltyLoss(center=0.).to(self.device)
                else:
                    raise NotImplementedError("{:s} not found".format(train_opt['gan_type']))
                self.l_gp_w = 10. # weight for gradient penality (used in 'optimize_parameters' function)

            # optimizers - weight decay for generator
            """
            Returns an iterator over module parameters, yielding both the name of the parameter as well as
            the parameter itself, which we unpack into k, v.
            ----------------------------------------------------
            optim_params = []
            for k, v in self.netG.named_parameters():  # optimize for a part of the model
                if v.requires_grad:
                    optim_params.append(v)
                else:
                    logger.warning('Params [{:s}] will not optimize.'.format(k))
            """

            # initialize generator optimizer with parameters that only require gradients
            self.optimizer_G = torch.optim.Adam(self.netG.parameters(), lr=train_opt['lr_G'], \
                betas=(train_opt['beta1_G'], train_opt['beta2_G']))

            """
            self.optimizer_G = torch.optim.RMSprop(optim_params, lr=train_opt['lr_G'], weight_decay=wd_G)
            """
            self.optimizers.append(self.optimizer_G) # add optimizer to list defined in base class
            # optimizer for discriminator for entire model parameters
            self.optimizer_D = torch.optim.Adam(self.netD.parameters(), lr=train_opt['lr_D'], \
                betas=(train_opt['beta1_D'], train_opt['beta2_D']))
            self.optimizers.append(self.optimizer_D) # add optimizer to list defined in base class

            # configure schedulers
            if train_opt['lr_scheme'] == 'MultiStepLR':
                # for each optimizer, we have a scheduler added to a list, defined in base class
                for optimizer in self.optimizers:
                    self.schedulers.append(
                        lr_scheduler.MultiStepLR_Restart(optimizer, train_opt['lr_steps'], # [20e3, 40e3, 60e3]
                                                         restarts=train_opt['restarts'], # null
                                                         weights=train_opt['restart_weights'], # null
                                                         gamma=train_opt['lr_gamma'], # 0.5
                                                         clear_state=train_opt['clear_state'])) # None
            elif train_opt['lr_scheme'] == 'CosineAnnealingLR':
                for optimizer in self.optimizers:
                    self.schedulers.append(
                        lr_scheduler.CosineAnnealingLR_Restart(optimizer, train_opt['T_period'],
                                                               eta_min=train_opt['eta_min'],
                                                               restarts=train_opt['restarts'],
                                                               weights=train_opt['restart_weights']))
            else:
                raise NotImplementedError('Choose MultiStepLR or CosineAnnealingLR')

            # create OrderedDict
            self.log_dict = OrderedDict()
        self.print_network(use_logger=True)
        self.load() 

    """
    Initializes model for mixed precision training, depending on 'opt_level'. Below is sample implementation
    -----------------------------------------------------------------------
    # Declare model and optimizer as usual, with default (FP32) precision
    model = torch.nn.Linear(D_in, D_out).cuda()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)

    # Allow Amp to perform casts as required by the opt_level
    model, optimizer = amp.initialize(model, optimizer, opt_level="O1")
    ...
    # loss.backward() becomes:
    with amp.scale_loss(loss, optimizer) as scaled_loss:
        scaled_loss.backward()
    """
    def initialize_amp(self):
        # [self.netG, self.netD], [self.optimizer_G, self.optimizer_D] = \
        # amp.initialize([self.netG, self.netD], [self.optimizer_G, self.optimizer_D],
        #                opt_level=self.opt['opt_level'], num_losses = 2)
        if self.opt['gpu_ids']: 
            """
            Implements data parallelism at the module level. This container parallelizes 
            the application of the given module by splitting the input across the specified gpus
            """
            assert torch.cuda.is_available()
            self.netG = nn.DataParallel(self.netG)
            self.netD = nn.DataParallel(self.netD)

    def test(self, data):
        
        
        if self.opt['precision'] == 'fp16':
            var_L_eval = self.var_L.half()
            if self.opt['network_G']['use_attention']:
                if self.opt['network_G']['use_attention']['generate_candidate']:
                    var_L_eval_candidate = self.cand_L_test.half()
        else:
            var_L_eval = self.var_L
            if self.opt['network_G']['use_attention']:
                if self.opt['network_G']['use_attention']['generate_candidate']:
                    var_L_eval_candidate = self.cand_L_test

        opt_val = self.opt['datasets']['val']
        num_HR = int (data['LR'].size(2) * self.opt['scale'])
        HR_ot = int(self.opt['scale'] * self.ot)
        if not opt_val['need_voxels']:
            print('---- Full size image prediction -----')
            pt, H, W = self.var_L.size(2), self.var_L.size(3), self.var_L.size(4)
            pt = int(pt * self.opt['scale'])
            self.fake_H = torch.empty(1, 1,  num_HR, H, W, device=self.device)
            if self.opt['precision'] == 'fp16':
                fake_H_in_chunks = torch.empty(self.nt, 1,  pt, H, W, dtype=torch.half, device=self.device)
            else:
                fake_H_in_chunks = torch.empty(self.nt, 1,  pt, H, W, device=self.device)
            stitch_mask = torch.zeros_like(self.fake_H, device=self.device)
            # generate predictions
            with torch.no_grad():
                if opt_val['full_volume']:
                    self.fake_H = self.netG_eval(var_L_eval)
                else:
                    for i in range(0, self.nt):
                        fake_H_in_chunks[[i],...] = self.netG_eval(var_L_eval[[i],...])
                    # stitch volume in z-direction
                    for i in range(0, self.nt - 1):
                        ts, te = i * (pt - HR_ot), i * (pt - HR_ot) + pt
                        self.fake_H[0, 0, ts:te, :, :] = (self.fake_H[0, 0, ts:te, :, :] * stitch_mask[0, 0, ts:te, :, :] +
                        fake_H_in_chunks[i,...].float() * (2 - stitch_mask[0, 0, ts:te, :, :])) / 2
                        stitch_mask[0, 0, ts:te, :, :] = 1.
                    # stitch last volume
                    self.fake_H[0, 0, -pt:, :, :] = \
                        (self.fake_H[0, 0, -pt:, :, :] * stitch_mask[0, 0, -pt:, :, :] +
                        fake_H_in_chunks[-1,...].float() * (2 - stitch_mask[0, 0, -pt:, :, :])) / 2
        else:
            if opt_val['need_voxels'] and not opt_val['need_voxels']['tile_x_y']:
                # print('---- Random voxel prediction-----')
                self.fake_H = self.netG_eval(var_L_eval).float()
            elif opt_val['need_voxels'] and opt_val['need_voxels']['tile_x_y']:
                # print('---- Sliding Tile Inference -----')
                pt, H, W = opt_val['slice_size'], data['LR'].size(3), data['LR'].size(4)
                pt = int(pt * self.opt['scale']) # 32*1 = 32
                self.fake_H = torch.empty(1, 1,  num_HR, H, W, device=self.device)
                # get predictions
                with torch.no_grad():
                    for row in range(0, data['LR'].size(3), opt_val['need_voxels']['tile_size']):
                        for column in range(0, data['LR'].size(3), opt_val['need_voxels']['tile_size']):
                            # [1, 1, 330, 64, 64]
                            LR_chunked = var_L_eval[:, :, :, row:row+opt_val['need_voxels']['tile_size'], column:column+opt_val['need_voxels']['tile_size']]
                            # store chunked prediction results
                            if self.opt['precision'] == 'fp16':
                                # [12, 1, 32, 64, 64]
                                tmp_chunk_along_z = torch.empty(self.nt, 1, pt, opt_val['need_voxels']['tile_size'], opt_val['need_voxels']['tile_size'],
                                                    dtype=torch.half, device=self.device)
                            else:
                                tmp_chunk_along_z = torch.empty(self.nt, 1, pt, opt_val['need_voxels']['tile_size'], opt_val['need_voxels']['tile_size'],
                                                    device=self.device)

                            # iterate over number of blocks to get predictions
                            for i in range(0, self.nt - 1):
                                tmp_chunk_along_z[i, :, :, :, :] = self.netG_eval(LR_chunked[:, :, i*(pt-self.ot):i*(pt-self.ot)+pt, :, :])
                            # add the last chunk
                            tmp_chunk_along_z[-1, :, :, :, :] = self.netG_eval(LR_chunked[:, :, -pt:, :, :])

                            # reconstruct the volume along z [1, 1, 330, 64, 64]
                            reconstructed_z = torch.empty(1, 1, num_HR, opt_val['need_voxels']['tile_size'],
                                                        opt_val['need_voxels']['tile_size'], device=self.device)
                            # stitch volume along z direction
                            stitch_mask = torch.zeros_like(reconstructed_z, device=self.device)
                            for i in range(0, self.nt - 1):
                                ts, te = i * (pt - HR_ot), i * (pt - HR_ot) + pt
                                reconstructed_z[0, 0, ts:te, :, :] = (reconstructed_z[0, 0, ts:te, :, :] * stitch_mask[0, 0, ts:te, :, :] + 
                                                                        tmp_chunk_along_z[i,...].float() * (2 - stitch_mask[0, 0, ts:te, :, :])) / 2
                                stitch_mask[0, 0, ts:te, :, :] = 1.
                            # stich last volume
                            reconstructed_z[0, 0, -pt:, :, :] = \
                                (reconstructed_z[0, 0, -pt:, :, :] * stitch_mask[0, 0, -pt:, :, :] +
                                tmp_chunk_along_z[-1,...].float() * (2 - stitch_mask[0, 0, -pt:, :, :])) / 2
                            # accumulate volume together
                            self.fake_H[0, 0, :, row:row+opt_val['need_voxels']['tile_size'], column:column+opt_val['need_voxels']['tile_size']] = reconstructed_z        
            else:
                raise ValueError('Unknown tiling case found in cSNGAN model!')
        self.netG.train()

    """
    Feed in LR and HR data to models, calculate loss and optimize gradients
    """
    def optimize_parameters(self, step):
        # put models on training
        self.netG.train()
        self.netD.train()
        # ------------------------ #
        # Generator Training       #
        # ------------------------ #
        # Turn off discriminator backpropagation during generator training
        for d_parameters in self.netD.parameters():
            d_parameters.requires_grad = False
        self.optimizer_G.zero_grad() # zero-gradient
        # mixed-precision gen train
        with amp.autocast():
            sr_gen = self.netG(self.var_L)
            hr_output_disc = self.netD(self.real_H.detach().clone())
            sr_output_disc = self.netD(sr_gen)
            # compute pixel and feature loss
            if self.cri_pix:
                pixel_loss = self.l_pix_w * self.cri_pix(sr_gen, self.real_H)
                self.log_dict['l_g_pix'] = pixel_loss.item()
            if self.cri_fea:
                content_loss = self.l_fea_w  * self.cri_fea(sr_gen, self.real_H)
                self.log_dict['l_g_fea'] = content_loss.item()

            # set up labels for adversarial loss
            real_label = torch.full([self.var_L.size(0), 1], 1.0, dtype=self.var_L.dtype, device=self.device)
            fake_label = torch.full([self.var_L.size(0), 1], 0.0, dtype=self.var_L.dtype, device=self.device)
            # compute adversarial loss
            d_loss_hr = self.cri_adv(hr_output_disc - torch.mean(sr_output_disc), fake_label) * 0.5
            d_loss_sr = self.cri_adv(sr_output_disc - torch.mean(hr_output_disc), real_label) * 0.5
            adversarial_loss = self.adv_w  * (d_loss_hr + d_loss_sr)
            self.log_dict['l_g_adv'] = adversarial_loss.item()
            g_loss = pixel_loss + adversarial_loss
            self.log_dict['l_g_total'] = g_loss.item()

        self.scaler.scale(g_loss).backward()
        self.scaler.step(self.optimizer_G)
        self.scaler.update()

        # ------------------------ #
        # Discriminator Training   #
        # ------------------------ #
        # Turn on discriminator backpropagation during discriminator training
        for d_parameters in self.netD.parameters():
            d_parameters.requires_grad = True
        self.optimizer_D.zero_grad()
        # mixed-precision disc training: calculate the classification score of the discriminator model for real samples
        with amp.autocast():
            hr_output_disc = self.netD(self.real_H)
            sr_output_disc = self.netD(sr_gen.detach().clone())
            d_loss_hr = self.cri_adv(hr_output_disc - torch.mean(sr_output_disc), real_label) * 0.5
            self.log_dict['l_d_real'] = d_loss_hr.item()
        self.scaler.scale(d_loss_hr).backward(retain_graph=True)
        # mixed-precision disc training: calculate the classification score of the discriminator model for fake samples
        with amp.autocast():
            sr_output_dics = self.netD(sr_gen.detach().clone())
            d_loss_sr = self.cri_adv(sr_output_dics - torch.mean(hr_output_disc), fake_label) * 0.5
            self.log_dict['l_d_fake'] = d_loss_sr.item()
        # Call the gradient scaling function in the mixed precision API to backpropagate the gradient information of the fake samples
        self.scaler.scale(d_loss_sr).backward()
        d_loss = d_loss_hr + d_loss_sr
        self.log_dict['l_d_total'] = d_loss.item()
        self.scaler.step(self.optimizer_D)
        self.scaler.update()
    
    """
    Returns the log dictionary that contains the gan (generator & discriminator) losses
    """
    def get_current_log(self):
        return self.log_dict

    def get_current_visuals(self, data, maskOn=True, need_HR=True):
        out_dict = OrderedDict()
        out_dict['LR'] = self.var_L.detach()[0, 0].float() # [channel, 512, 512]
        out_dict['SR'] = self.fake_H.detach()[0, 0].float() # [channel, 512, 512]
        if maskOn:
            # the way we contructed mask it is 1 x 1 x depth x height x width
            mask = data['mask'].to(self.device).float()[0, 0, :]
            out_dict['SR'] *= mask
        if need_HR:
            out_dict['HR'] = self.real_H.detach().float()[0, 0, :]
            if maskOn:
                out_dict['HR'] *= mask
        return out_dict
    """
    Returns a dictionary for the pipeline, with volume replaced by normalization output 
    """
    def run_test(self, data): 
        need_HR = False if self.opt['datasets']['dataroot_HR'] is None else True
        has_mask = False if self.opt['datasets']['maskroot_HR'] is None else True
        self.feed_test_data(data, need_HR=need_HR)
        self.test(data)  # test
        visuals = self.get_current_visuals(data, maskOn=has_mask, need_HR=need_HR)
        data['volume'] = visuals['SR'][None,None]
        return data 
        
    """
    Prints out both the generator and discriminator network structure
    """
    def print_network(self, use_logger=True):
        # Generator
        s, n = self.get_network_description(self.netG)
        if isinstance(self.netG, nn.DataParallel):
            net_struc_str = '{} - {}'.format(self.netG.__class__.__name__,
                                             self.netG.module.__class__.__name__)
        else:
            net_struc_str = '{}'.format(self.netG.__class__.__name__)
        if use_logger:
            logger.info('Network G structure: {}, with parameters: {:,d}'.format(net_struc_str, n))
            logger.info(s)
        else:
            pass
            # print('Network G structure: {}, with parameters: {:,d}'.format(net_struc_str, n))
            # print(s)
        if self.is_train:
            # Discriminator
            s, n = self.get_network_description(self.netD)
            if isinstance(self.netD, nn.DataParallel):
                net_struc_str = '{} - {}'.format(self.netD.__class__.__name__,
                                                self.netD.module.__class__.__name__)
            else:
                net_struc_str = '{}'.format(self.netD.__class__.__name__)
            if use_logger:
                logger.info('Network D structure: {}, with parameters: {:,d}'.format(net_struc_str, n))
                logger.info(s)
            else:
                pass
                # print('Network D structure: {}, with parameters: {:,d}'.format(net_struc_str, n))
                # print(s)
            if self.cri_fea:  # F, Perceptual Network
                s, n = self.get_network_description(self.cri_fea)
                if isinstance(self.cri_fea, nn.DataParallel):
                    net_struc_str = '{} - {}'.format(self.cri_fea.__class__.__name__,
                                                    self.cri_fea.module.__class__.__name__)
                else:
                    net_struc_str = '{}'.format(self.cri_fea.__class__.__name__)
                logger.info('Network F structure: {}, with parameters: {:,d}'.format(net_struc_str, n))
                logger.info(s)


    """
    Load the generator and discriminator weights if provided
    """
    def load(self, use_logger=True):
        load_path_G = self.opt['path']['pretrain_model_G']
        if load_path_G is not None: # load, model weights, if path is not None
            # 'self.load_network()' is implemented in base class
            self.load_network(load_path_G, self.netG)
            if use_logger:
                logger.info('Loading pretrained model for G [{:s}] ...'.format(load_path_G))
            else:
                print('Loading pretrained model for G [{:s}] ...'.format(load_path_G))
        load_path_D = self.opt['path']['pretrain_model_D']
        # load if opt['is_train'] is 'Train' and discriminator weight path is not None
        if self.opt['is_train'] and load_path_D is not None:
            self.load_network(load_path_D, self.netD)
            if use_logger:
                logger.info('Loading pretrained model for D [{:s}] ...'.format(load_path_D))
            else:
                print('Loading pretrained model for D [{:s}] ...'.format(load_path_D))

    """
    Save model weights, both generator and discriminator, at a particular iteration
    """
    def save(self, iter_step):
        self.save_network(self.netG, 'G', iter_step)
        self.save_network(self.netD, 'D', iter_step)
