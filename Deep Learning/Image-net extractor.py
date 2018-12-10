import urllib.request
import cv2
import numpy as np
import os

def store_raw_images():
    neg_images_link = 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03345487'   
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1
    
    if not os.path.exists('img'):
        os.makedirs('img')
        
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "img/"+str(pic_num)+".jpg")
            img = cv2.imread("img/"+str(pic_num)+".jpg")
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (300, 300))
            cv2.imwrite("img/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1
            
        except Exception as e:
            print(str(e)) 
            
def find_uglies():
    match = False
    for file_type in ['img']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

store_raw_images()
find_uglies()