from setting import parse_opts 
from datasets.brains18 import BrainS18Dataset
from datasets.lungCT import LIDC_CT
from model import generate_model
import torch
import numpy as np
from torch.utils.data import DataLoader
import torch.nn.functional as F
from scipy import ndimage
from torch import nn
import nibabel as nib
import sys
import cv2
import os
import numpy as np
import nibabel
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


def test(data_loader, model, img_names, sets):
    masks = []
    model.eval() # for testing 
    for batch_id, batch_data in enumerate(data_loader):
        # forward
        volume = batch_data
        if not sets.no_cuda:
            volume = volume.cuda()
        with torch.no_grad():
            probs = model(volume)
            probs = F.softmax(probs, dim=1)

        # resize mask to original size
        [batchsize, _, mask_d, mask_h, mask_w] = probs.shape
        data = nib.load(os.path.join(sets.data_root, img_names[batch_id]))
        data = data.get_data()
        [depth, height, width] = data.shape
        mask = probs[0]
        scale = [1, depth*1.0/mask_d, height*1.0/mask_h, width*1.0/mask_w]
        mask = ndimage.interpolation.zoom(mask, scale, order=1)
        mask = np.argmax(mask, axis=0)        
        masks.append(mask)
    return masks

def resize_data__(data):
    """
    Resize the data to the input size
    """ 
    [height, width, depth] = data.shape
    # scale = [self.input_D*1.0/depth, self.input_H*1.0/height, self.input_W*1.0/width] 
    scale = [64*1.0/height, 64*1.0/width, 32*1.0/depth]  
    data = ndimage.interpolation.zoom(data, scale, order=0)
    return data



if __name__ == '__main__':
    # settting
    sets = parse_opts()

    # os.environ["CUDA_VISIBLE_DEVICES"]=str(sets.gpu_id[0])   
    # model = UNet(in_nc=1, out_nc=1, nf=64).cuda()
    # model = nn.DataParallel(model)

    model, _ = generate_model(sets)

    # getting weights
    path_to_weight = './trails_ResNet-34/models/resnet_34_epoch_187_best_weight_0.372868.pth.tar'   
    checkpoint = torch.load(path_to_weight)
    model.load_state_dict(checkpoint['state_dict'])
    print('Model weights loaded!')

    # load image and mask
    img_path = nibabel.load('./data/data_lidc/segmentation/patches/images/LIDC-IDRI-0014-265-nod-345-71.nii.gz')
    img = img_path.get_fdata()
    img = rescale_img_to_rgb(img)

    mask_path = nibabel.load('./data/data_lidc/segmentation/patches/labels/LIDC-IDRI-0014-265-nod-345-71.nii.gz')
    mask = mask_path.get_fdata()

    img = resize_data__(img)
    cv2.imwrite('LIDC-IDRI-0014-265-nod-345-71.png', img[:,:,16])
    mask = resize_data__(mask)

    img = (img - img.mean()) / img.std()
    img = torch.from_numpy(np.expand_dims(np.expand_dims(img.transpose(2,0,1), axis=0), axis=0)).type(torch.FloatTensor)
    label_masks = torch.from_numpy(np.expand_dims(np.expand_dims(mask.transpose(2,0,1), axis=0), axis=0)).type(torch.FloatTensor)

    print('img shape:', img.shape)
    print('GT mask shape:', label_masks.shape)
    
    with torch.no_grad():
        model.eval()
        img = img.cuda()
        out_masks = model(img)

        output_prob = torch.sigmoid(out_masks).detach().cpu().numpy()
        output_prob_thresh = (output_prob > 0.5) * 1
        print('Out mask shape:', output_prob_thresh.shape)
        print('Pred unique:', np.unique(output_prob_thresh))

        # resize GT label
        [n, _, d, h, w] = out_masks.shape
        new_label_masks = np.zeros([n, _, d, h, w])
        for label_id in range(n):
            label_mask = label_masks[label_id]
            [ori_c, ori_d, ori_h, ori_w] = label_mask.shape 
            label_mask = np.reshape(label_mask, [ori_d, ori_h, ori_w])
            scale = [d*1.0/ori_d, h*1.0/ori_h, w*1.0/ori_w]
            label_mask = ndimage.interpolation.zoom(label_mask, scale, order=0)
            new_label_masks[label_id, 0] = label_mask
        new_label_masks = torch.tensor(new_label_masks).type(torch.FloatTensor).numpy()
        
        print('Downsampled mask unique:', np.unique(new_label_masks))
        iou = getIoU(new_label_masks, output_prob_thresh)
        print('IoU is:', iou)
        
        # print('Resized GT label shape:', new_label_masks.shape)
        # upsample predictions
        [n, _, d, h, w] = label_masks.shape
        [batch, ori_c, ori_d, ori_h, ori_w] = output_prob_thresh.shape
        scale = [d*1.0/ori_d, h*1.0/ori_h, w*1.0/ori_w]
        output_prob_thresh = ndimage.interpolation.zoom(output_prob_thresh[0,0,:,:,:], scale, order=0)

        # iou = getIoU(label_masks, output_prob_thresh)
        # print('IoU is:', iou)

# middle_pd = output_prob_thresh[0,0,16,:,:]
middle_pd = output_prob_thresh[16,:,:]
middle_pd = middle_pd*255.0
middle_pd = middle_pd.astype(np.uint8)
cv2.imwrite('LIDC-IDRI-0014-265-nod-345-71_prediction.png', middle_pd)

# # gt_middle = mask[:,:, 16]
gt_middle = label_masks.numpy()[0, 0, 16, :,:]
gt_middle = gt_middle*255.0
gt_middle = gt_middle.astype(np.uint8)
cv2.imwrite('LIDC-IDRI-0014-265-nod-345-71_gt.png', gt_middle)
