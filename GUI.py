import os
from tkinter import *
from tkinter import filedialog
from functools import reduce
from PIL import Image, ImageTk


root = Tk()
root.title('Meta Search Engine')
root.geometry("700x700")
initialDir = os.getcwd()+"/Data"
image = Image.open("trash.png")
image = image.resize((20, 20))
trashImage = ImageTk.PhotoImage(image)
label = []
removeButton = []
fileList = ["", "", ""]
def open():
    root.filename = filedialog.askopenfilename(initialdir = initialDir,title="Select a File", filetypes=(("txt files", "*.txt"),("all files", "*.*")) )
    for x in range(3):
        if fileList[x] == "":
            fileList[x] = root.filename[-23:]
            label[x].config(text = fileList[x])
            removeButton[x].grid(padx=10, pady=5, row=x, column=1)
            break

listFrame = LabelFrame(root, width=300, height=100, text = "File List...")
listFrame.grid(padx=10, pady=10, row=0, column=0, rowspan=3)
button1 = Button(root, text="Add File", width=15, command=open)
button1.grid(padx=30, pady=10, row=0, column=1)
button2 = Button(root, text="Process Data", width=15)
button2.grid(padx=30, pady=10, row=2, column=1)
for x in range (3):   
    label.append(Label(listFrame, text="", width=40, anchor="w",font=5))
    label[x].grid(padx=10, pady=5, row=x, column=0)
    removeButton.append(Button(listFrame, image=trashImage))

root.mainloop()