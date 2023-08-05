import os
import nrrd
import numpy as np
import matplotlib.pyplot as plt
import json
import cv2
import csv
from PIL import Image
import random


def rescale_img_to_rgb(img, need_clip=True):
    if need_clip:
        img = np.clip(img, 0, 1500)
    img = (img - img.min()) / (img.max() - img.min())
    img *= 255.0
    img = img.astype(np.uint8)
    return img

def generate_nodule_slices(ALLOWED_CND, test_set_annot):
    with open(test_set_annot, 'r') as file:
        nastaran_nodule_annot = json.load(file)
    print('Number of Nastaran nodule cases:', len(nastaran_nodule_annot.keys()))
    num_nastaran_nodule = 0
    for uid in nastaran_nodule_annot:
        center = nastaran_nodule_annot[uid]
        num_nastaran_nodule += len(center)
    print('Number of nodules in nastaran:', num_nastaran_nodule)

    # extract for each condition
    for cnd in ALLOWED_CND:
        if save_csv_annot:
            annot_csv = []
        print('Processing nodule condition:', cnd)
        save_path = os.path.join(path_to_save, cnd)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
    
        file_path_to_read = os.path.join(path_to_cases, cnd)
        files = os.listdir(file_path_to_read)
        for case in nastaran_nodule_annot:
            file_name = case + '.nrrd'
            if file_name in files:
                img_path = os.path.join(file_path_to_read, file_name)
                data, header = nrrd.read(img_path)
                data = data.transpose((2, 1, 0))
                coords = nastaran_nodule_annot[case]
                coords = np.array([[int(x),int(y),int(z)] for x,y,z in coords])
                for annot in coords:
                    x, y, z = annot
                    xs, xe = x - 25, x + 25
                    ys, ye = y - 25, y + 25
                    try:
                        nodule_slice = data[z]
                        rgb_slice = Image.fromarray(rescale_img_to_rgb(nodule_slice)).convert("RGB")
                        nodule_name = 'nod_{}_{}.png'.format(case, z)
                        nodule_save_path = os.path.join(save_path, nodule_name)
                        rgb_slice.save(nodule_save_path)
                        if save_csv_annot:
                            annot_csv.append([nodule_name, xs, ys, xe, ye, 'nodule'])
                    except Exception as e:
                        print('{}, Skipping....'.format(e))
        
        if save_csv_annot:
            save_path = os.path.join(path_to_save, '{}.csv'.format(cnd))
            with open(save_path, 'w') as f:
                write = csv.writer(f)
                write.writerows(annot_csv)

    print('All Nodule Slices Extracted!')


def generate_nonod_slices(ALLOWED_CND, nonod_annot):
    with open(nonod_annot, 'r') as file:
        nas_nonodule_annot = json.load(file)
    # extract for each condition
    for cnd in ALLOWED_CND:
        print('Processing non-nodule condition:', cnd)
        save_path = os.path.join(path_to_save, cnd)
        file_path_to_read = os.path.join(path_to_cases, cnd)
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        files = os.listdir(file_path_to_read)
        for case in nas_nonodule_annot:
            file_name = case + '.nrrd'
            if file_name in files:
                img_path = os.path.join(file_path_to_read, file_name)
                data, header = nrrd.read(img_path)
                data = data.transpose((2, 1, 0))
                coords = nas_nonodule_annot[case]
                for annot in coords:
                    z = (int(annot[0]) + int(annot[1]))//2
                    try:
                        data_annot = data[z, :, :]
                        clipped = np.clip(data_annot, 0, 1500)
                        clipped = np.true_divide(clipped, 1500)
                        clipped = (clipped*255.0).astype(np.uint8)
                        clipped_img = Image.fromarray(clipped)
                        nodule_name = 'nonod_{}_{}.png'.format(case, z)
                        nodule_save_path = os.path.join(save_path, nodule_name)
                        clipped_img.save(nodule_save_path)
                        nonodannot_csv.append([nodule_save_path])
                    except Exception as e:
                        print('{}, Skipping....'.format(e))             
    print('All Non-nodule Slices Extracted!')


if __name__ == '__main__':
    ALLOWED_CND = ['k1_d10_st1.0', 'k1_d25_st1.0', 'k1_d100_st1.0', 'k2_d10_st1.0', 'k2_d100_st1.0', 'k3_d10_st1.0', 'k3_d25_st1.0', 'k3_d100_st1.0']
    path_to_cases = '/dingo_data_leihao/nastaran_test_h5'
    save_csv_annot = True
    
    # ALLOWED_CND = ['test_cases-Nas-k1_d10_st1.0', 'test_cases-Nas-k1_d25_st1.0', 'test_cases-Nas-k1_d100_st1.0',\
    #                 'test_cases-Nas-k2_d10_st1.0', 'test_cases-Nas-k3_d10_st1.0', 'test_cases-Nas-k3_d25_st1.0',\
    #                 'test_cases-Nas-k3_d100_st1.0']
    # path_to_cases = '/workspace/cNormGAN-AC/results/nastaran_test_cases/HM-EQMergedData_Ref-k2d100'

    test_set_annot = '/datasets/nodule_annotations/ucla_nastaran_test_set_st1.0.json'
    path_to_save = '/datasets/Nas_TaskData/task_detection_512_512/Unnormalized'
    subset_folder = '' # test_st1.0_norm
    
    # extract nodule slices
    generate_nodule_slices(ALLOWED_CND, test_set_annot)
    # generate_nonod_slices(ALLOWED_CND, nonod_annot)




