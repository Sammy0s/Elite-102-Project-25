from tkinter import *

root = Tk()
root.title("Elite 102 Project")

def enterName():
    greating = "Welcome, " + e.get() + "!"
    welcome_label = Label(root, text=greating)
    welcome_label.pack()

welcomeLabel = Label(root, text="Welcome to my project!", padx=20, pady=5)
e = Entry(root)
submitButton = Button(root, text="Submit", command=enterName)


welcomeLabel.pack()
e.pack()
submitButton.pack()

e.insert(0, "Enter Your Name")

root.mainloop()