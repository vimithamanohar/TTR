""" masks.py does math operations on images and computes a mask.
However because of small movements in camera, there will be tiny
white regions all over the map. These are not areas where the images
truely differ. These need to be removed to be able to use these images
to generate boards.

This module computes contours in the mask and removes contours with
area less than a certain threshold. 
"""

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

base_dir = "/home/ubuntu/datasets/ttrfull1"
input_dir = base_dir + "/masks"
output_dir = base_dir + "/contour_masks"

file_list = [f for f in os.listdir(input_dir)]
file_list.sort()

def get_contour_mask(input_file_path):
    img = cv2.imread(input_file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    black = np.zeros(img.shape, dtype=np.uint8)
    
    indices = []
    for idx, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 2000:
            indices.append(idx)

    for idx in indices:
        cv2.drawContours(black, contours, idx, (255,255,255), -1)    
        
    return black

for file_name in file_list:
    input_file_path = input_dir + "/" + file_name
    contour_mask = get_contour_mask(input_file_path)
    
    output_file_path = output_dir + "/" + file_name
    cv2.imwrite(output_file_path, contour_mask)

