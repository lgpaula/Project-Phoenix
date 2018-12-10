from tkinter import *
import tkinter as tk
from tkinter import messagebox

#initiate the instance
win = tk.Tk()
#define values to extract the size of the screen
width_value = win.winfo_screenwidth()
height_value = win.winfo_screenheight()
#define the window as full screen in the format "width x height + 0 (x-axis) + 0 (y-axis)"
win.geometry(f"{width_value}x{height_value}+0+0")
#set up some parameters
win.resizable(False, True)
win.title("Test GUI")

win.grid_columnconfigure(0, weight=1)
win.grid_columnconfigure(1, weight=1)

def dema_intranet():
    messagebox.showinfo("Announcement", "This button will take you to the streaming server.")

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
topLeftFrame = tk.Frame(win, width=200, height=100)
topLeftFrame.grid(row=0, column=0, padx=10, sticky="w")

homeImg = tk.PhotoImage(file="home_icon.png")
homeb = tk.Button(topLeftFrame, image=homeImg, command=homeMenu , height=100, width=100)

rgbmenuImg = tk.PhotoImage(file="rgb_icon.png")
rgbmenub = tk.Button(topLeftFrame, image=rgbmenuImg, command=rgbmenu, height=100, width=100)

thermalmenuImg = tk.PhotoImage(file="thermal_icon.png")
thermalmenub = tk.Button(topLeftFrame, image=thermalmenuImg, command=thermalmenu, height=100, width=100)

homeb.grid(row=0, column=0, padx=10, pady=10)
rgbmenub.grid(row=0, column=1, padx=10, pady=10)
thermalmenub.grid(row=0, column=2, padx=10, pady=10)


#create an additional frame for the content on the top-right
topRightFrame = tk.Frame(win, width=300, height=100)
topRightFrame.grid(row=0, column=1, padx=10, sticky="e")

settImg = tk.PhotoImage(file="settings_icon.png")
settingb = tk.Button(topRightFrame, image=settImg, command=settings, height=100, width=100)

infoImg = tk.PhotoImage(file="copyright_icon.png")
infob = tk.Button(topRightFrame, image=infoImg, command=copyright, height=100, width=100)

loginImg = tk.PhotoImage(file="login_icon.png")
loginb = tk.Button(topRightFrame, image=loginImg, command=login, height=100, width=100)

exitImg = tk.PhotoImage(file="exit_icon.png")
exitb = tk.Button(topRightFrame, image=exitImg, command=quit, height=100, width=100)

settingb.grid(row=0, column=0, padx=10, pady=10)
infob.grid(row=0, column=1, padx=10, pady=10)
loginb.grid(row=0, column=2,padx=10, pady=10)
exitb.grid(row=0, column=3, padx=10, pady=10)


#create an additional frame for the content on the left
leftFrame = tk.Frame(win)
leftFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

#tk.Button(leftFrame, text="Example 1").grid(row=1, column=0, pady=5)


centerFrame = tk.Frame(win)
centerFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

mapImg = tk.PhotoImage(file="map_example.png")
map_label = tk.Label(centerFrame, image=mapImg).grid(row=0, column=0, padx=10, pady=10)

#create an additional frame for the content on the right
rightFrame = tk.Frame(win)
rightFrame.grid(row=1, column=2, padx=10, pady=10, sticky="ne")

tempMap = tk.PhotoImage(file="temp_heat_map.png")
tempMaplab = tk.Label(rightFrame, image=tempMap).grid(row=0, column=0, padx=10, pady=10)

#create an additional frame for the content on the bottom
bottomFrame = tk.Frame(win)
bottomFrame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

info = """Drone Speed = XXX Km/h   Drone Distance = XXX m   Wind Direction = XX   Wind Force = XX Knots"""
info_botton = tk.Label(bottomFrame, justify=tk.CENTER, text=info, font = "arial 14 bold").grid(row=0, column=0, padx=10, pady=10)
#run the window
win.mainloop()
