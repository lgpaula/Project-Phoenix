# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 02:36:35 2018

@author: Pikaa
"""


#Import opencv and numpy (calling them as cv2 and np)
import cv2
import numpy as np
#Import video using opencv and name it as cap
#cap = cv2.VideoCapture('forest_fire_youtube.mp4')
frame = cv2.imread('img_frame/1049.jpg')
#This loop ensures that we read frame by frame, where the frame is just an image from the video. Each image is proccessed 
#while(1):
    # cap.read gives you an array, we ignore the first part of the array and assign the second part to the varible frame
#    _, frame = cap.read()
    # we create the histogram
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # create the range we want 
lower = np.array([0, 100, 100])
upper = np.array([40, 255, 255])
    # mask is the image without the pixels that are not in the range we want
mask = cv2.inRange(hsv, lower, upper)
    # if pixel was removed from varible mask is black, if pixel in mask and frame(original image) is same, then it is replaced with white
res = cv2.bitwise_and(frame,frame, mask= mask)
kernel_open = np.ones((20,20), np.uint8)
opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
    #cv2.imshow('Original',frame)
    #Extract canny edge
edges = cv2.Canny(mask,50,100)

cv2.imshow('Original',opening)
cv2.imshow('Mask[extract color]',mask)
cv2.imshow('Res[extract black/white]',res)
cv2.imshow('Canny Edge',edges)
    #wait 5 miliseconds (not realy sure why, but seems either if u press the key it stops, or it's just a delay)
#    k = cv2.waitKey(5) & 0xFF
#    if k == 27:
#        break

cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()