import os
import random
from multiprocessing import Pool

import mxnet as mx
import mxnet.ndarray as nd

import cv2
import numpy as np
from matplotlib import pyplot as plt

class TTRData(object):
    def __init__(self, data_base_dir):
        self.colors = ("black.npy", "blue.npy", "green.npy", "red.npy", "yellow.npy")

        # Load all the edges and masks in memory
        self.edges = []
        self.masks = []
        for board_num in range(100):
            for color in self.colors:
                suffix = "/%s/%s" % (str(board_num), color)
                self.edges.append(np.load(data_base_dir + "/edges" + suffix))
                self.masks.append(np.load(data_base_dir + "/masks" + suffix))                                                        

        # Coordinates to extract the inner rectangle that has the graph
        self.cx1 = round(450/4)
        self.cy1 = round(530/4)
        self.cx2 = round(3570/4)
        self.cy2 = round(2420/4)

        # Load the blank board
        self.blank_board = cv2.imread(data_base_dir + "/blank_board.jpg")
        self.board_center = self.extract_center(self.blank_board)
        
    def overlay_image(self, background, foreground, mask):
        mask_inv = cv2.bitwise_not(mask)
        background = cv2.bitwise_and(background, background, mask=mask_inv)
        foreground = cv2.bitwise_and(foreground, foreground, mask=mask)
        return cv2.add(background, foreground)

    def extract_center(self, img):
        return img[self.cy1:self.cy2, self.cx1:self.cx2]

    def replace_center(self, base, overlay):
        base[self.cy1:self.cy2, self.cx1:self.cx2] = overlay
        return base    

    def get(self, edges=None):
        
        if edges == None:
            edges = [i for i in range(100)]
        
        board = np.array(self.board_center)
        label = np.zeros(100)

        # Add hundred random edges to board. Each edge can either be of one of 
        # the five colors or be empty.
        for i in range(len(edges)):
            
            # pick one of the five colors in random
            # zero is unfilled. 1 to 5 are colors as ordered in self.colors
            color_choice = random.randint(0, 5)
            
            # Add label
            label[edges[i]] = color_choice
            
            if color_choice == 0:
                # leave this edge unfilled
                continue
            
            # Add the edge to the board
            edge_image = self.edges[edges[i]*5 + color_choice-1]
            mask_image = self.masks[edges[i]*5 + color_choice-1]
            board = self.overlay_image(board, edge_image, mask_image)
            
        full_empty_board = np.array(self.blank_board)
        full_board = self.replace_center(full_empty_board, board)
        
        return full_board, label

ttr_data = TTRData("/home/ubuntu/datasets/ttr_base")

def get_one(x):
    return ttr_data.get()

batch_size = 8
pool = Pool(batch_size)
data_list = pool.map(get_one, [None for i in range(batch_size)])

images_dir = "/home/ubuntu/datasets/ttr_boards/boards"
label_path = "/home/ubuntu/datasets/ttr_boards/labels.lst"

def write_to_disk(image_index, image, label, label_file):
    image_path = "%s/%d.jpg" % (images_dir, image_index)
    cv2.imwrite(image_path, image)
    label = [str(i) for i in label]
    tab_seperated_labels = "\t".join(label)
    label_file.write("%d\t%s\tboards/%d.jpg\n" % (image_index, tab_seperated_labels, image_index))
    
total_images = 80
batches = total_images // batch_size

with open(label_path, "w") as label_file:
    for b in range(batches):
        data_list = pool.map(get_one, [None for i in range(batch_size)])
        for i in range(batch_size):
            image = data_list[i][0]
            label = data_list[i][1]
            image_index = b * batch_size + i
            write_to_disk(image_index, image, label, label_file)

