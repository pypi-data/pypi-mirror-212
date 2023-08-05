import pandas as pd
from evaluationScript.noduleCADEvaluationLUNA16 import noduleCADEvaluation
import os


if __name__ == '__main__':
    annotations_filename = '/workspace/SANet/data/ucla_filtered_testUID_70_30_split_annotGT.csv'
    val_path = '/workspace/SANet/data/ucla_filtered_testUID_70_30_split_pids.txt'
    res_path = './results_normCnd/SNGAN/k1_d100_st1/res/95/FROC/results.csv'


    noduleCADEvaluation(annotations_filename, res_path, val_path, os.path.join('./', 'tmp_res'), return_dict=False)


