#!/usr/bin/env python3
"""
	User chooses level, that is number of titles.
"""

from tkinter import *
from PIL import Image, ImageTk
import re
__author__ = "Hailey Johnson, Krikor Herlopian, Charitha Sree Jayaramireddy , Syrina Haldiman and Tatiyana Bramwell"
__copyright__ = "Copyright 2021, University of New Haven Final Project"

"""
	This page to allow the user to choose the level of the game.
	Level 1 means 2*2
	Level 2 means 5*5
	Level 3 means 6*6
	Level 4 means 8*8
	Level 5 means 10*10
"""

def center_window(width=200, height=100):
	"""
		center screen on window
	"""
		
	# get screen width and height
	screen_width = master.winfo_screenwidth()
	screen_height = master.winfo_screenheight()	
	# calculate position x and y coordinates
	x = (screen_width/2) - (width/2)
	y = (screen_height/2) - (height/2)
	master.geometry('%dx%d+%d+%d' % (width, height, x, y))



master = Tk()
master.title("Set - Level")
center_window(407,85)


def onClick(i):
    #update lev.txt file with new level number.
    with open("lev.txt", "w") as f:
        f.write(str(i))
    print(str(i))#this returns value to caller
    master.destroy()
    return


#add image numbers to the screen as Buttons

image = Image.open("numbers/1.png")
image = image.resize((64, 64), Image.ANTIALIAS)
num_img = ImageTk.PhotoImage(image)

image2 = Image.open("numbers/2.png")
image2 = image2.resize((64, 64), Image.ANTIALIAS)
num_img2 = ImageTk.PhotoImage(image2)

image3 = Image.open("numbers/3.png")
image3 = image3.resize((64, 64), Image.ANTIALIAS)
num_img3 = ImageTk.PhotoImage(image3)

image4 = Image.open("numbers/4.png")
image4 = image4.resize((64, 64), Image.ANTIALIAS)
num_img4 = ImageTk.PhotoImage(image4)


image5 = Image.open("numbers/5.png")
image5 = image5.resize((64, 64), Image.ANTIALIAS)
num_img5 = ImageTk.PhotoImage(image5)

u = 10
level = [1,2,3,4,5]
l = 0
for i in range(1,6):    
	if i == 1:
		level_button = Button(master,compound = "center",image = num_img, width = 64, height = 64,font=('arial 15 bold'),highlightbackground='light blue' ,bg = "light blue",fg = 'midnight blue', command=lambda i=i: onClick(i))
	elif i == 2:
		level_button = Button(master,compound = "center",image = num_img2, width = 64, height = 64,font=('arial 15 bold'),highlightbackground='light blue' ,bg = "light blue",fg = 'midnight blue', command=lambda i=i: onClick(i))
	elif i == 3:
		level_button = Button(master,compound = "center",image = num_img3, width = 64, height = 64,font=('arial 15 bold'),highlightbackground='light blue' ,bg = "light blue",fg = 'midnight blue', command=lambda i=i: onClick(i))
	elif i == 4:
		level_button = Button(master,compound = "center",image = num_img4, width = 64, height = 64,font=('arial 15 bold'),highlightbackground='light blue' ,bg = "light blue",fg = 'midnight blue', command=lambda i=i: onClick(i))
	else:
		level_button = Button(master,compound = "center",image = num_img5, width = 64, height = 64,font=('arial 15 bold'),highlightbackground='light blue' ,bg = "light blue",fg = 'midnight blue', command=lambda i=i: onClick(i))
	
	level_button.place(x = u, y = 10)
	l = l + 1
	u = u + 80


mainloop()