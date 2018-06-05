""" Create board and mask numpy files

During training, it is convinient to not have to read from JPEG files
and decode every single image. We'll convert the images into numpy
arrays and persist in files. We'll read these files directly during
training. 

We'll resize the images to 1012x759 to strike a balance between too
big images that takes too much memory and too small images that could
loose details necessary to recognize successfully.

We'll store only the part of the image that actually contains the graph
"""

import os
import cv2
import imutils
import random
import numpy as np
from matplotlib import pyplot as plt

ttr_base_dir = "/home/ubuntu/datasets/ttr_base/numpy"
output_edges_dir = ttr_base_dir + "/" + "edges"
output_masks_dir = ttr_base_dir + "/" + "masks"

input_base_dir = "/home/ubuntu/datasets/ttrfull1"
input_edges_dir = input_base_dir + "/" + "color_coded_boards"
input_masks_dir = input_base_dir + "/" + "color_coded_masks"

output_width = 1012
output_height = 759

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

for edge_num in range (100):
    colors = ("red.jpg", "green.jpg", "blue.jpg", "black.jpg", "yellow.jpg")
    for color in colors:
        # Read the input edge and mask
        suffix = "/" + str(edge_num) + "/" + color
        img_input_edge = cv2.imread(input_edges_dir + suffix)
        img_input_mask = cv2.imread(input_masks_dir + suffix)
        
        # Resize the edge
        edge = cv2.resize(img_input_edge, (1012, 759), interpolation = cv2.INTER_AREA)
        
        # Resize and convert the mask into binary
        mask = cv2.resize(img_input_mask, (1012, 759), interpolation = cv2.INTER_AREA)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
        
        # Extract the center that has the graph
        cx1 = round(450/4) # 113
        cy1 = round(530/4) # 133
        cx2 = round(3570/4) # 893
        cy2 = round(2420/4) # 605
        mask = mask[cy1:cy2, cx1:cx2]
        edge = edge[cy1:cy2, cx1:cx2]
        
        # Write the edge and mask into files
        edge_output_path = output_edges_dir + suffix.replace("jpg", "npy")
        mask_output_path = output_masks_dir + suffix.replace("jpg", "npy")
        create_dir(os.path.dirname(edge_output_path))
        create_dir(os.path.dirname(mask_output_path))
        np.save(edge_output_path, edge)
        np.save(mask_output_path, mask)

