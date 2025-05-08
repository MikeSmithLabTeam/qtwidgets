"""This is a boilerplate code snippet for a PyQt6 application.
You can use it to try out compound but simple widgets"""


import sys
import os
import cv2
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PyQt6.QtCore import pyqtSlot

# Add parent directory to Python path
# Add the root project directory to Python path (two levels up from test file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)


from qtwidgets.config import ConfigGui



def threshold(im, value=101, invert=False, configure=False):
    """
    Thresholds an image

    Pixels below thresh set to black, pixels above set to white
    modes =cv2.THRESH_BINARY (default), cv2.THRESH_BINARY_INV
    complete list here (https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html#ggaa9e58d2860d4afa658ef70a9b1115576ac7e89a5e95490116e7d2082b3096b2b8)
    """
    
    if configure:
        param_dict = {'value':[value,0,255,1],'invert':[int(invert),0,1,1]}
        print(param_dict)
        gui = ConfigGui(im, threshold, param_dict)
        thresh_img = threshold(im, **gui.reduced_dict)
    else:
        if value is None:
            invert = invert + cv2.THRESH_OTSU
        thresh_img = cv2.threshold(im, value, 255, int(invert))[1]
    return thresh_img

image_path = os.path.join(os.path.dirname(__file__), 'maxresdefault.jpg')
img = cv2.imread(image_path)[:,:,0]
threshold (img, invert=False, configure=True)


