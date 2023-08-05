import numpy as np
import torch
from torch.utils.data import Dataset
import os, imageio
from scipy.ndimage import zoom
import warnings
from scipy.ndimage.interpolation import rotate
import scipy
import math
import time
import nrrd
import pandas as pd
import SimpleITK as sitk
import h5py
import json
from utils.util import normalize, truncate_HU_uint8


class BboxReader(Dataset):
    def __init__(self, data_dir, set_name, cfg, mode='train', resample_vol=False, segment_lung=False, add_cnd=False):
        print('Inside BboxReader Dataset')
        print('-'*40)
        self.mode = mode
        print('mode:', self.mode)
        self.cfg = cfg
        self.r_rand = cfg['r_rand_crop']
        print('r_rand:', self.r_rand)
        self.augtype = cfg['augtype']
        print('augtype:', self.augtype)
        self.pad_value = cfg['pad_value']
        print('pad_value:', self.pad_value)
        self.data_dir = data_dir
        print('data_dir:', self.data_dir)
        self.stride = cfg['stride']
        print('stride:', self.stride)
        if segment_lung:
            print('Will segment lung')
            self.path_to_mask = segment_lung
        else:
            print('Will not segment lung')
            self.path_to_mask = None

        self.blacklist = cfg['blacklist']
        # print('blacklist:', self.blacklist)
        self.set_name = set_name
        self.need_resample = resample_vol
        self.add_cnd = add_cnd
        # print('set_name:', set_name)
        sizelim = 0
        sizelim2 = 10
        sizelim3 = 20

        labels = []
        with open(self.set_name, "r") as f:
            self.filenames = f.read().splitlines()

        if mode != 'test':
            self.filenames = [f for f in self.filenames if (f not in self.blacklist)]
        if self.mode in ['train', 'val']:
            csv_dir = cfg['train_anno']
        else:
            csv_dir = cfg['test_anno']

        # print('csv_dir:', csv_dir)
        annos_all = pd.read_csv(csv_dir)
        # print(annos_all.head())
        # print('-'*40)
        # collecting annotations
        for fn in self.filenames:
            annos = annos_all[annos_all['pid'] == fn]            
            temp_annos = []
            if len(annos) > 0:
                for index in range(len(annos)):
                    anno = annos.iloc[index]
                    temp_annos.append([anno['zmin'], anno['zmax'], anno['ymin'], anno['ymax'], anno['xmin'], anno['xmax']])
            l = np.array(temp_annos)
            if np.all(l==0):
                l=np.array([])
            labels.append(l)

        self.sample_bboxes = labels
        # print('all labels:', self.sample_bboxes)
        if self.mode in ['train', 'val']:
            self.bboxes = []
            for i, l in enumerate(labels):
                if len(l) > 0 :
                    for t in l:
                        self.bboxes.append([np.concatenate([[i],t])])
            self.bboxes = np.concatenate(self.bboxes, axis=0).astype(np.float32)
            # print('self.bboxes:', self.bboxes)
        self.crop = Crop(cfg)

    def __getitem__(self, idx):
        # print('Getting index:', idx)
        t = time.time()
        np.random.seed(int(str(t % 1)[2:7]))  # seed according to time
        is_random_img  = False
        if self.mode in ['train', 'val']:
            if idx >= len(self.bboxes):
                is_random_crop = True
                idx = idx % len(self.bboxes)
                is_random_img = np.random.randint(2)
            else:
                is_random_crop = False
        else:
            is_random_crop = False
        print('is_random_crop', False)

        if self.mode in ['train', 'val']:
            print('Entering in train or val')
            if not is_random_img:
                bbox = self.bboxes[idx]
                filename = self.filenames[int(bbox[0])]
                imgs = np.load(os.path.join(self.data_dir, '%s_zoom.npy' % (filename)))

                # lines = os.listdir(os.path.join(self.data_dir.replace('full', 'img'), filename))
                # lines = sorted(lines)
                # slice_files = [os.path.join(self.data_dir.replace('full', 'img'), filename, s) for s in lines]
                # slices = [imageio.imread(s) for s in slice_files]
                # imgs = np.array(slices)
                # imgs = imgs[np.newaxis, ...]

                bboxes = self.sample_bboxes[int(bbox[0])]
                isScale = self.augtype['scale'] and (self.mode=='train')
                sample, target, bboxes, coord = self.crop(imgs, bbox[1:], bboxes,isScale,is_random_crop)
                if self.mode == 'train' and not is_random_crop:
                     sample, target, bboxes = augment(sample, target, bboxes, do_flip = self.augtype['flip'], 
                                                             do_rotate=self.augtype['rotate'], do_swap = self.augtype['swap'])
            else:
                randimid = np.random.randint(len(self.filenames))
                filename = self.filenames[randimid]
                imgs = np.load(os.path.join(self.data_dir, '%s_zoom.npy' % (filename)))

                # lines = os.listdir(os.path.join(self.data_dir.replace('full', 'img'), filename))
                # lines = sorted(lines)
                # slice_files = [os.path.join(self.data_dir.replace('full', 'img'), filename, s) for s in lines]
                # slices = [imageio.imread(s) for s in slice_files]
                # imgs = np.array(slices)
                # imgs = imgs[np.newaxis, ...]

                bboxes = self.sample_bboxes[randimid]
                isScale = self.augtype['scale'] and (self.mode=='train')
                sample, target, bboxes, coord = self.crop(imgs, [], bboxes,isScale=False,isRand=True)

            if sample.shape[1] != self.cfg['crop_size'][0] or sample.shape[2] != \
                self.cfg['crop_size'][1] or sample.shape[3] != self.cfg['crop_size'][2]:
                print(filename, sample.shape)

            sample = (sample.astype(np.float32)-128)/128
            bboxes = fillter_box(bboxes, self.cfg['crop_size'])
            bboxes = corner_form_to_center_form(bboxes, self.cfg['bbox_border'])
            bboxes = np.array(bboxes)
            truth_labels = bboxes[:, -1]
            truth_bboxes = bboxes[:, :-1]

            return [torch.from_numpy(sample).float(), truth_bboxes, truth_labels]

        if self.mode in ['eval']:
            # print('Mode is in eval')
            filename = self.filenames[idx]
            if self.add_cnd:
                filename_to_read = filename+'_{}'.format(self.add_cnd)
            else:
                filename_to_read = filename

            print('Reading file:', filename_to_read)
            # read file
            if os.path.isfile(os.path.join(self.data_dir, filename_to_read+'.h5')):
                with h5py.File(os.path.join(self.data_dir, filename_to_read+'.h5'), 'r') as file:
                    file_data = file['data'][:,:,:]
                    header = read_config(filename)
            elif os.path.isfile(os.path.join(self.data_dir, filename_to_read+'.nrrd')):
                file_data, header = nrrd.read(os.path.join(self.data_dir, filename_to_read+'.nrrd'))
                file_data = file_data.transpose((2, 1, 0))
            else:
                raise ValueError('File not found with either .h5 or .nrrd extension!...Exiting')

            # numpyImage = np.clip(file_data, 0, 1500.).astype(np.float32)
            if self.need_resample:
                spacing = [header['spacings'][2], header['spacings'][0], header['spacings'][1]]
                file_data, _ = resample_vol(file_data, orig_spacing=spacing)
                # print('resample shape:', file_data.shape)
                # print('min-max:', file_data.min(), file_data.max())

            numpyImage = bound_image(file_data).astype(np.float32)
            # print('after bound:', numpyImage.min(), numpyImage.max())
            numpyImage /= 1500.0
            numpyImage *= 255.0
            numpyImage = numpyImage.astype(np.uint8)
            print(numpyImage.shape, numpyImage.min(), numpyImage.max())
            if self.path_to_mask:
                with h5py.File(os.path.join(self.path_to_mask, filename+'.h5'), 'r') as mask_file:
                    mask_data = mask_file['data'][:,:,:]
                coords = np.where(mask_data == 0)
                numpyImage[coords] = 0

            image = pad2factor(numpyImage)
            image = np.expand_dims(image, 0)
            bboxes = self.sample_bboxes[idx]

            bboxes = corner_form_to_center_form(bboxes, self.cfg['bbox_border'])
            bboxes = np.array(bboxes)
            truth_labels = bboxes[:, -1]
            truth_bboxes = bboxes[:, :-1]

            input = normalize(image.astype(np.float32))
            # input = (image.astype(np.float32) - 128.) / 128.
            return [torch.from_numpy(input).float(), truth_bboxes, truth_labels]


    def __len__(self):
        if self.mode == 'train':
            return int(len(self.bboxes) / (1-self.r_rand))//self.cfg['batch_size']*self.cfg['batch_size']
        elif self.mode =='val':
            return len(self.bboxes)//self.cfg['batch_size']*self.cfg['batch_size']
        else:
            return len(self.filenames)


"""
Used only for '.h5' files that have header information in json file
"""
def read_config(json_uid):
    config_path = os.path.join('/datasets/reference/k2_d100_st1/', json_uid+'.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    meta_data = {}
    meta_data['Spacing'] = [float(i) for i in config['Spacing'].split()]
    meta_data['Orientation'] = [float(i) for i in config['Orientation'].split()] 
    meta_data['Origin'] = [float(i) for i in config['Origin'].split()]
    header = {'units': ['mm', 'mm', 'mm'], 'spacings': meta_data['Spacing']} 
    return header

def bound_image(img, lower_bound=0, upper_bound=1500, shift_pixels=0):
    image_data = img.astype('float32')
    image_data[image_data < lower_bound] = lower_bound # Sets all values less than -1000 as -1000
    image_data[image_data > upper_bound] = upper_bound # Sets all values greater than 500 as 500
    shifted_pixels = image_data + shift_pixels
    shifted_pixels = shifted_pixels.astype(np.int16)
    return shifted_pixels

def resample_vol(image, orig_spacing, new_spacing=[1,1,1]):
    # Determine current pixel spacing
    spacing = np.array(orig_spacing)
    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor
    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
    return image, new_spacing


def corner_form_to_center_form(boxes, border):
    # print('converting bbox for corner to center')
    # print('bboxes are:', boxes)
    # print('border:', border)
    bboxes = []
    for box in boxes:
        """
        print('[({}+{})/2., ({}+{})/2., ({}+{})/2., ({}-{}+1+{}), ({}-{}+1+{}), ({}-{}+1+{})]'.format(box[0], box[1], box[2], box[3],
                                                                                        box[4], box[5], box[1], box[0], border,
                                                                                        box[3], box[2], border,
                                                                                        box[5], box[4], border))
        """
        bboxes.append([(box[0] + box[1]) / 2.,
                       (box[2] + box[3]) / 2.,
                       (box[4] + box[5]) / 2.,
                       box[1] - box[0] + 1 + border,
                       box[3] - box[2] + 1 + border,
                       box[5] - box[4] + 1 + border,
                       1])

    # print('converted boxes:', bboxes)  
    return bboxes

def pad2factor(image, factor=32, pad_value=0):
    # print('Inside pad2factor')
    # print('-'*40)
    depth, height, width = image.shape
    # print('depth, height, width:', depth, height, width)
    d = int(math.ceil(depth / float(factor))) * factor
    # print("d = int(math.ceil({}/{})) * {} = {}".format(depth, factor, factor, d))
    h = int(math.ceil(height / float(factor))) * factor
    # print("h = int(math.ceil({}/{})) * {} = {}".format(height, factor, factor, h))
    w = int(math.ceil(width / float(factor))) * factor
    # print("w = int(math.ceil({}/{})) * {} = {}".format(width, factor, factor, w))

    pad = []
    pad.append([0, d - depth])
    pad.append([0, h - height])
    pad.append([0, w - width])
    # print('adding pad: [{}-{}, {}-{}, {}-{}] = [{}, {}, {}]'.format(d, depth, h, height, w, width, d-depth, h-height, w-width))

    image = np.pad(image, pad, 'constant', constant_values=pad_value)
    return image


def fillter_box(bboxes, size):
    res = []
    for box in bboxes:
        if np.all(box[:6] > 0) and np.all(box[:6]  < size[0]):
            res.append(box)
    return np.array(res)

def augment(sample, target, bboxes, do_flip = True, do_rotate=True, do_swap = True):
    #  angle1 = np.random.rand()*180
    if do_rotate:
        validrot = False
        counter = 0
        while not validrot:
            newtarget = np.copy(target)
            angle1 = np.random.rand()*180
            size = np.array(sample.shape[2:4]).astype('float')
            rotmat = np.array([[np.cos(angle1/180*np.pi),-np.sin(angle1/180*np.pi)],[np.sin(angle1/180*np.pi),np.cos(angle1/180*np.pi)]])
            newtarget[1:3] = np.dot(rotmat,target[1:3]-size/2)+size/2
            if np.all(newtarget[:3]>target[3]) and np.all(newtarget[:3]< np.array(sample.shape[1:4])-newtarget[3]):
                validrot = True
                target = newtarget
                sample = rotate(sample,angle1,axes=(2,3),reshape=False)
                for box in bboxes:
                    box[1:3] = np.dot(rotmat,box[1:3]-size/2)+size/2
            else:
                counter += 1
                if counter ==3:
                    break
    if do_swap:
        if sample.shape[1]==sample.shape[2] and sample.shape[1]==sample.shape[3]:
            axisorder = np.random.permutation(3)
            sample = np.transpose(sample,np.concatenate([[0],axisorder+1]))
            target[:3] = target[:3][axisorder]
            bboxes[:,:3] = bboxes[:,:3][:,axisorder]

    if do_flip:
        # flipid = np.array([np.random.randint(2),np.random.randint(2),np.random.randint(2)])*2-1
        flipid = np.array([1,np.random.randint(2),np.random.randint(2)])*2-1
        sample = np.ascontiguousarray(sample[:,::flipid[0],::flipid[1],::flipid[2]])
        # for ax in range(3):
        #     if flipid[ax]==-1:
        #         target[ax] = np.array(sample.shape[ax+1])-target[ax]
        #         bboxes[:,ax]= np.array(sample.shape[ax+1])-bboxes[:,ax]
        for i in range(3):
            if flipid[i]==-1:
                tem = [0, 2, 4]
                ax = tem[i]
                target[ax] = np.array(sample.shape[i+1])-target[ax]
                bboxes[:,ax]= np.array(sample.shape[i+1])-bboxes[:,ax]
                target[ax+1] = np.array(sample.shape[i + 1]) - target[ax+1]
                bboxes[:, ax+1] = np.array(sample.shape[i + 1]) - bboxes[:, ax+1]
    return sample, target, bboxes

class Crop(object):
    # print('Inside Crop Class')
    # print('-'*40)
    def __init__(self, config):
        self.crop_size = config['crop_size']
        self.bound_size = config['bound_size']
        self.stride = config['stride']
        self.pad_value = config['pad_value']
    def __call__(self, imgs, target, bboxes,isScale=False,isRand=False):
        if isScale:
            radiusLim = [8.,120.]
            scaleLim = [0.75,1.25]
            scaleRange = [np.min([np.max([(radiusLim[0]/target[3]),scaleLim[0]]),1])
                         ,np.max([np.min([(radiusLim[1]/target[3]),scaleLim[1]]),1])]
            scale = np.random.rand()*(scaleRange[1]-scaleRange[0])+scaleRange[0]
            crop_size = (np.array(self.crop_size).astype('float')/scale).astype('int')
        else:
            crop_size=self.crop_size
        bound_size = self.bound_size
        target = np.copy(target)
        bboxes = np.copy(bboxes)

        start = []
        for i in range(3):
            # start.append(int(target[i] - crop_size[i] / 2))
            if not isRand:
                tem = [0,2,4]
                j = tem[i]
                # r = target[3] / 2
                # s = np.floor(target[i] - r)+ 1 - bound_size
                # e = np.ceil (target[i] + r)+ 1 + bound_size - crop_size[i]
                s = target[j] - bound_size
                e = target[j+1] + bound_size - crop_size[i]
            else:
                s = np.max([imgs.shape[i+1]-crop_size[i]/2,imgs.shape[i+1]/2+bound_size])
                e = np.min([crop_size[i]/2, imgs.shape[i+1]/2-bound_size])
                target = np.array([np.nan,np.nan,np.nan,np.nan])
            if s>e:
                start.append(np.random.randint(e,s))#!
            else:
                start.append(int(target[i])-int(crop_size[i]/2)+np.random.randint(-bound_size/2,bound_size/2))


        normstart = np.array(start).astype('float32')/np.array(imgs.shape[1:])-0.5
        normsize = np.array(crop_size).astype('float32')/np.array(imgs.shape[1:])
        xx,yy,zz = np.meshgrid(np.linspace(normstart[0],normstart[0]+normsize[0],int(self.crop_size[0]/self.stride)),
                           np.linspace(normstart[1],normstart[1]+normsize[1],int(self.crop_size[1]/self.stride)),
                           np.linspace(normstart[2],normstart[2]+normsize[2],int(self.crop_size[2]/self.stride)),indexing ='ij')
        coord = np.concatenate([xx[np.newaxis,...], yy[np.newaxis,...],zz[np.newaxis,:]],0).astype('float32')

        pad = []
        pad.append([0,0])
        for i in range(3):
            leftpad = max(0,-start[i])
            rightpad = max(0,start[i]+crop_size[i]-imgs.shape[i+1])
            pad.append([leftpad,rightpad])
        crop = imgs[:,
            max(start[0],0):min(start[0] + crop_size[0],imgs.shape[1]),
            max(start[1],0):min(start[1] + crop_size[1],imgs.shape[2]),
            max(start[2],0):min(start[2] + crop_size[2],imgs.shape[3])]
        crop = np.pad(crop,pad,'constant',constant_values =self.pad_value)
        for i in range(3):
            tem = [0, 2, 4]
            j = tem[i]
            target[j] = target[j] - start[i]
            target[j + 1] = target[j + 1] - start[i]
            # target[i] = target[i] - start[i]
        for i in range(len(bboxes)):
            for j in range(3):
                tem = [0, 2, 4]
                k = tem[j]
                bboxes[i][k] = bboxes[i][k] - start[j]
                bboxes[i][k + 1] = bboxes[i][k + 1] - start[j]
                # bboxes[i][j] = bboxes[i][j] - start[j]

        if isScale:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                crop = zoom(crop,[1,scale,scale,scale],order=1)
            newpad = self.crop_size[0]-crop.shape[1:][0]
            if newpad<0:
                crop = crop[:,:-newpad,:-newpad,:-newpad]
            elif newpad>0:
                pad2 = [[0,0],[0,newpad],[0,newpad],[0,newpad]]
                crop = np.pad(crop, pad2, 'constant', constant_values=self.pad_value)
            for i in range(6):
                target[i] = target[i]*scale
            for i in range(len(bboxes)):
                for j in range(6):
                    bboxes[i][j] = bboxes[i][j]*scale
        return crop, target, bboxes, coord

