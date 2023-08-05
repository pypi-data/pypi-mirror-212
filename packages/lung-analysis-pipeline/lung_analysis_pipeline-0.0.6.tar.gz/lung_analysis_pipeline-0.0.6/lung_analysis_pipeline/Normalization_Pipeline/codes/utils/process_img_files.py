import os
import re
import random
import numpy as np
import json
import nrrd
from sklearn.model_selection import train_test_split


def cvt_int(inputString):
    find_digit = re.search(r'\d', inputString)
    reformat_num = int(float(inputString[find_digit.start():]))
    reformat_str = inputString[:find_digit.start()] + str(reformat_num)
    return reformat_str

def rename_file_with_cd(data_path):
    img_conditions = os.listdir(data_path)
    for each_img_cd in img_conditions:
        dir_path = os.path.join(data_path, each_img_cd)
        cd_info = '_'.join([cvt_int(cd) for cd in dir_path.split('/')[-1].split('_')])
        for file in os.listdir(dir_path):
            file_name, ext = file.split('.')
            new_name = file_name + '_' + cd_info + '.' + ext
            new_name_path = os.path.join(dir_path, new_name)
            os.rename(os.path.join(dir_path, file), new_name_path)
    print('FILES RENAMED!')

def write_txt_file(data_list, name, path):
    file_name = '{}.txt'.format(name)
    file_path = os.path.join(path, file_name)
    with open(file_path, 'w') as f:
        f.write('\n'.join(data_list))

def generate_specific_uids(path_to_data, path_to_save_txt, split, need_testSet_withNod):
    mapping_uids = {}
    train_uids, val_uids, test_uids = [], [], []
    for file in os.listdir(path_to_data):
        condition = '_'.join(file.split('.')[0].split('_')[1:])
        if condition not in mapping_uids:
            mapping_uids[condition] = []
        file_name = file.split('.')[0]
        if file_name not in mapping_uids[condition]:
            mapping_uids[condition].append(file_name)
    # random or based on ref split
    if split == 'random':
        # get uid for each condition
        for key in mapping_uids:
            uids = mapping_uids[key]
            random.shuffle(uids)
            train_tmp, test_uid = train_test_split(uids, test_size=0.15)
            train_uid, val_uid = train_test_split(train_tmp, test_size=0.15)
            train_uids.extend(train_uid)
            val_uids.extend(val_uid)
            test_uids.extend(test_uid)
            """
            train_uids.extend(random.sample(train_uid, 15))
            val_uids.extend(random.sample(val_uid, 3))
            test_uids.extend(random.sample(test_uid, 4))
            """
    else:
        read_ref = [file.split('.h5')[0] for file in os.listdir(split) if file.endswith('.h5')]
        ref_test_uid = []
        nodule_count = 0
        if need_testSet_withNod:
            with open(need_testSet_withNod, 'r') as file:
                ucla_nodule_annot = json.load(file)
            for annot in ucla_nodule_annot:
                if nodule_count > 22:
                    break
                nodule_count += len(ucla_nodule_annot[annot])
                ref_test_uid.append(annot)
            ref_test_uid = ref_test_uid[:15]
            ref_train_val = [uid for uid in read_ref if uid not in ref_test_uid]
            ref_train_uid, ref_val_uid = train_test_split(ref_train_val, test_size=0.15)
        else:
            ref_train_tmp, ref_test_uid = train_test_split(read_ref, test_size=0.15)
            ref_train_uid, ref_val_uid = train_test_split(ref_train_tmp, test_size=0.15)
        # append uids
        for key in mapping_uids:
            uids = [file.split('_')[0] for file in mapping_uids[key]]
            for uid in uids:
                if uid in ref_train_uid:
                    train_uids.append(uid+'_'+key)
                elif uid in ref_val_uid:
                    val_uids.append(uid+'_'+key)
                elif uid in ref_test_uid:
                    test_uids.append(uid+'_'+key)
                else:
                    print('Skiping UID:', uid)
    # shuffle merged lists and write to file
    random.shuffle(train_uids)
    random.shuffle(val_uids)
    random.shuffle(test_uids)      
    write_txt_file(train_uids, 'train_all_ep', path_to_save_txt)
    write_txt_file(val_uids, 'valid_all_ep', path_to_save_txt)
    write_txt_file(test_uids, 'test_all_ep', path_to_save_txt)
    print('UIDS GENERATED! Train: {}, Val: {}, Test: {}'.format(len(train_uids), len(val_uids), len(test_uids)))

def generate_nodVol_split(path_to_vol, path_to_save_txt, need_external_test):
    files = [file for file in os.listdir(path_to_vol) if file.endswith('.nrrd')]
    print('Total files:', len(files))
    random.shuffle(files)
    train_uids, val_uids, test_uids = [], [], []
    data_dict = {'nod':[], 'nonod':[]}
    for uid in files:
        nod_type = uid.split('_')[0]
        data_dict[nod_type].append(uid)
    print('Total nodules {} and non-nodules {}'.format(len(data_dict['nod']), len(data_dict['nonod'])))
    if need_external_test:
        with open(need_external_test, 'r') as f:
            lines = f.readlines()
            test_cases = [l.rstrip() for l in lines]
        unique_test = []
        for case in test_cases:
            _ = case.split('_')[0]
            if _ not in unique_test:
                unique_test.append(_)
        allowed_uniques = []
        for file in data_dict['nod']:
            _ = file.split('_')[1]
            if _ in unique_test:
                allowed_uniques.append(file)
        random.shuffle(allowed_uniques)
        test_uids.extend(random.sample(allowed_uniques, 22))
        test_uids.extend(random.sample(data_dict['nonod'], 22))
        # print(len(test_uids))
        new_data_dict = {'nod':list(set(data_dict['nod'])-set(test_uids)), 'nonod':list(set(data_dict['nonod'])-set(test_uids))}
        # print(len(new_data_dict['nod']), len(new_data_dict['nonod']))
        for data in new_data_dict:
            uids = new_data_dict[data]
            ref_train_uid, ref_val_uid = train_test_split(uids, test_size=0.15)
            train_uids.extend(ref_train_uid)
            val_uids.extend(ref_val_uid)
    else:
        for data in data_dict:
            uids = data_dict[data]
            ref_train_tmp, ref_test_uid = train_test_split(uids, test_size=0.15)
            ref_train_uid, ref_val_uid = train_test_split(ref_train_tmp, test_size=0.15)
            train_uids.extend(ref_train_uid)
            val_uids.extend(ref_val_uid)
            test_uids.extend(ref_test_uid)
    # |----- shuffle uids ------------|
    random.shuffle(train_uids)
    random.shuffle(val_uids)
    random.shuffle(test_uids)
    # |----- write to file ------------|
    write_txt_file(train_uids, 'train_nodule', path_to_save_txt)
    write_txt_file(val_uids, 'val_nodule', path_to_save_txt)
    write_txt_file(test_uids, 'test_nodule', path_to_save_txt)
    print('UIDs Created!')

def remove_files(path_to_cases, cases_to_keep):
    with open(cases_to_keep, 'r') as f:
        lines = f.readlines()
        test_set_uids = [l.rstrip() for l in lines]
        for file in os.listdir(path_to_cases):
            file_name = file.split('.nrrd')[0]
            if file_name not in test_set_uids:
                os.remove(os.path.join(path_to_cases, file))
        print('FILES REMOVED!')

def seperate_cases(file_1, file_2):
    uids_to_exclude, uids_to_keep, nodule_annot_to_keep = [], [], []
    with open(file_1, 'r') as f:
        lines = f.readlines()
        set_uids = [l.rstrip().split("_")[0] for l in lines if 'k2_d25' in l]
        uids_to_exclude.extend(set_uids)
    with open(file_2, 'r') as f:
        lines = f.readlines()
        set_uids = [l.rstrip().split("_")[0] for l in lines if 'k2_d25' in l]
        uids_to_exclude.extend(set_uids)
    with open('/datasets/nodule_annotations/ucla_nodule_uids.txt', 'r') as f:
        lines = f.readlines()
        set_uids = [l.rstrip() for l in lines]
        nodule_annot_to_keep.extend(set_uids)
    all_uids = '/datasets/data/k2_d25_st1.0'
    for file in os.listdir(all_uids):
        if file.endswith('.h5'):
            file_name = file.split('.')[0]
            if file_name not in uids_to_exclude and file_name in nodule_annot_to_keep:
                uids_to_keep.append(file_name)
    for uid in uids_to_keep:
        print(uid)

def check_size(uid_path, vol_path):
    with open(uid_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    for line in lines:
        img_path = os.path.join(vol_path, line)
        data, header = nrrd.read(img_path)
        if data.shape[0] != 64 or data.shape[1] != 64 or data.shape[2] != 16:
            print(line)



if __name__ == '__main__':
    # path_to_data = '/datasets/data'
    # rename_file_with_cd(path_to_data)
    # path_to_merged_data = '/datasets/data_st1.0_merged'
    # generate_merged_uids(path_to_merged_data, '/datasets/uids/')
    # generate_specific_uids(path_to_merged_data, '/datasets/uids/merged_uids', split='/datasets/reference/k2_d100_st1.0',
    #                         need_testSet_withNod='/datasets/nodule_annotations/ucla_annotations.json')
    # remove_files('/workspace/cNormGAN_debug/results/SNGAN-Embed-Gen-Disc-allTileStitch-k1d10-k2d100-Nastaran/test_st1.0_nastaran/', 
    #                 '/datasets/nodule_annotations/ucla_nastaran_subset_32_test_uid.txt')
    # seperate_cases('/datasets/uids/merged_uids/merged_train_subset_uids.txt', '/datasets/uids/merged_uids/merged_valid_subset_uids.txt')
    # check_files('/datasets/uids/merged_uids/merged_train_subset_uids.txt', '/datasets/data_train_tmp', '/datasets/data_st1.0_merged')
    # path_to_nodVol = '/datasets/UCLA-Nas-NoduleVolume/unnormalized/k2_d100_st1.0'
    # generate_nodVol_split(path_to_nodVol, '/datasets/UCLA-Nas-NoduleVolume/uids', '/datasets/uids/merged_uids/merged_test_all_ep_uids.txt')
    check_size('/datasets/UCLA-Nas-NoduleVolume/uids/test_nodule.txt', '/datasets/UCLA-Nas-NoduleVolume/unnormalized/k2_d100_st1.0')

