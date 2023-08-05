from radiomics import featureextractor
import numpy as np 
import tempfile
import nibabel as nib 
import SimpleITK as sitk
from scipy import ndimage
from skimage import measure
from lung_analysis_pipeline.utils import util 
import logging
radiomics_logger = logging.getLogger("radiomics")
radiomics_logger.setLevel(logging.ERROR)
glcm_logger = logging.getLogger("radiomics.glcm")
glcm_logger.setLevel(logging.ERROR)
logger = logging.getLogger('base')

# def extract_features(image, mask): 
#     # Create an instance of the PyRadiomics feature extractor
#     self.extractor = featureextractor.RadiomicsFeatureExtractor()

#     # Get the default params 
#     params = extractor.getParams()

#     # Modify the parameters as desired
#     params['normalize'] = True
#     params['resampledPixelSpacing'] = [1.0, 1.0, 1.0]
#     params['binWidth'] = 25

#     # Extract features using the image and mask
#     features = extractor.execute(image, mask)
#     logger.info('Radiomic feature extractor is created.')

class radiomic_feature_extractor(): 
    def __init__(self, opt): 
        self.opt = opt 
        # self.extractor = featureextractor.RadiomicsFeatureExtractor()
        # First define the settings
        # settings = self.extractor.settings
        settings = self.opt.get('feature_extraction', {}).get('radiomics', {}).get('customization', {})
        self.extractor = featureextractor.RadiomicsFeatureExtractor()
        
        # Update the default settings with the user-defined settings
        self.extractor.settings.update(settings)
        # Instantiate the extractor
        # extractor = featureextractor.RadiomicsFeatureExtractor(**settings)  # ** 'unpacks' the dictionary in the function call
        logger.info('Radiomic feature extractor is created.')

        # If a subset of features is specified in opt, only enable that subset of features 
        if 'features' in self.opt['feature_extraction']['radiomics']: 
            features = self.opt['feature_extraction']['radiomics']['features']
            self.extractor.disableAllFeatures() 
            logger.info(f'Enabled features: {features}')
            for feature in features: 
                self.extractor.enableFeatureClassByName(feature)

        # Print the enabled feature classes and settings 
        # enabled_classes = self.extractor.enabledFeatures
        # for feature_class in enabled_classes:
        #     print(feature_class)
        # print(self.extractor.settings)

    def run_test(self, input_data, roi, threshold_size=0): 
        if roi == 'segmentation' or roi == 'user': 
            return self.extract_from_entire_mask(input_data, roi, threshold_size=threshold_size)
        elif roi == 'detection': 
            return self.extract_from_bbox(input_data, threshold_size=threshold_size)
        else: 
            raise ValueError('Feature extraction ROI source not supported. Need to specify user/detection/segmentation.')
    
    def extract_from_bbox(self, input_data, threshold_size=0):
        image = input_data['volume'][0][0].cpu().numpy().astype(np.float32)
        uid = input_data['uid'][0]

        # input_data['detection_bboxes'] = torch.from_numpy(detections)[None] 
        detection_bboxes = input_data['detection_bboxes'][0].cpu().numpy()

        features = [] 

        # Iterate through the detection results 
        for i, bbox in enumerate(detection_bboxes): 
            bbox = bbox.astype(int)
            _, z, y, x, d, _ = bbox 
            # Calculate starting and ending indices for each dimension
            start_z = max(0, z - d // 2)
            end_z = min(image.shape[0], z + d // 2 + 1)
            start_y = max(0, y - d // 2)
            end_y = min(image.shape[1], y + d // 2 + 1)
            start_x = max(0, x - d // 2)
            end_x = min(image.shape[2], x + d // 2 + 1)

            roi = image[start_z:end_z, start_y:end_y, start_x:end_x]
            roi_mask = np.ones_like(roi)

            # Extract features from the ROI
            feature = self.extractor.execute(sitk.GetImageFromArray(roi), sitk.GetImageFromArray(roi_mask))
            feature['NoduleFeatureID'] = f"{uid}-{i-1}"
            feature.move_to_end('NoduleFeatureID', last=False)

            features.append(util.convert_numpy_to_list(feature))
        
        input_data['radiomics'] = features
        return input_data

    def extract_from_entire_mask(self, input_data, roi_source, threshold_size=0): 
        image = input_data['volume'][0][0].cpu().numpy().astype(np.float32)
        uid = input_data['uid'][0]
        if roi_source == 'segmentation':
            mask = input_data['seg_mask'][0].cpu().numpy().astype(np.uint8)
        elif roi_source == 'user':
            mask = input_data['gt_mask'][0].cpu().numpy().astype(np.uint8)
        # Extract connected compontents in mask 
        labeled_mask, num_components = measure.label(mask, return_num=True)

        features = [] # list of OrderedDict 
        
        for i in range(1, num_components + 1):
            # Extract the binary mask for the current component
            component_mask = (labeled_mask == i)
            # Check if the size of the current component is larger than the threshold
            if np.sum(component_mask) < threshold_size:
                continue
            # Calculate the centroid of the current component
            # z, y, x = np.round(np.array(ndimage.center_of_mass(component_mask))).astype(int)
            # centroid = np.array([z, y, x])
            
            # Get a bounding box of this connected component and extract roi and mask 
            z, y, x = np.where(component_mask)
            start_z, end_z = np.min(z), np.max(z) + 1
            start_y, end_y = np.min(y), np.max(y) + 1
            start_x, end_x = np.min(x), np.max(x) + 1

            roi = image[start_z:end_z, start_y:end_y, start_x:end_x]
            roi_mask = mask[start_z:end_z, start_y:end_y, start_x:end_x]

            # Extract features from the ROI
            feature = self.extractor.execute(sitk.GetImageFromArray(roi), sitk.GetImageFromArray(roi_mask))
            feature['NoduleFeatureID'] = f"{uid}-{i-1}"
            feature.move_to_end('NoduleFeatureID', last=False)

            features.append(util.convert_numpy_to_list(feature))
        
        input_data['radiomics'] = features
        return input_data
    
    


