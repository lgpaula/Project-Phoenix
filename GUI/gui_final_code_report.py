from cefpython3 import cefpython as cef
import ctypes
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import sys
import os
import platform
import logging as _logging
from PIL import Image
from PIL import ImageTk

# Fix for PyCharm hints warnings
WindowUtils = cef.WindowUtils()

# Platforms
WINDOWS = (platform.system() == "Windows")

# Globals
logger = _logging.getLogger("tkinter_.py")

# Constants
# Tk 8.5 doesn't support png images
IMAGE_EXT = ".png" if tk.TkVersion > 8.5 else ".gif"

b_width =  75
b_height = 75
i_width = 30
i_height = 30
width_value = "1800"
height_value = "1200"

def img_resize(file, width, height):
    img = Image.open(file)
    img = img.resize((width, height), Image.ANTIALIAS)
    photoImg =  ImageTk.PhotoImage(img)
    return photoImg


class MainFrame(tk.Frame):

    def __init__(self, root):
        self.browser_frame = None
        self.navigation_bar = None
        self.info_frame = None

        # Root
        root.geometry(width_value + "x" + height_value)
        tk.Grid.rowconfigure(root, 0, weight=1)
        tk.Grid.columnconfigure(root, 0, weight=1)

        # MainFrame
        tk.Frame.__init__(self, root)
        self.master.title("Semi-Autonomous Fire Scout Drone Main Frame User Interface")
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.master.bind("<Configure>", self.on_root_configure)
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

        # DroneInformationFrame
        self.info_frame = InfoFrame(self)
        self.info_frame.grid(row=2, column=0,
                             sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 2, weight=0)
        tk.Grid.columnconfigure(self, 0, weight=1)

        # Pack MainFrame
        self.pack(fill=tk.BOTH, expand=tk.YES)

    def on_root_configure(self, _):
        logger.debug("MainFrame.on_root_configure")
        if self.browser_frame:
            self.browser_frame.on_root_configure()

    def on_configure(self, event):
        logger.debug("MainFrame.on_configure")
        if self.browser_frame:
            width = event.width
            height = event.height
            if self.navigation_bar:
                height = height - self.navigation_bar.winfo_height()
            self.browser_frame.on_mainframe_configure(width, height)

    def on_focus_in(self, _):
        logger.debug("MainFrame.on_focus_in")

    def on_focus_out(self, _):
        logger.debug("MainFrame.on_focus_out")

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
                                             url="C:/Users/jdomi/Documents/cefpython/examples/area_map.htm") #todo
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

    def on_mainframe_configure(self, width, height):
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
        self.home_image = None
        self.reload_image = None
        self.rgb_image = None
        self.thermal_image = None
        self.settings_image = None
        self.info_image = None
        self.login_image = None
        self.exit_image = None

        tk.Frame.__init__(self, master)
        resources = os.path.join(os.path.dirname(__file__), "resources")
        media = os.path.join(os.path.dirname(__file__), "media")

        # Home button
        home_png = os.path.join(media, "home"+IMAGE_EXT)
        if os.path.exists(home_png):
            self.home_image = img_resize(home_png, b_width, b_height)
        self.home_button = tk.Button(self, image=self.home_image,
                                     command=self.homemenu)
        self.home_button.grid(row=0, column=0, padx = 2.5)

        # Reload button
        reload_png = os.path.join(media, "reload"+IMAGE_EXT)
        if os.path.exists(reload_png):
            self.reload_image = img_resize(reload_png, b_width, b_height)
        self.reload_button = tk.Button(self, image=self.reload_image,
                                       command=self.reload)
        self.reload_button.grid(row=0, column=1, padx = 2.5)

        # RGB button
        rgb_png = os.path.join(media, "rgb"+IMAGE_EXT)
        if os.path.exists(rgb_png):
            self.rgb_image = img_resize(rgb_png, b_width, b_height)
        self.rgb_button = tk.Button(self, image=self.rgb_image,
                                       command=self.rgbmenu)
        self.rgb_button.grid(row=0, column=2, padx = 2.5)

        # Thermal button
        thermal_png = os.path.join(media, "thermal"+IMAGE_EXT)
        if os.path.exists(thermal_png):
            self.thermal_image = img_resize(thermal_png, b_width, b_height)
        self.thermal_button = tk.Button(self, image=self.thermal_image,
                                       command=self.thermalmenu)
        self.thermal_button.grid(row=0, column=3, padx = 2.5)

        # Url entry
        self.url_entry = tk.Entry(self)
        self.url_entry.bind("<FocusIn>", self.on_url_focus_in)
        self.url_entry.bind("<FocusOut>", self.on_url_focus_out)
        self.url_entry.bind("<Return>", self.on_load_url)
        self.url_entry.bind("<Button-1>", self.on_button1)
        #self.url_entry.grid(row=0, column=4, padx = 2.5,
                            #sticky=(tk.N + tk.S + tk.E + tk.W))
        tk.Grid.rowconfigure(self, 0, weight=100)
        tk.Grid.columnconfigure(self, 4, weight=100)

        # Settings button
        settings_png = os.path.join(media, "settings"+IMAGE_EXT)
        if os.path.exists(settings_png):
            self.settings_image = img_resize(settings_png, b_width, b_height)
        self.settings_button = tk.Button(self, image=self.settings_image,
                                     command=self.settingsmenu)
        self.settings_button.grid(row=0, column=5, padx = 2.5)

        # Info button
        info_png = os.path.join(media, "copyright"+IMAGE_EXT)
        if os.path.exists(info_png):
            self.info_image = img_resize(info_png, b_width, b_height)
        self.info_button = tk.Button(self, image=self.info_image,
                                     command=self.copyrightmenu)
        self.info_button.grid(row=0, column=6, padx = 2.5)

        # Login button
        login_png = os.path.join(media, "login"+IMAGE_EXT)
        if os.path.exists(home_png):
            self.login_image = img_resize(login_png, b_width, b_height)
        self.login_button = tk.Button(self, image=self.login_image,
                                     command=self.loginmenu)
        self.login_button.grid(row=0, column=7, padx = 2.5)

        # Exit button
        exit_png = os.path.join(media, "exit"+IMAGE_EXT)
        if os.path.exists(exit_png):
            self.exit_image = img_resize(exit_png, b_width, b_height)
        self.exit_button = tk.Button(self, image=self.exit_image,
                                     command=quit)
        self.exit_button.grid(row=0, column=8, padx = 2.5)

    def homemenu(self):
        self.message = messagebox.showinfo("Announcement", "This button will send the drone home.")

    def reload(self):
        if self.master.get_browser():
            self.master.get_browser().Reload()

    def rgbmenu(self):
        self.rgbWin = Toplevel(self)
        self.rgbWin.geometry("900x640+300+100")
        self.rgbWin.title("RGB Footage")
        self.rgbWin.resizable(False, True)
        self.explanation = """This window will contain
        the rgb camera footage for
        the user to go bananas with it."""
        self.explabel = tk.Label(self.rgbWin, justify=tk.CENTER,text=self.explanation, font = "arial 12 bold").pack()

    def thermalmenu(self):
        self.thermalWin = Toplevel(self)
        self.thermalWin.geometry("900x640+300+100")
        self.thermalWin.title("Thermal Camera Footage")
        self.thermalWin.resizable(False, True)
        self.explanation = """This window will contain
        the thermal camera footage for
        the user to go bananas with it."""
        self.explabel = tk.Label(self.thermalWin, justify=tk.CENTER, text=self.explanation, font = "arial 12 bold").pack()

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

    def settingsmenu(self):
        self.settWin = Toplevel(self)
        self.settWin.geometry("450x320+900+100")
        self.settWin.resizable(False, True)
        self.explanation = """This window will contain
        all of the set up options for
        the user to go bananas with them."""
        self.explabel = tk.Label(self.settWin, justify=tk.CENTER, text=self.explanation, font = "arial 12 bold").pack()

    def copyrightmenu(self):
        self.copyWin = Toplevel(self)
        self.copyWin.geometry("450x320+1000+100")
        self.copyWin.resizable(False, True)
        self.explanation = """This code is part of the 5th semester project
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
        self.explabel = tk.Label(self.copyWin, justify=tk.CENTER, text=self.explanation, font = "arial 12 bold").pack()

    def loginmenu(self):
        self.logWin = Toplevel(self)
        self.logWin.geometry("250x100+1200+100")
        self.logWin.resizable(False, True)
        self.username = tk.Label(self.logWin, text="Username:", font = "arial 12 bold")
        self.password = tk.Label(self.logWin, text="Password:", font = "arial 12 bold")
        self.uname_entry = Entry(self.logWin)
        self.pword_entry = Entry(self.logWin)

        self.username.grid(row=0, sticky=NE)
        self.password.grid(row=1, sticky=NE)

        self.uname_entry.grid(row=0, column=1)
        self.pword_entry.grid(row=1, column=1)

        self.c = Checkbutton(self.logWin, text="Keep me logged in", font ="arial 11 bold")
        self.c.grid(columnspan=2)

class InfoFrame(tk.Frame):
    def __init__(self, master):
        self.speed_image = None
        self.distance_image = None
        self.wind_image = None
        self.direction_image = None

        tk.Frame.__init__(self, master)
        media = os.path.join(os.path.dirname(__file__), "media")

        self.droneinfoFrame = tk.Frame(self)
        self.droneinfoFrame.grid(row = 2, column = 0, sticky = tk.SW)

        #SpeedInfo
        speed_png = os.path.join(media, "speed"+IMAGE_EXT)
        if os.path.exists(speed_png):
            self.speed_image = img_resize(speed_png, i_width, i_height)
        self.speed_imlab = tk.Label(self.droneinfoFrame, image=self.speed_image)
        self.speed_info = Text(self.droneinfoFrame, height=1.5, width=38)
        self.speed_unit = tk.Label(self.droneinfoFrame, text="Km/h", font = "arial 12 bold")

        self.speed_imlab.grid(row=0, column=0, sticky = tk.W)
        self.speed_info.grid(row=0, column=1, sticky = tk.W)
        self.speed_unit.grid(row=0, column=2, sticky= tk.W)

        #DistanceInfo
        distance_png = os.path.join(media, "distance"+IMAGE_EXT)
        if os.path.exists(distance_png):
            self.distance_image = img_resize(distance_png, i_width, i_height)
        self.distance_imlab = tk.Label(self.droneinfoFrame, image=self.distance_image)
        self.distance_info = Text(self.droneinfoFrame, height=1.5, width=38)
        self.distance_unit = tk.Label(self.droneinfoFrame, text="m", font = "arial 12 bold")

        self.distance_imlab.grid(row=0, column=3, sticky = tk.W)
        self.distance_info.grid(row=0, column=4, sticky = tk.W)
        self.distance_unit.grid(row=0, column=5, sticky= tk.W)

        #WindInfo
        wind_png = os.path.join(media, "wind"+IMAGE_EXT)
        if os.path.exists(wind_png):
            self.wind_image = img_resize(wind_png, i_width, i_height)
        self.wind_imlab = tk.Label(self.droneinfoFrame, image=self.wind_image)
        self.wind_info = Text(self.droneinfoFrame, height=1.5, width=38)
        self.wind_unit = tk.Label(self.droneinfoFrame, text="m/s", font = "arial 12 bold")

        self.wind_imlab.grid(row=0, column=6, sticky = tk.W)
        self.wind_info.grid(row=0, column=7, sticky = tk.W)
        self.wind_unit.grid(row=0, column=8, sticky= tk.W)

        #WDirectionInfo
        direction_png = os.path.join(media, "direction"+IMAGE_EXT)
        if os.path.exists(direction_png):
            self.direction_image = img_resize(direction_png, i_width, i_height)
        self.direction_imlab = tk.Label(self.droneinfoFrame, image=self.direction_image)
        self.direction_info = Text(self.droneinfoFrame, height=1.5, width=38)

        self.direction_imlab.grid(row=0, column=9, sticky = tk.W)
        self.direction_info.grid(row=0, column=10, sticky = tk.W)

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
    root = tk.Tk()
    app = MainFrame(root)
    # Tk must be initialized before CEF otherwise fatal error (Issue #306)
    cef.Initialize()

    app.mainloop()
    cef.Shutdown()
