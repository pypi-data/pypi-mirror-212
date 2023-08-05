from setting import parse_opts 
from datasets.lungCT import LIDC_CT
from model import generate_model
import torch
from torch import nn
import numpy as np
from torch.utils.data import DataLoader
import torch.nn.functional as F
import sys
import os
import numpy as np
from tqdm import tqdm
# from utils.logger import log
from build_unet_model import UNet


def getIoU(y_true, y_pred):
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.logical_and(y_true_f, y_pred_f).sum()
    union = np.logical_or(y_true_f, y_pred_f).sum()
    return (intersection + 1) * 1. / (union + 1)


def rescale_img_to_rgb(img):
    img = (img - img.min()) / (img.max() - img.min())
    img *= 255.0
    img = img.astype(np.uint8)
    return img


def test(test_loader, model):
    batches_per_epoch_test = len(test_loader)
    print('Test: {} batches per epoch'.format(batches_per_epoch_test))
    total_ious = 0.0

    with torch.no_grad():
        model.eval()
        for volumes, label_masks in tqdm(test_loader):
            volumes = volumes.cuda()
            out_masks = model(volumes)
            output_prob = torch.sigmoid(out_masks).detach().cpu().numpy()
            output_prob_thresh = (output_prob > 0.5) * 1
            iou = getIoU(label_masks, output_prob_thresh)
            total_ious += iou
        print('IoU over test set:', total_ious/len(test_loader))


if __name__ == '__main__':
    # settting
    sets = parse_opts()

    os.environ["CUDA_VISIBLE_DEVICES"]='3'   
    model = UNet(in_nc=1, out_nc=1, nf=64).cuda()
    model = nn.DataParallel(model)

    # getting model
    path_to_weight = './trails_UNet/models/UNet_epoch_106_best_weight_0.646983.pth.tar'
    checkpoint = torch.load(path_to_weight)
    model.load_state_dict(checkpoint['state_dict'])
    test_dataset = LIDC_CT('Test', sets.data_root, sets.img_test_list, sets, transforms=None)
    #  data_root: setting.py -- data directory 
    # sets.img_test_list: test_lidc_subset. path to ct and path to mask. each line is a new instance. 
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False, num_workers=sets.num_workers, pin_memory=False, drop_last=False)

    test(test_loader, model)

# right now is not saving anything. output_thread_vol 
# specify parameters in setting.py 



