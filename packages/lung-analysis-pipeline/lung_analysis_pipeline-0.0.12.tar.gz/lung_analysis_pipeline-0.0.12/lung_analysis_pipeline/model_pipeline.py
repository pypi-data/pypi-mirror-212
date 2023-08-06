from lung_analysis_pipeline.Normalization_Pipeline.codes.models import create_model as create_normalization_model
from lung_analysis_pipeline.NoduleSeg_MedicalNet.build_unet_model import create_seg_model 
from lung_analysis_pipeline.Feature_Extractor.HSCNN.model import create_feat_extractor 
from lung_analysis_pipeline.Feature_Extractor.radiomics.feature_extractor import radiomic_feature_extractor 
from lung_analysis_pipeline.NoduleDetect_SANet import create_detect_model 
from lung_analysis_pipeline.utils import util
import numpy as np 
import os 
import torch


class ModelPipeline: 
    def __init__(self, opt):
        # self.models = models 
        self.opt = opt 
        
        order = self.opt['order']
        if 'normalization' in order: 
            self.norm_model = create_normalization_model(opt)
        if 'detection' in order: 
            self.detect_model = create_detect_model(opt)
        if 'segmentation' in order: 
            self.seg_model = create_seg_model(opt)
        if 'feature_extraction' in order:
            self.feature_extractions = {}
            if 'deep_feature' in opt['feature_extraction']:
                self.feature_extractions['deep_feature'] = create_feat_extractor(opt)
            if 'radiomics' in opt['feature_extraction']:
                self.feature_extractions['radiomics'] = radiomic_feature_extractor(opt)
    def test(self, input_data): 
        
        if hasattr(self, 'norm_model'):
            input_data = self.norm_model.run_test(input_data)
            # save norm output 
            if self.opt['normalization']['output_path']:
                norm_results_dir = self.opt['normalization']['output_path']
                util.mkdir(norm_results_dir)
                sr_vol = util.tensor2img(input_data['volume'][0][0], out_type=np.uint16)
                util.save_vol(self.opt, [], norm_results_dir, input_data['uid'][0], sr_vol, dtype=self.opt['normalization']['output_dtype'])
        else: 
            input_data['volume'] = input_data['LR']
        
        if hasattr(self, 'detect_model'):
            detect_output = self.detect_model.run_test(input_data)
            if self.opt['detection']['output_path']:
                util.save_detect_bbox(self.opt, detect_output)

        if hasattr(self, 'seg_model'): 
            seg_output = self.seg_model.run_test(input_data, self.opt) 
            if self.opt['segmentation']['output_path']:
                seg_ressult_dir = self.opt['segmentation']['output_path']
                util.mkdir(seg_ressult_dir)
                util.save_mask(self.opt, seg_output)
        
        if hasattr(self, 'feature_extractions'): 
            for key, extractor in self.feature_extractions.items(): 
                # extract feature 
                feat_output = extractor.run_test(input_data, roi=self.opt['feature_extraction']['roi_source'], threshold_size=10)
                
                # only save results if output location is provided 
                if self.opt['feature_extraction'][key]['output_path']:
                    util.save_features(key, self.opt, feat_output)
        
        if self.opt['gpu_ids']: 
            torch.cuda.synchronize()

   