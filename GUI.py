import os
import ProcessData as PD
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk


root = Tk()
root.title('Meta Search Engine')
root.geometry("800x700")
initialDir = os.getcwd()+"/Data"
image = Image.open("trash.png")
image = image.resize((20, 20))
trashImage = ImageTk.PhotoImage(image)
label = []
removeButton = []
fileList = ["", "", ""]
selectedOption = StringVar(value="Mean Score")

def openFile():
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
a=0
def processData(fileList):
    substrings = [element[-6:-4] for element in fileList]
    string = '-'.join(substrings)
    option = selectedOption.get()
    evaluation.config(text=PD.evaluation(fileList, selectedOption.get()))
    fileLabel = Label(fileFrame, text="output-format-"+string+"-"+option+".txt", padx= 10, pady=10)
    fileLabel.grid(padx=10, pady=10, row=0, column=0, sticky="w")
    fileButton = Button(fileFrame, text="Open file", command=lambda: showContent("output-format-"+string+"-"+option+".txt"))
    fileButton.grid(padx=40, pady=10, row=0, column=1)
    vsb.pack(side="right", fill="y")

def showContent(fileName):
    canvas.configure(scrollregion=())
    canvas.unbind_all("<MouseWheel>")
    with open("Export Data/"+fileName, "r") as f:
        contents = f.read()
    top = Toplevel()
    text = Text(top)
    text.insert("1.0", contents)
    text.pack(fill="both", expand=True)
    top.wait_window()
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.bind_all("<MouseWheel>", on_mousewheel)

#First fame is for Data File input
frame1 = Frame(root, width=700, height=200)
frame1.pack()

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

#Second fame is for Evaluation message


frame2 = Frame(root, width=700, height=500)
frame2.pack()

fileFrame = Frame(frame2, width=700, height=50)
fileFrame.pack(side="top", fill="x", expand=True)


canvas = Canvas(frame2, borderwidth=0, highlightthickness=0, width=700, height=450)
frame3 = Frame(canvas)
vsb = Scrollbar(frame2, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4, 4), window=frame3, anchor="nw", tags="frame")
frame3.bind("<Configure>", on_frame_configure)
canvas.bind_all("<MouseWheel>", on_mousewheel)

#Implement compenents for adding file to the GUI
listFrame = LabelFrame(frame1, width=550, height=150, text = "File List...")
listFrame.grid(padx=10, pady=10, row=0, column=0, rowspan=3)
listFrame.grid_propagate(False)
button1 = Button(frame1, text="Add File", width=15, command=openFile)
button1.grid(padx=30, pady=10, row=0, column=1)
menu_button = Menubutton(frame1, textvariable=selectedOption, width=15, relief=RAISED, borderwidth=2, highlightbackground="#555", padx=10, pady=5)
menu_button.grid(padx=30, pady=10, row=1, column=1)
dropdown_menu = Menu(menu_button, tearoff=False)
dropdown_menu.add_radiobutton(label="Mean Score", variable=selectedOption, value="Mean Score")
dropdown_menu.add_radiobutton(label="K-mean", variable=selectedOption, value="K-mean")
dropdown_menu.add_radiobutton(label="Decision Tree", variable=selectedOption, value="Decision Tree")
menu_button.config(menu=dropdown_menu)

button2 = Button(frame1, text="Process Data", width=15, state=DISABLED, command=lambda: processData(fileList))
button2.grid(padx=30, pady=10, row=2, column=1)
for x in range (3):   
    label.append(Label(listFrame, text="", width=40, anchor="w",font=5))
    label[x].grid(padx=10, pady=5, row=x, column=0)
    removeButton.append(Button(listFrame, image=trashImage))

evaluation = Label(frame3, text="", padx= 10)
evaluation.pack()

root.mainloop()