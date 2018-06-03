""" Compute mask for each edge image

Compute mask for each edge image. Area covered by the edge must be
white on the map. Areas not covered by the edge must be black. Once we
have this mask, we can place an edge on a blank board with the
following operation:

    board_with_edge = board_without_edge + mask * edge_image

where,
- board_without_edge is board without a certain edge (E) covered. State
  of other edges don't matter.
- board_with_edge is board with edge E placed on it. State of other
  edges don't matter.
- edge_image is board with only edge E covered.
- mask is mask computed from edge_image using this module.
"""

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

base_dir = "/home/ubuntu/datasets/ttrfull1"
input_dir = base_dir + "/aligned"
masks_dir = base_dir + "/masks"

def get_mask(none_image_path, top_image_path):
    none_image = cv2.imread(none_image_path)
    top_image = cv2.imread(top_image_path)

    diff = cv2.absdiff(top_image, none_image)
    
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    
    gblur = cv2.medianBlur(gray_diff,5)
    
    ret, threshold_img = cv2.threshold(gblur, 30, 255, cv2.THRESH_BINARY)
    
    return threshold_img

file_list = [f for f in os.listdir(input_dir)]
file_list.sort()

none_image_path = base_dir + "/" + "none_aligned.jpg"

for file_name in file_list:
    input_file_path = input_dir + "/" + file_name
    mask = get_mask(none_image_path, input_file_path)
    
    output_path = masks_dir + "/" + file_name
    cv2.imwrite(output_path, mask)

