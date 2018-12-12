logo_label = tk.Label(centerFrame, image=logo).pack()
explanation = """This the dance of the D O double G.
 Your host with the most,
 drop like its hot cuz"""
text1_label = tk.Label(centerFrame, justify=tk.CENTER,text=explanation).pack()

menubar = tk.Menu(topFrame)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Home", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)

viewmenu = tk.Menu(menubar, tearoff=0)
viewmenu.add_command(label="RGB", command=donothing)
viewmenu.add_command(label="Thermal", command=donothing)
menubar.add_cascade(label="View", menu=viewmenu)

toolsmenu = tk.Menu(menubar, tearoff=0)
toolsmenu.add_command(label="Screenshot", command=donothing)
toolsmenu.add_command(label="Screencast", command=donothing)
menubar.add_cascade(label="Tools", menu=toolsmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)
win.config(menu=menubar)

#A frame with highlited borders
rightFrame = tk.Frame(win, relief='solid', bd=2)
rightFrame.grid(row=1, column=1, padx=10, pady=10, sticky="ne")


#Code to resize images
img = cv2.resize(imagetoresize, (image_size,image_size))
