import os
import cv2
import numpy as np
import pydicom as dicom
import h5py
import json


def _save_metadata(save_to, spacing, size, orientation, origin):
    header = {"PixelType": "short", "Dimension": "3", "Size": size, "Origin": origin, "Spacing": spacing, "Orientation": orientation, "MinPoint": "0 0 1", "Compression": "ZLib"}
    with open(save_to, 'w') as out_file:
        json.dump(header, out_file)

# check saving datatype of h5 file - overflow issue
def _save_h5(image, save_to):
    hf = h5py.File(save_to, 'w')
    hf.create_dataset('data', data=image, dtype='int16')
    hf.close()

def read_files(root, save_to):
    slices = [dicom.read_file(root + '/' + s) for s in os.listdir(root)]
    slices.sort(key=lambda x: x.InstanceNumber)
    image = np.stack([s.pixel_array for s in slices])
    # convert to int16
    image = image.astype(np.int16) 
    image[image == -2000] = 0
    # print('img min-max before linear processing:', image.min(), image.max())
    # convert to HU (all slices should have same RescaleIntercept and RescaleSlope(1))
    intercept = slices[0].RescaleIntercept
    slope = slices[0].RescaleSlope
    # doing a linear transform
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
    image += np.int16(intercept)
    
    image = np.clip(image, -1000, None)
    image += 1000
    # print('img min-max after cliping and addition:', image.min(), image.max())
    h5_file_name = os.path.join(save_to, '_'.join(root.split('/')[2:])+'.h5')
    h5_json_name = os.path.join(save_to, '_'.join(root.split('/')[2:])+'.json')
    _save_h5(image, h5_file_name)
    # information for metadata
    pixel_spacing = slices[0].PixelSpacing
    slice_thickness = slices[0].SliceThickness
    spacing = "{} {} {}".format(pixel_spacing[0], pixel_spacing[1], slice_thickness)
    size = [image.shape[1], image.shape[2], image.shape[0]]
    orientation = ' '.join(map(str, slices[0].ImageOrientationPatient)) # dummy orientation and origin information
    orientation = '-1 ' + orientation + ' -1'
    origin = "1 1 1"
    _save_metadata(h5_json_name, spacing, size, orientation, origin)

def main(root, save_to, include=None, exclude=None):
    if not os.path.exists(save_to):
        os.mkdir(save_to)
    for root, dirs, files in os.walk(root):
        if len(files) != 0:
            if include:
                if include in root:
                    if exclude:
                        if include+'_'+exclude not in root:
                            read_files(root, save_to)
                    else:
                        read_files(root, save_to)
            else:
                read_files(root, save_to)
    print('All files processed!')

"""
file = "/gan_data/UCLA/data/k2_d10_st1.0/af8923702f81618f9030387e9dd51589.h5"
with h5py.File(file, 'r') as file:
    IMG_THICKNESS, IMG_WIDTH, IMG_HEIGHT = file['data'].shape
    print(IMG_THICKNESS, IMG_WIDTH, IMG_HEIGHT)
    pixel_array = np.array(file['data'])
    print(pixel_array.dtype)
    print(pixel_array.min(), pixel_array.max())
"""

if __name__ == '__main__':
    main(root='/aapm_data', save_to='/workspace/NormGAN/aapm_3d_testset', include='full_1mm', exclude='sharp')