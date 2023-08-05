import numpy as np
import torch
import utils.util as util
import options.options as option
from models import create_model
import random
import nrrd
import os



def main(path_to_data, path_to_save_vol):
    need_HR = False
    has_mask = False
    data_merged = True
    ToTensor = util.ImgToTensor()

    # set-up dataset and label for conditional information
    uid = path_to_data.split('/')[-1]
    data, header = nrrd.read(path_to_data)
    data = data.transpose((2, 1, 0))
    vol_in = torch.from_numpy(np.expand_dims(data, axis=0))
    vol_in = torch.unsqueeze(ToTensor(vol_in), axis=0)
    class_label = {'d10':0, 'd25':1, 'd100': 2, 'k1':0, 'k2':1, 'k3':2, 'st1':0, 'st0.6':1, 'st2':2}
    if not data_merged:
        kernel_lbl, dose_lbl, st_lbl = self.opt['dataroot_LR'].split('/')[-1].split('_')
        kernel_lbl_to_assign, dose_lbl_to_assign, st_lbl_to_assign = util.cvt_int(kernel_lbl),\
                                                                                util.cvt_int(dose_lbl), util.cvt_int(st_lbl)
        kernel_lbl = torch.from_numpy(np.expand_dims(class_label[kernel_lbl_to_assign], axis=0))
        dose_lbl = torch.from_numpy(np.expand_dims(class_label[dose_lbl_to_assign], axis=0))
    else:
        kernel_lbl = torch.from_numpy(np.expand_dims(class_label[uid.split('_')[1:][0]], axis=0))
        dose_lbl = torch.from_numpy(np.expand_dims(class_label[uid.split('_')[1:][1]], axis=0))
    data = {'LR':vol_in, 'uid': uid, 'kernel': kernel_lbl, 'dose': dose_lbl}

    # set-up config
    opt = {
            'model': 'srgan',
            'scale': 1.0,
            'gpu_ids': [0],
            'precision': 'fp16',
            'result_format': 'nrrd',
            'need_label': True,
            "datasets": {"val": {"need_voxels": {"tile_x_y": True, "tile_size": 64},"slice_size": 32, "overlap_slice_size": 4, "LR_slice_size": 32, "LR_size": 64}},
            'path':{'pretrain_model_G': '../experiments/train_cSNGAN-AC-EQMergedData_tileStitch-32x64x64_Ref-k2d100/models/latest_G.pth'},
            'network_G':{'which_model_G': 'sr_resnet', 'norm_type': None, 'nf': 64, 'nb': 8, 'in_nc': 1, 'out_nc': 1,\
            "use_attention": False, 'need_embed':{'kernel_class': 3, 'dose_class': 3}, 'scale': 1.0},
            'is_train': False
        }
    opt = option.dict_to_nonedict(opt)
    torch.backends.cudnn.benchmark = True

    # create model and convert to fp16
    model = create_model(opt)
    model.half()

    if opt["precision"] == 'int8':
        model.prepare_quant(data, not_loader=True)
    model.feed_test_data(data, need_HR=need_HR)
    model.test(data)
    visuals = model.get_current_visuals(data, maskOn=has_mask, need_HR=need_HR)
    # save normalized visual
    try:    
        save_path = os.path.join(path_to_save_vol, 'norm_'+uid)
        sr_vol = util.tensor2img(visuals['SR'], out_type=np.uint16)
        nrrd.write(save_path, sr_vol, header, index_order='C')
        print('====== Volume Saved ======')
    except Exception as e:
        print(e)
    print('Exiting ...')
    exit()


if __name__ == '__main__':
    path_to_data = '/datasets/data_st1.0_merged/0a3e8ff1c12efe170b9b69c5f792772f_k1_d10_st1.nrrd'
    path_to_save_vol = '/datasets/reference'
    main(path_to_data, path_to_save_vol)