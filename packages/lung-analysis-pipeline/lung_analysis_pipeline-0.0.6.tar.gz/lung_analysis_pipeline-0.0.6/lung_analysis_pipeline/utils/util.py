import os, time, glob
import math
from datetime import datetime
import pydicom
import numpy as np
import cv2
import random
import torch
import logging
import nrrd
import json
import csv
import SimpleITK as sitk
import re
import nibabel as nib
import torch.nn.functional as F
from scipy import ndimage


"""
Get current timestamp in ymd-HMS format. Used when creataing a directory that already exists
"""
def get_timestamp():
    return datetime.now().strftime('%y%m%d-%H%M%S')

"""
Create a folder if it doesn't exist
"""
def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

"""
Make mupltiple directories, if it is an instance of string
"""
def mkdirs(paths):
    if isinstance(paths, str):
        mkdir(paths)
    else:
        for path in paths:
            mkdir(path)

"""
Create a folder if it doesn't exits, otherwise create a renamed version if it already exists
"""
def mkdir_and_rename(path):
    if os.path.exists(path):
        new_name = path + '_archived_' + get_timestamp()
        print('Path already exists. Rename it to [{:s}]'.format(new_name))
        logger = logging.getLogger('base')
        logger.info('Path already exists. Rename it to [{:s}]'.format(new_name))
        os.rename(path, new_name)
    os.makedirs(path)


"""
Set seed for numpy and torch arrays
"""
def set_random_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


"""
Create two logger named 'base' and 'val', with file name specified in 'phase' variable at the 
path specified in 'root' variable.
If 'screen=True', message is printed to screen
"""
def setup_logger(logger_name, root, phase, level=logging.INFO, screen=False):
    '''set up logger'''
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d - %(levelname)s: %(message)s', datefmt='%y-%m-%d %H:%M:%S')
    log_file = os.path.join(root, phase + '_{}.log'.format(get_timestamp()))
    fh = logging.FileHandler(log_file, mode='w')
    fh.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fh)
    if screen:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        l.addHandler(sh)

"""
Prints evaluaation metrics on screen
"""
def print_metrics(logger, metric_name, results):
    means = {}
    for view in list(results[list(results.keys())[0]].keys()):
        count = 0
        sum = 0.
        for k, v in results.items():
            count += 1
            sum += v[view]
            logger.info('{} for {} in {} view : {:.6f}'.format(metric_name, k, view, v[view]))
        means[view] = sum/count
        logger.info('Average {} in {} view : {:.6f}'.format(metric_name, view, means[view]))
    return means


####################
# image operations
####################
def tensor2img(tensor, out_type=np.uint8, min_max=(0, 1), intercept=-1024):
    '''
    Converts a torch Tensor into an image Numpy array
    Input: 3D(D,H,W)
    Output: 3D(H,W,D), np.uint8 (default), [0,1500] uint16, [-1000, 500] int16
    intercept is used when out_type is set to int16
    '''
    tensor = tensor.cpu().float().clamp_(*min_max)  # clamp
    tensor = (tensor - min_max[0]) / (min_max[1] - min_max[0])  # to range [0,1]
    img_np = tensor.numpy()
    if out_type == np.uint8:
        img_np = (img_np * 255.0).round()
        # Important. Unlike matlab, numpy.uint8() WILL NOT round by default.
    if out_type == np.uint16:
        img_np = (img_np * 1500.0).round()
    if out_type == np.int16:
        img_np = (img_np * 1500.0).round() + intercept 
    return img_np.astype(out_type)

def tensor2mask(tensor, out_type=np.uint8, min_max=(0, 1), intercept=-1024):
    '''
    Converts a torch Tensor into a mask Numpy array
    Input: 3D(D,H,W)
    Output: 3D(H,W,D), np.uint8 (default), [0,1] uint16
    '''
    mask_np = tensor.cpu().numpy()
    return mask_np.astype(out_type)


def img2tensor(image, cent=1., factor=255./2.):
    '''
    :Input 3D(H,W,D):
    :Output (1,D,H,W) [-1,1]
    '''
    return torch.Tensor((image / factor - cent)[:, :, :, np.newaxis].transpose((3, 2, 0, 1)))


"""
Converts incoming h5 data input (uint16 - D,H,W) to torch tensor float in a given range range [0, 1500].
For dataloader use, inplace operation
"""
class ImgToTensor(object):
    def __call__(self, sample, clip=False, raw_data_range=1500.):
        if clip:
            img = torch.from_numpy(np.clip(np.array(sample, np.float32, copy=False), 0, raw_data_range))
        else:
            img = torch.from_numpy(np.array(sample, np.float32, copy=False))
        return img.float().div_(raw_data_range)  # range is from 0 to 1500 for png


"""
Read json configuration file for each image and returns the spacing, orientation and origin of the image
"""
def read_config(config_path):
    config_path = os.path.join(config_path) 
    with open(config_path, 'r') as f:
        config = json.load(f)
    meta_data = {}
    meta_data['Spacing'] = [float(i) for i in config['Spacing'].split()]
    meta_data['Orientation'] = [float(i) for i in config['Orientation'].split()] 
    meta_data['Origin'] = [float(i) for i in config['Origin'].split()]
    return meta_data

def save_vol(opt, spacings, results_dir, patient_id, volume, dtype):
    # nrrd accepts in [W,H,D] format
    # [D,H,W]==>[W,H,D]
    # no need to transpose, just add index_order='C'
    # print(volume.shape)
    # volume = np.transpose(volume, (2, 1, 0))
    # print(volume.shape)
    if dtype == 'nrrd': 
        if len(spacings) != 0:
            copy_spacings = spacings.copy()
            copy_spacings[2] /= opt['scale']
        else:
            copy_spacings = []

        volume_path = os.path.join(results_dir, patient_id+'.nrrd')
        nrrd.write(volume_path, volume, index_order='C')
    elif dtype == 'nifti': 
        volume_path = os.path.join(results_dir, patient_id+'.nii.gz')
        volume = np.transpose(volume, (2, 1, 0))
        volume_img = nib.Nifti1Image(volume, np.eye(4))
        # Save the image to a file
        nib.save(volume_img, volume_path)
    else: 
        raise NotImplementedError('Output dtype not supported.')

def save_mask(opt, input_info, results_dir, seg_result_dtype, patient_id, mask):
    
    mask = mask.astype(np.uint8) # to unsigned char 
    if seg_result_dtype == 'nrrd': 
        volume_path = os.path.join(results_dir, patient_id+'.nrrd')

        header = {
            'units': ['mm', 'mm', 'mm'], 
            'Segment0_LabelValue': 1, 
        } 

        # save header in dict format 
        # spacings = input_info['spacings']
        # space_directions = ((spacings[0], 0, 0), (0, spacings[1], 0), (0, 0, spacings[2]))
        # header['space directions'] = space_directions
        # header['space origin'] = input_info['image_position']

        nrrd.write(volume_path, mask, header, index_order='C')
    elif seg_result_dtype == 'nifti': 
        volume_path = os.path.join(results_dir, patient_id+'.nii.gz')
        # print('mask shape before: {}'.format(mask.shape))
        mask = np.transpose(mask, (2, 1, 0))
        # print('mask shape after: {}'.format(mask.shape))
        mask_img = nib.Nifti1Image(mask, np.eye(4))

        # Save the image to a file
        nib.save(mask_img, volume_path)
    else: 
        raise NotImplementedError('Segmentation output dtype not supported.')

def save_vol_nested(opt, spacings, results_dir, input_info, volume):
    patient_id = input_info['patient_id'][0]
    time = input_info['time'][0]
    name = input_info['name'][0]
    # create nested directories if not exist 
    patient_dir = os.path.join(results_dir, patient_id)
    mkdir(patient_dir)
    time_dir = os.path.join(patient_dir, time)
    mkdir(time_dir)
    name_dir = os.path.join(time_dir, name)
    mkdir(name_dir) 
    mkdir(os.path.join(name_dir, 'NRRD'))
    volume_path = os.path.join(name_dir, 'NRRD', '1.nrrd')
    # nrrd accepts in [W,H,D] format
    # [D,H,W]==>[W,H,D]
    # no need to transpose, just add index_order='C'
    # volume = np.transpose(volume, (2, 1, 0))
    if len(spacings) != 0:
        copy_spacings = spacings.copy()
        copy_spacings[2] /= opt['scale']
    else:
        copy_spacings = []

    header = {'units': ['mm', 'mm', 'mm'], 'spacings': copy_spacings}
    nrrd.write(volume_path, volume, header, index_order='C')


def save_dicoms(opt, spacings, volume_path, volume):
    mkdir(volume_path)
    copy_spacings = spacings.copy()
    copy_spacings[2] /= opt['scale'] 
    # if opt['datasets']['val']['data_type'] == 'h5':     
    #     config_path =  os.path.join(opt['datasets']['val']['dataroot_LR'], uid + '.json')
    #     meta_data = read_config(config_path)
    #     spacings = meta_data['Spacing']
    #     spacings[2] /= opt['scale'] 
    #     orientations = meta_data['Orientation']
    #     orientations = [orientations[i:i+3] for i in range(0, len(orientations), 3)]
    #     origin = meta_data['Origin']  
    # elif opt['datasets']['val']['data_type'] == 'dicom':
    #     spacings[2] /= opt['scale'] 
    # else: 
    #     raise NotImplementedError('supported output format: nrrd or dicom')
    write_dicom(copy_spacings, volume, volume_path)            
    print("written as dcm completed")
    # for i, pixel_array in enumerate(vol): 
    #     write_dicom(i+1, opt, meta_data, pixel_array, volume_path)

def save_features(feature_type, opt, data): 
    feat_dtype = opt['feature_extraction'][feature_type]['output_dtype']
    feat_file = opt['feature_extraction'][feature_type]['output_path']
    id = data['uid'][0]
    if feature_type == 'deep_feature':
        save_feature_csv(feat_file, feat_dtype, id, data['deep_feature'].cpu().numpy())
    elif feature_type == 'radiomics':
        save_feature_json(feat_file, feat_dtype, id, data['radiomics']) 
    else: 
        raise NotImplementedError('Feature extraction output dtype not supported.')

def save_feature_json(filename, feat_dtype, id, features): 
    # Check if the file exists and create it if it doesn't
    results_dir = os.path.dirname(filename)
    mkdir(results_dir)
    # Check if the JSON file exists
    if os.path.exists(filename):
        # File exists, load its contents
        with open(filename, 'r') as file:
            existing_data = json.load(file)
    else:
        # File doesn't exist, create an empty object
        existing_data = []
    
    existing_data.extend(features)

    # Write the updated data to the JSON file
    with open(filename, 'w') as file:
        json.dump(existing_data, file)

def save_feature_csv(feat_output_file, feat_dtype, id, features): 
    """
    param feat_output_file: path to the csv file that the features are saved to. 
    param feature_dtype: format of the output file. Only support csv for now. 
    param id: image id.
    param features: a numpy array of size [num_nodule, 256]. 
    This function appends features to the specified csv file.     
    """
    # Check if the file exists and create it if it doesn't
    results_dir = os.path.dirname(feat_output_file)
    mkdir(results_dir)
    if not os.path.exists(feat_output_file):
        with open(feat_output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            header_row = ["ID"]
            for i in range(256):
                header_row.append(f"Feature_{i}")
            writer.writerow(header_row)
    with open(feat_output_file, 'a', newline='') as f:
        writer = csv.writer(f)
        for i in range(len(features)):
            feature_id = f"{id}-{i}"
            row = [feature_id]
            for j in range(256):
                row.append(features[i][j])
            writer.writerow(row)
    

def save_detect_bbox(opt, data): 
    """
    Saves the output of nodule detection model to a given file. Only csv supported. 
    """

    if opt['detection']['output_dtype'] == 'csv': 
        # output location 
        output_location = opt['detection']['output_path']
        results_dir = os.path.dirname(output_location)
        mkdir(results_dir)
        
        # data to be saved 
        if data is None: 
            print('data is None')
            return 
        if data['detection_bboxes'] is  None:
            return 
        
        detection_bboxes = data['detection_bboxes']
        
        # create the file if not exists 
        if not os.path.exists(output_location):
            with open(output_location, 'w', newline='') as f:
                writer = csv.writer(f)
                header_row = ['ID','center_z','center_y','center_x', 'diameter', 'probability']
                

                writer.writerow(header_row)
        
        # write data to file 
        with open(output_location, 'a', newline='') as f:
            writer = csv.writer(f)
            uid = data['uid'][0]
            for i in range(len(detection_bboxes)):
                # generate a bounding box id 
                bbox_id = f"{uid}-{i}"
                # [center_z, center_y, center_x]
                z, y, x, d, p = detection_bboxes[i][1], detection_bboxes[i][2], detection_bboxes[i][3], detection_bboxes[i][4], detection_bboxes[i][0]
                row = [bbox_id, z, y, x, d, p]
                # save the row 
                writer.writerow(row)
    else: 
        raise NotImplementedError('Nodule detection output dtype not supported.')

def write_dicom(spacings, new_arr, path):
    new_img = sitk.GetImageFromArray(new_arr)
    new_img.SetSpacing(spacings)
    
    writer = sitk.ImageFileWriter()
    # Use the study/series/frame of reference information given in the meta-data
    # dictionary and not the automatically generated information from the file IO
    writer.KeepOriginalImageUIDOn()

    modification_time = time.strftime("%H%M%S")
    modification_date = time.strftime("%Y%m%d")

    # Copy some of the tags and add the relevant tags indicating the change.
    # For the series instance UID (0020|000e), each of the components is a number, cannot start
    # with zero, and separated by a '.' We create a unique series ID using the date and time.
    # tags of interest:
    direction = new_img.GetDirection()
    series_tag_values = [("0008|0031",modification_time), # Series Time
                    ("0008|0021",modification_date), # Series Date
                    ("0008|0008","DERIVED\\SECONDARY"), # Image Type
                    ("0020|000e", "1.2.826.0.1.3680043.2.1125."+modification_date+".1"+modification_time), # Series Instance UID
                    ("0020|0037", '\\'.join(map(str, (direction[0], direction[3], direction[6],# Image Orientation (Patient)
                                                    direction[1],direction[4],direction[7])))),
                    ("0008|103e", "Normalized image"), # series description
                    ("0020|000d", "1.2.826.0.1.3680043.2.1125."+modification_date+".1"+modification_time), # study instance UID
                    ("0008|0020", modification_date), # study date
                    ("0008|0030", modification_time),  # study time
                    # Setting the type to CT preserves the slice location.
                    # set the type to CT so the thickness is carried over
                    ("0008|0060", "CT"),
                    ("0028|1050", "-600"), # WindowCenter
                    ("0028|1051", "1500"), # WindowWidth
                    ("0028|1054", "HU"), # RescaleType
                    ("0018|0050", str(spacings[2]))  # slice thickness
                    ]  

    # Write slices to output directory
    list(map(lambda i: writeSlices(writer, i, series_tag_values, new_img, path), range(new_img.GetDepth())))

def writeSlices(writer, index, series_tag_values, new_img, path):
    # DicomSeriesFromArray
    #https://simpleitk.readthedocs.io/en/next/Examples/DicomSeriesFromArray/Documentation.html
    image_slice = new_img[:,:,index]

    # Tags shared by the series.
    list(map(lambda tag_value: image_slice.SetMetaData(tag_value[0], tag_value[1]), series_tag_values))

    # Slice specific tags.
    image_slice.SetMetaData("0008|0012", time.strftime("%Y%m%d")) # Instance Creation Date
    image_slice.SetMetaData("0008|0013", time.strftime("%H%M%S")) # Instance Creation Time

    # (0020, 0032) image position patient determines the 3D spacing between slices.
    pos = [str(i) for i in new_img.TransformIndexToPhysicalPoint((0,0,index))]
    image_slice.SetMetaData("0020|0032", '\\'.join(pos)) # Image Position (Patient)
    image_slice.SetMetaData("0020|1041", pos[2]) # Slice location
    image_slice.SetMetaData("0020|0013", str(index+1)) # Instance Number

    # No need to set intercept/slope in ITK
    # RescaleIntercept 
    # image_slice.SetMetaData("0028|1052", "-1000")
    # RescaleSlope
    # image_slice.SetMetaData("0028|1053", "1")
    
    # Write to the output directory and add the extension dcm, to force writing in DICOM format.
    writer.SetFileName(os.path.join(path, '{0:0=3d}.dcm'.format(index+1)))
    writer.Execute(image_slice)

# need some work to get it working using pydicom
def write_pydicom(index, opt, meta_data, pixel_array, path):
    fullpath = os.path.join(path, '{0:0=3d}.dcm'.format(index))
    pixel_array = pixel_array.astype(np.int16)

    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    file_meta.MediaStorageSOPInstanceUID = "1.2.840.113654.2.55.102869246940549636091903990697209280630"
    file_meta.ImplementationClassUID = '1.2.40.0.13.1.1.1'
    file_meta.TransferSyntaxUID = '1.2.840.10008.1.2.1' 

    ds = FileDataset(fullpath, {},file_meta = file_meta, preamble=b"\0"*128)

    # ds.SOPClassUID = '1.2.840.10008.5.1.4.1.1.2'
    # ds.SOPInstanceUID = "1.2.840.113654.2.55.102869246940549636091903990697209280630"
    ds.SeriesDescription = 'Normalized images'
    ds.SeriesInstanceUID = '1.2.840.113654.2.55.102869246940549636091903990697209280630'
    # ds.StudyInstanceUID =  '1.2.840.113654.2.55.102869246940549636091903990697209280630'
    # ds.StudyID = ''
    # ds.ContentDate = str(datetime.date.today()).replace('-','')
    # ds.ContentTime = str(time.time()) #milliseconds since the epoch
    ds.Modality = "CT"
    ds.SamplesPerPixel = 1
    ds.PhotometricInterpretation = "MONOCHROME2"
    ds.PixelRepresentation = 0
    ds.HighBit = 11
    ds.BitsStored = 12
    ds.BitsAllocated = 16
    ds.Columns, ds.Rows = pixel_array.shape
    ds.SeriesNumber = 1
    ds.AcqusitionNumber = 1
    
    ds.RescaleSlope = "1"
    ds.RescaleIntercept = "-1000"
    ds.RescaleType  = "HU"
    ds.WindowCenter = "-600"
    ds.WindowWidth = "1500"    
    ds.InstanceNumber = index


    spacings = meta_data['Spacing']
    spacings[2] /= opt['scale'] 
    # orientations = meta_data['Orientation']
    # origin = meta_data['Origin']  

    # ds.ImagePositionPatient = origin       
    # ds.SliceLocation = origin[2] - (index - 1) * spacings[2]   
    # ds.ImageOrientationPatient = orientations[:6]
    ds.SliceThickness = spacings[2] + 1e-10 
    ds.PixelSpacing = [spacings[0], spacings[1]]
    ds.PixelData = pixel_array.tobytes()
    ds.save_as(fullpath)
    

####################
# metric
####################
def calculate_psnr(img1, img2):
    # img1 and img2 have range [0, 1]
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    mse = np.mean((img1 - img2)**2)
    if mse == 0:
        return float('inf')
    return 20 * math.log10(255.0 / math.sqrt(mse))


def ssim(img1, img2):
    C1 = (0.01 * 255)**2
    C2 = (0.03 * 255)**2
    # C1 = (0.01)**2
    # C2 = (0.03)**2
    img1 = img1.astype(np.float64)
    img2 = img2.astype(np.float64)
    kernel = cv2.getGaussianKernel(11, 1.5)
    window = np.outer(kernel, kernel.transpose())

    mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
    mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
    mu1_sq = mu1**2
    mu2_sq = mu2**2
    mu1_mu2 = mu1 * mu2
    sigma1_sq = cv2.filter2D(img1**2, -1, window)[5:-5, 5:-5] - mu1_sq
    sigma2_sq = cv2.filter2D(img2**2, -1, window)[5:-5, 5:-5] - mu2_sq
    sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

    ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                            (sigma1_sq + sigma2_sq + C2))
    return ssim_map.mean()


def calculate_ssim(img1, img2):
    '''calculate SSIM
    the same outputs as MATLAB's
    img1, img2: [0, 255]
    '''
    if not img1.shape == img2.shape:
        raise ValueError('Input images must have the same dimensions.')
    if img1.ndim == 2:
        return ssim(img1, img2)
    elif img1.ndim == 3:
        if img1.shape[2] == 3:
            ssims = []
            for i in range(3):
                ssims.append(ssim(img1, img2))
            return np.array(ssims).mean()
        elif img1.shape[2] == 1:
            return ssim(np.squeeze(img1), np.squeeze(img2))
    else:
        raise ValueError('Wrong input image dimensions.')


def getIoU(y_true, y_pred):
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.logical_and(y_true_f, y_pred_f).sum()
    union = np.logical_or(y_true_f, y_pred_f).sum()
    return (intersection + 1) * 1. / (union + 1)

"""
Creates 'pdist' model, which we need to calcuate 'pdist' metric during validation
"""
def create_pdist_model(network='vgg', use_gpu=True):
    '''
    percetual similarity metric
    https://github.com/richzhang/PerceptualSimilarity
    :param network can be vgg or alex
    '''
    print("Initializing pdist model")
    print("-"*40)
    # Initializing the model
    model = dm.DistModel()
    model.initialize(model='net-lin', net=network, use_gpu=use_gpu)
    return model


def calculate_pdist(model, img1, img2):
    # expand channel to 3 dim for vgg
    img1 = np.expand_dims(img1, axis=2)
    img1 = np.repeat(img1, 3, axis=2)
    img2 = np.expand_dims(img2, axis=2)
    img2 = np.repeat(img2, 3, axis=2)
    #  image from [-1,1]
    img1 = img2tensor(img1)
    img2 = img2tensor(img2)

    # Compute distance
    with torch.no_grad():
        dist = model.forward(img1, img2)
    return dist[0]

def cvt_int(self, inputString):
    find_digit = re.search(r'\d', inputString)
    reformat_num = int(float(inputString[find_digit.start():]))
    reformat_str = inputString[:find_digit.start()] + str(reformat_num)
    return reformat_str

def load_dicom(folder_location):
    '''
    :function 
    Load dicom images in one folder, give them correct ordering. 
    :returns
    A 3D volume and pixel spacings 
    '''
    # retrieve names of all dcm files
    dicom_names = glob.glob(os.path.join(folder_location,'*.dcm'))
    spacings = [] 
    # load dcm files 
    files = []
    for fname in dicom_names:
        files.append(pydicom.dcmread(fname))

    # skip files with no SliceLocation 
    slices = []
    skipcount = 0
    for f in files:
        if hasattr(f, 'SliceLocation'):
            slices.append(f)
        else:
            skipcount = skipcount + 1

    # ensure slices are in the correct order (sorted)
    slices = sorted(slices, key=lambda s: s.SliceLocation)

    # pixel spacings, assuming all slices are the same
    ps = [0, 0, 0]
    ps[0], ps[1] = float(slices[0].PixelSpacing[0]), float(slices[0].PixelSpacing[1])
    cosines0 = slices[0].ImageOrientationPatient
    iip0 = slices[0].ImagePositionPatient
    normal0 = [cosines0[1]*cosines0[5] - cosines0[2]*cosines0[4], 
                cosines0[2]*cosines0[3] - cosines0[0]*cosines0[5],
                cosines0[0]*cosines0[4] - cosines0[1]*cosines0[3]]
    dist0 = 0 
    for i in range(3): 
        dist0 += normal0[i]*iip0[i]
    
    iip1 = slices[1].ImagePositionPatient
    dist1 = 0 
    for i in range(3): 
        dist1 += normal0[i]*iip1[i]

    # subtract and take abs to obtain pixel spacing in z direction 
    ps[2] = abs(dist1 - dist0)

    # create 3D volume in [D,H,W]
    # img_shape = list(slices[0].pixel_array.shape)
    # img_shape.append(len(slices))
    img_shape = [len(slices), slices[0].pixel_array.shape[0], slices[0].pixel_array.shape[1]]
    vol = np.zeros(img_shape)

    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img2d = s.pixel_array
        vol[i,:,:] = img2d
    
    # generate id 
    patient_id = slices[0].PatientID.replace("_", "-")
    timepoint = slices[0].StudyDate
    series_instance_uid = slices[0].SeriesInstanceUID
    modality = slices[0].Modality
    volume_id = f"{patient_id}_{timepoint}_{series_instance_uid}_{modality}"
    # print(volume_id)
    return vol, ps, volume_id


### options 
"""
Converts the 'OrderedDict()'to NoneDict, which return None for missing key
"""
def dict_to_nonedict(opt):
    if isinstance(opt, dict):
        new_opt = dict()
        for key, sub_opt in opt.items():
            new_opt[key] = dict_to_nonedict(sub_opt)
        return NoneDict(**new_opt)
    elif isinstance(opt, list):
        return [dict_to_nonedict(sub_opt) for sub_opt in opt]
    else:
        return opt

"""
Converts dictionary into readable string
"""
def dict2str(opt, indent_l=1):
    msg = ''
    for k, v in opt.items():
        if isinstance(v, dict):
            msg += ' ' * (indent_l * 2) + k + ':[\n'
            msg += dict2str(v, indent_l + 1)
            msg += ' ' * (indent_l * 2) + ']\n'
        else:
            msg += ' ' * (indent_l * 2) + k + ': ' + str(v) + '\n'
    return msg


class NoneDict(dict):
    def __missing__(self, key):
        return None

"""
Returns an object with a run_test function (for non_DL methods such as bm3d). 
"""
class PythonFunctionWrapper:
    def __init__(self, python_function):
        self.python_function = python_function

    def run_test(self, input_data):
        output = self.python_function(input_data)
        return output

def rescale_image(image, min_value, max_value):
    # Find the minimum and maximum values of the image
    current_min = np.min(image)
    current_max = np.max(image)

    # Rescale the image to the desired range
    rescaled_image = (image - current_min) * (max_value - min_value) / (current_max - current_min) + min_value

    return rescaled_image

def resize_image(data, size=(52,52,52)):
    """
    Resize the data to the input size
    """ 
    # [height, width, depth] = data.shape
    [depth, height, width] = data.shape 
    # scale = [self.input_D*1.0/depth, self.input_H*1.0/height, self.input_W*1.0/width] 
    target_depth, target_height, target_width = size 
    scale = [target_depth*1.0/depth, target_height*1.0/height, target_width*1.0/width] 
    data = ndimage.interpolation.zoom(data, scale, order=0)
    return data

def extract_roi(image, centroid): 
    """
    image: 3D numpy array in zyx 
    centorid: tuple (z, y, x) 
    Return a ROI of the input image centered at (z,y,x) and size (52,52,52)
    """
    # if isinstance(centroid, torch.Tensor):
    #     z, y, x = centroid.int()
    # else: 
    #     z, y, x = centroid

    z, y, x = centroid

    # Extract the bounding box of shape [52,52,52] around the centroid
    z_min, z_max = max(0, z - 26), min(image.shape[0], z + 26)
    y_min, y_max = max(0, y - 26), min(image.shape[1], y + 26)
    x_min, x_max = max(0, x - 26), min(image.shape[2], x + 26)
    # add zero padding if expected ROI lies partially out of the image                 
    roi = image[z_min:z_max, y_min:y_max, x_min:x_max]
    # pad_dims = [0, 52-(x_max-x_min), 0, 52-(y_max-y_min), 0, 52-(z_max-z_min)]
    # roi = F.pad(roi, pad_dims, mode='constant', value=0)
    pad_dims = ((0, 52-(z_max-z_min)), (0, 52-(y_max-y_min)), (0, 52-(x_max-x_min)))
    roi = np.pad(roi, pad_width=pad_dims, mode='constant', constant_values=0)
    
    return roi 

def extract_roi_with_diameter(image, centroid, diameter):
    z, y, x = centroid

    # Calculate starting and ending indices for each dimension
    start_z = max(0, z - diameter // 2)
    end_z = min(image.shape[0], z + diameter // 2 + 1)
    start_y = max(0, y - diameter // 2)
    end_y = min(image.shape[1], y + diameter // 2 + 1)
    start_x = max(0, x - diameter // 2)
    end_x = min(image.shape[2], x + diameter // 2 + 1)

    # Slice the image and extract the ROI
    roi = image[start_z:end_z, start_y:end_y, start_x:end_x]

    return roi

def convert_numpy_to_list(data):
    if isinstance(data, np.ndarray):
        return data.tolist()
    elif isinstance(data, dict):
        return {key: convert_numpy_to_list(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_to_list(item) for item in data]
    else:
        return data
