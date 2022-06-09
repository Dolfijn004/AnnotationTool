import os
import tkinter
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

WIDTH, HEIGHT = 1200, 800
topx, topy, botx, boty = 0, 0, 0, 0
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
    WIDTH, HEIGHT))  # canvas is groter dan window op deze manier...maakt alles wonky als je het niet op zoomed zet
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
        if resized_width < image_area.winfo_width() - 4:  # check if image is less wide than the canvas
            centering_width = (image_area.winfo_width() - resized_width) / 2
            image_area.create_image(centering_width, 0, image=img, anchor=NW)
        elif resized_height < image_area.winfo_height() - 4:  # check if image is taller than the canvas
            centering_height = (image_area.winfo_height() - resized_height) / 2
            image_area.create_image(0, centering_height, image=img, anchor=NW)
        else:
            image_area.create_image(0, 0, image=img, anchor=NW)
        # canvas.pack(side=tk.LEFT, expand=0, fill=tk.BOTH)

    if (test):
        window.mainloop()


def resize_image(width, height):
    canvas_width = image_area.winfo_width() - 4
    canvas_height = image_area.winfo_height() - 4  # canvas width and height variables minus the border
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
    if topx in polygon_point_coord and topy in polygon_point_coord:
        image_area.create_polygon(polygon_point_coord)
    else:
        image_area.bind('<Button-1>', create_oval)
        polygon_point_coord.append((topx, topy))


def create_oval(event):
    xcoord, ycoord = image_area.canvasx(event.x), image_area.canvasy(event.y)
    image_area.create_oval((xcoord - 10, ycoord + 10, xcoord + 10, ycoord - 10))


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


# Frame for buttons
buttonFrame = Frame(window, height=window.winfo_height(), width=window.winfo_width(), borderwidth=20, relief=GROOVE)
buttonFrame.grid(row=0, column=0, sticky='nsew')

# frame for the canvas
canvasFrame = Frame(window, height=window.winfo_height(), width=window.winfo_width(), borderwidth=20, relief=GROOVE)
canvasFrame.grid(row=0, column=1, sticky='se')

# left frame
propertiesFrame = Frame(window, height=window.winfo_height(), width=window.winfo_width(), borderwidth=20, relief=GROOVE)
propertiesFrame.grid(row=0, column=2, sticky='ne')

# grid configuration
window.rowconfigure(0, weight=3)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=3)
window.columnconfigure(2, weight=1)

# buttons
openButton = Button(buttonFrame, text="Open", style="W.TButton", command=GetImageFilePath)
openButton.grid(row=0, column=0)
openFolderButton = Button(buttonFrame, text="Open Folder", style="W.TButton")
openFolderButton.grid(row=1, column=0)
saveButton = Button(buttonFrame, text="Save", style="W.TButton",  command=saveAnnotations)
saveButton.grid(row=2, column=0)
saveAsButton = Button(buttonFrame, text="Save As", style="W.TButton")
saveAsButton.grid(row=3, column=0)
drawAnnotationBtn = Button(buttonFrame, text="Draw Rect", style="W.TButton", command=cropImages)
drawAnnotationBtn.grid(row=4, column=0)
createRecButton = Button(buttonFrame, text="Clear Annotations", style="W.TButton", command=clearRectangles)
createRecButton.grid(row=5, column=0)  # create button is clear button?
zoomInButton = Button(buttonFrame, text="Zoom In", style="W.TButton")
zoomInButton.grid(row=6, column=0)
zoomOutButton = Button(buttonFrame, text="Zoom Out", style="W.TButton")
zoomOutButton.grid(row=7, column=0)
nextImage = Button(buttonFrame, text="Next Image", style="W.TButton")
nextImage.grid(row=8, column=0)
preImage = Button(buttonFrame, text="Prev Image", style="W.TButton")
preImage.grid(row=9, column=0)
createPolygonBtn = Button(buttonFrame, text="Create poly", style="W.TButton", command=create_polygon)
createPolygonBtn.grid(row=10, column=0)

# canvas
image_area = Canvas(canvasFrame, width=1450, height=950)
image_area.grid(row=0, column=1, sticky='nsew')


# listbox for labels
list = Listbox(propertiesFrame, width=40, height=20)
list.grid(row=2, column=2)
#entry
entryButton = Button(propertiesFrame, text="Add label", width=20)
entryButton.grid(row=1, column=2)
#label
labelEntry = Entry(propertiesFrame, width=30)
labelEntry.grid(row=0, column=2)
#-------
#label for folder list
label2 = Label(propertiesFrame, text= "Images in the folder")
label2.grid(row=3, column=2)
#listbox for images in folder
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
