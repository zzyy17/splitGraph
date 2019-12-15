#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/7/15 21:30 
# @Author : zhou_me 
# @Site :  
# @File : NameArea.py 
# @Software: PyCharm
import numpy as np
import imutils
from imutils import contours
import cv2
import os
import sys
import csv
import operator
import shutil

# For every original image, generate a folder named by it's filename to store it's split images
# Do not leave any blank area about the lines, they have to be crossed. and pay attention to
# small area that might have circle.

# input_images_dir = 'C:\\xyq\\splitGraph\\example'  # file format should be '*.tif'
input_images_dir = 'H:\\pax6-tbr2\\py'  # file format should be '*.tif'
output_images_names_prefix = ['VZ', 'ISVZ', 'OSVZ', 'IZ', 'CP']  # output filename rules, from the inside out.
list_arc_len = []  # store the arclength of all contours
cnts_list = []


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
    print(file)
    image = cv2.imread(file)
    b, g, r = cv2.split(image)

    # find contours in the image and initialize the mask that will be used to remove the bad contours
    tmp_cnts = cv2.findContours(r.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(tmp_cnts)

    csv_list = []
    color = [255, 255, 255]
    # for method in ("left-to-right", "right-to-left"):
    method = 'left-to-right'
    num_seq = [0, 0, 0, 0, 0]
    (cnts, boundingBoxes) = contours.sort_contours(cnts, method=method)

    # 0 means clockwise, 1 means counterclockwise
    lens = sort_splits(g.copy(), cnts, output_dir)

    print('lens: %d ' % lens)
    if lens < 3:
        print('Check your input image: %s' % file)
        sys.exit(0)

    nu = 0
    temp_image_r = r.copy()
    for c in cnts_list:
        nu += 1
        if nu == 1:
            continue
        tmp_image_g = g.copy()
        tmp_image_b = b.copy()
        # cv2.drawContours(tmp_image_g, [c], -1, (255, 255, 255), 1)
        # mask = np.zeros(tmp_image_g.shape).astype(tmp_image_g.dtype)
        # cv2.fillPoly(mask, [c], color)
        # tmp_result = cv2.bitwise_and(tmp_image_g, mask)
        try:
            # result = rect_splits(tmp_result, c)
            #if not(result == ''):
            # arc_len_tmp = cv2.arcLength(c, True)
            (cx, cy), radius = cv2.minEnclosingCircle(c)
            center = (int(cx), int(cy))
            # radius = int(radius)
            # cv2.circle(tmp_result, center, radius, (255, 255, 255), 3)
            nb = tmp_image_b[int(cy), int(cx)]
            # cv2.circle(tmp_result, center, 20, (255, 255, 255), 10)
            if nb == 50:
                i_seq = 0
            elif nb == 100:
                i_seq = 1
            elif nb == 150:
                i_seq = 2
            elif nb == 200:
                i_seq = 3
            elif nb == 250:
                i_seq = 4
            else:
                i_seq = 0

            if i_seq >= 0:
                num_seq[i_seq] += 1
                if method == 'left-to-right':
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    file_name_str = output_images_names_prefix[i_seq] + '_' + str(num_seq[i_seq]).zfill(2)
                    cv2.putText(temp_image_r, file_name_str, center, font, 1.2, (255, 255, 255), 2)

        except Exception as ex:
            print(ex)

    cv2.imwrite(
        output_dir + '//' + file_name, temp_image_r)

def rect_splits(image, contours):
    """
    return minimize rectangle area for the contours
    """
    (x, y, w, h) = cv2.boundingRect(contours)
    rect = ''
    if h > 20 and w > 20:
        rect = image.copy()[y:y + h, x:x + w]
    return rect


def sort_splits(image, cnts, output_dir):
    """
    sort splits image by G value
    """
    #  sort the contours
    # clone = image.copy()
    # loop over the sorted contours and label them
    ll = 0
    cnts_list.clear()
    try:
        for (i, c) in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)
            if h > 20 and w > 20:
                # sortedImage = contours.label_contour(clone, c, num)
                ll += 1
                cnts_list.append(c)
                # list_arc_len.append(cv2.arcLength(c, True))
        # list_arc_len.sort()
        # show the sorted contour image
        # cv2.imwrite(output_dir + '/res' + str(seq) + '.tiff', sortedImage)
    except BaseException:
        sys.exit(0)
    return ll


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

        # output_images_dir_clockwise = input_images_dir + '\\' + file_name + '\\' + 'clockwise'
        # output_images_dir_counterclockwise = input_images_dir + '\\' + file_name + '\\' + 'counterclockwise'
        # output_images_dir_temp = input_images_dir + '\\' + file_name + '\\' + 'temp'
        # is_exists_1 = os.path.exists(output_images_dir_clockwise)
        # is_exists_2 = os.path.exists(output_images_dir_counterclockwise)
        # is_exists_3 = os.path.exists(output_images_dir_temp)
        # if not is_exists_1:
        #     try:
        #         os.makedirs(output_images_dir_clockwise)
        #     except OSError as exception:
        #         print(exception)
        #         sys.exit(0)
        #
        # if not is_exists_2:
        #     try:
        #         os.makedirs(output_images_dir_counterclockwise)
        #     except OSError as exception:
        #         print(exception)
        #         sys.exit(0)
        #
        # if not is_exists_3:
        #     try:
        #         os.makedirs(output_images_dir_temp)
        #     except OSError as exception:
        #         print(exception)
        #         sys.exit(0)

        split_graph(file, output_images_dir)


class Points:
    def __init__(self, image_name, area_num):
        self.image_name = image_name
        self.area_num = area_num


if __name__ == '__main__':
    process()
    cv2.waitKey(0)

