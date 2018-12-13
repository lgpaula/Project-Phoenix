from tkinter import *
import tkinter as tk
from tkinter import messagebox

win = tk.Tk()
width_value = win.winfo_screenwidth()
height_value = win.winfo_screenheight()
win.geometry(f"{width_value}x{height_value}+0+0")
win.resizable(False, True)
win.title("Test GUI")

win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)

topLeftFrame = tk.Frame(win, relief='solid', bd=2)
topLeftFrame.grid(row=0, column=0, padx=10, sticky="w")

homeImg = tk.PhotoImage(file="home_icon.png")
homeb = tk.Button(topLeftFrame, image=homeImg, height=100, width=100).grid(row=0, column=0, padx=10, pady=10)

rgbmenuImg = tk.PhotoImage(file="rgb_icon.png")
rgbmenub = tk.Button(topLeftFrame, image=rgbmenuImg, height=100, width=100)

thermalmenuImg = tk.PhotoImage(file="thermal_icon.png")
thermalmenub = tk.Button(topLeftFrame, image=thermalmenuImg, height=100, width=100)

rgbmenub.grid(row=0, column=1, padx=10, pady=10)
thermalmenub.grid(row=0, column=2, padx=10, pady=10)

topRightFrame = tk.Frame(win, relief='solid', bd=2)
topRightFrame.grid(row=0, column=1, padx=10, sticky="e")

settImg = tk.PhotoImage(file="settings_icon.png")
settingb = tk.Button(topRightFrame, image=settImg, height=100, width=100)

infoImg = tk.PhotoImage(file="copyright_icon.png")
infob = tk.Button(topRightFrame, image=infoImg, height=100, width=100)

loginImg = tk.PhotoImage(file="login_icon.png")
loginb = tk.Button(topRightFrame, image=loginImg, height=100, width=100)

settingb.grid(row=0, column=0, padx=10, pady=10)
infob.grid(row=0, column=1, padx=10, pady=10)
loginb.grid(row=0, column=2,padx=10, pady=10)

exitImg = tk.PhotoImage(file="exit_icon.png")
exitb = tk.Button(topRightFrame, image=exitImg, command=quit, height=100, width=100).grid(row=0, column=3, padx=10, pady=10)

leftFrame = tk.Frame(win, relief='solid', bd=2)
leftFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
tk.Button(leftFrame, text="Example 1").grid(row=1, column=0, pady=5)
tk.Button(leftFrame, text="Example 2").grid(row=2, column=0, pady=5)
tk.Button(leftFrame, text="Example 3").grid(row=3, column=0, pady=5)

rightFrame = tk.Frame(win)
rightFrame.grid(row=1, column=1, padx=10, pady=10, sticky="ne")

tempMap = PhotoImage(file="temp_heat_map.png")
tempMaplab = tk.Label(rightFrame, image=tempMap).grid(row=0, column=0, padx=5, pady=5)


win.mainloop()
