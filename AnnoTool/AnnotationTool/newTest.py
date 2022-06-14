import os
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *
import cv2
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
from PIL.features import codecs
import os
import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk, ImageGrab
from pynput import keyboard
from pynput.keyboard import Listener

WIDTH, HEIGHT = 1200, 800
topx, topy, botx, boty = 0, 0, 0, 0
currentx, currenty = 0, 0
rect_id = None
polygon_point_coord = list()
rect_list = list()
rect_main_data = list()
ImageFilePath = ""
ImgOpen = None
prodDir = ""
ImageFound = False

window = tk.Tk()
window.title("Image Annotation Tool")
window.geometry('%sx%s' % (
    WIDTH, HEIGHT))
window.state("zoomed")
window.configure(background='grey')

# creating style object to style the buttons
style = Style()

# This will be adding style, and
# naming that style variable as
# W.Tbutton (TButton is used for ttk.Button).
style.configure('W.TButton', font=
('calibri', 9, 'bold'),
                foreground='black',
                padding=[30, 10, 30, 10])


# functions


def GetImageFilePath():
    global ImageFilePath
    global ImageFound
    global img
    global canvas
    global ImageFrame
    test = False
    ImageFilePath = filedialog.askopenfilename()
    ImgOpen = Image.open(ImageFilePath)
    if len(ImageFilePath) > 0:
        test = True
        resized_width, resized_height = resize_image(ImgOpen.width, ImgOpen.height)
        ImgOpen = ImgOpen.resize((resized_width, resized_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(ImgOpen)
        ImageFound = True
        if resized_width < image_area.winfo_width():  # check if image is less wide than the canvas
            centering_width = (image_area.winfo_width() - resized_width) / 2
            image_area.create_image(centering_width, 0, image=img, anchor=NW)
        elif resized_height < image_area.winfo_height():  # check if image is taller than the canvas
            centering_height = (image_area.winfo_height() - resized_height) / 2
            image_area.create_image(0, centering_height, image=img, anchor=NW)
        else:
            image_area.create_image(0, 0, image=img, anchor=NW)

    if (test):
        window.mainloop()


def openFolder():
    global image
    global pic
    global images
    global picOpen
    global ImageFound
    directory = filedialog.askdirectory()
    os.chdir(directory)  # it permits to change the current dir
    allImages = os.listdir()
    allImages.reverse()
    for image in allImages:  # it returns the list of files song
        pos = 0
        if image.endswith(('png', 'jpg', 'jpeg', 'ico')):
            folderList.insert(pos, image)
            pos += 1
    folderList.selection_set(0)
    folderList.see(0)
    folderList.activate(0)
    folderList.selection_anchor(0)
    image = folderList.curselection()
    images = folderList.get(image[0])
    img1 = Image.open(images)
    pic = ImageTk.PhotoImage(img1, )
    ImageFound = True
    if len(images) > 0:
        test = True
        resized_width, resized_height = resize_image(img1.width, img1.height)
        picOpen = img1.resize((resized_width, resized_height), Image.ANTIALIAS)
        imgg = ImageTk.PhotoImage(picOpen)
        if resized_width < image_area.winfo_width() - 4:  # check if image is less wide than the canvas
            centering_width = (image_area.winfo_width() - resized_width) / 2
            image_area.create_image(centering_width, 0, image=imgg, anchor=NW)
        elif resized_height < image_area.winfo_height() - 4:  # check if image is taller than the canvas
            centering_height = (image_area.winfo_height() - resized_height) / 2
            image_area.create_image(0, centering_height, image=imgg, anchor=NW)
        else:
            image_area.create_image(0, 0, image=imgg, anchor=NW)

    if (test):
        window.mainloop()


def nextImage():
    try:
        next_one = folderList.curselection()
        next_one = next_one[0] + 1
        image = folderList.get(next_one)
        img1 = Image.open(image)
        resized_width, resized_height = resize_image(img1.width, img1.height)
        img1 = img1.resize((resized_width, resized_height), Image.ANTIALIAS)
        imagg = ImageTk.PhotoImage(img1)
        if resized_width < image_area.winfo_width() - 4:  # check if image is less wide than the canvas
            centering_width = (image_area.winfo_width() - resized_width) / 2
            image_area.create_image(centering_width, 0, image=imagg, anchor=NW)
        elif resized_height < image_area.winfo_height() - 4:  # check if image is taller than the canvas
            centering_height = (image_area.winfo_height() - resized_height) / 2
            image_area.create_image(0, centering_height, image=imagg, anchor=NW)
        else:
            image_area.create_image(0, 0, image=imagg, anchor=NW)
    except:
        tkinter.messagebox.showwarning("Warning", "no next image available.")


def prevImage():
    try:
        next_one = folderList.curselection()
        next_one = next_one[0] - 1
        image = folderList.get(next_one)
        img1 = Image.open(image)
        resized_width, resized_height = resize_image(img1.width, img1.height)
        img1 = img1.resize((resized_width, resized_height), Image.ANTIALIAS)
        imagg = ImageTk.PhotoImage(img1)
        if resized_width < image_area.winfo_width() - 4:  # check if image is less wide than the canvas
            centering_width = (image_area.winfo_width() - resized_width) / 2
            image_area.create_image(centering_width, 0, image=imagg, anchor=NW)
        elif resized_height < image_area.winfo_height() - 4:  # check if image is taller than the canvas
            centering_height = (image_area.winfo_height() - resized_height) / 2
            image_area.create_image(0, centering_height, image=imagg, anchor=NW)
        else:
            image_area.create_image(0, 0, image=imagg, anchor=NW)
    except:
        tkinter.messagebox.showwarning("Warning", "no previous image available.")


# connecting arrows to functions
# window.bind('<Right>', lambda x: nextImage())
# window.bind('<Left>', lambda x: preImage())

def resize_image(width, height):
    canvas_width = image_area.winfo_width()
    canvas_height = image_area.winfo_height()  # canvas width and height variables minus the border
    if width / height > canvas_width / canvas_height:  # checking if dimensions are bigger then the canvas' dimensions
        height = round(height * canvas_width / width)
        width = canvas_width
        return width, height
    elif width / height < canvas_width / canvas_height:  # checking if dimensions are smaller than the canvas' dimensions
        width = round(width * canvas_height / height)
        height = canvas_height
        return width, height
    else:  # dimensions are equal
        width = canvas_width
        height = canvas_height
        return width, height


def get_mouse_posn(event):
    global topy, topx
    topx, topy = image_area.canvasx(event.x), image_area.canvasy(event.y)  # convert to real canvas coordinates


def update_sel_rect(event):
    global botx, boty
    botx, boty = image_area.canvasx(event.x), image_area.canvasy(event.y)  # convert to real canvas coordinates
    image_area.coords(rect_id, topx, topy, botx,
                      boty)  # Update selection rect.   #  doet atm niks want rect_id wordt nergens aangemaakt
    #  kan ook niet want rect wordt gemaakt op release event


def draw_rect(self):
    draw_data = image_area.create_rectangle(topx, topy, botx, boty, outline="green", fill="")
    rect_list.append((topx, topy, botx, boty))
    rect_main_data.append(draw_data)


def create_polygon():
    image_area.bind('<Button-1>', create_oval)


def create_oval(event):
    try:
        first_oval_coordx, first_oval_coordy = polygon_point_coord[0]
    except:
        first_oval_coordx, first_oval_coordy = -100, -100

    if (currentx > first_oval_coordx + 10 or currentx < first_oval_coordx - 10) or (currenty < first_oval_coordy - 10 or currenty > first_oval_coordy + 10):
        xcoord, ycoord = image_area.canvasx(event.x), image_area.canvasy(event.y)
        oval = image_area.create_oval((xcoord - 7, ycoord + 7, xcoord + 7, ycoord - 7), fill="blue", outline="blue")  # finds coords of cursor and makes oval
        image_area.tag_bind(oval, '<Enter>', enter_poly)
        image_area.tag_bind(oval, '<Leave>', leave_poly)  # binds events to each oval
        polygon_point_coord.append((xcoord, ycoord))  # saves coords of ovals, idk if needed
    else:
        image_area.create_polygon(polygon_point_coord)
        image_area.unbind('<Button-1>')


def enter_poly(event):
    oval = image_area.find_closest(event.x, event.y)[0]
    if oval == 1:
        image_area.itemconfig(oval, fill="green", outline="green")


def leave_poly(event):
    oval = image_area.find_closest(event.x, event.y)[0]
    if oval == 1:
        image_area.itemconfig(oval, fill="blue", outline="blue")


def cropImages():
    rect_id = image_area.create_rectangle(topx, topy, topx, topy, dash=(2, 2), fill='', outline='red')
    image_area.bind('<Button-1>', get_mouse_posn)
    image_area.bind('<B1-Motion>', update_sel_rect)
    image_area.bind('<ButtonRelease-1>', draw_rect)
    image_area.update()


def saveAnnotations():
    im = Image.open(ImageFilePath)
    mainDir = os.path.dirname(ImageFilePath)
    global prodDir
    prodDir = os.path.splitext(ImageFilePath)[0]
    if not os.path.exists(prodDir):
        os.makedirs(prodDir)
    i = 0
    for po in rect_list:
        i = i + 1
        img1 = im.crop((po[0], po[1], po[2], po[3]))
        print(os.path.join(prodDir, "img" + str(i) + ".jpg"))
        img1.save(os.path.join(prodDir, "img" + str(i) + ".jpg"))
    tk.messagebox.showinfo("Completed ", "Annotations has been saved successfully")
    # beetje research gedaan, lambda handler zou dit in coco mogelijk kunnen maken


def clearRectangles():
    global rect_main_data
    global rect_list

    if len(rect_main_data) > 0:
        for rect in rect_main_data:
            image_area.delete(rect)
    rect_main_data.clear()
    rect_list.clear()

    image_area.pack()
    window.mainloop()


def motion(event):
    global currentx, currenty
    currentx, currenty = image_area.canvasx(event.x), image_area.canvasy(event.y)


def on_press_save():
    saveAnnotations()


window.bind("<Control-s>", lambda x: on_press_save())


def on_press_open():
    GetImageFilePath()


window.bind("<Control-o>", lambda x: on_press_open())


def on_press_Clear():
    clearRectangles()


window.bind("<Control-z>", lambda x: on_press_Clear())


def on_press_folder():
    openFolder()


window.bind("<Control-f>", lambda x: on_press_folder())


def left():
    prevImage()


window.bind("<Left>", lambda x: left())


def right():
    nextImage()


window.bind("<Right>", lambda x: right())


def on_zoomin_press():
    pass


window.bind("<Up>", lambda x: on_zoomin_press())


def on_zoomout_press():
    pass


window.bind("<Down>", lambda x: on_zoomout_press())

# MainFrame voor rest de andere frames
mainFrame = tk.Frame(window).grid(sticky='nsew')

# Frame for buttons
buttonFrame = tk.Frame(mainFrame, height=window.winfo_height(), width=window.winfo_width(), borderwidth=10, relief=FLAT)
buttonFrame.grid(row=0, column=0, sticky='nsew')

# frame for the canvas
canvasFrame = tk.Frame(mainFrame, height=window.winfo_height(), width=window.winfo_width(), relief=FLAT)
canvasFrame.grid(row=0, column=1, sticky='nsew')

# left frame
propertiesFrame = tk.Frame(mainFrame, height=window.winfo_height(), width=window.winfo_width(), borderwidth=10,
                           relief=FLAT)
propertiesFrame.grid(row=0, column=2, sticky='nsew')

# grid configuration
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=100000)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(0, weight=1)

# buttons
openButton = Button(buttonFrame, text="Open", style="W.TButton", command=GetImageFilePath)
openButton.grid(row=0, column=0)
openFolderButton = Button(buttonFrame, text="Open Folder", style="W.TButton", command=openFolder)
openFolderButton.grid(row=1, column=0)
saveButton = Button(buttonFrame, text="Save", style="W.TButton", command=saveAnnotations)
saveButton.grid(row=2, column=0)
saveAsButton = Button(buttonFrame, text="Save As", style="W.TButton")
saveAsButton.grid(row=3, column=0)
drawAnnotationBtn = Button(buttonFrame, text="Draw Rect", style="W.TButton", command=cropImages)
drawAnnotationBtn.grid(row=4, column=0)
clearRecButton = Button(buttonFrame, text="Clear Annotations", style="W.TButton", command=clearRectangles)
clearRecButton.grid(row=5, column=0)
zoomInButton = Button(buttonFrame, text="Zoom In", style="W.TButton")
zoomInButton.grid(row=6, column=0)
zoomOutButton = Button(buttonFrame, text="Zoom Out", style="W.TButton")
zoomOutButton.grid(row=7, column=0)
nextImage = Button(buttonFrame, text="Next Image", style="W.TButton", command=nextImage)
nextImage.grid(row=8, column=0)
preImage = Button(buttonFrame, text="Prev Image", style="W.TButton", command=prevImage)
preImage.grid(row=9, column=0)
createPolygonBtn = Button(buttonFrame, text="Create poly", style="W.TButton", command=create_polygon)
createPolygonBtn.grid(row=10, column=0)

# canvas
image_area = Canvas(canvasFrame, bg='grey')
image_area.grid(row=0, column=1, sticky='nsew')
image_area.pack(fill='both', expand=True)
image_area.bind('<Motion>', motion)

# listbox for labels
list = Listbox(propertiesFrame, width=40, height=20)
list.grid(row=2, column=2)
# entry
entryButton = Button(propertiesFrame, text="Add label", width=20)
entryButton.grid(row=1, column=2)
# label
labelEntry = Entry(propertiesFrame, width=30)
labelEntry.grid(row=0, column=2)
# -------
# label for folder list
label2 = Label(propertiesFrame, text="Images in the folder")
label2.grid(row=3, column=2)
# listbox for images in folder
folderList = Listbox(propertiesFrame, width=40, height=40)
folderList.grid(row=4, column=2)

# scrollbar
# scrollbarH = Scrollbar(canvasFrame, orient="horizontal", command=image_area.xview)
# scrollbarV = Scrollbar(canvasFrame, orient="vertical", command=image_area.yview)
# image_area.configure(yscrollcommand=scrollbarV.set, xscrollcommand=scrollbarH.set)
# image_area.configure(scrollregion=(0, 0, 1000, 1000))
# scrollbarH.grid(sticky="we")
# scrollbarV.grid(sticky="ns")


# menubar
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New")
filemenu.add_command(label="Open Folder")
filemenu.add_command(label="Save Annotation")
filemenu.add_separator()
filemenu.add_command(label="Close Image")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

editMenu = Menu(menubar, tearoff=0)
editMenu.add_command(label="Select Area")
editMenu.add_command(label="show Area")
editMenu.add_command(label="Delete Area")
menubar.add_cascade(label="Edit", menu=editMenu)

viewMenu = Menu(menubar, tearoff=0)
viewMenu.add_command(label="Zoom In")
viewMenu.add_command(label="Zoom Out")
viewMenu.add_separator()
viewMenu.add_command(label="Show Labels")
menubar.add_cascade(label="View", menu=viewMenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Tutorial")
helpmenu.add_command(label="About...")
menubar.add_cascade(label="Help", menu=helpmenu)
window.config(menu=menubar)

window.mainloop()
