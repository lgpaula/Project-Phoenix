from tkinter import *
import tkinter as tk

#initiate the instance
win = tk.Tk()
#set up some parameters
win.title("Test GUI")
win.resizable(True, True)

def callback():
    print ("click!")

b = Button(win, text="OK", command=callback)
b.pack()
#run the window
win.mainloop()
