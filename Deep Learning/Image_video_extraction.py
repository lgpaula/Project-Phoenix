import cv2
import numpy as np
import os
from tqdm import tqdm 
each_frame = 50


if not os.path.exists('img_frame'):
    os.makedirs('img_frame')
DIR = 'J:/DEMA Optagelser'
def extractor(video, pic_num):

    cap = video
    i=0
    while(cap.isOpened()):
        i +=1
        ret, frame = cap.read()
        if ret == True: 
            r = i%each_frame
            if r == 0:
                cv2.imwrite("img_frame//"+str(pic_num)+".jpg",frame) 
                pic_num +=1
        else:  
            break
    cap.release()
    cv2.destroyAllWindows()
    return pic_num
    
def create_train_data(DIR):
    for video in tqdm(os.listdir(DIR)):
        path = os.path.join(DIR,video)        
        vid = cv2.VideoCapture(path)
        pic_num = 0
        for img_name in os.listdir('img_frame'):
            pic_num +=1
            
        extractor(vid, pic_num)
    return pic_num

create_train_data(DIR)