#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: zhou_me
@file: removeEdge.py 
@time: 2019/07/15
@contact: zhou_me@worksap.co.jp
@site:  
@software: PyCharm
"""
import imutils
import cv2
import os
import sys


input_images_dir = 'C:\\xyq\\vz'  # file format should be '*.tif'


def init():
    """"
    load the input images, return the list of file name
    """
    result_list_files = []
    files = os.listdir(input_images_dir)
    for i in files:
        if os.path.splitext(i)[1] == '.tif':
            result_list_files.append(i)

    # create new folder
    output_images_dir = input_images_dir + '\\' + 'update'
    print(output_images_dir)
    is_exists = os.path.exists(output_images_dir)
    if not is_exists:
        try:
            os.makedirs(output_images_dir)
        except OSError as exception:
            print(exception)
            sys.exit(0)

    return (result_list_files, output_images_dir)


def process():
    (files, output_images_dir) = init()
    for file in files:
        file_name = input_images_dir + '\\' + file
        print(file_name)
        image = cv2.imread(file_name)

        b, g, r = cv2.split(image)
        tmp_cnts = cv2.findContours(g, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(tmp_cnts)
        cv2.drawContours(image, [cnts[0]], -1, (0, 0, 0), 1)

        cv2.imwrite(
            output_images_dir + '//' + file,
            image)


if __name__ == '__main__':
    process()
    cv2.waitKey(0)
