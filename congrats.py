from tkinter import *
from PIL import ImageTk, Image
def center_window(width=800, height=800):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    

root = Tk()
root.title("Jigsaw - Congratulations")

#root.geometry("800x800+0+0")

center_window()
back_img = Image.open('congrats1.png')
back_img = back_img.resize((770, 770), Image.ANTIALIAS)
back_img1 = ImageTk.PhotoImage(back_img)
background_label = Label(root, image=back_img1, compound = "left", bg = "white", fg = None)
background_label.pack(side = "top", fill ="both")
background_label.place(x=0, y=0, relwidth = 1, relheight = 1)
i = 0
def destroy():
    root.destroy()

root.after(4000, destroy)


root.mainloop()
