import tkinter
import random
import json
import tkinter as tk
from datetime import datetime
import time
import subprocess
from tkinter import messagebox

"""
	Stress Survey, this will survey the user on his stress level before the game starts and when user closes the game
"""

#user selected radio button
global user_select
user_select = ""

root = tk.Tk()
root.title("Stress Level Survey")
root.config(background="white")
root.resizable(0,0)

#label creation
label = tk.Label(text="\nHow stressed are you on a scale of 1-5 (1 being no stress at all and 5 being very overwhelmed)?\n", font=('Arial', 15)).grid(column=0, row=0,padx=(10, 10))
#label.config(font=('Courier', 20))

#Action. 
def radioCall():
	"""
		When Radio Button selected, we update user_select with latest value chosen
	"""
	radioSel=radioVar.get()
	global user_select
	if radioSel== 1:
		user_select = "Selected 1, no stress"
	elif radioSel== 2:
		user_select = "Selected 2, very little stress"
	elif radioSel== 3:
		user_select = "Selected 3, somewhat stressed"
	elif radioSel== 4:
		user_select = "Selected 4, pretty stressed"
	elif radioSel== 5:
		user_select = "Selected 5, very stressed/overwhelmed"

#Create 5 Radio Button, for stress level 1 2 3 4 5
radioVar= tk.IntVar()
radio1=tk.Radiobutton(root, text="1", variable=radioVar, value=1, command=radioCall)
radio1.grid(column=0,row=3, columnspan=5)
radio2=tk.Radiobutton(root, text="2", variable=radioVar, value=2, command=radioCall)
radio2.grid(column=0,row=4, columnspan=5)
radio3=tk.Radiobutton(root, text="3", variable=radioVar, value=3, command=radioCall)
radio3.grid(column=0,row=5, columnspan=5)
radio4=tk.Radiobutton(root, text="4", variable=radioVar, value=4, command=radioCall)
radio4.grid(column=0,row=6, columnspan=5)
radio5=tk.Radiobutton(root, text="5", variable=radioVar, value=5, command=radioCall)
radio5.grid(column=0,row=7, columnspan=5)

def center_window(width=800, height=800):
	"""
		this will center the screen on window
	"""
	# get screen width and height
	screen_width = root.winfo_screenwidth()
	screen_height = root.winfo_screenheight()
	# calculate position x and y coordinates
	x = (screen_width/2) - (width/2)
	y = (screen_height/2) - (height/2)
	root.geometry('%dx%d+%d+%d' % (width, height, x, y))
	
def ButtonCallBack():
	"""
		When submit Button selected, we will write the result to stressSurveyResults.txt
		If user hasnt selected a radiobutton, just show him popup message that he needs to do selection before submitting
	"""
	if user_select:
		with open("stressSurveyResults.txt", 'a') as file2:
			file2.write("\n")
			localtime = time.asctime(time.localtime(time.time()))
			file2.write(localtime + ": ")
			#file2.write(str(date.today()))
			file2.write(user_select)
		root.destroy()
	else:
		messagebox.showinfo("Message", "Please make a selection")
	#subprocess.check_output([sys.executable, "main.py"])
   

button = tk.Button(root, text="Submit", bg='#1E90FF',width=10, command=ButtonCallBack)
button.grid(row=9,column=0,columnspan=5,pady=(20,20))

def disable_event():
	"""
		when user clicks the X on top side corner, we make sure to force him to do this survey and not close it.
	"""
	messagebox.showinfo("Message", "Please answer the stress survey and press 'submit' to continue to the game")

#disable closing survey without submitting
root.protocol("WM_DELETE_WINDOW", disable_event)

center_window(670,240)
#Calling Main()
root.mainloop()


