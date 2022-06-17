import os
import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *
import cv2 as cv
import numpy as np
from PIL.features import codecs
import os
import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk, ImageGrab
from pynput import keyboard
from pynput.keyboard import Listener
import json

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
('calibri', 10, 'bold'),
                foreground='black',
                padding=[30, 10, 30, 10],
                width=18)


# functions
def GetImageFilePath():
    global ImageFilePath
    global ImageFound
    global img
    global canvas
    global ImageFrame
    global image_area
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
    global img
    global image_area
    global allImages
    directory = filedialog.askdirectory()
    os.chdir(directory)  # it permits to change the current dir
    allImages = os.listdir()
    allImages.reverse()
    for image in allImages:  # it returns the list of files
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
        img = ImageTk.PhotoImage(picOpen)
        if resized_width < image_area.winfo_width() - 4:  # check if image is less wide than the canvas
            centering_width = (image_area.winfo_width() - resized_width) / 2
            image_area.create_image(centering_width, 0, image=img, anchor=NW)
        elif resized_height < image_area.winfo_height() - 4:  # check if image is taller than the canvas
            centering_height = (image_area.winfo_height() - resized_height) / 2
            image_area.create_image(0, centering_height, image=img, anchor=NW)
        else:
            image_area.create_image(0, 0, image=img, anchor=NW)
    if (test):
        window.mainloop()


def nextImage():
    global image
    global pic
    global images
    global ImageFound
    global img
    global image_area
    global allImages
    try:
        next_one = folderList.curselection()
        next_one = next_one[0] + 1
        folderList.selection_clear(0, 'end')
        folderList.selection_set(next_one)
        folderList.activate(next_one)
        folderList.selection_anchor(next_one)
        image = folderList.curselection()
        images = folderList.get(image)
        ImgOpen = Image.open(images)
        ImageFound = True
        if len(images) > 0:
            test = True
            resized_width, resized_height = resize_image(ImgOpen.width, ImgOpen.height)
            img1 = ImgOpen.resize((resized_width, resized_height), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img1)
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
    except:
        tkinter.messagebox.showwarning("Warning", "Please press the Previous button")


def prevImage():
    global image
    global pic
    global images
    global ImageFound
    global img
    global image_area
    global allImages
    try:
        prev_one = folderList.curselection()
        prev_one = prev_one[0] - 1
        folderList.selection_clear(0, 'end')
        folderList.selection_set(prev_one)
        folderList.activate(prev_one)
        folderList.selection_anchor(prev_one)
        image = folderList.curselection()
        images = folderList.get(image)
        ImgOpen = Image.open(images)
        ImageFound = True
        if len(images) > 0:
            test = True
            resized_width, resized_height = resize_image(ImgOpen.width, ImgOpen.height)
            img1 = ImgOpen.resize((resized_width, resized_height), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img1)
            if resized_width < image_area.winfo_width() - 4:  # check if image is less wide than the canvas
                centering_width = (image_area.winfo_width() - resized_width) / 2
                image_area.create_image(centering_width, 0, image=img, anchor=NW)
            elif resized_height < image_area.winfo_height() - 4:  # check if image is taller than the canvas
                centering_height = (image_area.winfo_height() - resized_height) / 2
                image_area.create_image(0, centering_height, image=img, anchor=NW)
            else:
                image_area.create_image(0, 0, image=img, anchor=NW)
        if (test):
            window.mainloop()
    except:
        tkinter.messagebox.showwarning("Warning", "Please press the Next button")


def showimage(event):
    global image
    global pic
    global images
    global picOpen
    global ImageFound
    global img
    global image_area
    global allImages
    n = folderList.curselection()
    folderList.selection_set(n)
    folderList.see(n)
    folderList.activate(n)
    folderList.selection_anchor(n)
    image = folderList.curselection()
    images = folderList.get(image)
    ImgOpen = Image.open(images)
    ImageFound = True
    if len(images) > 0:
        test = True
        resized_width, resized_height = resize_image(ImgOpen.width, ImgOpen.height)
        img1 = ImgOpen.resize((resized_width, resized_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img1)
        if resized_width < image_area.winfo_width() - 4:  # check if image is less wide than the canvas
            centering_width = (image_area.winfo_width() - resized_width) / 2
            image_area.create_image(centering_width, 0, image=img, anchor=NW)
        elif resized_height < image_area.winfo_height() - 4:  # check if image is taller than the canvas
            centering_height = (image_area.winfo_height() - resized_height) / 2
            image_area.create_image(0, centering_height, image=img, anchor=NW)
        else:
            image_area.create_image(0, 0, image=img, anchor=NW)
    if (test):
        window.mainloop()


window.bind("<<ListboxSelect>>", showimage)


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
    global rect_id
    global topx, topy
    global rect_list
    topx, topy = image_area.canvasx(event.x), image_area.canvasy(event.y)  # convert to real canvas coordinates
    rect_id = image_area.create_rectangle(topx, topy, topx, topy, outline="green", fill="grey", activefill="blue",
                                          stipple="gray12")


def update_sel_rect(event):
    global rect_id
    global topx, topy, botx, boty
    global rect_list
    curx = image_area.canvasx(event.x)
    botx = curx
    cury = image_area.canvasy(event.y)
    boty = cury
    image_area.coords(rect_id, topx, topy, curx, cury)


def draw_rect(self):
    global topx, topy, botx, boty
    global rect_id
    global rect_list
    image_area.coords(rect_id, topx, topy, botx, boty)
    rect_list.append(rect_id)
    image_area.unbind('<ButtonPress-1>')
    image_area.unbind('<B1-Motion')
    image_area.unbind('<ButtonRelease-1>')


def create_polygon():
    image_area.bind('<Button-1>', create_oval)


def create_oval(event):
    try:
        first_oval_coordx, first_oval_coordy = polygon_point_coord[0]
    except:
        first_oval_coordx, first_oval_coordy = -100, -100

    if (currentx > first_oval_coordx + 10 or currentx < first_oval_coordx - 10) or (
            currenty < first_oval_coordy - 10 or currenty > first_oval_coordy + 10):
        xcoord, ycoord = image_area.canvasx(event.x), image_area.canvasy(event.y)
        oval = image_area.create_oval((xcoord - 7, ycoord + 7, xcoord + 7, ycoord - 7), fill="blue",
                                      outline="blue")  # finds coords of cursor and makes oval
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
    image_area.bind('<Button-1>', get_mouse_posn)
    image_area.bind('<B1-Motion>', update_sel_rect)
    image_area.bind('<ButtonRelease-1>', draw_rect)


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
    global rect_id
    image_area.delete(rect_id)
    image_area.pack()
    window.mainloop()


def clearAllRectangles():
    global rect_main_data
    global rect_list
    global rect_id

    for i in rect_list:
        image_area.delete(i)
    rect_list.clear()
    image_area.pack()
    window.mainloop()

def clear_image():
    image_area.delete("all")


def load_json(filepath):
    f = open(filepath)
    annos = json.load(f)
    print(annos.keys)


# hier wordt door mij aan gewerkt
def click_tutorial():
    global popup
    popup = Toplevel(window)
    popup.title("Tutorial")
    popup.geometry("1100x1000")
    scrollbar = Scrollbar(popup, orient=VERTICAL)
    scrollbar.pack(side=RIGHT, fill=Y)


    introduction_label = Label(popup,
                               padding=[10, 20, 10, 20],
                               font="Bold", text="Greetings and thank you for using our annotation tool."
                               "\nin this window we will go over the functionality of the application itself "
                               "\nand the ways you're able to interact with it."
                               "\nlet's start with the left side buttons from top to bottom: ")

    open_labels = Label(popup,
                        text="the first button you see is called open, with this button you wil be able to place a singular image inside the gray middle area of your screen."
                             "\nplacing this image will allow you to make use of later mentioned buttons and their functionality."
                             "\nan alternative way of using this functionality is via pressing Control + o on your keyboard at the same time or by selecting new on the"
                             "\nnavbar under file"
                             "\n"
                             "\nsidenote: these keybinds and navbar items will be mentioned for each and every functionality that can be accessed by one or the other"
                             "\n"
                             "\nthe second button seen on the top right is called open folder, instead of a singular image this button will allow you to place a set of images"
                             "\nstored inside of a folder inside the middle gray area of the application. to the lower right of the screen will you be able to see the images"
                             "\nthat are contained within a selected folder displayed under the little area named Images in the folder."
                             "\nthis button can also be alternatively be accessed via the combination of Control + f on your keyboard or the navbar when selecting open folder"
                             " under file")

    save_labels = Label(popup,
                        text="next up are the two save buttons, the first of the two is simply named save, this button wil save the made annotations to whereever on your computer"
                             "\nyou decide to save it inside your file explorer"
                             "\n it can be accessed with the combination of Control + s or on the navbar by selecting save annotation under file"
                             "\n"
                             "\n the second save option named save as is meant for saving where you want to alter the format you save in aswell as choose where you want to save"
                             "the annotation")

    annotations_label = Label(popup, text="the following two buttons are used for making and removing annotations."
                                          "\nthe first one in line named Draw Rect is used for drawing rectangles on a image that can be saved as annotations. these can be drawn within"
                                          "\n the grey area where the image resides starting from one corner of the rectangle moving the mouse towards where the opposite corner would be"
                                          "\n"
                                          "\nthe way to remove these annotations made by using draw rectangle is via the button named Clear annotations."
                                          "\nThis will remove all rectangles and polygons from the currently selected image"
                                          "\nthe keybind to alternatively use this function is the combination of Control + z")

    zoom_label = Label(popup,
                       text="coming up next are the zoom buttons starting with the first one named zoom in. zoom in, "
                            "\nwhen being pressed will enlarge the picture making a certained"
                            "\npart of the image come closer up on the screen"
                            "\nthis will also be possible to use when pressing the upwards arrow key on your keyboard"
                            "\n"
                            "\nto opposite is able to be done aswell with the zoom out button. instead of enlarging the currently selected picture this will make the picture more"
                            "\ndistant from the screen shrinking the image inside of the gray area"
                            "\nthis can be done via the downward arrow key on your keyboard")

    selection_label = Label(popup,
                            text="\nfollowing up from the zoom buttons we have the navigation buttons for folders. beginning with the button next image."
                                 "\nthis button will be able to be used when a folder has been selected instead of a singular image the button will allow you to proceed to image that"
                                 " is next in line within the folder"
                                 "\nthis can be utilized just like with the zoom buttons and their arrow key keybinds. with the keybind of this function being the right arrow key."
                                 "\n"
                                 "\nthe button named previous image below it does the exact opposite, allowing you to move to a previous image within the selected folder instead of "
                                 "\n procedding to the next image"
                                 "\nthis button can be used with a arrow key aswell with the keybind being the left arrow key on your keyboard.")

    polygon_label = Label(popup, text="the last button included on the last side of the screen is named create polygon."
                                      "\n"
                                      "\nthis button will allow you to place small circles within the image selected. placing enough of these will make a annotation with the shape being made up "
                                      "\nof the connections that are visible as lines between the placed dots connecting with eachother based on the order they are placed in. (to name a example:"
                                      "\nthe first circle connects with the second one which in turn connects with the third one. this can go on until the last one is placed on the same spot as"
                                      " the first circle creating the polygon annotation."
                                      "\n")

    navitems_label = Label(popup,
                           text="from here we're going to cover the navbar items. those that are already mentioned are repeated"
                                "\nhere in short as a quick reminder of their function."
                                "\nthese parts are categorized based on what navbar item they reside in")

    file_label = Label(popup, text="(File)"
                                   "\nthis contains everything surrounding loading in the files you want to work on aswell as closing it"
                                   "\n(New):"
                                   "\nwil allow you to choose an image that will replace what is currently selected"
                                   "\n(Open Folder):"
                                   "\nallows you to open a entire folder full of images (content displayed in lower right section of the application)"
                                   "\nSave Annotation:"
                                   "\nsaves your annotation in the location of your choosing"
                                   "\n(Close Image):"
                                   "\nemptying the gray area (if you haven't saved beforehand this data might be lost)"
                                   "\n(Exit):"
                                   "\ncloses the program")

    edit_label = Label(popup, text="(Edit)"
                                   " revolves around adding, altering and deleting of annotations"
                                   " (Select Area):"
                                   " allows you to draw a rectangle just like the button draw rectangle allows you to"
                                   " (Show Area):"
                                   " shows the annotations only in a newly created window"
                                   " (Delete Area):"
                                   " deletes all annotations like with the clear annotation buttons")

    view_label = Label(popup, text="(View)"
                                   " this sections is used for changing how you want the image to be seen within the gray area of the application"
                                   " (Zoom In):"
                                   " get a closer up view of the image with each press of the button"
                                   " (Zoom Out):"
                                   " get a further away view of the image with each press of the button"
                                   " (Show Labels):")

    help_label = Label(popup, text="(Help)"
                                   " helps out when things are unclear or to learn specifics about the application itself"
                                   " (Tutorial):"
                                   " pressing this will allow you to view the window with explanations you are currently reading"
                                   " (About...):"
                                   " some extra information about the application itself")
    introduction_label.pack(anchor="w")
    open_labels.pack(anchor="w")
    save_labels.pack(anchor="w")
    annotations_label.pack(anchor="w")
    zoom_label.pack(anchor="w")
    selection_label.pack(anchor="w")
    polygon_label.pack(anchor="w")
    navitems_label.pack(anchor="w")
    file_label.pack(anchor="w")
    edit_label.pack(anchor="w")
    view_label.pack(anchor="w")
    help_label.pack(anchor="w")


# tot en met hier

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
photoopen = PhotoImage(file="icons/new.png")
openButton = Button(buttonFrame, text="Open", style="W.TButton", command=GetImageFilePath, image=photoopen, compound="top")
openButton.grid(row=0, column=0)
photofile = PhotoImage(file="icons/file.png")
openFolderButton = Button(buttonFrame, text="Open Folder", style="W.TButton", command=openFolder, image=photofile, compound="top")
openFolderButton.grid(row=1, column=0)
photosave = PhotoImage(file="icons/save.png")
saveButton = Button(buttonFrame, text="Save", style="W.TButton", command=saveAnnotations, image=photosave, compound="top")
saveButton.grid(row=2, column=0)
photosaveas = PhotoImage(file="icons/save-as.png")
saveAsButton = Button(buttonFrame, text="Save As", style="W.TButton", image=photosaveas, compound="top")
saveAsButton.grid(row=3, column=0)
photorect = PhotoImage(file="icons/rect.png")
drawAnnotationBtn = Button(buttonFrame, text="Draw Rect", style="W.TButton", command=cropImages, image=photorect, compound="top")
drawAnnotationBtn.grid(row=4, column=0)
photoundo = PhotoImage(file="icons/undo.png")
clearRecButton = Button(buttonFrame, text="Clear Last Annotation", style="W.TButton", command=clearRectangles, image=photoundo, compound="top")
clearRecButton.grid(row=5, column=0)
photobin = PhotoImage(file="icons/bin.png")
clearRecButton = Button(buttonFrame, text="Clear All Annotations", style="W.TButton", command=clearAllRectangles, image=photobin, compound="top")
clearRecButton.grid(row=6, column=0)
#zoomInButton = Button(buttonFrame, text="Zoom In", style="W.TButton")
#zoomInButton.grid(row=7, column=0)
#zoomOutButton = Button(buttonFrame, text="Zoom Out", style="W.TButton")
#zoomOutButton.grid(row=8, column=0)
photonext = PhotoImage(file="icons/next.png")
nextImage = Button(buttonFrame, text="Next Image", style="W.TButton", command=nextImage, image=photonext, compound="top")
nextImage.grid(row=9, column=0)
photoprev = PhotoImage(file="icons/prev.png")
preImage = Button(buttonFrame, text="Prev Image", style="W.TButton", command=prevImage, image=photoprev, compound="top")
preImage.grid(row=10, column=0)
photopoly = PhotoImage(file="icons/poly.png")
createPolygonBtn = Button(buttonFrame, text="Create poly", style="W.TButton", command=create_polygon, image=photopoly, compound="top")
createPolygonBtn.grid(row=11, column=0)
photocancel = PhotoImage(file="icons/cancel.png")
closeBtn = Button(buttonFrame, text="Close Image", style="W.TButton", command=clear_image, image=photocancel, compound="top")
closeBtn.grid(row=12, column=0)

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
filemenu.add_command(label="New", command=GetImageFilePath)
filemenu.add_command(label="Open Folder", command=openFolder)
filemenu.add_command(label="Save Annotation")
filemenu.add_separator()
filemenu.add_command(label="Close Image",)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

editMenu = Menu(menubar, tearoff=0)
editMenu.add_command(label="Select Area", command=draw_rect)
editMenu.add_command(label="show Area")
editMenu.add_command(label="Delete Area", command= clearRectangles)
menubar.add_cascade(label="Edit", menu=editMenu)

viewMenu = Menu(menubar, tearoff=0)
viewMenu.add_command(label="Zoom In")
viewMenu.add_command(label="Zoom Out")
viewMenu.add_separator()
viewMenu.add_command(label="Show Labels")
menubar.add_cascade(label="View", menu=viewMenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Tutorial", command=click_tutorial)
helpmenu.add_command(label="About...")
menubar.add_cascade(label="Help", menu=helpmenu)
window.config(menu=menubar)

window.mainloop()
