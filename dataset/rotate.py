""" Rotate captured images
Images of the boards were captured with a camera on a selfie stick 
mouted on a table inbetween books to hold the selfie stick. Not the 
perfect setup. Naturally pictures taken weren't perfect either. For a 
start, the pictures had to be rotated to the correct angle. Some had to 
be rotated 90 degree and some had to be rotated 270 degree.
"""

import cv2
import imutils
from matplotlib import pyplot as plt
import os

base_dir = "/home/ubuntu/datasets/ttrfull1"
input_dir = base_dir + "/orig"
output_dir = base_dir + "/rotated"

file_list = [f for f in os.listdir(input_dir)]
file_list.sort()

# first image of the second type
index = file_list.index("IMG_20171218_011549.jpg")

# first list needs to be rotated 90 degree
first_list = file_list[:index]

# second list needs to be rotated 270 degree
second_list = file_list[index:]

def rotate_images(file_list, degree, out_dir):
    for file_name in file_list:
        # read input image
        src_file = input_dir + "/" + file_name
        img = cv2.imread(src_file)
        
        #rotate image
        rotated = imutils.rotate_bound(img, degree)
        
        #write output
        out_file = out_dir + "/" + file_name
        cv2.imwrite(out_file, rotated)

rotate_images(first_list, 90, output_dir)

rotate_images(second_list, 270, output_dir)

