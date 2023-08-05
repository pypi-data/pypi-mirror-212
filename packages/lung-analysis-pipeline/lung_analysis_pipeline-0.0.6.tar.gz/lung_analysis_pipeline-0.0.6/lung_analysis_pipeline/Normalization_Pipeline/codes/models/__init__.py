import logging
logger = logging.getLogger('base')
from collections import OrderedDict
import os
import lung_analysis_pipeline.utils.util as util
from ..non_DL import bm3d_ht as bm3d
import pkg_resources

"""
Create a normalizatio model given opt 
"""
def create_model(opt):
    model = opt['normalization']['model']
    ## convert opt to normalization module option format 
    if model == 'bm3d':
        return util.PythonFunctionWrapper(bm3d.calculate_scan_bm3d)
    elif model == 'wgan': 
        model = 'srgan'
        which_model_G = 'vanilla'
        # pretrain_model_G = "Normalization_Pipeline/weights/WGAN/latest_G.pth"
    elif model == 'sngan': 
        model = 'srgan'
        which_model_G = 'sr_resnet'
        # pretrain_model_G = "Normalization_Pipeline/weights/SNGAN/latest_G.pth"
    elif model == 'sr_resnet': 
        model = 'sr'
        which_model_G = 'sr_resnet'
        # pretrain_model_G = "Normalization_Pipeline/weights/SRResNet/latest_G.pth"
    elif model == 'rrdb': 
        model = 'sr'
        which_model_G = 'RRDB'
        # pretrain_model_G = "Normalization_Pipeline/weights/RRDB/latest_G.pth"
    else:
        raise NotImplementedError('Model [{:s}] not implemented.'.format(opt['normalization']['model']))
    # convert relative path to path in pip package 
    # pretrain_model_G = pkg_resources.resource_filename('lung_analysis_pipeline', pretrain_model_G)
    pretrain_model_G = opt['normalization']['weights']

    scale = 1.0
    option = OrderedDict([('name', opt['normalization']['model'])])
    option['is_train'] = False
    option['model'] = model
    option['scale'] = scale
    option['gpu_ids'] = opt['gpu_ids']
    option['precision'] = 'fp16'
    option["result_format"] = opt['normalization']['output_type']
    option["need_label"] = False
    option["data_merged"] = True
    option['train'] = None

    # dataset 
    dataset = OrderedDict([('data_type', opt['dataset']['image_type'])])
    dataset['name'] = opt['dataset']['source'] 
    dataset['uids_path'] = opt['dataset']['uids_location']
    dataset['dataroot_HR'] = opt['dataset']['dataroot_HR']
    dataset['dataroot_LR'] = opt['dataset']['dataroot_LR']
    dataset['need_voxels'] = OrderedDict([('tile_x_y', True), ('tile_size', 64)])
    dataset['slice_size'] = 32 
    dataset['overlap_slice_size'] = 4
    dataset['LR_slice_size'] = 32
    dataset['phase'] = 'val'
    dataset['scale'] = scale
    dataset['LR_size'] = 64
    dataset['dataset_name'] = opt['dataset']['source']
    option['datasets'] = OrderedDict([('val', dataset)])
    
    results_root = opt['normalization']['output_location']
    option['path'] = OrderedDict([
        ('results_root', results_root), 
        ('log', results_root),
        ("pretrain_model_G", pretrain_model_G)
    ])

    for key, path in option['path'].items():
        if path and key in option['path']:
            option['path'][key] = os.path.expanduser(path)

    # network 
    option['network_G'] = OrderedDict([
        ('which_model_G', which_model_G),
        ('norm_type', None), 
        ('nf', 64), 
        ('nb', 8), 
        ('in_nc', 1), 
        ('out_nc', 1), 
        ('use_attention', False), 
        ('need_embed', False), 
        ('scale', scale), 
    ])

    option = util.dict_to_nonedict(option)

    ## instantiate only G
    if model == 'sr':
        from .SR_model import SRModel as M
    ## 'srgan' instantiates both G and D
    elif model == 'srgan':
        from .SRGAN_model import SRGANModel as M
    elif model == 'srgan_exp':
        from .SRGAN_exp import SRGANModel as M
    else:
        raise NotImplementedError('Model [{:s}] not implemented.'.format(model))
    
    m = M(option)
    m.half()
    # copy net and convert to fp16 if necessary
    logger.info('Normalization model [{:s}] is created.'.format(m.__class__.__name__))
    logger.info(util.dict2str(option))

    return m
