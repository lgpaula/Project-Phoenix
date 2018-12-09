import cv2
import numpy as np
import os
from tqdm import tqdm 
#cap = cv2.VideoCapture('forest_fire_youtube.mp4')
cap = 40
image_size = 224
def img_extractor(img, pic_num):
    height, width, channels = img.shape
    img_copy = img
#    auto_height = 480
#    auto_width = round(width/height*auto_height)
#    img = cv2.resize(img, (auto_width,auto_height))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 100, 100])
    upper = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    res = cv2.bitwise_and(img,img, mask= mask)
    
    kernel_open = np.ones((10,10), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_open)
    kernel_dilute = np.ones((20,20), np.uint8)
    img_dilation = cv2.dilate(mask, kernel_dilute, iterations=1)
    
    im2,ctrs, hier = cv2.findContours(img_dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
    
#    num = 0
#    pic_num = 0 
    if not os.path.exists('img'):
        os.makedirs('img')
#    for img_name in os.listdir('img'):
#        if img_name == str(pic_num)+".jpg":
#            pic_num +=1
#            
        
    
    for i, ctr in enumerate(sorted_ctrs): 
            # Get bounding box 
        x, y, w, h = cv2.boundingRect(ctr)
        
        T =w
        if w > h:
            dif = round((w-h)/2)
            y = y - dif
            T = w
        if w < h:
            dif = round((h-w)/2)
            x = x - dif
            T = h
#       
        x1= x-cap
        y1= y-cap
        T= T+cap*2
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x1+T > width:
            x1 = width - T-1
        if y1+T > height:
            y1 = height -T-1
        
            # Getting ROI 
        if T>150: 
              
#            cv2.rectangle(img,(x,y),( x + w, y + h ),(0,255,0),2) 
            
        #        crop_img = img[y:y+h, x:x+w]         
            pic_num += 1
            roi = img_copy[y1:y1+T, x1:x1+T]
            IMG = cv2.resize(roi, (image_size,image_size))
            cv2.imwrite("img//"+str(pic_num)+".jpg",IMG)        
#            cv2.imshow("img//"+str(pic_num)+".jpg",roi)
            
    return pic_num
            
DIR = 'C:/Users/Pikaa/Videos/img_frame'
def create_train_data(DIR):
    pic_num = 0
    for img in os.listdir(DIR):
        path = os.path.join(DIR,img)        
        img = cv2.imread(path)
        print(path)
        pic_num_old = pic_num
                 
        pic_num = img_extractor(img, pic_num)
        pic_total =  pic_num - pic_num_old


create_train_data(DIR)
        
    
          