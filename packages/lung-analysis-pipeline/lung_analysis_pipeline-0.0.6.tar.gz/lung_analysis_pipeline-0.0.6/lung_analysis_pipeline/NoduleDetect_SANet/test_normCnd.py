import numpy as np
import torch
import os
import traceback
import time
import nrrd
import sys
import matplotlib.pyplot as plt
import logging
import argparse
import torch.nn.functional as F
from scipy.stats import norm
from torch.utils.data import DataLoader
from tqdm import tqdm
import termcolor
from torch.autograd import Variable
from torch.nn.parallel.data_parallel import data_parallel
from scipy.ndimage.measurements import label
from scipy.ndimage import center_of_mass
from net.sanet import SANet
from dataset.collate import train_collate, test_collate, eval_collate
# from dataset.bbox_reader import BboxReader
from dataset.bbox_reader_UCLA import BboxReader
from config import config
import pandas as pd
import pickle
from evaluationScript.noduleCADEvaluationLUNA16 import noduleCADEvaluation
from utils.prepare_dataset_UCLA import seperate_cnds


this_module = sys.modules[__name__]
os.environ['CUDA_VISIBLE_DEVICES'] = '2'


parser = argparse.ArgumentParser()
parser.add_argument('--net', '-m', metavar='NET', default=config['net'],
                    help='neural net')
parser.add_argument("--mode", type=str, default = 'eval',
                    help="you want to test or val")
parser.add_argument("--weight", type=str, default='./model.ckpt',
                    help="path to model weights to be used")
parser.add_argument("--dicom-path", type=str, default=None,
                    help="path to dicom files of patient")
parser.add_argument("--out-dir", type=str, default=config['out_dir'],
                    help="path to save the results")
parser.add_argument("--test-set-name", type=str, default=config['test_set_name'],
                    help="path to save the results")


def main(cur_model_data_dir, out_dir, cur_cnd):
    args = parser.parse_args()
    logging.basicConfig(format='[%(levelname)s][%(asctime)s] %(message)s', level=logging.INFO)
    if args.mode == 'eval':
        print('Running in eval mode')
        print('Reading data from:', cur_model_data_dir)
        print('Test set name:', test_set_name)
        print('output dir:', out_dir)

        num_workers = 1
        initial_checkpoint = args.weight
        print('Initial checkpoint:', initial_checkpoint)
        net = args.net
        print('Network args:', net)        
        
        net = getattr(this_module, net)(config)
        net = net.cuda()
        termcolor.cprint('Network Instantiated | on CUDA', 'green')
        if initial_checkpoint:
            print('[Loading model from %s]' % initial_checkpoint)
            checkpoint = torch.load(initial_checkpoint)
            epoch = checkpoint['epoch']
            net.load_state_dict(checkpoint['state_dict'])
            print('Model weights loaded!')
        else:
            print('No model weight file specified. Exiting...')
            return None

        save_dir = os.path.join(out_dir, 'res', str(epoch))
        print('Saving dir:', save_dir)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        if not os.path.exists(os.path.join(save_dir, 'FROC')):
            os.makedirs(os.path.join(save_dir, 'FROC'))
    
        dataset = BboxReader(cur_model_data_dir, test_set_name, config, mode='eval', segment_lung=USE_MASK, add_cnd=cur_cnd)
        print('Dataset created')
        test_loader = DataLoader(dataset, batch_size=1, shuffle=False,
                                 num_workers=num_workers, pin_memory=False, collate_fn=train_collate)
        # for i, (input, truth_bboxes, truth_labels) in enumerate(dataset):
        #     print(type(input), input.min(), input.max())
        #     break
        return eval(net, test_loader, save_dir)
    else:
        logging.error('Mode %s is not supported' % (args.mode))


def eval(net, dataset, save_dir=None):
    net.set_mode('eval')
    net.use_rcnn = True

    print('Total # of eval data %d' % (len(dataset)))
    for i, (input, truth_bboxes, truth_labels) in enumerate(dataset):
        try:
            input = Variable(input).cuda()
            print('input on cuda size:', input.shape)
            truth_bboxes = np.array(truth_bboxes)
            truth_labels = np.array(truth_labels)
            pid = dataset.dataset.filenames[i]

            print('[%d] Predicting %s' % (i, pid))

            with torch.no_grad():
                net.forward(input, truth_bboxes, truth_labels)

            detections = net.rpn_proposals.cpu().numpy()
            print('final detections shape:', detections.shape)

            if len(detections):
                detections = detections[:, 1:-1]
                np.save(os.path.join(save_dir, '%s_detections.npy' % (pid)), detections)

            # clear gpu memory
            del input, truth_bboxes, truth_labels
            torch.cuda.empty_cache()

        except Exception as e:
            del input, truth_bboxes, truth_labels
            torch.cuda.empty_cache()
            traceback.print_exc()
            return
   
    print('All detections done!')
    # Generate prediction csv for the use of performning FROC analysis
    res = []
    for pid in dataset.dataset.filenames:
        if os.path.exists(os.path.join(save_dir, '%s_detections.npy' % (pid))):
            detections = np.load(os.path.join(save_dir, '%s_detections.npy' % (pid)))
            detections = detections[:, [3, 2, 1, 4, 0]]
            names = np.array([[pid]] * len(detections))
            res.append(np.concatenate([names, detections], axis=1))
    
    res = np.concatenate(res, axis=0)
    col_names = ['pid','center_x','center_y','center_z','diameter', 'probability']
    eval_dir = os.path.join(save_dir, 'FROC')
    res_path = os.path.join(eval_dir, 'results.csv')
    
    df = pd.DataFrame(res, columns=col_names)
    df.to_csv(res_path, index=False)
    # start evaluating
    if not os.path.exists(os.path.join(eval_dir, 'res')):
        os.makedirs(os.path.join(eval_dir, 'res'))

    annotations_filename = '/workspace/SANet/data/ucla_filtered_testUID_70_30_split_annotGT.csv'
    val_path = '/workspace/SANet/data/ucla_filtered_testUID_70_30_split_pids.txt'
    return noduleCADEvaluation(annotations_filename, res_path, val_path, os.path.join(eval_dir, 'res'), return_dict=True)


if __name__ == '__main__':
    USE_MASK = '/datasets/bodymask/k2_d100_st1.0_lungonly'
    out_dir = './results_normCnd_pred-in-DiamBox'
    test_UIDS = '/datasets/uids/70-30_split/ucla_testUID_70_30_split.txt' # to generate cnds in dataset
    cnds = seperate_cnds(test_UIDS)
    assert len(cnds['k1_d10_st1']) == len(cnds['k1_d25_st1']) == len(cnds['k1_d100_st1'])
    test_set_name = './data/ucla_filtered_testUID_70_30_split_pids.txt' # uids to read from overall test set

    """
    # build path to dataset
    data_dir = {'Unnorm':'/datasets/data_st1.0_merged'}
    norm_cases, excludeCnd = '/norm_data', ['UnNorm']
    for case in os.listdir(norm_cases):
        if case not in excludeCnd:
            model_cls = os.listdir(os.path.join(norm_cases, case))
            for model in model_cls:
                model_name = model.split('-70-30-')[0].split('test_')[-1]
                if (model_name not in data_dir) and (model_name not in excludeCnd):
                    path_to_cases =  os.path.join(norm_cases, case, model, 'merged_cases', 'test_st1.0_norm')
                    assert len(os.listdir(path_to_cases)) == 240, "Number of cases not equal to 240!!"
                    data_dir[model_name] = path_to_cases
    """

    data_dir = {'SNGAN_withCBAM_cand_Attn':'/norm_data/GANs/test_SNGAN_withCandidateAtten-CBAM_70-30-Split_tileStitch-32x64x64_Ref-k2d100/merged_cases/test_st1.0_norm'}
    
    # store resulting output
    if os.path.exists(os.path.join(out_dir, 'FROC_dict_LT.pkl')):
        print('Storing in already existing dictionary!')
        master_dict = pickle.load(open(os.path.join(out_dir, 'FROC_dict_LT.pkl'), "rb"))
    else:
        master_dict = {}

    # run inference
    for model in data_dir:
        print('Processing model:', model)
        master_dict[model] = {}
        for cnd in cnds:
            print('Running condition:', cnd)
            cnd_dir = os.path.join(out_dir, model, cnd)
            if not os.path.exists(cnd_dir):
                os.makedirs(cnd_dir)
            out_result = main(cur_model_data_dir=data_dir[model], out_dir=cnd_dir, cur_cnd=cnd)
            master_dict[model][cnd] = out_result

    with open(os.path.join(out_dir, 'FROC_dict_LT_v1.pkl'), 'wb') as file:
        pickle.dump(master_dict, file)

    """
    for cnd in cnds:
        print('Running condition:', cnd)
        cnd_dir = os.path.join(out_dir, cnd)
        if not os.path.exists(cnd_dir):
            os.makedirs(cnd_dir)
        out_result = main(out_dir=cnd_dir, cur_cnd=cnd)        
        master_dict[cnd] = out_result
    with open(os.path.join(out_dir, 'FROC_dict.pkl'), 'wb') as file:
        pickle.dump(master_dict, file)
    """
    # python test_normCnd.py --weight='./model.ckpt'
