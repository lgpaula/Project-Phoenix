from tkinter import *
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
from math import ceil

#Goole API KEY Jacobo = AIzaSyD1GHUkmGtbGcss3KMugwOfBF8hz_CeQmQ

#initiate the instance
win = tk.Tk()
#define values to extract the size of the screen
screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()
#define the window as full screen in the format "width x height + 0 (x-axis) + 0 (y-axis)"
win.geometry(f"{screen_width}x{screen_height}+0+0")
#set up some parameters
win.resizable(False, True)
win.title("Semi-Autonomous Fire Scout Drone Main Frame User Interface")

win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)

#create variables for different percentages of the screen size
tenth_w = ceil(0.1*screen_width)
one_in_fifteen_w = ceil(0.015*screen_width)
one_in_fourfive_w = ceil(0.45*screen_width)
tenth_h = ceil(0.1*screen_height)
one_in_forty_h = ceil(0.4*screen_height)
one_in_fivefive_h = ceil(0.55*screen_height)


def img_resize(file, width, height):
    img = Image.open(file)
    img = img.resize((width, height), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)
    return photoImg

def homeMenu():
    messagebox.showinfo("Announcement", "This button will send the drone home.")

def rgbmenu():
    rgbWin = Toplevel(win)
    rgbWin.geometry(f"{width_value}x{height_value}+0+0")
    rgbWin.resizable(False, True)
    explanation = """This window will contain
    the rgb camera footage for
    the user to go bananas with it."""
    explabel = tk.Label(rgbWin, justify=tk.CENTER,text=explanation).pack()

def thermalmenu():
    thermalWin = Toplevel(win)
    thermalWin.geometry(f"{width_value}x{height_value}+0+0")
    thermalWin.resizable(False, True)
    explanation = """This window will contain
    the thermal camera footage for
    the user to go bananas with it."""
    explabel = tk.Label(thermalWin, justify=tk.CENTER, text=explanation, font = "arial 14 bold").pack()

def settings():
    settWin = Toplevel(win)
    settWin.geometry(f"400x300+550+200")
    settWin.resizable(False, True)
    explanation = """This window will contain
    all of the set up options for
    the user to go bananas with them."""
    explabel = tk.Label(settWin, justify=tk.CENTER, text=explanation, font = "arial 14 bold").pack()


def copyright():
    copyWin = Toplevel(win)
    copyWin.geometry(f"400x300+550+200")
    copyWin.resizable(False, True)
    explanation = """This code is part of the 5th semester project
    of the Robotics Bachelor at Aalborg University
    performed by students:

    Kenneth Richard Geipel
    Lucas Goncalves de Paula
    Kristyan Hyttel
    Jacobo Domingo Gil
    Iuliu Novac

    The use of this code is freely available
    but publications (with reference) may
    only be persued due to agreement with
    the developers."""
    explabel = tk.Label(copyWin, justify=tk.CENTER, text=explanation, font = "arial 14 bold").pack()

def login():
    logWin = Toplevel(win)
    logWin.geometry(f"250x100+625+200")
    logWin.resizable(False, True)
    username = tk.Label(logWin, text="Username:", font = "arial 14 bold")
    password = tk.Label(logWin, text="Password:", font = "arial 14 bold")
    uname_entry = Entry(logWin)
    pword_entry = Entry(logWin)

    username.grid(row=0, sticky=NE)
    password.grid(row=1, sticky=NE)

    uname_entry.grid(row=0, column=1)
    pword_entry.grid(row=1, column=1)

    c = Checkbutton(logWin, text="Keep me logged in", font ="Calibri 11 bold")
    c.grid(columnspan=2)


#create an additional frame for the content on the top-left
topLeftFrame = tk.Frame(win, relief='solid', bd=2)
topLeftFrame.grid(row=0, column=0, padx=10, sticky="w")

homeImg = img_resize("media/home_icon.png", tenth_h, tenth_h)
homeb = tk.Button(topLeftFrame, image=homeImg, command=homeMenu, width=tenth_h, height= tenth_h)

rgbmenuImg = img_resize("media/rgb_icon.png", tenth_h, tenth_h)
rgbmenub = tk.Button(topLeftFrame, image=rgbmenuImg, command=rgbmenu, height=tenth_h, width=tenth_h)

thermalmenuImg = img_resize("media/thermal_icon.png", tenth_h, tenth_h)
thermalmenub = tk.Button(topLeftFrame, image=thermalmenuImg, command=thermalmenu, height=tenth_h, width=tenth_h)

homeb.grid(row=0, column=0, padx=10, pady=10)
rgbmenub.grid(row=0, column=1, padx=10, pady=10)
thermalmenub.grid(row=0, column=2, padx=10, pady=10)


#create an additional frame for the content on the top-right
topRightFrame = tk.Frame(win)
topRightFrame.grid(row=0, column=2, padx=10, sticky="ne")

settImg = img_resize("media/settings_icon.png", tenth_h, tenth_h)
settingb = tk.Button(topRightFrame, image=settImg, command=settings, height=tenth_h, width=tenth_h)

infoImg = img_resize("media/copyright_icon.png", tenth_h, tenth_h)
infob = tk.Button(topRightFrame, image=infoImg, command=copyright, height=tenth_h, width=tenth_h)

loginImg = img_resize("media/login_icon.png", tenth_h, tenth_h)
loginb = tk.Button(topRightFrame, image=loginImg, command=login, height=tenth_h, width=tenth_h)

exitImg = img_resize("media/exit_icon.png", tenth_h, tenth_h)
exitb = tk.Button(topRightFrame, image=exitImg, command=quit, height=tenth_h, width=tenth_h)

settingb.grid(row=0, column=0, padx=10, pady=10)
infob.grid(row=0, column=1, padx=10, pady=10)
loginb.grid(row=0, column=2,padx=10, pady=10)
exitb.grid(row=0, column=3, padx=10, pady=10)


#create an additional frame for the content on the left
#leftFrame = tk.Frame(win)
#leftFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

#tk.Button(leftFrame, text="Example 1").grid(row=1, column=0, pady=5)


centerFrame = tk.Frame(win)
centerFrame.grid(row=1, column=1, padx=10, pady=10)

mapImg = img_resize("media/middle_earth_map.png", one_in_fourfive_w, one_in_fivefive_h)
map_label = tk.Label(centerFrame, image=mapImg).grid(row=0, column=0, padx=10, pady=10)

#create an additional frame for the content on the right
rightFrame = tk.Frame(win)
rightFrame.grid(row=1, column=2, padx=10, pady=10, sticky="e")

tempMap = img_resize("media/temp_heat_map.png", one_in_fifteen_w, one_in_forty_h)
tempMaplab = tk.Label(rightFrame, image=tempMap).grid(row=0, column=0, padx=10, pady=10)

#create an additional frame for the content on the bottom
bottomFrame = tk.Frame(win)
bottomFrame.grid(row=2, column=1, padx=10, pady=10, sticky="s")

info = """Drone Speed = XXX Km/h   Drone Distance = XXX m  Wind Direction = XX   Wind Force = XX Knots"""
info_botton = tk.Label(bottomFrame, justify=tk.CENTER, text=info, font = "arial 14 bold").grid(row=0, column=0, padx=10, pady=10)
#run the window
win.mainloop()
