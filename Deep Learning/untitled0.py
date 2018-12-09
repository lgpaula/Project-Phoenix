import cv2
import numpy as np
import os
from tqdm import tqdm 
img = cv2.imread("1.jpg")
#cap = cv2.VideoCapture('forest_fire_youtube.mp4')
cap = 40
height, width, channels = img.shape
pic_num=0
img_copy=img
#auto_height = 480
#auto_width = round(width/height*auto_height)
#img = cv2.resize(img, (auto_width,auto_height))
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower = np.array([0, 100, 100])
upper = np.array([40, 255, 255])
mask = cv2.inRange(hsv, lower, upper)
res = cv2.bitwise_and(img,img, mask= mask)

#kernel_open = np.ones((20,20), np.uint8)
#opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
kernel_dilute = np.ones((50,50), np.uint8)
img_dilation = cv2.dilate(mask, kernel_dilute, iterations=1)

im2,ctrs, hier = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

#num = 0
#pic_num = 0 
#if not os.path.exists('img'):
#os.makedirs('img')
#for img_name in os.listdir('img'):
#if img_name == str(pic_num)+".jpg":
#pic_num +=1
#


for i, ctr in enumerate(sorted_ctrs): 
# Get bounding box 
    x, y, w, h = cv2.boundingRect(ctr)

    T
    if w > h:
        dif = round((w-h)/2)
        y = y - dif
        h = w
    else:
        dif = round((h-w)/2)
        x = x - dif
        w = h
#       
    x1= x-cap
    y1= y-cap
    w1= w+cap*2
    h1= h+cap*2
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if x1+w1 > width:
        w1 = width - x1
    if y1+h1 > height:
        h1 = height -y1

# Getting ROI 
    if w > 100 and h > 100: 

#cv2.rectangle(img,(x,y),( x + w, y + h ),(0,255,0),2) 

#crop_img = img[y:y+h, x:x+w] 
        pic_num += 1
        roi = img_copy[y1:y1+h1, x1:x1+w1]
        cv2.imwrite("img"+str(pic_num)+".jpg",roi)
        print("y1 "+str(y1)+" h1 "+str(h1)+" T "+str(T)+" width "+str(width)+" height "+str(height))
#        cv2.imshow("img"+str(pic_num)+".jpg",roi)


    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
cv2.destroyAllWindows()
