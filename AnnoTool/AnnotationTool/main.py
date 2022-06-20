import tkinter
import tkinter.messagebox
from tkinter import *
from tkinter.ttk import *
import os
import tkinter as tk
import tkinter.filedialog as filedialog
from PIL import Image, ImageTk
import json

WIDTH, HEIGHT = 1200, 800
topx, topy, botx, boty = 0, 0, 0, 0
currentx, currenty = 0, 0
rect_id = None
polygon_point_coord = list()
rect_list = list()
rect_main_data = list()
image_file_path = ""
img_open = None
prod_dir = ""
image_found = False
rect_dict = {}

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

# on pressing select
def select_press():
    image_area.bind('<Button-1>', select_pressed)


# once a shape is pressed the coordinates are shown in the bottom
def select_pressed(event):
    global rect_dict
    global coords_label
    id_selected = image_area.find_withtag("current")[0]
    location_selected = rect_dict.get(id_selected)
    print(location_selected)
    coords_label['text'] = 'Coordinates: {}'.format(location_selected)


# opens one image when using the open image button
def get_image_file_path():
    global image_file_path
    global image_found
    global img
    global canvas
    global image_frame
    global image_area
    draw_annotations_button['state'] = tk.NORMAL
    create_polygon_button['state'] = tk.NORMAL
    clear_rect_button['state'] = tk.NORMAL
    clear_rect_button['state'] = tk.NORMAL
    close_button['state'] = tk.NORMAL
    clear_last_rect['state'] = tk.NORMAL
    save_button['state'] = tk.NORMAL
    select_button['state'] = tk.NORMAL

    test = False
    image_file_path = filedialog.askopenfilename()
    img_open = Image.open(image_file_path)
    if len(image_file_path) > 0:
        test = True
        resized_width, resized_height = resize_image(img_open.width, img_open.height)
        img_open = img_open.resize((resized_width, resized_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img_open)
        image_found = True
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


# opens a folder and displays it in the folder view
def open_folder():
    global image
    global pic
    global images
    global pic_open
    global image_found
    global img
    global image_area
    global all_images
    pre_image['state'] = tk.NORMAL
    next_image['state'] = tk.NORMAL
    draw_annotations_button['state'] = tk.NORMAL
    create_polygon_button['state'] = tk.NORMAL
    clear_rect_button['state'] = tk.NORMAL
    clear_last_rect['state'] = tk.NORMAL
    close_button['state'] = tk.NORMAL
    save_button['state'] = tk.NORMAL
    select_button['state'] = tk.NORMAL
    directory = filedialog.askdirectory()
    os.chdir(directory)  # it permits to change the current dir
    all_images = os.listdir()
    all_images.reverse()
    for image in all_images:  # it returns the list of files
        pos = 0
        if image.endswith(('png', 'jpg', 'jpeg', 'ico')):
            folder_list.insert(pos, image)
            pos += 1
    folder_list.selection_set(0)
    folder_list.see(0)
    folder_list.activate(0)
    folder_list.selection_anchor(0)
    image = folder_list.curselection()
    images = folder_list.get(image[0])
    img1 = Image.open(images)
    pic = ImageTk.PhotoImage(img1, )
    image_found = True
    if len(images) > 0:
        test = True
        resized_width, resized_height = resize_image(img1.width, img1.height)
        pic_open = img1.resize((resized_width, resized_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(pic_open)
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


# goes to the next image in the folder view via the next image button
def next_image():
    global image
    global pic
    global images
    global image_found
    global img
    global image_area
    global all_images
    try:
        next_one = folder_list.curselection()
        next_one = next_one[0] + 1
        folder_list.selection_clear(0, 'end')
        folder_list.selection_set(next_one)
        folder_list.activate(next_one)
        folder_list.selection_anchor(next_one)
        image = folder_list.curselection()
        images = folder_list.get(image)
        img_open = Image.open(images)
        image_found = True
        if len(images) > 0:
            test = True
            resized_width, resized_height = resize_image(img_open.width, img_open.height)
            img1 = img_open.resize((resized_width, resized_height), Image.ANTIALIAS)
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


# goes to the previous image in the folder view via the previous image button
def prev_image():
    global image
    global pic
    global images
    global image_found
    global img
    global image_area
    global all_images
    try:
        prev_one = folder_list.curselection()
        prev_one = prev_one[0] - 1
        folder_list.selection_clear(0, 'end')
        folder_list.selection_set(prev_one)
        folder_list.activate(prev_one)
        folder_list.selection_anchor(prev_one)
        image = folder_list.curselection()
        images = folder_list.get(image)
        img_open = Image.open(images)
        image_found = True
        if len(images) > 0:
            test = True
            resized_width, resized_height = resize_image(img_open.width, img_open.height)
            img1 = img_open.resize((resized_width, resized_height), Image.ANTIALIAS)
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
        tkinter.messagebox.showwarning("Warning", "Please press the Next button")


#  shows the image which has been clicked on from the folder view
def show_image(event):
    global image
    global pic
    global images
    global pic_open
    global image_found
    global img
    global image_area
    global all_images
    n = folder_list.curselection()
    folder_list.selection_set(n)
    folder_list.see(n)
    folder_list.activate(n)
    folder_list.selection_anchor(n)
    image = folder_list.curselection()
    images = folder_list.get(image)
    img_open = Image.open(images)
    image_found = True
    if len(images) > 0:
        test = True
        resized_width, resized_height = resize_image(img_open.width, img_open.height)
        img1 = img_open.resize((resized_width, resized_height), Image.ANTIALIAS)
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


window.bind("<<ListboxSelect>>", show_image)


def resize_image(width, height):
    #  Determines what the dimensions of the image should be to keep the same ratio.
    #
    #  Based on if the image has a smaller or larger ration than the canvas the image will be resized through a formula.
    canvas_width = image_area.winfo_width()
    canvas_height = image_area.winfo_height()  # canvas width and height variables
    if width / height > canvas_width / canvas_height:  # checking if ratio are bigger then the canvas' ratio
        height = round(height * canvas_width / width)
        width = canvas_width
        return width, height
    elif width / height < canvas_width / canvas_height:  # checking if ratio are smaller than the canvas' ratio
        width = round(width * canvas_height / height)
        height = canvas_height
        return width, height
    else:  # dimensions are equal
        width = canvas_width
        height = canvas_height
        return width, height


# initializes the rectangle
def get_mouse_posn(event):
    global rect_id
    global topx, topy
    global rect_list
    topx, topy = image_area.canvasx(event.x), image_area.canvasy(event.y)  # convert to real canvas coordinates
    rect_id = image_area.create_rectangle(topx, topy, topx, topy, outline="green", fill="grey", activefill="blue",
                                          stipple="gray12")


# updates the rectangle based on where the cursor is moving
def update_sel_rect(event):
    global rect_id
    global topx, topy, botx, boty
    curx = image_area.canvasx(event.x)
    botx = curx
    cury = image_area.canvasy(event.y)
    boty = cury
    image_area.coords(rect_id, topx, topy, curx, cury)


# finishes the rectangle, binds event to the rectangle and unbinds all key events
def draw_rect(self):
    global topx, topy, botx, boty
    global rect_id
    global rect_list
    global rect_dict
    image_area.coords(rect_id, topx, topy, botx, boty)
    image_area.tag_bind(rect_id, '<Button-1>', select_rect)
    rect_list.append(rect_id)
    rect_dict[rect_id] = (topx, topy, botx, boty)
    print(rect_dict)
    image_area.unbind('<Button-1>')
    image_area.unbind('<B1-Motion>')
    image_area.unbind('<ButtonRelease-1>')


def select_rect(event):
    x, y = image_area.canvasx(event.x), image_area.canvasy(event.y)
    ids = max(image_area.find_overlapping(x, y, x, y))
    print(ids)


# bind button-1 to create ovals and a polygon
def create_polygon():
    image_area.bind('<Button-1>', create_oval)


# creating ovals and connecting them when the first oval is clicked again
def create_oval(event):
    try:
        first_oval_coordx, first_oval_coordy = polygon_point_coord[0]  # get the coords of the first oval
    except:
        first_oval_coordx, first_oval_coordy = -100, -100  # dummy value if it is the first oval being placed

    if (currentx > first_oval_coordx + 10 or currentx < first_oval_coordx - 10) or (
            currenty < first_oval_coordy - 10 or currenty > first_oval_coordy + 10):  # check if the cursor is
        # anywhere near the first oval
        xcoord, ycoord = image_area.canvasx(event.x), image_area.canvasy(event.y)
        oval = image_area.create_oval((xcoord - 7, ycoord + 7, xcoord + 7, ycoord - 7), fill="blue",
                                      outline="blue")  # finds coords of cursor and makes oval
        image_area.tag_bind(oval, '<Enter>', enter_poly)
        image_area.tag_bind(oval, '<Leave>', leave_poly)  # binds events to each oval
        polygon_point_coord.append((xcoord, ycoord))  # saves coords of oval
    else:  # connecting the ovals when there has been clicked near the first oval
        image_area.create_polygon(polygon_point_coord, outline="blue", stipple="gray12")
        image_area.unbind('<Button-1>')


# highlight the oval if it is the first oval placed
def enter_poly(event):
    oval = image_area.find_closest(event.x, event.y)[0]
    if oval == 1:
        image_area.itemconfig(oval, fill="green", outline="green")


# undo the effect of enter_poly
def leave_poly(event):
    oval = image_area.find_closest(event.x, event.y)[0]
    if oval == 1:
        image_area.itemconfig(oval, fill="blue", outline="blue")


# bind all the buttons for making rectangles
def make_rect():
    image_area.bind('<Button-1>', get_mouse_posn)
    image_area.bind('<B1-Motion>', update_sel_rect)
    image_area.bind('<ButtonRelease-1>', draw_rect)


# save the image in jpg
def save_annotations():
    im = Image.open(image_file_path)
    main_dir = os.path.dirname(image_file_path)
    global prod_dir
    prod_dir = os.path.splitext(image_file_path)[0]
    if not os.path.exists(prod_dir):
        os.makedirs(prod_dir)
    i = 0
    for po in rect_list:
        i = i + 1
        img1 = im.crop((po[0], po[1], po[2], po[3]))
        print(os.path.join(prod_dir, "img" + str(i) + ".jpg"))
        img1.save(os.path.join(prod_dir, "img" + str(i) + ".jpg"))
    tk.messagebox.showinfo("Completed ", "Annotations has been saved successfully")


# undo rectangles
def clear_rectangle():
    global rect_main_data
    global rect_list
    global rect_id
    image_area.delete(rect_list[-1])
    rect_list.pop()
    image_area.pack()
    window.mainloop()


# clear all the rectangles at once
def clear_all_rectangles():
    global rect_main_data
    global rect_list
    global rect_id

    for i in rect_list:
        image_area.delete(i)
    rect_list.clear()
    image_area.pack()
    window.mainloop()


# delete the image and it's annotations at once
def clear_image():
    image_area.delete("all")
    pre_image['state'] = tk.DISABLED
    next_image['state'] = tk.DISABLED
    draw_annotations_button['state'] = tk.DISABLED
    create_polygon_button['state'] = tk.DISABLED
    clear_rect_button['state'] = tk.DISABLED
    clear_last_rect['state'] = tk.DISABLED
    save_button['state'] = tk.DISABLED
    clear_last_rect['state'] = tk.DISABLED
    select_button['state'] = tk.DISABLED



#  enter labels into label_list
def enter_labels():
    if len(label_entry.get()) == 0:  # check if entry field is empty
        tkinter.messagebox.showwarning("Warning", "The input field is empty.")
    else:
        entered_label = label_entry.get()
        label_list.insert(0, entered_label)


#  tracks the mouse all the time
def motion(event):
    global currentx, currenty
    currentx, currenty = image_area.canvasx(event.x), image_area.canvasy(event.y)


#  tutorial
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


#  all keybinds
def on_press_save():
    save_annotations()


window.bind("<Control-s>", lambda x: on_press_save())


def on_press_open():
    get_image_file_path()


window.bind("<Control-o>", lambda x: on_press_open())


def on_press_Clear():
    clear_rectangle()


window.bind("<Control-z>", lambda x: on_press_Clear())


def on_press_folder():
    open_folder()


window.bind("<Control-f>", lambda x: on_press_folder())


def left():
    prev_image()


window.bind("<Left>", lambda x: left())


def right():
    next_image()


window.bind("<Right>", lambda x: right())


def on_zoomin_press():
    pass


window.bind("<Up>", lambda x: on_zoomin_press())


def on_zoomout_press():
    pass


window.bind("<Down>", lambda x: on_zoomout_press())

# main_frame for the other frames
main_frame = tk.Frame(window).grid(sticky='nsew')

# Frame for buttons
button_frame = tk.Frame(main_frame, height=window.winfo_height(), width=window.winfo_width(), borderwidth=10,
                        relief=FLAT)
button_frame.grid(row=0, column=0, sticky='nsew', rowspan=2)

# frame for the canvas
canvas_frames = tk.Frame(main_frame, height=window.winfo_height(), width=window.winfo_width(), relief=FLAT)
canvas_frames.grid(row=0, column=1, sticky='nsew')

# frame voor next en previous image buttons
nepre_frame = tk.Frame(main_frame, height=40, width=window.winfo_width(), relief=FLAT)
nepre_frame.grid(row=1, column=1, sticky='nsew')

# left frame
properties_frame = tk.Frame(main_frame, height=window.winfo_height(), width=window.winfo_width(), borderwidth=10,
                            relief=FLAT)
properties_frame.grid(row=0, column=2, sticky='nsew', rowspan=2)

# grid configuration window
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=100000)
window.grid_columnconfigure(2, weight=1)
window.grid_rowconfigure(0, weight=12)
window.grid_rowconfigure(1, weight=1)

# grid configuration next and previous buttons
nepre_frame.grid_columnconfigure(0, weight=1)
nepre_frame.grid_columnconfigure(1, weight=1)
nepre_frame.grid_columnconfigure(2, weight=1)

# buttons left
photo_open = PhotoImage(file="icons/new.png")
open_button = Button(button_frame, text="Open Image", style="W.TButton", command=get_image_file_path, image=photo_open,
                     compound="top")
open_button.grid(row=0, column=0)
photo_file = PhotoImage(file="icons/file.png")
open_folder_button = Button(button_frame, text="Open Folder", style="W.TButton", command=open_folder, image=photo_file,
                            compound="top")
open_folder_button.grid(row=1, column=0)
photo_save = PhotoImage(file="icons/save.png")
save_button = Button(button_frame, text="Save", style="W.TButton", command=save_annotations, image=photo_save,
                     compound="top", state=['disabled'])
save_button.grid(row=2, column=0)
# photosaveas = PhotoImage(file="icons/save-as.png")
# saveAsButton = Button(button_frame, text="Save As", style="W.TButton", image=photosaveas, compound="top")
# saveAsButton.grid(row=3, column=0)
photo_select = PhotoImage(file="icons/objects.png")
select_button = Button(button_frame, text="Select", style="W.TButton", command=select_press, image=photo_select,
                       compound="top", state=['disabled'])
select_button.grid(row=3, column=0)
photo_rect = PhotoImage(file="icons/rect.png")
draw_annotations_button = Button(button_frame, text="Draw Rectangle", style="W.TButton", command=make_rect,
                                 image=photo_rect, compound="top",  state=['disabled'])
draw_annotations_button.grid(row=4, column=0)
photo_poly = PhotoImage(file="icons/poly.png")
create_polygon_button = Button(button_frame, text="Create poly", style="W.TButton", command=create_polygon,
                               image=photo_poly, compound="top",  state=['disabled'])
create_polygon_button.grid(row=5, column=0)
photo_undo = PhotoImage(file="icons/undo.png")
clear_last_rect = Button(button_frame, text="Clear Last Annotation", style="W.TButton", command=clear_rectangle,
                           image=photo_undo, compound="top",  state=['disabled'])
clear_last_rect.grid(row=6, column=0)
photo_bin = PhotoImage(file="icons/bin.png")
clear_rect_button = Button(button_frame, text="Clear All Annotations", style="W.TButton", command=clear_all_rectangles,
                           image=photo_bin, compound="top", state=['disabled'])
clear_rect_button.grid(row=7, column=0)
photo_cancel = PhotoImage(file="icons/cancel.png")
close_button = Button(button_frame, text="Close Image", style="W.TButton", command=clear_image, image=photo_cancel,
                      compound="top", state=['disabled'])
close_button.grid(row=8, column=0)


# canvas
image_area = Canvas(canvas_frames, bg='grey')
image_area.grid(row=0, column=1, sticky='nsew')
image_area.pack(fill='both', expand=True)
image_area.bind('<Motion>', motion)

# buttons under the canvas
photo_next = PhotoImage(file="icons/next.png")
next_image = Button(nepre_frame, text="Next Image", style="W.TButton", command=next_image, image=photo_next,
                    compound="right", state=['disabled'])
next_image.grid(row=0, column=2, sticky='e')
photo_prev = PhotoImage(file="icons/prev.png")
pre_image = Button(nepre_frame, text="Prev Image", style="W.TButton", command=prev_image, image=photo_prev,
                   compound="left", state=['disabled'])
pre_image.grid(row=0, column=0, sticky='w')

# Coordinates under canvas
coords_label = Label(nepre_frame, text="Select Shape for Coordinates", font=('calibri', 10, 'bold'))
coords_label.grid(row=0, column=1)


# listbox for labels
label_list = Listbox(properties_frame, width=40, height=20)
label_list.grid(row=2, column=2)

# entry
entry_button = Button(properties_frame, text="Add label", width=20, command=enter_labels)
entry_button.grid(row=1, column=2)

# label
label_entry = Entry(properties_frame, width=30)
label_entry.grid(row=0, column=2)
# -------
# label for folder list
label2 = Label(properties_frame, text="Images in the folder")
label2.grid(row=3, column=2)
# listbox for images in folder
folder_list = Listbox(properties_frame, width=40, height=30)
folder_list.grid(row=4, column=2)

# menubar
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=get_image_file_path)
filemenu.add_command(label="Open Folder", command=open_folder)
filemenu.add_command(label="Save Annotation")
filemenu.add_separator()
filemenu.add_command(label="Close Image", )
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)
menubar.add_cascade(label="File", menu=filemenu)

edit_menu = Menu(menubar, tearoff=0)
edit_menu.add_command(label="Select Area", command=draw_rect)
edit_menu.add_command(label="show Area")
edit_menu.add_command(label="Delete Area", command=clear_rectangle)
menubar.add_cascade(label="Edit", menu=edit_menu)

view_menu = Menu(menubar, tearoff=0)
view_menu.add_command(label="Zoom In")
view_menu.add_command(label="Zoom Out")
view_menu.add_separator()
view_menu.add_command(label="Show Labels")
menubar.add_cascade(label="View", menu=view_menu)

help_menu = Menu(menubar, tearoff=0)
help_menu.add_command(label="Tutorial", command=click_tutorial)
help_menu.add_command(label="About...")
menubar.add_cascade(label="Help", menu=help_menu)
window.config(menu=menubar)

window.mainloop()
