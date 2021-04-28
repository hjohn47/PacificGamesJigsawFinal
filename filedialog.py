#!/usr/bin/env python3
"""
	Shows a file dialog for user to select a file to upload.
"""

import tkinter
import tkinter.filedialog
from tkinter import messagebox as mbox
from PIL import Image

__author__ = "Hailey Johnson, Krikor Herlopian, Charitha Sree Jayaramireddy , Syrina Haldiman and Tatiyana Bramwell"
__copyright__ = "Copyright 2021, University of New Haven Final Project"


def showFileDialog():
	try:
		image_file_name = tkinter.filedialog.askopenfilename(filetypes=[("Image File",['.jpg','.jpeg','.png'])])
		if image_file_name:
			image = Image.open(image_file_name)
			width, height = image.size
			# let us check the image size meets criteria of application.if not let us prompt user to choose different file
			if width <= 500 or height <= 500 or width >= 700 or height >= 700:
				mbox.showinfo("Image Size", "Image width and height size cannot be less than 500 pixel or more than 700 pixel")	
				showFileDialog()
			else:	
				print(image_file_name)
	except:
		pass
		
		
try:
	top = tkinter.Tk()
	top.withdraw()  # hide window
	showFileDialog()
	top.destroy()
except:
	pass
	

	

