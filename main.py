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
import csv
import math
import operator

# For every original image, generate a folder named by it's filename to store it's split images
# Do not leave any blank area about the lines, they have to be crossed. and pay attention to
# small area that might have circle.

input_images_dir = 'C:\\xyq\\splitGraph\\example'  # file format should be '*.tif'
# input_images_dir = 'G:\\qian\\code\\splitGraph\\example'  # file format should be '*.tif'
output_images_names_prefix = ['VZ', 'ISVZ', 'OSVZ', 'IZ', 'CP']  # output filename rules, from the inside out.
list_arc_len = []  # store the arclength of all contours


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


def split_graph(file_name, output_dir, output_dir_clockwise, output_dir_counterclockwise):
    file = input_images_dir + '\\' + file_name
    image = cv2.imread(file)
    b, g, r = cv2.split(image)
    tmp_image = r

    # find contours in the image and initialize the mask that will be used to remove the bad contours
    tmp_cnts = cv2.findContours(tmp_image.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(tmp_cnts)

    # 0 means clockwise, 1 means counterclockwise
    save_splits(image, cnts, output_dir)

    lens = len(list_arc_len)

    print(lens)
    if lens < 3:
        print('Check your input image: %s' % file)
        sys.exit(0)

    csv_list = []
    color = [255, 255, 255]
    # for method in ("left-to-right", "right-to-left"):
    method = 'left-to-right'
    num_seq = [0, 0, 0, 0, 0]
    (cnts, boundingBoxes) = contours.sort_contours(cnts, method=method)
    for c in cnts:
        cv2.drawContours(image, [c], -1, (0, 255, 0), 1)
        mask = np.zeros(image.shape).astype(image.dtype)
        cv2.fillPoly(mask, [c], color)
        tmp_result = cv2.bitwise_and(image, mask)
        try:
            result = rect_splits(tmp_result, c)
            if not(result == ''):
                arc_len_tmp = cv2.arcLength(c, True)
                if arc_len_tmp < list_arc_len[math.floor(lens/4)]:
                    i_seq = 0
                elif arc_len_tmp < list_arc_len[math.floor(lens/4 * 2)]:
                    i_seq = 1
                elif arc_len_tmp < list_arc_len[math.floor(lens/4 * 3)]:
                    i_seq = 2
                elif arc_len_tmp < list_arc_len[math.floor(lens/4 * 4 - 1)]:
                    i_seq = 3
                else:
                    i_seq = 4

                if not (arc_len_tmp == list_arc_len[lens - 1]) and i_seq < 3:
                    num_seq[i_seq] += 1
                    if method == 'left-to-right':
                        # cv2.imwrite(output_dir_clockwise + '//' + output_images_names_prefix[i_seq] + '_' + str(num_seq[i_seq]).zfill(2) + '.tif', tmp_result)

                        file_name = output_images_names_prefix[i_seq] + '_' + str(num_seq[i_seq]).zfill(2)
                        area_num = cv2.contourArea(c, True)
                        M = cv2.moments(c)
                        cx = int(M['m10'] / M['m00'])
                        cy = int(M['m01'] / M['m00'])
                        pts = Points(file_name, area_num * 0.325 * 0.325, cx, cy)

                        csv_list.append(pts)

                    elif method == 'right-to-left':
                        cv2.imwrite(output_dir_counterclockwise + '//' + output_images_names_prefix[i_seq] + '_' + str(num_seq[i_seq]).zfill(2) + '.tif',
                                    tmp_result)
        except Exception as exp:
            print(exp)
            sys.exit(0)

    csv_list.sort(key=operator.attrgetter('image_name'))
    # generate csv file to store area information
    with open(output_dir + '/area.csv', mode='w', encoding='utf8', newline='') as area_write:
        employee_writer = csv.writer(area_write, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for iter in csv_list:
            employee_writer.writerow([iter.image_name, iter.area_num, iter.cx, iter.cy])


def rect_splits(image, contours):
    """
    return minimize rectangle area for the contours
    """
    (x, y, w, h) = cv2.boundingRect(contours)
    rect = ''
    if h > 5 and w > 5:
        rect = image[y:y + h, x:x + w]
    return rect


def save_splits(image, cnts, output_dir):
    """
    save area info in csv
    """
    #  sort the contours
    # clone = image.copy()
    # loop over the sorted contours and label them
    try:
        for (i, c) in enumerate(cnts):
            (x, y, w, h) = cv2.boundingRect(c)
            if h > 5 and w > 5:
                # sortedImage = contours.label_contour(clone, c, num)
                list_arc_len.append(cv2.arcLength(c, True))
        list_arc_len.sort()
        # show the sorted contour image
        # cv2.imwrite(output_dir + '/res' + str(seq) + '.tiff', sortedImage)
    except BaseException:
        sys.exit(0)

def process():
    """"
    1. load files
    2. find Contours and draw contours, crop image
    3. minimize all images, and save to local
    """
    files = init()
    for file in files:
        print(file)
        file_name = os.path.splitext(file)[0]    # filename without suffix
        output_images_dir = input_images_dir + '\\' + file_name
        is_exists = os.path.exists(output_images_dir)
        if not is_exists:
            try:
                os.makedirs(output_images_dir)
            except OSError as exception:
                print(exception)
                sys.exit(0)

        output_images_dir_clockwise = input_images_dir + '\\' + file_name + '\\' + 'clockwise'
        output_images_dir_counterclockwise = input_images_dir + '\\' + file_name + '\\' + 'counterclockwise'
        is_exists_1 = os.path.exists(output_images_dir_clockwise)
        is_exists_2 = os.path.exists(output_images_dir_counterclockwise)
        if not is_exists_1:
            try:
                os.makedirs(output_images_dir_clockwise)
            except OSError as exception:
                print(exception)
                sys.exit(0)

        if not is_exists_2:
            try:
                os.makedirs(output_images_dir_counterclockwise)
            except OSError as exception:
                print(exception)
                sys.exit(0)
        split_graph(file, output_images_dir, output_images_dir_clockwise, output_images_dir_counterclockwise)


class Points:
    def __init__(self, image_name, area_num, cx, cy):
        self.image_name = image_name
        self.area_num = area_num
        self.cx = cx
        self.cy = cy


if __name__ == '__main__':
    process()
    cv2.waitKey(0)
