#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: zhou_me
@file: crop2.py 
@time: 2019/07/08
@contact: zhou_me@worksap.co.jp
@site:  
@software: PyCharm
"""
import cv2
import numpy as np
import os
img = cv2.imread("test.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,threshed = cv2.threshold(gray,170,255,cv2.THRESH_BINARY)

# find contours without approx
cnts = cv2.findContours(threshed,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)[-2]

# get the max-area contour
cnt = sorted(cnts, key=cv2.contourArea)[-1]

# calc arclentgh
arclen = cv2.arcLength(cnt, True)

# do approx
eps = 0.0005
epsilon = arclen * eps
approx = cv2.approxPolyDP(cnt, epsilon, True)

# draw the result
canvas = img.copy()
for pt in approx:
    cv2.circle(canvas, (pt[0][0], pt[0][1]), 7, (0,255,0), -1)

cv2.drawContours(canvas, [approx], -1, (0,0,255), 2, cv2.LINE_AA)

# save
cv2.imwrite("result.png", canvas)