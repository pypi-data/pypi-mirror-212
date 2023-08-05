import os


def rename_files(file_path):
    for ld in os.listdir(file_path):
        file_ext = ld.split(".")[-1]
        file_name = ld.split("_")[0] + "." + file_ext 
        os.rename(os.path.join(file_path, ld), os.path.join(file_path, file_name))
    print('ALL FILES RENAMED!')

def write_uids():
    ext = ".h5"
    h5_file_path = "/aapm_data/aapm_3d_lowdose_testset"
    file = open('aapm_uids.txt', 'w')
    for arg in os.listdir(h5_file_path):
        if arg.endswith(ext):
            name = arg.split(ext)[0]
            file.write(name + "\n")
    file.close()


if __name__ == "__main__":
    write_uids()
    # low_dose_path = "/aapm_data/aapm_3d_lowdose_testset"
    # full_dose_path = "/aapm_data/aapm_3d_fulldose_testset"
    # rename_files(full_dose_path)