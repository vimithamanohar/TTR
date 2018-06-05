""" After running group_folder_aligned_ref.py, the folder was manually
fixed to remove duplicate images. This script removes the corresponding
masks too.
"""

import os
import shutil

base_dir = "/home/ubuntu/datasets/ttrfull1"
src_dir = base_dir + "/" + "corrected_masks"
ref_base_dir = base_dir + "/" + "group_aligned_corrected"
dst_base_dir = base_dir + "/" + "group_masks_corrected"

for dir_num in range(100):
    ref_dir = ref_base_dir + "/" + str(dir_num)
    for file_name in os.listdir(ref_dir):
        src_path = src_dir + "/" + file_name
        
        # create the dst dir
        dst_dir = dst_base_dir + "/" + str(dir_num)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        
        # copy src to dst
        dst_path = dst_dir + "/" + file_name
        shutil.copy(src_path, dst_path)

