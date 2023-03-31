import os
import ProcessData as PD
from tkinter import *
from tkinter import filedialog
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
            if fileList[x] != "":
                label[x].config(text = fileList[x])           
                removeButton[x].grid(padx=10, pady=5, row=x, column=1)
                removeButton[x].config( command=lambda: removeFile(x))
                disableButton()
                break
    
def removeFile(number):
    label[number].config(text = "")
    fileList[number] = ""
    removeButton[number].grid_forget()
    button1.config(state=NORMAL)
    button2.config(state=DISABLED)

def disableButton():
    if "" not in fileList:
        button1.config(state=DISABLED)
        button2.config(state=NORMAL)

def processData(fileList):
    evaluation.config(text=PD.evaluation(fileList))
#First fame is for Data File input
frame1 = Frame(root, width=700, height=200)
frame1.pack()

#Second fame is for Evaluation message
frame2 = Frame(root, width=700, height=500)
frame2.pack()

#Implement compenents for frame1
listFrame = LabelFrame(frame1, width=300, height=100, text = "File List...")
listFrame.grid(padx=10, pady=10, row=0, column=0, rowspan=3)
button1 = Button(frame1, text="Add File", width=15, command=open)
button1.grid(padx=30, pady=10, row=0, column=1)
button2 = Button(frame1, text="Process Data", width=15, state=DISABLED, command=lambda: processData(fileList))
button2.grid(padx=30, pady=10, row=2, column=1)
for x in range (3):   
    label.append(Label(listFrame, text="", width=40, anchor="w",font=5))
    label[x].grid(padx=10, pady=5, row=x, column=0)
    removeButton.append(Button(listFrame, image=trashImage))

#Implement compenents for frame2
evaluation = Label(frame2, text="", padx= 20, pady=20)
evaluation.pack()

root.mainloop()