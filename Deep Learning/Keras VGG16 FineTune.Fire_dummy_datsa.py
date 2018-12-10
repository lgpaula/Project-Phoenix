
import cv2                 # working with, mainly resizing, images
import numpy as np         # dealing with arrays
import os                  # dealing with directories
from random import shuffle # mixing up or currently ordered data that might lead our network astray in training.
from tqdm import tqdm      # a nice pretty percentage bar for tasks. Thanks to viewer Daniel BA1/4hler for this suggestion
import matplotlib.pyplot as plt
#from __future__ import print_function
#import keras
#from keras.preprocessing.image import ImageDataGenerator, load_img

Fire_DIR = 'C:/Users/Pikaa/Documents/GitHub/Project-Phoenix/Deep Learning/DMSorted'
Truck_DIR = 'C:/Users/Pikaa/Documents/GitHub/Project-Phoenix/Deep Learning/FireSorted'
#TEST_DIR = 'J:/test'
Fire_lable = [0,1]
Truck_lable = [1,0]
image_size = 224

def create_train_data(TRAIN_DIR, label):
    training_data = []
    for img in tqdm(os.listdir(TRAIN_DIR)):
        if img =="Thumbs.db":
            break
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
#testing_data =process_test_data(TEST_DIR)
train_data=[]
train_data.extend(Fire_data)
train_data.extend(Truck_data)
np.save('train_data.npy', train_data)
train_data = np.load('train_data.npy')
    

shuffle(train_data)
    
train = train_data[:-100]
test = train_data[-100:]

X = np.array([i[0] for i in train]).reshape(-1,image_size,image_size,3)
#Y = [i[1] for i in train]
Y = np.array([i[1] for i in train])

test_x = np.array([i[0] for i in test]).reshape(-1,image_size,image_size,3)
test_y = np.array([i[1] for i in test])
#train_data = np.load('train_data.npy')
#Fire_data_X = np.array([i[0] for i in Fire_data]).reshape(-1,image_size,image_size,3)
#Fire_data_Y = np.array([i[1] for i in Fire_data])
#Truck_data_X = np.array([i[0] for i in Truck_data]).reshape(-1,image_size,image_size,3)
#Truck_data_Y = np.array([i[1] for i in Truck_data])    
#
#X =[]
#X.extend(Fire_data_X)
#X.extend(Truck_data_X)
#Y =[]
#Y.extend(Fire_data_Y)
#Y.extend(Truck_data_Y)



#import tensorflow as tf
#
#k = tf.placeholder(tf.float32)
#
## Make a normal distribution, with a shifting mean
#mean_moving_normal = tf.random_normal(shape=[1000], mean=(5*k), stddev=1)
## Record that distribution into a histogram summary
#tf.summary.histogram("normal/moving_mean", mean_moving_normal)
#
## Setup a session and summary writer
#sess = tf.Session()
#writer = tf.summary.FileWriter("/tmp/histogram_example")
#
#summaries = tf.summary.merge_all()
#
## Setup a loop and write the summaries to disk
#N = 400
#for step in range(N):
#  k_val = step/float(N)
#  summ = sess.run(summaries, feed_dict={k: k_val})
#  writer.add_summary(summ, global_step=step)
#

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
model.add(layers.Dropout(0.5))
model.add(layers.Dense(2, activation='softmax'))
tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))

# Show a summary of the model. Check the number of trainable parameters
model.summary()


# No Data augmentation 
train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

# Change the batchsize according to your system RAM
train_batchsize = 100
val_batchsize = 10

# Compile the model
model.compile(loss='categorical_crossentropy',
              optimizer=optimizers.RMSprop(lr=1e-4),
              metrics=['acc'])

nb_train_samples = len(X)
nb_validation_samples = len(test_x)
batch_size = 8

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
    epochs=5,
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

#
## Plot the accuracy and loss curves
#acc = history.history['acc']
#val_acc = history.history['val_acc']
#loss = history.history['loss']
#val_loss = history.history['val_loss']
#
#epochs = range(len(acc))
#
#plt.plot(epochs, acc, 'b', label='Training acc')
#plt.plot(epochs, val_acc, 'r', label='Validation acc')
#plt.title('Training and validation accuracy')
#plt.legend()
#
#plt.figure()
#
#plt.plot(epochs, loss, 'b', label='Training loss')
#plt.plot(epochs, val_loss, 'r', label='Validation loss')
#plt.title('Training and validation loss')
#plt.legend()
#
#plt.show()
#
#scores = model.evaluate(X, Y, verbose=0)
#print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

#import matplotlib.pyplot as plt

# if you need to create the data:
#test_data = process_test_data()
# if you already have some saved:
#test_data = testing_data
#
#fig=plt.figure()
#
#for num,data in enumerate(test_data[100:200]):
#    # cat: [1,0]
#    # dog: [0,1]
#    
#    img_num = data[1]
#    img_data = data[0]
#    
#    y = fig.add_subplot(10,10,num+1)
#    orig = img_data
#    data = img_data.reshape(-1,image_size,image_size,3)
#    #model_out = model.predict([data])[0]
#    model_out = model.predict([data])[0]
#    
#    if np.argmax(model_out) == 1: str_label='Fire'
#    else: str_label='Truck'
#        
#    y.imshow(orig,cmap='gray')
#    plt.title(str_label)
#    y.axes.get_xaxis().set_visible(False)
#    y.axes.get_yaxis().set_visible(False)
#plt.show()
#
#
#from sklearn.model_selection import train_test_split
#from sklearn.datasets import load_iris
#from sklearn import svm
#from sklearn.metrics import accuracy_score
#
#iris = load_iris()
#X = iris.data[:, :5]  # we only take the first two features.
#y = iris.target
#
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=51)
#svm_model = svm.SVC(kernel='linear', C=1, gamma='auto')
#svm_model.fit(X_train,y_train)
#predictions = svm_model.predict(X_test)
#accuracy_score(predictions, y_test)
#
#from sklearn.model_selection import cross_val_score
#
#scores = cross_val_score(svm_model, iris.data, iris.target, cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))