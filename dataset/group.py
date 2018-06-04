""" Group edge images by edge index

Group edge images by edge index. We  do this by computing
IoU (Intersection over Union) for pairs of mask. Edge images with high
IoU are images covering same edge (but different colors).
"""

import os
import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt

def get_array(img_path):
    # Read the image
    mask = cv2.imread(img_path)

    # Convert to black and white
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Convert to black and white binary
    mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)[1]
    
    # crop out the carpet and border of the board
    cx1 = 450
    cy1 = 530
    cx2 = 3570
    cy2 = 2420
    mask = mask[cy1:cy2, cx1:cx2]

    return mask

def get_iou(mask1, mask2):
    # Compute intersection
    intersection = cv2.bitwise_and(mask1, mask2)
    intersection = intersection / 255
    intersection = intersection.sum()
    
    # Compute union
    union = cv2.bitwise_or(mask1, mask2)
    union = union / 255
    union = union.sum()
    
    # Compute and return Intersection Over Union
    iou = intersection/union
    return iou

input_dir = "/home/ubuntu/datasets/ttrfull1/corrected_masks"
file_list = os.listdir(input_dir)
file_list.sort()

images = []

for file in file_list:
    file_path = input_dir + "/" + file
    img = get_array(file_path)
    images.append(img)

n = len(images)
for i in range(n):
    print(file_list[i])
    for j in range(i+1, n):
        mask1 = images[i]
        mask2 = images[j]
        iou = get_iou(mask1, mask2)
        if(iou > 0.50):
            print(file_list[j] + ": " + str(iou))

