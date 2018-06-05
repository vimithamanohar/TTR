""" Create a folder for each group and place all files from that group
in the folder. If two edge images cover the same edge, they belong to 
the same group.
"""

import os
import imutils
import cv2
import shutil
import numpy as np
from matplotlib import pyplot as plt

group_file_path = "/home/ubuntu/datasets/ttrfull1/group.txt"
output_dir = "/home/ubuntu/datasets/ttrfull1/group"
input_dir = "/home/ubuntu/datasets/ttrfull1/corrected_masks"

dir_num = -1

with open(group_file_path) as group_file:
    for line in group_file:
        arr = line.split()

        if (len(arr) == 1):
            # create new dir
            dir_num += 1
            new_dir = output_dir + "/" + str(dir_num)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            # copy file to new dir
            src_path = input_dir + "/" + arr[0]
            dst_path = new_dir + "/" + arr[0]
            shutil.copyfile(src_path, dst_path)

        elif (len(arr) == 2):
            # copy file
            file_name = arr[0]
            file_name = file_name[:-1]
            src_path = input_dir + "/" + file_name
            dst_path = output_dir + "/" + str(dir_num) + "/" + file_name
            shutil.copyfile(src_path, dst_path)

