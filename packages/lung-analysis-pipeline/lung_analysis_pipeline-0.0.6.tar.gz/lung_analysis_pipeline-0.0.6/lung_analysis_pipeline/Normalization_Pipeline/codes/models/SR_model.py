import logging
from collections import OrderedDict
import torch
import torch.nn as nn
from . import lr_scheduler
from . import networks
from .base_model import BaseModel
from apex import amp
import apex

logger = logging.getLogger('base')


class SRModel(BaseModel):
    def __init__(self, opt):
        super(SRModel, self).__init__(opt)
        train_opt = opt['train']
        if self.is_train:
            self.netG.train()

            # set-up loss: pixel loss
            loss_type = train_opt['pixel_criterion']
            if loss_type == 'l1':
                print('l1 loss: l1')
                self.cri_pix = nn.L1Loss().to(self.device)
            elif loss_type == 'l2':
                print('l2: MSE loss')
                self.cri_pix = nn.MSELoss().to(self.device)
            else:
                raise NotImplementedError('Loss type [{:s}] is not recognized.'.format(loss_type))
            # weights to be multiplied to pixel loss
            self.l_pix_w = train_opt['pixel_weight']

            # set-up optimizers
            wd_G = train_opt['weight_decay_G'] if train_opt['weight_decay_G'] else 0
            optim_params = []
            for k, v in self.netG.named_parameters():  # can optimize for a part of the model
                if v.requires_grad:
                    optim_params.append(v)
                else:
                    logger.warning('Params [{:s}] will not optimize.'.format(k))
            if opt["network_G"]["which_model_G"] == "fsrcnn":
                self.optimizer_G = torch.optim.Adam([
                        {'params': self.netG.first_part.parameters()},
                        {'params': self.netG.mid_part.parameters()},
                        {'params': self.netG.last_part.parameters(), 'lr': train_opt['lr_G'] * 0.1}
                        ], lr=train_opt['lr_G'])
            else:
                self.optimizer_G = torch.optim.Adam(
                    optim_params, lr=train_opt['lr_G'], weight_decay=wd_G, betas=(train_opt['beta1_G'], train_opt['beta2_G']))
            self.optimizers.append(self.optimizer_G)

            # set-up schedulers
            if train_opt['lr_scheme'] == 'MultiStepLR':
                for optimizer in self.optimizers:
                    self.schedulers.append(
                        lr_scheduler.MultiStepLR_Restart(optimizer, train_opt['lr_steps'],
                                                         restarts=train_opt['restarts'],
                                                         weights=train_opt['restart_weights'],
                                                         gamma=train_opt['lr_gamma'],
                                                         clear_state=train_opt['clear_state']))
            elif train_opt['lr_scheme'] == 'CosineAnnealingLR':
                for optimizer in self.optimizers:
                    self.schedulers.append(
                        lr_scheduler.CosineAnnealingLR_Restart(optimizer, train_opt['T_period'],
                                                        eta_min=train_opt['eta_min'],
                                                        restarts=train_opt['restarts'],
                                                        weights=train_opt['restart_weights']))
            else:
                raise NotImplementedError('Choose MultiStepLR or CosineAnnealingLR')
            self.log_dict = OrderedDict()
        self.print_network()
        self.load()

    def initialize_amp(self):
        self.netG, self.optimizer_G = amp.initialize(self.netG, self.optimizer_G, opt_level=self.opt['opt_level'])
        if self.opt['gpu_ids']:
            assert torch.cuda.is_available()
            self.netG = nn.DataParallel(self.netG)
    
    def run_test(self, data): 
        need_HR = False if self.opt['datasets']['dataroot_HR'] is None else True
        has_mask = False if self.opt['datasets']['maskroot_HR'] is None else True
        self.feed_test_data(data, need_HR=need_HR)
        self.test(data)  # test
        visuals = self.get_current_visuals(data, maskOn=has_mask, need_HR=need_HR)
        data['volume'] = visuals['SR'][None,None]
        return data 

    def test(self, data):

        self.netG_eval.eval()
        if self.opt['precision'] == 'fp16':
            var_L_eval = self.var_L.half()
        else:
            var_L_eval = self.var_L

        opt_val = self.opt['datasets']['val']
        # HR slice num
        num_HR = int (data['LR'].size(2) * self.opt['scale'])
        # HR slice overlap
        HR_ot = int(self.opt['scale'] * self.ot)

        if not opt_val['need_voxels']:
            print('---- Full size image prediction -----')
            pt, H, W = int(self.var_L.size(2)*self.opt['scale']), self.var_L.size(3), self.var_L.size(4)
            self.fake_H = torch.empty(1, 1,  num_HR, H, W, device=self.device)
            if self.opt['precision'] == 'fp16':
                fake_H_in_chunks = torch.empty(self.nt, 1,  pt, H, W, dtype=torch.half, device=self.device)
            else:
                fake_H_in_chunks = torch.empty(self.nt, 1,  pt, H, W, device=self.device)
            
            # mask, record 1 when there is value in this pixel
            stitch_mask = torch.zeros_like(self.fake_H, device=self.device)
            with torch.no_grad():
                if opt_val['full_volume']:
                    self.fake_H = self.netG_eval(var_L_eval)
                else:
                    for i in range(0, self.nt):
                        fake_H_in_chunks[[i],...] = self.netG_eval(var_L_eval[[i],...])
                    # stitch volume in z-direction: n-1 volumes
                    for i in range(0, self.nt - 1):
                        ts, te = i * (pt - HR_ot), i * (pt - HR_ot) + pt
                        # `stitch_mask` and `fake_H` are fp32 for better numerical stability - fp16 inference results are casted into fp32
                        self.fake_H[0, 0, ts:te, :, :] = \
                        (self.fake_H[0, 0, ts:te, :, :] * stitch_mask[0, 0, ts:te, :, :] +
                        fake_H_in_chunks[i,...].float() * (2 - stitch_mask[0, 0, ts:te, :, :])) / 2
                        stitch_mask[0, 0, ts:te, :, :] = 1.
                    # the last volume
                    self.fake_H[0, 0, -pt:, :, :] = \
                        (self.fake_H[0, 0, -pt:, :, :] * stitch_mask[0, 0, -pt:, :, :] +
                        fake_H_in_chunks[-1,...].float() * (2 - stitch_mask[0, 0, -pt:, :, :])) / 2
        else:
            if opt_val['need_voxels'] and not opt_val['need_voxels']['tile_x_y']:
                # print('---- Random voxel prediction-----')
                self.fake_H = self.netG_eval(var_L_eval).float()
            elif opt_val['need_voxels'] and opt_val['need_voxels']['tile_x_y']:
                # print('---- Sliding tile prediction ----')
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
                raise ValueError('Unknown tiling case found in SR model!')
        self.netG.train()

    def optimize_parameters(self, step):
        self.optimizer_G.zero_grad()
        self.fake_H = self.netG(self.var_L)
        l_pix = self.l_pix_w * self.cri_pix(self.fake_H, self.real_H)
        with amp.scale_loss(l_pix, self.optimizer_G) as scale_loss:
            scale_loss.backward()
        self.optimizer_G.step()
        self.log_dict['l_pix'] = l_pix.item()

    def get_current_log(self):
        return self.log_dict

    def get_current_visuals(self, data, maskOn=True, need_HR=True):
        out_dict = OrderedDict()
        out_dict['LR'] = self.var_L.detach()[0, 0].float().cpu()
        out_dict['SR'] = self.fake_H.detach()[0, 0].float().cpu()
        if maskOn:
            # the way we contructed mask it is 1 x 1 x depth x width x height
            mask = data['mask'].detach().float().cpu()[0, 0, :]
            out_dict['SR'] *= mask
        if need_HR:
            out_dict['HR'] = self.real_H.detach().float().cpu()[0, 0, :]
            if maskOn:
                out_dict['HR'] *= mask
        return out_dict

    def print_network(self):
        s, n = self.get_network_description(self.netG)
        if isinstance(self.netG, nn.DataParallel):
            net_struc_str = '{} - {}'.format(self.netG.__class__.__name__,
                                             self.netG.module.__class__.__name__)
        else:
            net_struc_str = '{}'.format(self.netG.__class__.__name__)

        logger.info('Network G structure: {}, with parameters: {:,d}'.format(net_struc_str, n))
        logger.info(s)

    def load(self):
        load_path_G = self.opt['path']['pretrain_model_G']
        if load_path_G is not None:
            logger.info('Loading pretrained model for G [{:s}] ...'.format(load_path_G))
            self.load_network(load_path_G, self.netG)

    def save(self, iter_step):
        self.save_network(self.netG, 'G', iter_step)
