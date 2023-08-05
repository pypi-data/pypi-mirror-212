import os
import json
import numpy as np
import nrrd
import pandas as pd


def seperate_cnds(uids_path):
    with open(uids_path, 'r') as f:
        lines = f.readlines()
        uids = [l.rstrip() for l in lines]
    master_dict = {}
    for case in uids:
        cnd = '_'.join(case.split('_')[1:])
        if cnd not in master_dict:
            master_dict[cnd] = []
        master_dict[cnd].append(case)
    # check if different conditions have same lengths
    assert len(master_dict['k1_d10_st1']) == len(master_dict['k1_d25_st1']) == len(master_dict['k1_d100_st1'])
    return master_dict


def generate_nodule_csv(annot_file, uids_path, dict_to_write):
    # read uids file
    uids = seperate_cnds(uids_path)['k1_d100_st1']
    # read annotation file
    with open(annot_file, 'r') as file:
        nodule_annot = json.load(file)
        print('Number of cases in annot file:', len(nodule_annot))
    num_nodule = 0
    num_cases_with_nodules = 0
    filenames_to_write = []
    # generate bbox
    for uid in uids:
        filename = uid.split('_')[0]
        if filename in nodule_annot:
            filenames_to_write.append(filename)
            num_cases_with_nodules += 1
            annot = nodule_annot[filename]
            num_nodule += len(annot)
            for cur_idx, each_nod in enumerate(annot):
                if len(each_nod) == 2:
                    center, diam = each_nod
                elif len(each_nod) == 1:
                    center = each_nod
                    diam = None
                else:
                    raise ValueError('Unknown length of annot found!')

                # generate bbox
                x, y, z = center
                x, y, z = int(x), int(y), int(z)
                zs, ze, ys, ye, xs, xe = z-box_size//2, z+box_size//2, y-box_size//2, y+box_size//2, x-box_size//2, x+box_size//2
                # write to dict
                dict_to_write['pid'].append(filename)
                dict_to_write['nodule_class'].append(nodule_class)
                dict_to_write['xmin'].append(xs)
                dict_to_write['xmax'].append(xe)
                dict_to_write['ymin'].append(ys)
                dict_to_write['ymax'].append(ye)
                dict_to_write['zmin'].append(zs)
                dict_to_write['zmax'].append(ze)
                dict_to_write['nodule_id'].append(cur_idx)
                dict_to_write['center_x'].append(x)
                dict_to_write['center_y'].append(y)
                dict_to_write['center_z'].append(z)
                if diam:
                    csv_dict['diameter'].append(diam)
                else:
                    csv_dict['diameter'].append(-1)
                dict_to_write['x_size'].append(box_size)
                dict_to_write['y_size'].append(box_size)

    print('{}/{} cases have nodules'.format(num_cases_with_nodules, len(uids)))
    print('Total number of nodules:', num_nodule)
    return dict_to_write, filenames_to_write


if __name__ == '__main__':
    box_size = 50
    nodule_class = 'GG-Nod'
    header = ['pid', 'nodule_class', 'xmin', 'xmax', 'ymin', 'ymax', 'zmin', 'zmax', 'nodule_id', 'center_x',\
            'center_y', 'center_z', 'diameter', 'x_size', 'y_size']
    csv_dict = {}
    for head in header:
        csv_dict[head] = []
    test_set_annot = '/datasets/nodule_annotations/ucla_annotations_filtered.json'
    UIDS = '/datasets/uids/70-30_split/ucla_testUID_70_30_split.txt'
    
    # mains
    master_dict, filenames = generate_nodule_csv(test_set_annot, UIDS, csv_dict)
    # df = pd.DataFrame(master_dict)
    # # write data
    # df.to_csv('sanet_testUID_70_30_split_annotGT.csv', index=False)
    # with open("sanet_testUID_70_30_split_pids.txt", "w") as outfile:
    #     outfile.write("\n".join(filenames))

