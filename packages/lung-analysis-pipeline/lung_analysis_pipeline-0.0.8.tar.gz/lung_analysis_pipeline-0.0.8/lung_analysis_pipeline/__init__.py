import logging
from lung_analysis_pipeline.utils import util
from lung_analysis_pipeline.options import opt as option
from lung_analysis_pipeline.dataset import create_dataset, create_dataloader
from lung_analysis_pipeline.model_pipeline import ModelPipeline
import argparse
import torch
import os 
from tqdm import tqdm
import logging
logger = logging.getLogger('base')

def run_pipeline(option_path): 
    ## read option file
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-opt', type=str, required=True, help='Path to options JSON file.')
    if not os.path.isfile(option_path):
        raise ValueError('Option file does not exist.')
    opt = option.parse(option_path, is_train=False)
    opt = util.dict_to_nonedict(opt)
    
    ## set up logger
    util.mkdir(opt['output']['log'])
    util.setup_logger(None, opt['output']['log'], 'test.log', level=logging.INFO, screen=False)
    logger = logging.getLogger('base')
    logger.info(util.dict2str(opt))
    torch.backends.cudnn.benchmark = True
    
    ## define data loader 
    dataset_opt = opt['dataset']
    test_set = create_dataset(dataset_opt) # original input option
    test_loader = create_dataloader(test_set, dataset_opt) 
    logger.info('Number of test volumes in [{:s}]: {:d}'.format(dataset_opt['source'], len(test_set)))

    ## create a pipeline 
    pipeline = ModelPipeline(opt)
        
    ## loop over the data loader and run the pipeline on each batch 
    for i, data in enumerate(tqdm(test_loader)):
        # print('Processing case: {}'.format(i))
        logger.info('Processing case: {}'.format(i)) 
        output = pipeline.test(data)
        ## do something to the output, e.g. save it 
        