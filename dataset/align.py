""" Align images
Images of the boards were captured with a camera on a selfie stick
mouted on a table inbetween books to hold the selfie stick. Not the
perfect setup. Naturally pictures taken weren't perfect either.

One problem is because of small movement in the camera, the location
of the board moves a little in the images. Also, camera turns a little
and we end up capturing the board from different angles.

There are computer vision techniques available to correct these
effects. We'll use OpenCV's ECC image alignment feature to align the
captured images to create images as if the camera never moved while
taking all these images.

This is important because we'll extract the edges from these images and
place them on blank board to create any board configuration we want.
If the images are not aligned, we will end up with blocks misplaced on
board.

Thanks:
https://www.learnopencv.com/image-alignment-ecc-in-opencv-c-python/
"""

from matplotlib import pyplot as plt
import cv2
import numpy as np
import os

def align(reference_image, img_to_align):

    #print("Aligning % and %s" % (reference_image, img_to_align))

    # Create cv2 images
    reference_image =  cv2.imread(reference_image);
    img_to_align =  cv2.imread(img_to_align);

    # Convert images to grayscale
    im1_gray = cv2.cvtColor(reference_image,cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(img_to_align,cv2.COLOR_BGR2GRAY)

    # Find size of image1
    sz = reference_image.shape

    # Define the motion model
    warp_mode = cv2.MOTION_HOMOGRAPHY

    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else :
        warp_matrix = np.eye(2, 3, dtype=np.float32)

    # Specify the number of iterations.
    number_of_iterations = 5000;

    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-6;

    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations,  termination_eps)

    # Run the ECC algorithm. The results are stored in warp_matrix.
    (cc, warp_matrix) = cv2.findTransformECC (im1_gray,im2_gray,warp_matrix, warp_mode, criteria)

    if warp_mode == cv2.MOTION_HOMOGRAPHY :
        # Use warpPerspective for Homography
        im2_aligned = cv2.warpPerspective (img_to_align, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else :
        # Use warpAffine for Translation, Euclidean and Affine
        im2_aligned = cv2.warpAffine(img_to_align, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP);

    return im2_aligned

base_dir = "/home/ubuntu/datasets/ttrfull1"
input_dir = base_dir + "/rotated"
output_dir = base_dir + "/aligned"

#IMG_20171218_055805.jpg is the board without blocks on it
none_image_name = "IMG_20171218_055805.jpg"
none_image_path = input_dir + "/" + none_image_name
none_image = cv2.imread(input_dir + "/" + none_image_name)

for image_name in os.listdir(input_dir):

    if image_name == none_image_name:
        continue

    img_path = input_dir + "/" + image_name
    aligned = align(none_image_path, img_path)
    cv2.imwrite("%s/%s" % (output_dir, image_name), aligned)

