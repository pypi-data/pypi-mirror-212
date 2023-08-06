import os
import nrrd
import numpy as np
import matplotlib.pyplot as plt
import json
import cv2
import random
import h5py


def read_annot(path_to_annot):
    with open(path_to_annot, 'r') as file:
        annot = json.load(file)
    num_annot = 0
    for uid in annot:
        center = annot[uid]
        num_annot += len(center)
    print('Number of cases:', len(annot.keys()))
    print('Number of annotations in {} cases: {}'.format(len(annot.keys()), num_annot))
    return annot

def write_images(out_path, uid, volume, center, spacings, rad, tag=None, level=-600, width=1500):
    offset = 1000
    wl = level-width/2 + offset
    wh = level+width/2 + offset
    # <---- clip to [0, 1150] window ---->
    # volume = volume.astype(np.int16) # np.int16
    # volume = np.clip(volume, wl, wh).astype(np.int16) # np.int16
    
    dx, dy, dz = spacings
    rx = ry = int(rad)
    rz = int(round(dz * rad))//2
    if len(center) == 2:
        center, slice_num = center
    x, y, z = [int(x) for x in center]
    xs, xe = x - rx, x + rx 
    ys, ye = y - ry, y + ry
    zs, ze = z - rz, z + rz
    if tag:
        nodule_name = '{}_{}_{}-{}-{}-{}-{}-{}.nrrd'.format(tag, uid, ys, ye, xs, xe, zs, ze)
        nodule_save_path = os.path.join(out_path, nodule_name)   
    header = {'units': ['mm', 'mm', 'mm'], 'spacings': spacings}
    nodule_volume = volume[zs:ze, ys:ye, xs:xe].astype(np.uint16) # np.int16
    nrrd.write(nodule_save_path, nodule_volume, header, index_order='C')

def create_nodule_conditions(ALLOWED_CND, path_to_cases, nodule_annot, under_subset=None):
    nastaran_nodule_annot =  read_annot(nodule_annot)
    # create dataset for each condition
    for cnd in ALLOWED_CND:
        print('Processing nodule condition:', cnd)
        save_path = os.path.join(path_to_save_vol, cnd)
        if under_subset:
            file_path_to_read = os.path.join(path_to_cases, cnd, under_subset)
        else:
            file_path_to_read = os.path.join(path_to_cases, cnd)

        if not os.path.exists(save_path):
            os.makedirs(save_path)
        files = os.listdir(file_path_to_read)
        for case in nastaran_nodule_annot:
            file_name = case + '.nrrd'
            if file_name in files:
                img_path = os.path.join(file_path_to_read, file_name)
                data, header = nrrd.read(img_path)
                data = data.transpose((2, 1, 0))
                coords = nastaran_nodule_annot[case]
                for annot in coords:
                    write_images(save_path, case, data, annot, header['spacings'], rad=64/2, tag='nod', level=-600, width=1500)
    print('All Nodule Volumes Extracted!')

def get_nonodule_cases(path_to_ref, nodule_annot):
    annot =  read_annot(nodule_annot)
    non_nodule_cases = [file.split('.nrrd')[0] for file in os.listdir(path_to_ref) if (file.endswith('.nrrd') and file.split('.nrrd')[0] not in annot.keys())]
    random.shuffle(non_nodule_cases)
    return non_nodule_cases

def generate_random_coords(non_nodule_cases, path_to_bodymask, num_cases_to_extract):
    FILL_RATIO_THRESHOLD = 0.95
    t, w, h = 16, 64, 64
    scale = 1
    num_non_nodules = 0
    nonod_coord = {}
    # extract cases
    while num_non_nodules <= num_cases_to_extract:
        for case in non_nodule_cases:
            if num_non_nodules > num_cases_to_extract:
                break
            if case not in nonod_coord:
                nonod_coord[case] = []
            fill_ratio = 0.
            mask_data, header = nrrd.read(os.path.join(path_to_bodymask, case+'.nrrd'))
            mask_data = mask_data.transpose((2, 1, 0)) 
            non_zeros = np.where(mask_data != 0)
            mask_data[non_zeros] = 1
            IMG_THICKNESS, IMG_WIDTH, IMG_HEIGHT = mask_data.shape
            while fill_ratio < FILL_RATIO_THRESHOLD:
                rnd_t_HR = random.randint(0, IMG_THICKNESS - int(t * scale))
                rnd_h = random.randint(0, IMG_HEIGHT - h)
                rnd_w = random.randint(0, IMG_WIDTH - w)
                extracted_cube = mask_data[rnd_t_HR:rnd_t_HR+int(t*scale), rnd_w:rnd_w+w, rnd_h:rnd_h+h].sum()
                total_required = (scale * t * w * h)
                fill_ratio = extracted_cube/total_required
            nonod_coord[case].append([round(rnd_t_HR/scale), round(rnd_t_HR/scale)+t, rnd_w, rnd_w+w,\
                                        rnd_h, rnd_h+h])
            num_non_nodules += 1
    return nonod_coord

def create_nonodule_conditions(ALLOWED_CND, path_to_cases, nonod_coord):
    if type(nonod_coord) is not dict:
        nonod_coord = read_annot(nonod_coord)
    for cnd in ALLOWED_CND:
        print('Processing non-nodule condition:', cnd)
        save_path = os.path.join(path_to_save_vol, cnd)
        file_path_to_read = os.path.join(path_to_cases, cnd)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        files = os.listdir(file_path_to_read)
        for case in nonod_coord:
            file_name = case + '.nrrd'
            if file_name in files:
                img_path = os.path.join(file_path_to_read, file_name)
                data, header = nrrd.read(img_path)
                data = data.transpose((2, 1, 0))
                coords = nonod_coord[case]
                for annot in coords:
                    nonod_vol = data[annot[0]:annot[1], annot[2]:annot[3], annot[4]:annot[5]]
                    nonod_vol = nonod_vol.astype(np.int16)    
                    nodule_name = 'nonod_{}_{}-{}-{}-{}-{}-{}.nrrd'.format(case, annot[2], annot[3], annot[4], annot[5],
                                                                                annot[0], annot[1])
                    nodule_save_path = os.path.join(save_path, nodule_name)
                    nrrd.write(nodule_save_path, nonod_vol, header, index_order='C')
    print('All Non-nodule Volumes Extracted!')


if __name__ == '__main__': 
    # ALLOWED_CND = ['k1_d10_st1.0', 'k1_d25_st1.0', 'k1_d100_st1.0', 'k2_d10_st1.0', 'k2_d100_st1.0', 'k3_d10_st1.0', 'k3_d25_st1.0', 'k3_d100_st1.0']
    # unnorm_cases = '/dingo_data_leihaowei/nastaran_test_h5'
    ALLOWED_CND = ['test_cases-Nas-k1_d10_st1.0', 'test_cases-Nas-k1_d25_st1.0', 'test_cases-Nas-k1_d100_st1.0',\
                    'test_cases-Nas-k2_d10_st1.0', 'test_cases-Nas-k3_d10_st1.0',\
                    'test_cases-Nas-k3_d25_st1.0', 'test_cases-Nas-k3_d100_st1.0']
    
    norm_cases = '../../results/nastaran_test_cases/BM3D-EQMergedData_Ref-k2d100'
    # path_to_ref = '/dingo_data_leihaowei/nastaran_test_h5/k2_d100_st1.0'
    # path_to_bodymask = '/dingo_data_leihaowei/nastaran_test_lung_mask/k2_d100_st1.0'
    nodule_annot = '/datasets/nodule_annotations/ucla_nastaran_test_set_st1.0.json'
    non_nodule_annot = '' #'/datasets/non-nodule_annotations/nas_non_nodule_annot_v1.json'

    # ======================================
    # Path to extract cases from and save to 
    # ======================================
    path_to_cases = norm_cases
    path_to_save_vol = '/datasets/Nas_TaskData/task_segment_32_64_64/normalized/BM3D'
    # =====================================================================
    # create unnormalized nodule cases for each condition
    create_nodule_conditions(ALLOWED_CND, path_to_cases, nodule_annot, under_subset=None)
    # =====================================================================

    """
    # create unnormalized non-nodule cases for each condition
    if non_nodule_annot:
        print('Reading non-nodules from annot')
        create_nonodule_conditions(ALLOWED_CND, path_to_cases, non_nodule_annot)
    else:
        # generate nonodule coordinates via bodymask
        print('Generating coordinates with bodymask')
        nonodule_cases = get_nonodule_cases(path_to_ref, nodule_annot)
        nonod_coods = generate_random_coords(nonodule_cases, path_to_bodymask, 67)
        with open('/datasets/non-nodule_annotations/nas_non_nodule_annot_v1.json', "w") as outfile:
            json.dump(nonod_coods, outfile)
        create_nonodule_conditions(ALLOWED_CND, path_to_cases, nonod_coods)
    """