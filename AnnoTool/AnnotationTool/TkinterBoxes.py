import tkinter
from tkinter import *
from tkinter import filedialog

import cv2
from PIL import Image, ImageTk
import cv2 as cv
import numpy as np

import codecs

global image
mask = np.ones((490, 500))

app = Tk()
app.geometry('500x700')
app.state('zoomed')
def openInsertion():
    path = filedialog.askopenfile()
    if path:
        print(path)
        image = Image.open(path.name)
        print(image.width)
        test = ImageTk.PhotoImage(image)
        label1 = tkinter.Label(image=test)
        label1.image = test
        label1.place(relx=0.5, rely=0.5)


def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y


def draw_smth(event):
    global lasx, lasy
    image_area.create_line((lasx, lasy, event.x, event.y), fill='purple', width=2)
    lasx, lasy = event.x, event.y

    if lasx < 500 and lasx >= 0 and lasy < 400 and lasy >= 0:
        mask[lasy][lasx] = 0
        mask[lasy + 1][lasx + 1] = 0
        mask[lasy - 1][lasx - 1] = 0
        mask[lasy + 1][lasx - 1] = 0
        mask[lasy - 1][lasx + 1] = 0


def select_area():
    image_area.bind("<Button-1>", get_x_and_y)
    image_area.bind("<B1-Motion>", draw_smth)


def return_shape(image_in):
    image = image_in
    gray = image_in
    edged = cv2.Canny(gray, 30, 200)

    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    cv2.drawContours(image, contours, -1, (0, 0, 0), 3)
    th, im_th = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
    im_floodill = im_th.copy()
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(im_floodill, mask, (0, 0), (255, 255, 255))
    cv2.imshow("Floodfilled Image", im_floodill)
    im_floodill = np.abs(im_floodill - np.ones((490, 500)) * 255)
    #returned niks dus is useless atm

def show_mask():
    global image_for_mask_multiplication
    mask_3_channels = np.ones((490, 500, 3))

    image_mattt = (mask * 225).astype(np.uint8)
    the_real_mask = return_shape(image_mattt)

    mask_3_channels[:, :, :0] = the_real_mask / 255
    mask_3_channels[:, :, :1] = the_real_mask / 255
    mask_3_channels[:, :, :2] = the_real_mask / 255

    real_area = np.array(image_for_mask_multiplication) * mask_3_channels
    real_area = Image.fromarray(np.uint8(real_area)).convert('RGB')

    real_area.show()


def save_image():
    path_save = filedialog.asksaveasfilename()
    print(path_save)
    global img
    if path_save:
        img.save(str(path_save), 'PNG')


image_area = Canvas(app, width=490, height=500, bg='#008080')
image_area.pack()

open_image = tkinter.Button(app, width=20, text='Find Image', command=openInsertion)
open_image.pack()

crop_area = tkinter.Button(app, width=20, text='Select Area', command=select_area)
crop_area.pack()

show_area = tkinter.Button(app, width=20, text='Show Area', command=show_mask)
show_area.pack()

Save_Image = tkinter.Button(app, width=20, text='Save Image', command=save_image)
Save_Image.pack()

app.mainloop()
