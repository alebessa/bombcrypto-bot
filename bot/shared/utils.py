from collections import namedtuple

import cv2
import imutils
import numpy as np
import os
from pyautogui import Point
from pyscreeze import Box
from skimage.metrics import structural_similarity as compare_ssim
import sys

def resource_path(relative_path):
    """PyInstaller compatible path wrapper"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def im_path(name, zoom, folder='images', ext='png'):
    """Util func for accessing images in the image folder"""
    return resource_path(f'{folder}/{zoom}/{name}.{ext}')

def center(coords):
    """Returns the centroid of the box defined by the coods iter: (top_left.x, top_left.y, box_width, box_height)"""
    return Point(coords[0] + int(coords[2] / 2), coords[1] + int(coords[3] / 2))

RelativeDimensions = namedtuple('RelativeDimensions', 'x_offset y_offset width height')
def relative_box(x, y, relative_dims, proportion):
    """
    Returns a proportional Box relative to a point.
    
    Example 100% zoom:
    A_dims = RelativeDimensions(
        x_offset = 4,
        y_offset = 2,
        width = 4,
        height = 3
    )
    A = relative_box(2, 2, X_dims, 1.0)
    
    >>>
    p0: (2, 2)
        .


                    p1: (6, 4)    
                        .-------------
                        |            |
                        |     A      | h: 3
                        |            |
                        --------------
                            w: 4
    """

    x_offset = np.rint(relative_dims.x_offset * proportion).astype(int)
    y_offset = np.rint(relative_dims.y_offset * proportion).astype(int)
    w = np.rint(relative_dims.width * proportion).astype(int)
    h = np.rint(relative_dims.height * proportion).astype(int)

    return Box(x + x_offset, y + y_offset , w, h)

def contour_centroid(cnt):
    (x, y, w, h) = cv2.boundingRect(cnt)
    return np.rint(x + w / 2).astype(int), np.rint(y + h / 2).astype(int)

def max_diff_centroid(im1, im2):
    """Compares two images and returns the centroid of the biggest differing area"""

    # load the two input images
    imageA = cv2.imread(im1) if type(im1) == str else np.asarray(im1)
    imageB = cv2.imread(im2) if type(im1) == str else np.asarray(im2)

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = compare_ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")


    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)


    max_cnt = max(cnts, key=lambda cnt: cv2.contourArea(cnt))
    center = contour_centroid(max_cnt)

    return center