#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/7/14 1:12 
# @Author : zhou_me 
# @Site :  
# @File : calculateArea.py 
# @Software: PyCharm
import imutils
from imutils import contours
import cv2
import os
import sys

# input_images_dir = ''  # 'E:\\zn\\WT-1&2 brain'  # file format should be '*.tif'
# unit area size
# u_para = ''
# unit_area_size = 0.0  # 0.207 * 0.207
cnts_list = []


def init(input_images_dir,u_para):
    """"
    load the input images, return the list of file name
    """
    try:
        unit_area_size = float(u_para) * float(u_para)
    except Exception as exp:
        print('Please input right number of pixel size. ' + exp)
        sys.exit(0)

    result_list_files = []
    files = os.listdir(input_images_dir)
    for i in files:
        if os.path.splitext(i)[1] == '.tif':
            result_list_files.append(i)

    return result_list_files,unit_area_size


def calculate_area(file, input_images_dir, output_images_dir,unit_area_size):
    file_name = input_images_dir + '\\' + file
    print(file_name)
    image = cv2.imread(file_name, 0)

    # find contours in the image and initialize the mask that will be used to remove the bad contours
    tmp_cnts = cv2.findContours(image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(tmp_cnts)
    (cnts, boundingBoxes) = contours.sort_contours(cnts, method='left-to-right')

    lens = sort_splits(cnts)
    print('lens: %d' % lens)

    # cv2.imwrite(output_images_dir + '//' + 'res.tif', image)
    nu = 0
    for c in cnts_list:
        nu += 1
        print(nu)
        if nu == 1:
            continue
        try:
            result = rect_splits(image, c)
            if not (result == ''):
                # (cx, cy), radius = cv2.minEnclosingCircle(c)
                # center = (int(cx),int(cy))
                area_num = cv2.contourArea(c, False) * unit_area_size
                # print(area_num)
                #
                M = cv2.moments(c)
                (cx, cy) = (M['m10'] / M['m00'], M['m01'] / M['m00'])
                center = (int(cx), int(cy))
                # radius = int(radius)
                # cv2.circle(image, center, radius, (255, 255, 255), 3)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(image, str(round(area_num, 2)), center, font, 1.2, (255, 255, 255), 2)
        except Exception as exp:
            print(exp)
            sys.exit(0)

    cv2.imwrite(output_images_dir + '//' + file[:-3] + '.tif', image)


def rect_splits(image, contours):
    """
    return minimize rectangle area for the contours
    """
    (x, y, w, h) = cv2.boundingRect(contours)
    rect = ''
    if h > 20 and w > 20:
        rect = image.copy()[y:y + h, x:x + w]
    return rect


def sort_splits(cnts):
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


def process(input_images_dir, u_para):
    """"
    1. load files
    2. find Contours and draw contours, crop image
    3. minimize all images, and save to local
    """
    (files, unit_area_size) = init(input_images_dir, u_para)
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

        calculate_area(file, input_images_dir, output_images_dir,unit_area_size)


def main(argv):
    if len(argv) < 2:
        print('Please input at least two parameters, the first one is the input directory, the second one is pixel size.')
        sys.exit(0)

    input_images_dir = argv[1]
    u_para = argv[2]
    process(input_images_dir, u_para)
    cv2.waitKey(0)


if __name__ == '__main__':
    print('Please input two parameters:')
    print('1. the input directory. For example, E:\\zh\\test ')
    print('2. pixel size. For example, 0.207')
    main(sys.argv)
