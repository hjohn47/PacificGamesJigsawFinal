import tkinter
import random
import json
from tkinter import *
from tkinter import ttk
import tkinter as tk
from datetime import datetime
import time
import subprocess
from tkinter import messagebox
#import menu.py

global user_select
user_select = ""

root = tkinter.Tk()
root.title("Stress Level Survey")
root.geometry("700x600")
root.config(background="white")
root.resizable(0,0)

#label creation
label = tk.Label(text="How stressed are you on a scale of 1-5 (1 being no stress at all and 5 being very overwhelmed)?\n", font=('Arial', 15)).grid(column=0, row=0)
#label.config(font=('Courier', 20))

#Action
def radioCall():
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

#Create 5 Radio Button
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

def ButtonCallBack():
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
   

button = tk.Button(root, text="Submit", bg='#1E90FF', command=ButtonCallBack)
button.place(x=500, y=200)

def disable_event():
   messagebox.showinfo("Message", "Please answer the stress survey and press 'submit' to continue to the game")
root.protocol("WM_DELETE_WINDOW", disable_event)

#Calling Main()
root.mainloop()


