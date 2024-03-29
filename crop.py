#!/usr/bin/env python  
#-*- coding:utf-8 _*-  
""" 
@author: zhou_me
@file: crop.py 
@time: 2019/07/05
@contact: zhou_me@worksap.co.jp
@site:  
@software: PyCharm
"""
import cv2
image = cv2.imread("test.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edged = cv2.Canny(image, 10, 250)
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
idx = 0
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    if w > 50 and h > 50:
        idx += 1
        new_img = image[y:y+h, x:x+w]
        cv2.imwrite(str(idx) + '.png', new_img)

cv2.imshow("im", image)
cv2.waitKey(0)
