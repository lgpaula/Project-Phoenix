# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 08:50:40 2018

@author: Pikaa
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

def generate_data(vidCapture, frames_to_skip):
    
    for i in range(frames_to_skip):
        _, frame = vidCapture.read()
    #_, frame = vidCapture.read()
    return frame

def update(data):
    mat.set_data(data)
    return mat 

def data_gen():
    while True:
        yield generate_data(vidCapture, frames_to_skip)
frames_to_skip = 10        
vidCapture = cv2.VideoCapture('DJI_0096.mp4')        
fig, ax = plt.subplots()
mat = ax.imshow(generate_data(vidCapture, frames_to_skip))
cbar = plt.colorbar(mat, cax=None, ax=None, use_gridspec=True)
cbar.ax.set_yticklabels(['20','80','200','400','600','99999'])
cbar.set_label('Tempreture', rotation=270)
#plt.colorbar.ColorbarBase(ax, cmap=None, norm=None, alpha=None, values=None, boundaries=None, orientation='vertical', ticklocation='auto', extend='neither', spacing='uniform', ticks=None, format=None, drawedges=False, filled=True, extendfrac=None, extendrect=False, label='')
ax.grid(True)

ani = animation.FuncAnimation(fig, update, data_gen, interval=500, save_count=50)
plt.show()