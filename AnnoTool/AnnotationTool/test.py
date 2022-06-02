import os
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import cv2
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np
from PIL.features import codecs

root = Tk()
root.geometry('1500x1000')
root.state("normal")
root.title("Image Annotation Tool")
global image
mask = np.ones((490, 500))

# creating style object to style the buttons
style = Style()

# This will be adding style, and
# naming that style variable as
# W.Tbutton (TButton is used for ttk.Button).
style.configure('W.TButton', font=
('calibri', 10, 'bold'),
                foreground='black',
                padding=[40, 10, 40, 10])


# functions
def openImage():
    path = filedialog.askopenfilename(initialdir=os.getcwd(), title="select Image File",
                                      filetypes=(("JPG File", "*.jpg"), ("PNG File", "*.png")))
    if path:
        # this variable is used for the whole program
        global image
        image = Image.open(path)
        image = image.resize((image_area.winfo_width(), image_area.winfo_height()), Image.ANTIALIAS)
        image = ImageTk.PhotoImage(image)
        image_area.create_image(0, 0, image=image, anchor=NW)


# Frame for buttons
buttonFrame = Frame(root, height=1000, width=15)
buttonFrame.grid(row=0, column=0, sticky='nsew')

# frame for the canvas
canvasFrame = Frame(root, height=root.winfo_height(), width=root.winfo_width())
canvasFrame.grid(row=0,  column=1, sticky='ew')

# left frame
propertiesFrame = Frame(root, height=1000, width=20)
propertiesFrame.grid(row=0, column=2, sticky='ne')

# grid configuration
root.rowconfigure(0, weight=3)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.columnconfigure(2, weight=1)

# buttons
openButton = Button(buttonFrame, text="Open", style="W.TButton", command=openImage)
openButton.grid(row=0, column=0)
openFolderButton = Button(buttonFrame, text="Open Folder", style="W.TButton")
openFolderButton.grid(row=1, column=0)
saveButton = Button(buttonFrame, text="Save", style="W.TButton")
saveButton.grid(row=2, column=0)
saveAsButton = Button(buttonFrame, text="Save As", style="W.TButton")
saveAsButton.grid(row=3, column=0)
drawAnnotationBtn = Button(buttonFrame, text="Select Area ", style="W.TButton")
drawAnnotationBtn.grid(row=4, column=0)
createRecButton = Button(buttonFrame, text="Draw Rect", style="W.TButton")
createRecButton.grid(row=5, column=0)
zoomInButton = Button(buttonFrame, text="Zoom In", style="W.TButton")
zoomInButton.grid(row=6, column=0)
zoomOutButton = Button(buttonFrame, text="Zoom Out", style="W.TButton")
zoomOutButton.grid(row=7, column=0)
nextImage = Button(buttonFrame, text="Nxt Image", style="W.TButton")
nextImage.grid(row=8, column=0)
preImage = Button(buttonFrame, text="Pre Image", style="W.TButton")
preImage.grid(row=9, column=0)

# canvas
image_area = Canvas(canvasFrame, width=1100, height=950, bg='grey')
image_area.grid(row=0, column=1)

# listbox
list = Listbox(propertiesFrame, width=40, height=1000)
list.grid(row=0, column=2)

# menubar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New")
filemenu.add_command(label="Open Folder")
filemenu.add_command(label="Save Annotation")
filemenu.add_separator()
filemenu.add_command(label="Close Image")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
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
root.config(menu=menubar)

root.mainloop()
