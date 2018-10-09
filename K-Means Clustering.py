# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 12:24:02 2018

@author: Pikaa
"""

import numpy as np
import cv2

#img = cv2.imread('DJI_0162.jpg')
 cv2.VideoCapture('DJI_0058.mp4')
Z = img.reshape((-1,3))

Z = np.float32(Z)

# define criteria, number of clusters(K) and apply kmeans()
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))

cv2.imshow('res2',res2)
cv2.waitKey(0)
cv2.destroyAllWindows()