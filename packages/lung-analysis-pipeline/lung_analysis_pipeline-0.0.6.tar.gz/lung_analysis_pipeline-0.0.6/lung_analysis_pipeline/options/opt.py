import os
import os.path as osp
import logging
from collections import OrderedDict
import json
import lung_analysis_pipeline.utils.util as util

def parse(opt_path, is_train=False):
    # remove comments starting with '//'
    json_str = ''
    with open(opt_path, 'r') as f:
        for line in f:
            line = line.split('//')[0] + '\n'
            json_str += line
    opt = json.loads(json_str, object_pairs_hook=OrderedDict)

    check_order(opt)

    # results_root = opt['output']['output_location']
    # opt['output']['log'] = results_root
    # util.mkdir(results_root) 

    # For feature extraction, redirect to another file if the output path already exists 
    # for operation in ['feature_extraction', 'detection']:
    if 'feature_extraction' in opt: 
        for extractor in ['deep_feature', 'radiomics']:
            if extractor in opt['feature_extraction']:  
                opt['feature_extraction'][extractor]['output_path'] and os.path.exists(opt['feature_extraction'][extractor]['output_path'])
                filename = os.path.basename(opt['feature_extraction'][extractor]['output_path'])

                # Extract the file name without extension and append timestamp 
                file_name_without_ext = os.path.splitext(filename)[0]
                new_file_name = file_name_without_ext + util.get_timestamp() + os.path.splitext(filename)[1]

                # Get the directory of the path and new path 
                directory = os.path.dirname(opt['feature_extraction'][extractor]['output_path'])
                opt['feature_extraction'][extractor]['output_path'] = os.path.join(directory, new_file_name)
                
                logger = logging.getLogger('base')
                logger.info('File already exists. Rename it to [{:s}]'.format(opt['feature_extraction'][extractor]['output_path']))
   
    if 'detection' in opt and 'output_path' in opt['detection'] and os.path.exists(opt['detection']['output_path']): 
        filename = os.path.basename(opt['detection']['output_path'])

        # Extract the file name without extension and append timestamp 
        file_name_without_ext = os.path.splitext(filename)[0]
        new_file_name = file_name_without_ext + util.get_timestamp() + os.path.splitext(filename)[1]

        # Get the directory of the path and new path 
        directory = os.path.dirname(opt['detection']['output_path'])
        opt['detection']['output_path'] = os.path.join(directory, new_file_name)
        
        logger = logging.getLogger('base')
        logger.info('File already exists. Rename it to [{:s}]'.format(opt['detection']['output_path']))
    
    gpu_list = ','.join(str(x) for x in opt['gpu_ids']) if opt['gpu_ids'] else ""
    os.environ['CUDA_VISIBLE_DEVICES'] = gpu_list
    # print('export CUDA_VISIBLE_DEVICES=' + gpu_list)
    
    
    return opt


"""
Check if specified operations are allowed. 
"""
def check_order(opt): 
    order = opt['order']
    for i, ops in enumerate(order): 
        if ops not in opt:
            raise ValueError('Please specify {} operation.'.format(ops))
        if ops == 'normalization': 
            if i != 0: 
                raise ValueError('Normalization operation order not supported!')
            if opt[ops]['model'] == 'bm3d' or "weights" not in opt[ops]: 
                raise ValueError('Need to specify path to normalization model weights.')
        elif ops == 'detection': 
            if "weights" not in opt[ops]: 
                raise ValueError('Need to specify path to detection model weights.')
        elif ops == 'segmentation': 
            # there has to exist detection before seg or use detection is set to false 
            if opt[ops]['use_decetion_bbox'] and not 'detection' in order[:i]: 
                raise ValueError('Segmentation operation order not supported!')
            if 'model' not in opt[ops]: 
                raise ValueError("Need to specify a segmentation model.")
            # check if the specified model is supported 
            if opt[ops]['model'] != 'unet': 
                raise NotImplementedError('Model [{:s}] not implemented.'.format(opt[ops]['model']))
            if 'weights' not in opt[ops]: 
                raise ValueError('Need to specify path to segmentation model weights.')
        elif ops == 'feature_extraction': 
            if 'roi_source' not in opt[ops]:
                raise ValueError('Segmentation operation order not supported! Need to specify source of ROI.')
            if opt[ops]['roi_source'] == 'segmentation' and not 'segmentation' in order[:i]: 
                raise ValueError('Feature extraction order not supported. Need to specify a segmentation method.')
            if opt[ops]['roi_source'] == 'detection' and not 'detection' in order[:i]: 
                raise ValueError('Feature extraction order not supported. Need to specify a detection method.')
            if opt[ops]['roi_source'] == 'user' and 'feature_roi_centroid' not in opt['dataset']: 
                raise ValueError('Feature extraction order not supported. Need to specify a ROI location.')
            if opt[ops]['roi_source'] == 'user' and 'feature_mask' not in opt['dataset']: 
                raise ValueError('Feature extraction order not supported. Need to specify a mask location.')
            if opt[ops]['deep_feature']: 
                if 'model' not in opt[ops]['deep_feature']: 
                    raise ValueError('Need to specify a deep learning model for feature extraction.')
                if opt[ops]['deep_feature']['model'] != 'hscnn': 
                    raise ValueError('Deep feature extraction model not supported.')
                if 'weights' not in opt[ops]['deep_feature']: 
                    raise ValueError('Need to specify path to deep feature extraction model weights.')