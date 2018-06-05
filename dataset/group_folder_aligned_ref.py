""" group_folder.py groups mask images into folders. This script does
the same for board images.
"""

import os
import shutil

base_dir = "/home/ubuntu/datasets/ttrfull1"
input_dir = base_dir + "/group"
output_dir = base_dir + "/group_aligned_ref"
ref_dir = base_dir + "/aligned"

num_dirs = 105

def copy_files(src_dir, dst_dir):
    src_files = os.listdir(src_dir)
    for file_name in src_files:
        file_path = src_dir + "/" + file_name
        shutil.copy(src_dir, dst_dir)

for dir_num in range(105):
    # src and dst dir paths
    src_dir = input_dir + "/" + str(dir_num)
    dst_dir = output_dir + "/" + str(dir_num)
    
    # create the dst dir
    os.makedirs(dst_dir)
    
    # list of files to copy
    file_names = os.listdir(src_dir)
    
    # copy from ref to dst
    for file_name in file_names:
        src_file_path = ref_dir + "/" + file_name
        dst_file_path = dst_dir + "/" + file_name
        shutil.copy(src_file_path, dst_file_path)

