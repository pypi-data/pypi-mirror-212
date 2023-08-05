import os
import random
from sklearn.model_selection import train_test_split
import shutil
import nrrd


def write_txt_file(data_list, name, path):
    file_name = '{}.txt'.format(name)
    file_path = os.path.join(path, file_name)
    with open(file_path, 'w') as f:
        f.write('\n'.join(data_list))

def create_train_val_test(path_to_files, path_to_save_txt, external_test=None):
    all_files = os.listdir(path_to_files)
    if external_test:
        with open(external_test, 'r') as f:
            lines = f.readlines()
            test_cases = [l.rstrip() for l in lines]
    all_files = list(set(all_files)-set(test_cases))
    train_set, val_set = [], []
    nodule_cases, nonodule_cases = [], []
    for file in all_files:
        nod_type = file.split('_')[0]
        if nod_type == 'nod':
            nodule_cases.append(file)
        elif nod_type == 'nonod':
            nonodule_cases.append(file)
        else:
            raise ValueError('Unknown Type Found!')
    nodule_train, nodule_val = train_test_split(nodule_cases, test_size=0.15)
    nonodule_train, nonodule_val = train_test_split(nonodule_cases, test_size=0.15)
    train_set.extend(nodule_train)
    train_set.extend(nonodule_train)
    val_set.extend(nodule_val)
    val_set.extend(nonodule_val)
    random.shuffle(train_set)
    random.shuffle(val_set)
    write_txt_file(train_set, 'UCLA-Nas-train_nodules', path_to_save_txt)
    write_txt_file(val_set, 'UCLA-Nas-val_nodules', path_to_save_txt)

def merge_cases(path_to_cnd, path_to_save_merged):
    cnds = [cnd for cnd in os.listdir(path_to_cnd) if cnd != 'merged']
    for each_cnd in cnds:
        files = os.listdir(os.path.join(path_to_cnd, each_cnd))
        for each_file in files:
            src = os.path.join(path_to_cnd, each_cnd, each_file)
            dest = os.path.join(path_to_save_merged, '{}_cnd-{}.nrrd'.format(each_file.split('.nrrd')[0], each_cnd))
            shutil.copy(src, dest)
    print('All files copied!')

def generate_specific_uids(path_to_data):
    mapping_uids = {}
    for file in os.listdir(path_to_data):
        if file.endswith('.nrrd'):   
            condition = file.split('.nrrd')[0].split('_cnd-')[-1]
            if condition not in mapping_uids:
                mapping_uids[condition] = []
            if file not in mapping_uids[condition]:
                mapping_uids[condition].append(file)
    return mapping_uids

def generate_merged_train_test_uid(path_to_data, path_to_save_merged_txt, external_test):
    mapped_cnd = generate_specific_uids(path_to_data)
    train_set, test_set = [], []
    with open(external_test, 'r') as f:
        lines = f.readlines()
        test_cases = [l.rstrip() for l in lines]
    for cnd in mapped_cnd:
        all_files = mapped_cnd[cnd]
        test_cnd_cases = [file.split('.nrrd')[0]+'_cnd-{}.nrrd'.format(cnd) for file in test_cases]
        all_files = list(set(all_files)-set(test_cnd_cases))
        train_set.extend(all_files)
        test_set.extend(test_cnd_cases)
    print('Total train set samples:', len(train_set))
    print('Total test set samples:', len(test_set))
    random.shuffle(train_set)
    random.shuffle(test_set)
    write_txt_file(train_set, 'UCLA-Nas-merged_train_nodules', path_to_save_merged_txt)
    write_txt_file(test_set, 'UCLA-merged_test_nodules', path_to_save_merged_txt)

def check_size(vol_path, train_nods, path_to_save_merged_txt):
    updated_train = []
    files_skipped = 0
    with open(train_nods, 'r') as file:
        train_nodules = file.readlines()
        train_nodules = [line.strip() for line in train_nodules]
    for nod in train_nodules:
        img_path = os.path.join(vol_path, nod)
        data, header = nrrd.read(img_path)
        if data.shape[0] != 64 or data.shape[1] != 64 or data.shape[2] != 16:
            print('Skipping train file {} ...'.format(nod))
            files_skipped += 1
        else:
            updated_train.append(nod)
    random.shuffle(updated_train)
    print('{} files skipped'.format(files_skipped))
    write_txt_file(updated_train, 'UCLA-merged_train_nodules_v1', path_to_save_merged_txt)


if __name__ == '__main__':
    path_to_files = '/datasets/UCLA-Nas-NoduleVolume/unnormalized/k2_d100_st1.0'
    external_test = '/datasets/UCLA-Nas-NoduleVolume/uids/UCLA-test_uids.txt'
    path_to_save_txt = '/datasets/UCLA-Nas-NoduleVolume/uids'
    # create_train_val_test(path_to_files, path_to_save_txt, external_test)
    # =====================================================================
    path_to_cnd = '/datasets/UCLA-Nas-NoduleVolume/unnormalized'
    path_to_save_merged = '/datasets/UCLA-Nas-NoduleVolume/unnormalized/merged/data'
    # merge_cases(path_to_cnd, path_to_save_merged)
    # =====================================================================
    path_to_save_merged_txt = '/datasets/UCLA-Nas-NoduleVolume/unnormalized/merged'
    # generate_merged_train_test_uid(path_to_save_merged, path_to_save_merged_txt, external_test)
    # =====================================================================
    # check_size(path_to_save_merged, '/datasets/UCLA-Nas-NoduleVolume/unnormalized/merged/UCLA-Nas-merged_train_nodules.txt', path_to_save_merged_txt)
