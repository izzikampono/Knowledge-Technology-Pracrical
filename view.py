from tkinter import * 
from tkinter.ttk import *

from PIL import Image, ImageTk

root=Tk()
root.geometry("500x500")
# canvas.grid(column=2)

root.title("Halogenic Compound Classifier")



# my_button = Button(root, text="YES").pack()
# my_button2 = Button(root,text = "NO").pack()


def change():
    my_text=["HELLo","world"]
    my_label.config(text=my_text[0])
    my_label2.config(text=my_text[1])


my_button = Button(root,text = "Please update",width = 20,
                   command = change).grid(row=3,column=3)
#create labels
my_label = Label(root,text="TEST",font=('Helvetica 16 bold'))
my_label2 = Label(root,text="TEST2",font = ('Helvetica 16 bold'))

#placement of labels
my_label.grid(row=1,column=3)
my_label2.grid(row=2,column=3)


# my_label.pack()
# my_label2.pack()
#my_button.pack()

root.mainloop()