#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: zhou_me
@file: mergeChannel.py 
@time: 2019/12/12
@contact: zhou_me@worksap.co.jp
@site:  
@software: PyCharm
"""
import imutils
from imutils import contours
import cv2
import numpy as np
import os
import sys

input_images_dir = 'C:\\xyq\\calculateArea\\merge'  # file format should be '*.tif'


def init():
    """"
    load the input images, return the list of file name
    """
    print('[log] Current input directory: ' + input_images_dir)
    result_list_files = []
    files = os.listdir(input_images_dir)
    for i in files:
        if os.path.splitext(i)[1] == '.tif':
            result_list_files.append(i)

    return result_list_files


def process():
    """"
    1. load files
    2. find Contours and draw contours, crop image
    3. minimize all images, and save to local
    """
    files = init()
    number_file = set()
    filename_list = set()
    for file in files:
        file_name = file.split("_")[0]  # filename without suffix
        filename_list.add(os.path.basename(file))

        if file_name in number_file:
            pass
        else:
            number_file.add(file_name)
            output_file_name = os.path.splitext(file)[0]
            output_images_dir = input_images_dir + '\\' + file_name
            is_exists = os.path.exists(output_images_dir)
            if not is_exists:
                try:
                    os.makedirs(output_images_dir)
                except OSError as exception:
                    print(exception)
                    sys.exit(0)

    # merge two image
    for f1 in number_file:
        f1_pax6 = f1 + '_pax6.tif'
        f1_tbr2 = f1 + '_tbr2.tif'
        if f1_pax6 in filename_list and f1_tbr2 in filename_list:
            img_pax6 = cv2.imread(input_images_dir + '\\' + f1_pax6, cv2.IMREAD_GRAYSCALE)
            img_tbr2 = cv2.imread(input_images_dir + '\\' + f1_tbr2, cv2.IMREAD_GRAYSCALE)
            zeros = np.zeros(img_pax6.shape[:2], dtype="uint8")
            img = cv2.merge([img_pax6, img_tbr2, zeros])
            print('[log] Create new image file: ' + f1 + '.tif')
            cv2.imwrite(input_images_dir + '\\' + f1 + '\\' + f1 + '.tif', img)
        else:
            print('[msg] Error. Files Not Found! ' + f1_pax6 + '/' + f1_tbr2)


if __name__ == '__main__':
    process()
    cv2.waitKey(0)