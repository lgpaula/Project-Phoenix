from tkinter import *
import tkinter as tk
from tkinter import messagebox

win = tk.Tk()
width_value = win.winfo_screenwidth()
height_value = win.winfo_screenheight()
win.geometry(f"{width_value}x{height_value}+0+0")
win.resizable(False, True)
win.title("Test GUI")

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
    explabel = tk.Label(thermalWin, justify=tk.CENTER,text=explanation).pack()

def settings():
    settWin = Toplevel(win)
    settWin.geometry(f"400x300+550+200")
    settWin.resizable(False, True)
    explanation = """This window will contain
    all of the set up options for
    the user to go bananas with them."""
    explabel = tk.Label(settWin, justify=tk.CENTER,text=explanation).pack()


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
    explabel = tk.Label(copyWin, justify=tk.CENTER,text=explanation).pack()

def login():
    logWin = Toplevel(win)
    logWin.geometry(f"250x100+625+200")
    logWin.resizable(False, True)
    username = tk.Label(logWin, text="Username:", font ="Calibri 11 bold")
    password = tk.Label(logWin, text="Password:", font ="Calibri 11 bold")
    uname_entry = Entry(logWin)
    pword_entry = Entry(logWin)

    username.grid(row=0, sticky=NE)
    password.grid(row=1, sticky=NE)

    uname_entry.grid(row=0, column=1)
    pword_entry.grid(row=1, column=1)

    c = Checkbutton(logWin, text="Keep me logged in", font ="Calibri 11 bold")
    c.grid(columnspan=2)



homeImg = PhotoImage(file="home_icon.png")
homeb = Button(win, image=homeImg, command=homeMenu, height=150, width=150)

rgbmenuImg = PhotoImage(file="rgb_icon.png")
rgbmenub = Button(win, image=rgbmenuImg, command=rgbmenu, height=100, width=100)

thermalmenuImg = PhotoImage(file="thermal_icon.png")
thermalmenub = Button(win, image=thermalmenuImg, command=thermalmenu, height=100, width=100)

settImg = PhotoImage(file="settings_icon.png")
settingb = Button(win, image=settImg, command=settings, height=100, width=100)

infoImg = PhotoImage(file="copyright_icon.png")
infob = Button(win, image=infoImg, command=copyright, height=100, width=100)

loginImg = PhotoImage(file="login_icon.png")
loginb = Button(win, image=loginImg, command=login, height=100, width=100)

exitImg = PhotoImage(file="exit_icon.png")
exitb = Button(win, image=exitImg, command=quit, height=100, width=100)

tempMap = PhotoImage(file="temp_heat_map.png")
tempMaplab = tk.Label(win, image=tempMap)

homeb.grid(row=0, column=1, padx=10, pady=10)
rgbmenub.grid(row=0, column=2, padx=10, pady=10)
thermalmenub.grid(row=0, column=3, padx=10, pady=10)
settingb.grid(row=0, column=4, padx=10, pady=10)
infob.grid(row=0, column=5, padx=10, pady=10)
loginb.grid(row=0, column=6, padx=10, pady=10)
exitb.grid(row=0, column=10, padx=10, pady=10)
tempMaplab.grid(row=1, column=10, padx=10, pady=10)

#run the window
win.mainloop()
