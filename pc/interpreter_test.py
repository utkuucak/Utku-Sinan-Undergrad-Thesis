# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 16:44:56 2018

@author: Toshiba
"""
from image_interpreter import Image_Interpreter
import cv2
#import numpy as np

img = cv2.imread('images/image-Forward-1524918304.2155614.jpg')

imgint = Image_Interpreter()

imgint.interprete_img(img)
cv2.waitKey(0)