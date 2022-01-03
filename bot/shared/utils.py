from collections import namedtuple

import numpy as np
import os
from pyautogui import Point
from pyscreeze import Box
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
