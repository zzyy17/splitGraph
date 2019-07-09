# import the necessary packages
import numpy as np
import imutils
from imutils import contours
import cv2

def is_contour_bad(c):
    # approximate the contour
    peri = 0.01 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0, True)

    # the contour is 'bad' if it is not a rectangle
    return len(approx) > 3

# load the shapes image, convert it to grayscale, and edge edges in the image
image = cv2.imread('test_new.tif')
b, g, r = cv2.split(image)
cv2.imwrite('new_r.png', r)
tmp_image = r
# gray = cv2.cvtColor(tmp_image, cv2.COLOR_BGR2GRAY)
# edged = cv2.Canny(gray, 50, 100)
# cv2.imshow('Original', image)
# cv2.imwrite('temp.png', image)

# find contours in the image and initialize the mask that will be used to remove the bad contours
cnts = cv2.findContours(tmp_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(cnts)
cnts = imutils.grab_contours(cnts)
mask = np.ones(image.shape[:2], dtype='uint8') * 255
# mask = np.ones(image)
# sort_contours(cnts, method="left-to-right"):
# loop over the contours
num = 0
for c in cnts:
    # if the contour is bad, draw it on the mask
    num += 1
    cv2.drawContours(mask, [c], -1, 0, -1)
    #if is_contour_bad(c):
        #cv2.drawContours(mask, [c], -1, 0, -1)
        # mask = np.zeros(image.shape).astype(image.dtype)
        # color = [255, 255, 255]
        # cv2.fillPoly(mask, [c], color)
        # result = cv2.bitwise_and(image, mask)
        #
        # cv2.imwrite('temp' + str(num) + '.png', result)
    cv2.imwrite('temp'+str(num) + '.png', mask)

# loop over the sorting methods
# for method in ("left-to-right", "right-to-left", "top-to-bottom", "bottom-to-top"):
#     num += 1
#     # sort the contours
#     (cnts, boundingBoxes) = contours.sort_contours(cnts, method=method)
#     clone = image.copy()
#
#     # loop over the sorted contours and label them
#     for (i, c) in enumerate(cnts):
#         sortedImage = contours.label_contour(clone, c, i)
#
#     # show the sorted contour image
#     cv2.imwrite('temp' + str(num) + '.png', sortedImage)
#     #cv2.imshow(method, sortedImage)

# remove the contours from the image and show the resulting images
# image = cv2.bitwise_and(image, image, mask=mask)
# cv2.imshow('Mask', mask)
cv2.imwrite('new1.png', mask)
# cv2.imshow('After', image)
cv2.waitKey(0)
