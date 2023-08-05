import logging
from collections import OrderedDict
import torch
import torch.nn as nn
from . import lr_scheduler
from . import networks
from .base_model import BaseModel
from .modules.loss import GANLoss, GradientPenaltyLoss
from tqdm import tqdm
"""
Amp allows users to easily experiment with different pure and mixed precision modes. 
Commonly-used default modes are chosen by selecting an “optimization level” or opt_level; each opt_level 
establishes a set of properties that govern Amp’s implementation of pure or mixed precision training.
- opt_level: 01 = Mixed Precision (recommended for typical use)
"""
from apex import amp
import apex
logger = logging.getLogger('base')


"""
Instantiates both generator and discriminator, put models in training, define losses, optimizers and schedulers
"""
class SRGANModel(BaseModel):
    def __init__(self, opt):
        super(SRGANModel, self).__init__(opt)
        train_opt = opt['train']
        if self.is_train:
            # define discriminator
            self.netD = networks.define_D(opt).to(self.device)  # D
            # put the generator and discriminator on training
            self.netG.train()
            self.netD.train()

        # define losses, optimizer and scheduler for training mode
        if self.is_train:
            # Set Generator pixel loss if 'pixel_weight' is greater than 0
            if train_opt['pixel_weight'] > 0:
                l_pix_type = train_opt['pixel_criterion'] # l1
                if l_pix_type == 'l1':
                    """
                    Creates a criterion that measures the mean absolute error (MAE) between 
                    each element in the input xx and target yy 
                    """
                    self.cri_pix = nn.L1Loss().to(self.device)

                elif l_pix_type == 'l2':
                    """
                    Creates a criterion that measures the mean squared error (squared L2 norm) between each
                    element in the input xx and target yy .
                    """
                    self.cri_pix = nn.MSELoss().to(self.device)

                else:
                    raise NotImplementedError('Loss type [{:s}] not recognized.'.format(l_pix_type))
                self.l_pix_w = train_opt['pixel_weight'] # get pixel weight
            else:
                logger.info('Skipping pixel loss ...')
                self.cri_pix = None

            # auxially loss
            if self.opt['network_D']['aux_lbl_loss']:
                logger.info('Including auxillary loss')
                self.aux_loss = nn.NLLLoss().to(self.device)

            # set Generator feature loss if 'feature_weight' is greater than 0
            if train_opt['feature_weight']:
                # print("feature weight is:", train_opt['feature_weight'])
                l_fea_type = train_opt['feature_criterion']
                # print("feature type:", l_fea_type)
                if l_fea_type == 'l1':
                    # print("feature criterion L1")
                    self.cri_fea = nn.L1Loss().to(self.device)
                elif l_fea_type == 'l2':
                    # print("feature criterion MSE")
                    self.cri_fea = nn.MSELoss().to(self.device)
                else:
                    raise NotImplementedError('Loss type [{:s}] not recognized.'.format(l_fea_type))
                self.l_fea_w = train_opt['feature_criterion']['feature_weight'] # get feature weight
            else:
                logger.info('Skipping feature loss ...')
                self.cri_fea = None
            
            # if feature criterion is defined, we load VGG perceptual loss
            if self.cri_fea:
                self.netF = networks.define_F(opt, use_bn=False).to(self.device)

            # print("Defining Gan Loss for real-fake image prediction")
            # print("-"*40)
            self.cri_gan = GANLoss(train_opt['gan_type'], real_label_val=1.0, fake_label_val=0.0).to(self.device)
            # print("cri_gan loss:", self.cri_gan)
            self.l_gan_w = train_opt['gan_weight']
            # print("gan weight:", self.l_gan_w)
            # D_update_ratio (how many times discriminator should be train after each generator training) 
            # and D_init_iters
            self.D_update_ratio = train_opt['D_update_ratio'] if train_opt['D_update_ratio'] else 1
            # print("D update ratio:", self.D_update_ratio)
            self.D_init_iters = train_opt['D_init_iters'] if train_opt['D_init_iters'] else 0
            # print("D init iters:", self.D_init_iters) # ?

            # if opt['gan_type'] is 'wgan', initialize gradient penality
            if "wgan" in train_opt['gan_type']:
                if train_opt['gan_type'] == "wgan-gp":
                    self.cri_gp = GradientPenaltyLoss(center=1.).to(self.device)
                elif train_opt['gan_type'] == "wgan-gp0":
                    self.cri_gp = GradientPenaltyLoss(center=0.).to(self.device)
                else:
                    raise NotImplementedError("{:s} not found".format(train_opt['gan_type']))
                self.l_gp_w = 10. # weight for gradient penality (used in 'optimize_parameters' function)

            # optimizers - weight decay for generator
            wd_G = train_opt['weight_decay_G'] if train_opt['weight_decay_G'] else 0
            optim_params = []
            """
            Returns an iterator over module parameters, yielding both the name of the parameter as well as
            the parameter itself, which we unpack into k, v.
            """
            for k, v in self.netG.named_parameters():  # optimize for a part of the model
                if v.requires_grad:
                    optim_params.append(v)
                else:
                    logger.warning('Params [{:s}] will not optimize.'.format(k))

            # initialize generator optimizer with parameters that only require gradients
            # initialize with weight decay and two beta coefficients
            self.optimizer_G = torch.optim.Adam(optim_params, lr=train_opt['lr_G'], \
                weight_decay=wd_G, betas=(train_opt['beta1_G'], train_opt['beta2_G']))

            """
            self.optimizer_G = torch.optim.RMSprop(optim_params, lr=train_opt['lr_G'], weight_decay=wd_G)
            """
            self.optimizers.append(self.optimizer_G) # add optimizer to list defined in base class
            # weight decay for discriminator
            wd_D = train_opt['weight_decay_D'] if train_opt['weight_decay_D'] else 0
            # optimizer for discriminator for entire model parameters
            self.optimizer_D = torch.optim.Adam(self.netD.parameters(), lr=train_opt['lr_D'], \
                weight_decay=wd_D, betas=(train_opt['beta1_D'], train_opt['beta2_D']))
            """
            self.optimizer_D = torch.optim.RMSprop(optim_params, lr=train_opt['lr_D'], weight_decay=wd_D)
            """
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
            # print("log dict:", self.log_dict)
        self.print_network(use_logger=True) # print the instantiated model
        self.load()  # load G and D if needed

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
        [self.netG, self.netD], [self.optimizer_G, self.optimizer_D] = \
        amp.initialize([self.netG, self.netD], [self.optimizer_G, self.optimizer_D],
                       opt_level=self.opt['opt_level'], num_losses = 2)
        if self.opt['gpu_ids']: 
            """
            Implements data parallelism at the module level. This container parallelizes 
            the application of the given module by splitting the input across the specified
            """
            assert torch.cuda.is_available()
            self.netG = nn.DataParallel(self.netG)
            self.netD = nn.DataParallel(self.netD)

    def test(self, data):
        self.netG_eval.eval()
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
        # HR slice num
        num_HR = int (data['LR'].size(2) * self.opt['scale'])
        # print('num HR is:', num_HR)
        # HR slice overlap
        HR_ot = int(self.opt['scale'] * self.ot)
        # print('HR_ot is:', HR_ot)
        if not opt_val['need_voxels']:
            print('---- Full size image prediction -----')
            # print('LR Var Size:', var_L_eval.shape)
            pt, H, W = self.var_L.size(2), self.var_L.size(3), self.var_L.size(4)
            pt = int(pt * self.opt['scale'])
            self.fake_H = torch.empty(1, 1,  num_HR, H, W, device=self.device)
            if self.opt['precision'] == 'fp16':
                fake_H_in_chunks = torch.empty(self.nt, 1,  pt, H, W, dtype=torch.half, device=self.device)
            else:
                fake_H_in_chunks = torch.empty(self.nt, 1,  pt, H, W, device=self.device)
            # mask, record 1 when there is value in this pixel
            stitch_mask = torch.zeros_like(self.fake_H, device=self.device)
            # print('stich mask size:', stitch_mask.shape)
            # generate predictions
            with torch.no_grad():
                if opt_val['full_volume']:
                    if self.opt['network_G']['need_embed']:
                        self.fake_H = self.netG_eval(var_L_eval, self.test_kernel_label, self.test_dose_label)
                    else:
                        self.fake_H = self.netG_eval(var_L_eval)
                else:
                    for i in range(0, self.nt):
                        if self.opt['network_G']['need_embed']:
                            fake_H_in_chunks[[i],...] = self.netG_eval(var_L_eval[[i],...], self.test_kernel_label, self.test_dose_label)
                        else:
                            # print('Chunk size: {}, going through gen size: {}'.format(i, var_L_eval[[i,...]].shape))
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
                if self.opt['network_G']['need_embed']:
                    self.fake_H = self.netG_eval(var_L_eval, self.test_kernel_label, self.test_dose_label).float()
                else:
                    self.fake_H = self.netG_eval(var_L_eval).float()
            elif opt_val['need_voxels'] and opt_val['need_voxels']['tile_x_y']:
                # print('---- Sliding Tile Inference -----')
                # print('case has to be tiled back:', self.var_L.shape)
                pt, H, W = opt_val['slice_size'], data['LR'].size(3), data['LR'].size(4)
                pt = int(pt * self.opt['scale']) # 32*1 = 32
                self.fake_H = torch.empty(1, 1,  num_HR, H, W, device=self.device)
                # get predictions
                with torch.no_grad():
                    for row in range(0, data['LR'].size(3), opt_val['need_voxels']['tile_size']):
                        for column in range(0, data['LR'].size(3), opt_val['need_voxels']['tile_size']):
                            # [1, 1, 330, 64, 64]
                            LR_chunked = var_L_eval[:, :, :, row:row+opt_val['need_voxels']['tile_size'], column:column+opt_val['need_voxels']['tile_size']]
                            # get candidate if needed
                            if self.opt['network_G']['use_attention']:
                                if self.opt['network_G']['use_attention']['generate_candidate']:
                                    LR_chunked_candidate = var_L_eval_candidate[:, :, :, row:row+opt_val['need_voxels']['tile_size'], column:column+opt_val['need_voxels']['tile_size']]

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
                                if self.opt['network_G']['need_embed']:
                                    if self.opt['network_G']['use_attention']:
                                        if self.opt['network_G']['use_attention']['generate_candidate']:
                                            tmp_chunk_along_z[i, :, :, :, :] = self.netG_eval(LR_chunked[:, :, i*(pt-self.ot):i*(pt-self.ot)+pt, :, :], 
                                                                        self.test_kernel_label, self.test_dose_label, LR_chunked_candidate[:, :, i*(pt-self.ot):i*(pt-self.ot)+pt, :, :])
                                    else:
                                        tmp_chunk_along_z[i, :, :, :, :] = self.netG_eval(LR_chunked[:, :, i*(pt-self.ot):i*(pt-self.ot)+pt, :, :], 
                                                                    self.test_kernel_label, self.test_dose_label)
                                else:
                                    tmp_chunk_along_z[i, :, :, :, :] = self.netG_eval(LR_chunked[:, :, i*(pt-self.ot):i*(pt-self.ot)+pt, :, :])
                
                            # add the last chunk
                            if self.opt['network_G']['need_embed']:
                                if self.opt['network_G']['use_attention']:
                                    if self.opt['network_G']['use_attention']['generate_candidate']:
                                        tmp_chunk_along_z[-1, :, :, :, :] = self.netG_eval(LR_chunked[:, :, -pt:, :, :], self.test_kernel_label, self.test_dose_label, LR_chunked_candidate[:, :, -pt:, :, :])
                                else:
                                    tmp_chunk_along_z[-1, :, :, :, :] = self.netG_eval(LR_chunked[:, :, -pt:, :, :], self.test_kernel_label, self.test_dose_label)
                            else:
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

                            """
                            img_to_stitch = var_L_eval[volume_chunk] # [12, 1, 32, 64, 64]
                            if self.opt['precision'] == 'fp16':
                                fake_H_in_chunks = torch.empty(self.nt, 1,  pt, opt_val['need_voxels']['tile_size'], opt_val['need_voxels']['tile_size'], dtype=torch.half, device=self.device)
                                # print('fake H in chunck (empty):', fake_H_in_chunks.shape)
                            else:
                                fake_H_in_chunks = torch.empty(self.nt, 1,  pt, opt_val['need_voxels']['tile_size'], opt_val['need_voxels']['tile_size'], device=self.device)
                            
                            # get predictions
                            for i in range(0, self.nt):
                                if self.opt['network_G']['need_embed']:
                                    fake_H_in_chunks[[i],...] = self.netG_eval(img_to_stitch[[i],...], self.test_kernel_label, self.test_dose_label)
                                else:
                                    # print('Chunk size: {}, going through gen size: {}'.format(i, var_L_eval[[i,...]].shape))
                                    fake_H_in_chunks[[i],...] = self.netG_eval(img_to_stitch[[i],...])
                            # reconstruct to original volume size
                            reconstructed_z = torch.empty(1, 1, num_HR, opt_val['need_voxels']['tile_size'], opt_val['need_voxels']['tile_size'], device=self.device)
                            stitch_mask = torch.zeros_like(reconstructed_z, device=self.device)
                            # stictch prediction
                            for i in range(0, self.nt - 1):
                                ts, te = i * (pt - HR_ot), i * (pt - HR_ot) + pt
                                reconstructed_z[0, 0, ts:te, :, :] = (reconstructed_z[0, 0, ts:te, :, :] * stitch_mask[0, 0, ts:te, :, :] + 
                                                                        fake_H_in_chunks[i,...].float() * (2 - stitch_mask[0, 0, ts:te, :, :])) / 2
                                stitch_mask[0, 0, ts:te, :, :] = 1.
                            # the last volume
                            reconstructed_z[0, 0, -pt:, :, :] = \
                                (reconstructed_z[0, 0, -pt:, :, :] * stitch_mask[0, 0, -pt:, :, :] +
                                fake_H_in_chunks[-1,...].float() * (2 - stitch_mask[0, 0, -pt:, :, :])) / 2
                            # add chunk to initial volume
                            self.fake_H[0, 0, :, row:row+opt_val['need_voxels']['tile_size'], column:column+opt_val['need_voxels']['tile_size']] = reconstructed_z
                            volume_chunk += 1
                            """   
                    # print('Stitched shape after prediction:', self.fake_H.shape)             
            else:
                raise ValueError('Unknown tiling case found in cSNGAN model!')
        self.netG.train()

    """
    Feed in LR and HR data to models, calculate loss and optimize gradients
    """
    def optimize_parameters(self, step):
        # print("Parameter optimization in progress")
        # print("-"*40)
        # optimize generator
        self.optimizer_G.zero_grad() # zero-gradient
        # print("Step is:", step)
        # send 'LR' data to generator and get a 'fake_HR' images, assiginig it 'self.fake_H'
        if self.opt['network_G']['need_embed']:
            if self.opt['network_G']['use_attention']:
                if self.opt['network_G']['use_attention']['generate_candidate']:
                    self.fake_H = self.netG(self.var_L, self.train_kernel_label, self.train_dose_label, self.cand_L_train)
            else:
                self.fake_H = self.netG(self.var_L, self.train_kernel_label, self.train_dose_label)
        else:
            self.fake_H = self.netG(self.var_L)
        # print("Output after generator output:", self.fake_H.shape)
        l_g_total = 0 # loss for generator
        # print("Check for optimizing generator: {} % {} == 0 and {} > {} = {}".format(step, self.D_update_ratio, step, self.D_init_iters,
        # (step % self.D_update_ratio == 0 and step > self.D_init_iters)))
        # ------------------------ #
        # Calcualte Generator Loss #
        # ------------------------ #
        if step % self.D_update_ratio == 0 and step > self.D_init_iters:
            # print("Optimizing generator - loss will be calculated")
            # if generator pixel loss is defined, calculate pixel loss
            if self.cri_pix:
                # calculate loss between output from generator (given 'LR' data) & real 'HR'
                l_g_pix = self.cri_pix(self.fake_H, self.real_H)
                # multiply pixel_weight (1 -> all pixel are equally important) with calculate pixel loss
                # append loss to 'l_g_total' 
                l_g_total += self.l_pix_w * l_g_pix 
            
            # if feature loss (perceptual loss) is defined, calculate feature loss
            if self.cri_fea:  # feature loss
                # get real-output after passing real data ('real_H') to perceptual network (PN)
                real_fea = self.netF(self.real_H).detach()
                # get fake feature-output after passing fake HR data (self.fake_H) to PN
                fake_fea = self.netF(self.fake_H) 
                # calculate feature loss, either 'L1' or 'MSE' loss
                l_g_fea = self.cri_fea(fake_fea, real_fea)
                # multiple feature weight with feature loss and add to 'l_g_total'
                l_g_total += self.l_fea_w * l_g_fea

            # send fake 'HR', output of gan model, as input to discriminator and get fake prediction 
            if self.opt['network_D']['need_embed']:
                if self.opt['network_D']['aux_lbl_loss']:
                    pred_g_fake, pred_g_kernel_fake, pred_g_dose_fake = self.netD(self.fake_H, self.train_kernel_label, self.train_dose_label)
                else:
                    pred_g_fake = self.netD(self.fake_H, self.train_kernel_label, self.train_dose_label)
            else:
                if self.opt['network_D']['aux_lbl_loss']:
                    pred_g_fake, pred_g_kernel_fake, pred_g_dose_fake = self.netD(self.fake_H)
                else:
                    pred_g_fake = self.netD(self.fake_H)
            
            # if 'gan_type' is 'hinge', no need to call the 'self.cri_gan()' function, we can simply 
            # calculate the gan generator loss, else, utilize the 'self.cri_gan()' function
            if self.opt['train']['gan_type'] == 'hinge':
                l_g_gan = -pred_g_fake.mean()
            else:
                l_g_gan = self.cri_gan(pred_g_fake, True)
            
            # multipley gan weight ('self.l_gan_w' = 5e-3) with gan generator loss & add to 'l_g_total'
            l_g_total += self.l_gan_w * l_g_gan
            # calculate auxially loss for generator if specified
            if self.opt['network_D']['aux_lbl_loss']:
                if self.opt['network_D']['aux_lbl_loss']['apply_to_gen']:
                    g_aux_kernel_loss = self.aux_loss(pred_g_kernel_fake, self.train_kernel_label.view(-1, 1).squeeze(1))
                    g_aux_dose_loss = self.aux_loss(pred_g_dose_fake, self.train_dose_label.view(-1, 1).squeeze(1))
                    l_g_total += (g_aux_kernel_loss + g_aux_dose_loss)

            # backpropogate loss, step-up optimizer
            with amp.scale_loss(l_g_total , self.optimizer_G, loss_id=0) as errG_scaled:
                errG_scaled.backward()
            self.optimizer_G.step()
            # print("generator back-propagation done at step {}!".format(step))

        # print("Optimizing discriminator")
        # optimize discriminator
        self.optimizer_D.zero_grad()
        l_d_total = 0

        # for 'wgan-gp0', we do need gradient on real data
        if self.opt['train']['gan_type'] == 'wgan-gp0':
            # print("setting 'requires_grad' to be true for HR data")
            self.real_H.requires_grad_()

        # get prediction from discriminator based on real 'HR' data
        if self.opt['network_D']['need_embed']:
            if self.opt['network_D']['aux_lbl_loss']:
                pred_d_real, aux_kernel_real, aux_dose_real = self.netD(self.real_H, self.train_kernel_label, self.train_dose_label)
                pred_d_fake, aux_kernel_fake, aux_dose_fake = self.netD(self.fake_H.detach(), self.train_kernel_label.detach(), self.train_dose_label.detach())  # detach to avoid back propogation to G
            else:
                pred_d_real = self.netD(self.real_H, self.train_kernel_label, self.train_dose_label)
                pred_d_fake = self.netD(self.fake_H.detach(), self.train_kernel_label.detach(), self.train_dose_label.detach())  # detach to avoid back propogation to G
        else:
            if self.opt['network_D']['aux_lbl_loss']:
                pred_d_real, aux_kernel_real, aux_dose_real = self.netD(self.real_H)
                pred_d_fake, aux_kernel_fake, aux_dose_fake = self.netD(self.fake_H.detach())
            else:
                # get predictions form discriminator based on 'real_H' data
                pred_d_real = self.netD(self.real_H)
                # get predictions form discriminator based on 'fake_HR' data
                pred_d_fake = self.netD(self.fake_H.detach())  # detach to avoid back propogation to G

        # ---------------------------- #
        # Calcualte Discriminator Loss #
        # ---------------------------- #
        l_d_real = self.cri_gan(pred_d_real, True)
        l_d_fake = self.cri_gan(pred_d_fake, False)
        l_d_total = l_d_real + l_d_fake

        # calculate auxially loss for discriminator generator
        if self.opt['network_D']['aux_lbl_loss']:
            l_d_aux_kernel_real = self.aux_loss(aux_kernel_real, self.train_kernel_label.view(-1, 1).squeeze(1))
            l_d_aux_dose_real = self.aux_loss(aux_dose_real, self.train_dose_label.view(-1, 1).squeeze(1))
            l_d_aux_kernel_fake = self.aux_loss(aux_kernel_fake, self.train_kernel_label.view(-1, 1).squeeze(1))
            l_d_aux_dose_fake = self.aux_loss(aux_dose_fake, self.train_dose_label.view(-1, 1).squeeze(1))
            l_d_total += (l_d_aux_kernel_real + l_d_aux_kernel_fake + l_d_aux_dose_real + l_d_aux_dose_fake)
            # compute accuracy
            kernel_accuracy = self.compute_acc(torch.exp(aux_kernel_real), self.train_kernel_label.view(-1, 1).squeeze(1))
            dose_accuracy = self.compute_acc(torch.exp(aux_dose_real), self.train_dose_label.view(-1, 1).squeeze(1))

        # if 'wgan' in 'gan_tpye', we calculate gradient penality, multiply with gradient penalty weight and add
        # to 'l_d_gp'
        if 'wgan' in self.opt['train']['gan_type']:
            if self.opt['train']['gan_type'] == 'wgan-gp0':
                l_d_gp = self.cri_gp(self.real_H, pred_d_real)
            elif self.opt['train']['gan_type'] == 'wgan-gp':
                batch_size = self.real_H.size(0)
                eps = torch.rand(batch_size, device=self.device).view(batch_size, 1, 1, 1, 1)
                x_interp = (1 - eps) * self.real_H + eps * self.fake_H.detach()
                x_interp.requires_grad_()
                if self.opt['network_D']['need_embed']:
                    if self.opt['network_D']['aux_lbl_loss']:
                        pred_d_x_interp, prd_x_kernel_interp, pred_x_dose_interp = self.netD(x_interp, self.train_kernel_label, self.train_dose_label)
                    else:
                        pred_d_x_interp = self.netD(x_interp, self.train_kernel_label, self.train_dose_label)
                else:
                    if self.opt['network_D']['aux_lbl_loss']:
                        pred_d_x_interp, prd_x_kernel_interp, pred_x_dose_interp = self.netD(x_interp)
                    else:
                        pred_d_x_interp = self.netD(x_interp)
                l_d_gp = self.cri_gp(x_interp, pred_d_x_interp)
            else:
                raise NotImplementedError('Gan type [{:s}] not recognized'.format(self.opt['train']['gan_type']))
            l_d_total += self.l_gp_w * l_d_gp # weight for gp (self.l_gp_w) = 10

        # backpropogate loss, step-up optimizer
        with amp.scale_loss(l_d_total , self.optimizer_D, loss_id=1) as errD_scaled:
            errD_scaled.backward()
        self.optimizer_D.step()

        # print("Check for logging generator: {} % {} == 0 and {} > {} = {}".format(step, self.D_update_ratio, step, self.D_init_iters,
        # (step % self.D_update_ratio == 0 and step > self.D_init_iters)))
        
        # Set logs - Log Generator  
        if step % self.D_update_ratio == 0 and step > self.D_init_iters:
            # Generator
            # append pixel loss (L1) loss, if specified
            if self.cri_pix:
                self.log_dict['l_g_pix'] = l_g_pix.item()
            # append perceptual loss/feature loss, if specified
            if self.cri_fea:
                self.log_dict['l_g_fea'] = l_g_fea.item()
            # append gan loss
            self.log_dict['l_g_gan'] = l_g_gan.item()
            # append total loss (pixel loss (if specified) + feature loss (if specified) + gan loss/hinge loss)
            self.log_dict['l_g_total'] = l_g_total.item()

        # Log Discriminator
        self.log_dict['l_d_total'] = l_d_total.item()
        if 'wgan' in self.opt['train']['gan_type']:
            # append gradient penalty
            self.log_dict['l_d_gp'] = l_d_gp.item()
            # append wasertian distance = - (real loss + fake loss)
            self.log_dict['w_dist'] = - ( l_d_real.item() + l_d_fake.item() )# pred_d_real - pred_d_fake
        
        # D outputs (mean of output from real HR and mean of output from fake HR)
        self.log_dict['D_real'] = torch.mean(pred_d_real.detach())
        self.log_dict['D_fake'] = torch.mean(pred_d_fake.detach())
        if self.opt['network_D']['aux_lbl_loss']:
            self.log_dict['Kernel_acc'] = kernel_accuracy
            self.log_dict['Dose_acc'] = dose_accuracy
    
    """
    Returns the log dictionary that contains the gan (generator & discriminator) losses
    """
    def get_current_log(self):
        return self.log_dict

    def get_current_visuals(self, data, maskOn=True, need_HR=True):
        # print('is maskOn:', maskOn) # False during validation / True during training
        # print('need_HR:', need_HR) # True during validation and training
        out_dict = OrderedDict()
        out_dict['LR'] = self.var_L.detach()[0, 0].float() # [channel, 512, 512]
        out_dict['SR'] = self.fake_H.detach()[0, 0].float() # [channel, 512, 512]
        # print('get current visual shape LR:', out_dict['LR'].shape)
        # print('HR shape:', out_dict['SR'].shape)
        if maskOn:
            # the way we contructed mask it is 1 x 1 x depth x height x width
            mask = data['mask'].to(self.device).float()[0, 0, :]
            # print('shap of mask:', mask.shape)
            out_dict['SR'] *= mask
            # print('unique element in mask', torch.unique(mask))
        if need_HR:
            out_dict['HR'] = self.real_H.detach().float()[0, 0, :]
            if maskOn:
                out_dict['HR'] *= mask
        return out_dict

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
                s, n = self.get_network_description(self.netF)
                if isinstance(self.netF, nn.DataParallel):
                    net_struc_str = '{} - {}'.format(self.netF.__class__.__name__,
                                                    self.netF.module.__class__.__name__)
                else:
                    net_struc_str = '{}'.format(self.netF.__class__.__name__)
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
        # 'self.save_network()' is implemented in base class
        self.save_network(self.netG, 'G', iter_step)
        self.save_network(self.netD, 'D', iter_step)
    
    def run_test(self, data): 
        need_HR = False if self.opt['datasets']['dataroot_HR'] is None else True
        has_mask = False if self.opt['datasets']['maskroot_HR'] is None else True
        self.feed_test_data(data, need_HR=need_HR)
        self.test(data)  # test
        visuals = self.get_current_visuals(data, maskOn=has_mask, need_HR=need_HR)
        data['volume'] = visuals['SR'][None,None]
        return data 