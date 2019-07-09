#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: zhou_me
@file: main.py 
@time: 2019/07/05
@contact: zhou_me@worksap.co.jp
@site:  
@software: PyCharm
"""
import numpy as np
import imutils
from imutils import contours
import cv2
import os
import sys

# For every original image, generate a folder named by it's filename to store it's split images
# Do not leave any blank area about the lines, they have to be crossed. and pay attention to
# small area that might have circle.

# input_images_dir = 'C:\\xyq\\splitGraph\\example'  # file format should be '*.tif'
input_images_dir = 'G:\\qian\\code\\splitGraph\\example'  # file format should be '*.tif'
output_images_names_prefix = ['VZ', 'ISVZ', 'OSVZ', 'IZ+CP']  # output filename rules, from the inside out.


def init():
    """"
    load the input images, return the list of file name
    """
    result_list_files = []
    files = os.listdir(input_images_dir)
    for i in files:
        if os.path.splitext(i)[1] == '.tif':
            result_list_files.append(i)

    return result_list_files


def split_graph(file_name, output_dir):
    file = input_images_dir + '\\' + file_name
    image = cv2.imread(file)
    b, g, r = cv2.split(image)
    tmp_image = r

    # find contours in the image and initialize the mask that will be used to remove the bad contours
    tmp_cnts = cv2.findContours(tmp_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(tmp_cnts)

    # 0 means clockwise, 1 means counterclockwise
    # save_splits(image, cnts, output_dir, 0)

    num = 0
    color = [255, 255, 255]
    for c in cnts:
        cv2.drawContours(image, [c], -1, (0, 255, 0), 1)
        mask = np.zeros(image.shape).astype(image.dtype)
        cv2.fillPoly(mask, [c], color)
        tmp_result = cv2.bitwise_and(image, mask)
        try:
            result = rect_splits(tmp_result, c)
            if not(result == ''):
                num += 1
                cv2.imwrite(output_dir + '/temp' + str(num) + '.png', result)
        except BaseException:
            print(BaseException)
            sys.exit(0)


def rect_splits(image, contours):
    """
    return minimize rectangle area for the contours
    """
    (x, y, w, h) = cv2.boundingRect(contours)
    rect = ''
    if h > 5 and w > 5:
        rect = image[y:y + h, x:x + w]
    return rect


def save_splits(image, cnts, output_dir, seq):
    """
    Define how to name these splits graph, clockwise or unclockwise
    clockwise 0
    counterclockwise 1
    """
    if seq == 0:
        (cnts, boundingBoxes) = contours.sort_contours(cnts, method='left-to-right')
    elif seq == 1:
        (cnts, boundingBoxes) = contours.sort_contours(cnts, method='right-to-left')

    # sort the contours
    clone = image.copy()

    # loop over the sorted contours and label them
    for (i, c) in enumerate(cnts):
        sortedImage = contours.label_contour(clone, c, i)

    # show the sorted contour image
    cv2.imwrite(output_dir + '/res' + str(seq) + '.tif', sortedImage)


def process():
    """"
    1. load files
    2. find Contours and draw contours, crop image
    3. minimize all images, and save to local
    """
    files = init()
    for file in files:
        file_name = os.path.splitext(file)[0]    # filename without suffix
        output_images_dir = input_images_dir + '\\' + file_name
        is_exists = os.path.exists(output_images_dir)
        if not is_exists:
            try:
                os.makedirs(output_images_dir)
            except OSError as exception:
                print(exception)
                sys.exit(0)
        split_graph(file, output_images_dir)


if __name__ == '__main__':
    process()
    cv2.waitKey(0)
