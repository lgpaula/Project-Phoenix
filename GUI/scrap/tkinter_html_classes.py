# Example of embedding CEF Python browser using Tkinter toolkit.
# This example has two widgets: a navigation bar and a browser.
#
# NOTE: This example often crashes on Mac (Python 2.7, Tk 8.5/8.6)
#       during initial app loading with such message:
#       "Segmentation fault: 11". Reported as Issue #309.
#
# Tested configurations:
# - Tk 8.5 on Windows/Mac
# - Tk 8.6 on Linux
# - CEF Python v55.3+
#
# Known issue on Linux: When typing url, mouse must be over url
# entry widget otherwise keyboard focus is lost (Issue #255
# and Issue #284).

from cefpython3 import cefpython as cef
from tkinter import *
from tkinter import messagebox
import tkinter as tk
import ctypes
from PIL import Image
from PIL import ImageTk
from math import ceil
import sys
import os
import platform
import logging as _logging


# Platforms
WINDOWS = (platform.system() == "Windows")

# Globals
logger = _logging.getLogger("tkinter_.py")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"


screen_width = win.winfo_screenwidth()
screen_height = win.winfo_screenheight()

tenth_w = ceil(0.05*screen_width)
one_in_fifteen_w = ceil(0.015*screen_width)
one_in_fourfive_w = ceil(0.45*screen_width)
tenth_h = ceil(0.05*screen_height)
one_in_forty_h = ceil(0.4*screen_height)
one_in_fivefive_h = ceil(0.55*screen_height)

def img_resize(file, width, height):
    img = Image.open(file)
    img = img.resize((width, height), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)
    return photoImg


class MainFrame(tk.Frame):
    def __init__(self, root):
        self.topleft_frame = None
        self.topright_frame = None
        self.map_frame = None
        self.bottom_frame = None

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("Semi-Autonomous Fire Scout Drone Main Frame User Interface")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)

        #TopLeftFrame
        self.topleft_frame = TopLeftFrame(self)
        self.topleft_frame.grid(row=0, column=0,
                                 sticky=(tk.NW))
        tk.Grid.rowconfigure(self, 0, weight=0)
        tk.Grid.columnconfigure(self, 0, weight=0)

        #TopRightFrame
        self.topright_frame = TopRightFrame(self)
        self.topright_frame.grid(row=0, column=1,
                                 sticky=(tk.NE))
        tk.Grid.rowconfigure(self, 0, weight=0)
        tk.Grid.columnconfigure(self, 1, weight=0)

        #MapFrame
        self.map_frame = MapFrame(self)
        self.map_frame.grid(row=1, column=0,
                                 sticky=(tk.W))
        tk.Grid.rowconfigure(self, 1, weight=0)
        tk.Grid.columnconfigure(self, 0, weight=0)

        #BottomFrame
        self.bottom_frame = BottomFrame(self)
        self.bottom_frame.grid(row=2, column=0,
                                 sticky=(tk.W))
        tk.Grid.rowconfigure(self, 2, weight=0)
        tk.Grid.columnconfigure(self, 0, weight=0)

        self.pack(fill=tk.BOTH, expand=tk.YES)

class MapFrame(tk.Frame):

    def __init__(self, master):
        self.browser_frame = None
        self.navigation_bar = None

        self.setup_icon()
        self.bind("<Configure>", self.on_configure)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

        # NavigationBar
        self.navigation_bar = NavigationBar(self)
        self.navigation_bar.grid(row=0, column=0,
                                 sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=0)
        tk.Grid.columnconfigure(self, 0, weight=0)

        # BrowserFrame
        self.browser_frame = BrowserFrame(self, self.navigation_bar)
        self.browser_frame.grid(row=1, column=0,
                                sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 1, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def on_root_configure(self, _):
        logger.debug("MapFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        logger.debug("MapFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height
            if self.navigation_bar:
                height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_mapframe_configure(width, height)

    def on_focus_in(self, _):
        logger.debug("MapFrame.on_focus_in")

    def on_focus_out(self, _):
        logger.debug("MapFrame.on_focus_out")

    def on_close(self):
        if self.browser_frame:
            self.browser_frame.on_root_close()
        self.master.destroy()

    def get_browser(self):
        if self.browser_frame:
            return self.browser_frame.browser
        return None

    def get_browser_frame(self):
        if self.browser_frame:
            return self.browser_frame
        return None

    def setup_icon(self):
        resources = os.path.join(os.path.dirname(__file__), "resources")
        icon_path = os.path.join(resources, "tkinter"+IMAGE_EXT)
        if os.path.exists(icon_path):
            self.icon = tk.PhotoImage(file=icon_path)
            # noinspection PyProtectedMember
            self.master.call("wm", "iconphoto", self.master._w, self.icon)

class BrowserFrame(tk.Frame):

    def __init__(self, master, navigation_bar=None):
        self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None
        tk.Frame.__init__(self, master)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)
        self.bind("<Configure>", self.on_configure)
        self.focus_set()

    def embed_browser(self):
        window_info = cef.WindowInfo()
        rect = [0, 0, self.winfo_width(), self.winfo_height()]
        window_info.SetAsChild(self.get_window_handle(), rect)
        self.browser = cef.CreateBrowserSync(window_info,
                                             url="C:/Users/jdomi/Documents/cefpython/examples/html_simple_map.htm") #todo
        assert self.browser
        self.browser.SetClientHandler(LoadHandler(self))
        self.browser.SetClientHandler(FocusHandler(self))
        self.message_loop_work()

    def get_window_handle(self):
        if self.winfo_id() > 0:
            return self.winfo_id()
        elif MAC:
            # On Mac window id is an invalid negative value (Issue #308).
            # This is kind of a dirty hack to get window handle using
            # PyObjC package. If you change structure of windows then you
            # need to do modifications here as well.
            # noinspection PyUnresolvedReferences
            from AppKit import NSApp
            # noinspection PyUnresolvedReferences
            import objc
            # Sometimes there is more than one window, when application
            # didn't close cleanly last time Python displays an NSAlert
            # window asking whether to Reopen that window.
            # noinspection PyUnresolvedReferences
            return objc.pyobjc_id(NSApp.windows()[-1].contentView())
        else:
            raise Exception("Couldn't obtain window handle")

    def message_loop_work(self):
        cef.MessageLoopWork()
        self.after(10, self.message_loop_work)

    def on_configure(self, _):
        if not self.browser:
            self.embed_browser()

    def on_root_configure(self):
        # Root <Configure> event will be called when top window is moved
        if self.browser:
            self.browser.NotifyMoveOrResizeStarted()

    def on_mapframe_configure(self, width, height):
        if self.browser:
            if WINDOWS:
                ctypes.windll.user32.SetWindowPos(
                    self.browser.GetWindowHandle(), 0,
                    0, 0, width, height, 0x0002)
            elif LINUX:
                self.browser.SetBounds(0, 0, width, height)
            self.browser.NotifyMoveOrResizeStarted()

    def on_focus_in(self, _):
        logger.debug("BrowserFrame.on_focus_in")
        if self.browser:
            self.browser.SetFocus(True)

    def on_focus_out(self, _):
        logger.debug("BrowserFrame.on_focus_out")
        if self.browser:
            self.browser.SetFocus(False)

    def on_root_close(self):
        if self.browser:
            self.browser.CloseBrowser(True)
            self.clear_browser_references()
        self.destroy()

    def clear_browser_references(self):
        # Clear browser references that you keep anywhere in your
        # code. All references must be cleared for CEF to shutdown cleanly.
        self.browser = None

class LoadHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnLoadStart(self, browser, **_):
        if self.browser_frame.master.navigation_bar:
            self.browser_frame.master.navigation_bar.set_url(browser.GetUrl())

class FocusHandler(object):

    def __init__(self, browser_frame):
        self.browser_frame = browser_frame

    def OnTakeFocus(self, next_component, **_):
        logger.debug("FocusHandler.OnTakeFocus, next={next}"
                     .format(next=next_component))

    def OnSetFocus(self, source, **_):
        logger.debug("FocusHandler.OnSetFocus, source={source}"
                     .format(source=source))
        return False

    def OnGotFocus(self, **_):
        """Fix CEF focus issues (#255). Call browser frame's focus_set
           to get rid of type cursor in url entry widget."""
        logger.debug("FocusHandler.OnGotFocus")
        self.browser_frame.focus_set()

class NavigationBar(tk.Frame):

    def __init__(self, master):
        self.back_state = tk.NONE
        self.forward_state = tk.NONE
        self.back_image = None
        self.forward_image = None
        self.reload_image = None

        tk.Frame.__init__(self, master)
        resources = os.path.join(os.path.dirname(__file__), "resources")

        # Back button
        back_png = os.path.join(resources, "back"+IMAGE_EXT)
        if os.path.exists(back_png):
            self.back_image = tk.PhotoImage(file=back_png)
        self.back_button = tk.Button(self, image=self.back_image,
                                     command=self.go_back)
        self.back_button.grid(row=0, column=0)

        # Forward button
        forward_png = os.path.join(resources, "forward"+IMAGE_EXT)
        if os.path.exists(forward_png):
            self.forward_image = tk.PhotoImage(file=forward_png)
        self.forward_button = tk.Button(self, image=self.forward_image,
                                        command=self.go_forward)
        self.forward_button.grid(row=0, column=1)

        # Reload button
        reload_png = os.path.join(resources, "reload"+IMAGE_EXT)
        if os.path.exists(reload_png):
            self.reload_image = tk.PhotoImage(file=reload_png)
        self.reload_button = tk.Button(self, image=self.reload_image,
                                       command=self.reload)
        self.reload_button.grid(row=0, column=2)

        # Url entry
        self.url_entry = tk.Entry(self)
        self.url_entry.bind("<FocusIn>", self.on_url_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_url_focus_out)
        self.url_entry.bind("<Return>", self.on_load_url)
        self.url_entry.bind("<Button-1>", self.on_button1)
        self.url_entry.grid(row=0, column=3,
                            sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 3, weight=100)

        # Update state of buttons
        self.update_state()

    def go_back(self):
        if self.master.get_browser():
            self.master.get_browser().GoBack()

    def go_forward(self):
        if self.master.get_browser():
            self.master.get_browser().GoForward()

    def reload(self):
        if self.master.get_browser():
            self.master.get_browser().Reload()

    def set_url(self, url):
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

    def on_url_focus_in(self, _):
        logger.debug("NavigationBar.on_url_focus_in")

    def on_url_focus_out(self, _):
        logger.debug("NavigationBar.on_url_focus_out")

    def on_load_url(self, _):
        if self.master.get_browser():
            self.master.get_browser().StopLoad()
            self.master.get_browser().LoadUrl(self.url_entry.get())

    def on_button1(self, _):
        """Fix CEF focus issues (#255). See also FocusHandler.OnGotFocus."""
        logger.debug("NavigationBar.on_button1")
        self.master.master.focus_force()

    def update_state(self):
        browser = self.master.get_browser()
        if not browser:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
            self.after(100, self.update_state)
            return
        if browser.CanGoBack():
            if self.back_state != tk.NORMAL:
                self.back_button.config(state=tk.NORMAL)
                self.back_state = tk.NORMAL
        else:
            if self.back_state != tk.DISABLED:
                self.back_button.config(state=tk.DISABLED)
                self.back_state = tk.DISABLED
        if browser.CanGoForward():
            if self.forward_state != tk.NORMAL:
                self.forward_button.config(state=tk.NORMAL)
                self.forward_state = tk.NORMAL
        else:
            if self.forward_state != tk.DISABLED:
                self.forward_button.config(state=tk.DISABLED)
                self.forward_state = tk.DISABLED
        self.after(100, self.update_state)

class TopLeftFrame(tk.Frame):

    def __init__(self, master):
        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

        self.topLeftFrame = tk.Frame(self, relief='solid', bd=2)
        self.topLeftFrame.grid(row=0, column=0, padx=10, sticky=(tk.NW))

    def homeButton(self):
        self.homeImg = img_resize("media/home_icon.png", tenth_h, tenth_h)
        self.homeb = tk.Button(topLeftFrame, image=homeImg, command=homeMenu, width=tenth_h, height= tenth_h)


    def rgbButton(self):
        self.rgbmenuImg = img_resize("media/rgb_icon.png", tenth_h, tenth_h)
        self.rgbmenub = tk.Button(topLeftFrame, image=rgbmenuImg, command=rgbmenu, height=tenth_h, width=tenth_h)

    def thermalButton(self):
        self.thermalmenuImg = img_resize("media/thermal_icon.png", tenth_h, tenth_h)
        self.thermalmenub = tk.Button(topLeftFrame, image=thermalmenuImg, command=thermalmenu, height=tenth_h, width=tenth_h)


    self.homeb.grid(row=0, column=0, padx=5, pady=5)
    self.rgbmenub.grid(row=0, column=1, padx=5, pady=5)
    self.thermalmenub.grid(row=0, column=2, padx=5, pady=5)

    def homeMenu(self):
        messagebox.showinfo("Announcement", "This button will send the drone home.")

    def rgbmenu(self):
        rgbWin = Toplevel(win)
        rgbWin.geometry(f"{width_value}x{height_value}+0+0")
        rgbWin.resizable(False, True)
        explanation = """This window will contain
        the rgb camera footage for
        the user to go bananas with it."""
        explabel = tk.Label(rgbWin, justify=tk.CENTER,text=explanation).pack()

    def thermalmenu(self):
        thermalWin = Toplevel(win)
        thermalWin.geometry(f"{width_value}x{height_value}+0+0")
        thermalWin.resizable(False, True)
        explanation = """This window will contain
        the thermal camera footage for
        the user to go bananas with it."""
        explabel = tk.Label(thermalWin, justify=tk.CENTER, text=explanation, font = "arial 14 bold").pack()

class TopRightFrame(tk.Frame):

    def settings(self):
        settWin = Toplevel(win)
        settWin.geometry(f"400x300+550+200")
        settWin.resizable(False, True)
        explanation = """This window will contain
        all of the set up options for
        the user to go bananas with them."""
        explabel = tk.Label(settWin, justify=tk.CENTER, text=explanation, font = "arial 14 bold").pack()


    def copyright(self):
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

    def login(self):
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

class BottomFrame(tk.Frame):
    def __init__(self,master):
        self.navigation_bar = navigation_bar
        self.closing = False
        self.browser = None


if __name__ == '__main__':
    logger.setLevel(_logging.INFO)
    stream_handler = _logging.StreamHandler()
    formatter = _logging.Formatter("[%(filename)s] %(message)s")
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.info("CEF Python {ver}".format(ver=cef.__version__))
    logger.info("Python {ver} {arch}".format(
            ver=platform.python_version(), arch=platform.architecture()[0]))
    logger.info("Tk {ver}".format(ver=tk.Tcl().eval('info patchlevel')))
    assert cef.__version__ >= "55.3", "CEF Python v55.3+ required to run this"
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error

    win = tk.Tk()
    win.geometry(f"{screen_width}x{screen_height}+0+0")
    win.resizable(False, True)
    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=1)
    app = MainFrame(win)
    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    cef.Initialize()

    app.mainloop()
    cef.Shutdown()
