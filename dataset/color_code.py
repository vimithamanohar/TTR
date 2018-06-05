""" Name edge images and masks according to their color

Name edge images and masks according to their color. All red images
were taken before all green images which were taken before all black
images, .... So, just sorting images by name inside a group folder
will sort them by color.
"""

import os
import shutil

base_path = "/home/ubuntu/datasets/ttrfull1"
input_masks_base_path = base_path + "/" + "group_masks_corrected"
input_boards_base_path = base_path + "/" + "group_aligned_corrected"
output_masks_base_path = base_path + "/" + "color_coded_masks"
output_boards_base_path = base_path + "/" + "color_coded_boards"

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

for board_num in range(100):
    input_boards_path = input_boards_base_path + "/" + str(board_num)
    files_list = os.listdir(input_boards_path)
    files_list.sort()
    
    color_file_names = ("red.jpg", "green.jpg", "black.jpg", "blue.jpg", "yellow.jpg")
    
    input_masks_path = input_masks_base_path + "/" + str(board_num)
    input_boards_path = input_boards_base_path + "/" + str(board_num)
    output_masks_path = output_masks_base_path + "/" + str(board_num)
    output_boards_path = output_boards_base_path + "/" + str(board_num)
    
    create_dir(output_masks_path)
    create_dir(output_boards_path)
    
    for i in range(5):
        # copy mask
        src_path = input_masks_path + "/" + files_list[i]
        dst_path = output_masks_path + "/" + color_file_names[i]
        shutil.copy(src_path, dst_path)
        
        # copy board
        src_path = input_boards_path + "/" + files_list[i]
        dst_path = output_boards_path + "/" + color_file_names[i]
        shutil.copy(src_path, dst_path)

