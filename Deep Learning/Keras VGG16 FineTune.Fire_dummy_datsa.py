
import cv2                 # working with, mainly resizing, images
import numpy as np         # dealing with arrays
import os                  # dealing with directories
from random import shuffle # mixing up or currently ordered data that might lead our network astray in training.
from tqdm import tqdm      # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
import matplotlib.pyplot as plt
#from __future__ import print_function
#import keras
#from keras.preprocessing.image import ImageDataGenerator, load_img
def Prepare_dataset():
    Fire_DIR = 'C:/Users/Pikaa/Documents/GitHub/Project-Phoenix/Deep Learning/DMSorted'
    DEMA_DIR = 'C:/Users/Pikaa/Documents/GitHub/Project-Phoenix/Deep Learning/FireSorted'
    Truck_DIR = 'C:/Users/Pikaa/Documents/GitHub/Project-Phoenix/Deep Learning/trucks'
    #TEST_DIR = 'J:/test'
    Fire_lable = [0,1,0]
    Truck_lable = [1,0,0]
    Dema_lable = [0,0,1]
    image_size = 224
    
    def create_train_data(TRAIN_DIR, label):
        training_data = []
        for img in tqdm(os.listdir(TRAIN_DIR)):
            path = os.path.join(TRAIN_DIR,img)
            print(path)
            img = cv2.imread(path)
            img = cv2.resize(img, (image_size,image_size))
            training_data.append([np.array(img),np.array(label)])
        shuffle(training_data)
        np.save('train_data.npy', training_data)
        return training_data
    #def process_test_data(TEST_DIR):
    #    testing_data = []
    #    for img in tqdm(os.listdir(TEST_DIR)):
    #        path = os.path.join(TEST_DIR,img)
    #        img_num = img.split('.')[0]
    #        img = cv2.imread(path)
    #        img = cv2.resize(img, (image_size,image_size))
    #        testing_data.append([np.array(img), img_num])   
    #        
    #    shuffle(testing_data)
    #    np.save('test_data.npy', testing_data)
    #    return testing_data
    
    Fire_data = create_train_data(Fire_DIR, Fire_lable)
    Truck_data = create_train_data(Truck_DIR, Truck_lable)
    Dema_data = create_train_data(DEMA_DIR, Dema_lable)
    shuffle(Fire_data)
    shuffle(Fire_data)
    shuffle(Truck_data)
    shuffle(Truck_data)
    shuffle(Dema_lable)
    shuffle(Dema_lable)
    
    length_F = len(Fire_data)
    validation_ratio = 0.2
    endF = round(length_F*validation_ratio)
    train_F = Fire_data[:-endF]
    test_F = Fire_data[-endF:]
    
    length_T = len(Truck_data)
    endT = round(length_T*validation_ratio)
    train_T = Truck_data[:-endT]
    test_T = Truck_data[-endT:]
    
    length_D = len(Dema_data)
    endD = round(length_T*validation_ratio)
    train_D = Dema_data[:-endD]
    test_D = Dema_data[-endD:]
    
    
    train=[]
    train.extend(train_F)
    train.extend(train_T)
    train.extend(train_D)
    test=[]
    test.extend(test_F)
    test.extend(test_T)
    test.extend(test_D)
    
    #Fire_data = create_train_data(Fire_DIR, Fire_lable)
    #Truck_data = create_train_data(Truck_DIR, Truck_lable)
    #testing_data =process_test_data(TEST_DIR)
    #train_data=[]
    #train_data.extend(Fire_data)
    #train_data.extend(Truck_data)
    #np.save('train_data.npy', train_data)
    #train_data = np.load('train_data.npy')
    #shuffle(train_data)
    #shuffle(train_data)
    #shuffle(train_data)
    #shuffle(train_data)
    #shuffle(train_data)
    #length = len(train_data)
    #validation_ratio = 0.2
    #end = round(length*validation_ratio)
    #train = train_data[:-end]
    #test = train_data[-end:]
    
    
    X = np.array([i[0] for i in train]).reshape(-1,image_size,image_size,3)
    #Y = [i[1] for i in train]
    Y = np.array([i[1] for i in train])
    
    test_x = np.array([i[0] for i in test]).reshape(-1,image_size,image_size,3)
    test_y = np.array([i[1] for i in test])
    return (X , Y, test_x, test_y)
    
def Train_model (X , Y, test_x, test_y, num):
    for i in range(num):        
        from keras.applications import VGG16
        from tensorflow.keras.callbacks import TensorBoard
        import tensorflow as tf
        from tensorflow.keras.datasets import cifar10
        from tensorflow.keras.preprocessing.image import ImageDataGenerator
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
        from tensorflow.keras.layers import Conv2D, MaxPooling2D
        # more info on callbakcs: https://keras.io/callbacks/ model saver is cool too.
        from tensorflow.keras.callbacks import TensorBoard
        import pickle
        import time
        
        NAME = "Fire-VGG16-{}".format(int(time.time()))
        
        
        #Load the VGG model
        vgg_conv = VGG16(weights='imagenet', include_top=False, input_shape=(image_size, image_size, 3))
        
        # Freeze all the layers
        for layer in vgg_conv.layers[:]:
            layer.trainable = False
        
        # Check the trainable status of the individual layers
        for layer in vgg_conv.layers:
            print(layer, layer.trainable)
        
        
        from keras import models
        from keras import layers
        from keras import optimizers
        
        # Create the model
        model = models.Sequential()
        
        # Add the vgg convolutional base model
        model.add(vgg_conv)
        
        # Add new layers
        model.add(layers.Flatten())
        model.add(layers.Dense(1024, activation='relu'))
        model.add(layers.Dropout(0.3))
        model.add(layers.Dense(1024, activation='relu'))
        #model.add(layers.Dropout(0.3))
        model.add(layers.Dense(3, activation='softmax'))
        tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))
        
        # Show a summary of the model. Check the number of trainable parameters
#        model.summary()
        
        
        # No Data augmentation 
        train_datagen = ImageDataGenerator(rescale=1./255)
        validation_datagen = ImageDataGenerator(rescale=1./255)
        
        
        # Compile the model
        model.compile(loss='categorical_crossentropy',
                      optimizer=optimizers.RMSprop(lr=1e-4),
                      metrics=['acc'])
        
        nb_train_samples = len(X)
        nb_validation_samples = len(test_x)
        batch_size = 16
        
        train_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)
        val_datagen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True)
        
        train_generator = train_datagen.flow(np.array(X), Y, batch_size=batch_size)
        validation_generator = val_datagen.flow(np.array(test_x), test_y, batch_size=batch_size)
        
        history = model.fit_generator(
            train_generator, 
            steps_per_epoch=nb_train_samples // batch_size,
            epochs=30,
            validation_data=validation_generator,
            validation_steps=nb_validation_samples // batch_size,
            verbose=4,
            callbacks=[tensorboard])
        
        # Save the Model
        # serialize model to JSON
        model_json = model.to_json()
        with open("Fire-VGG16-{}".format(int(time.time())), "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        model.save_weights("model.h5")
        print("Saved model to disk")
        
        #from keras.models import model_from_json
        ## later...
        # # load json and create model
        #json_file = open('model.json', 'r')
        #loaded_model_json = json_file.read()
        #json_file.close()
        #loaded_model = model_from_json(loaded_model_json)
        ## load weights into new model
        #loaded_model.load_weights("model.h5")
        #print("Loaded model from disk")
        #
X , Y, test_x, test_y = Prepare_dataset()
Train_model (X , Y, test_x, test_y, 1)