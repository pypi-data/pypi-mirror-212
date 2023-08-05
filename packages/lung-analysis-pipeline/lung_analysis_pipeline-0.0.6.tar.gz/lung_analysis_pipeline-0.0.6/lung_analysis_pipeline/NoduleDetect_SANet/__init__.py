import torch 
import pkg_resources

from .net.sanet import SANet 
from .config import config
import logging
logger = logging.getLogger('base')


def create_detect_model(opt): 
    # define config 

    # load pre-trained model 
    # path_to_weight = 'model.ckpt'
    # path_to_weight = pkg_resources.resource_filename(__name__, path_to_weight)
    path_to_weight = opt['detection']['model']
    
    checkpoint = torch.load(path_to_weight)
    model = SANet(config)
    model.cuda()
    model.load_state_dict(checkpoint['state_dict'])
    logger.info('Nodule detection model {:s} is created.'.format(model.__class__.__name__)) 

    return model 
