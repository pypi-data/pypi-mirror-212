import numpy as np
import os
from sklearn.model_selection import KFold


def main(path_to_uids):
    with open(path_to_uids) as f:
        path_to_save_folds = '/'.join(path_to_uids.split('/')[:-1])
        print('Saving folds uids at:', path_to_save_folds)
        lines = np.array(f.readlines())
        cv = KFold(n_splits=5, random_state=1, shuffle=True)
        for loop_idx, (train_index, valid_index) in enumerate(cv.split(lines)):
            fold_name_train = os.path.join(path_to_save_folds, "ucla_train_uids_fold_{}.txt".format(loop_idx+1))
            fold_name_validation = os.path.join(path_to_save_folds, "ucla_valid_uids_fold_{}.txt".format(loop_idx+1))
            train_uids = lines.take(train_index).tolist()
            validation_uids = lines.take(valid_index).tolist()
            # write out uids
            with open(fold_name_train, 'w') as train_file:
                train_file.write(''.join(train_uids))
            with open(fold_name_validation, 'w') as valid_file:
                valid_file.write(''.join(validation_uids))
    print('All folds saved!')


if __name__ == "__main__":
    path_to_uids = "/workspace/NormGAN/uids_to_split/ucla_all_uids.txt" 
    main(path_to_uids)