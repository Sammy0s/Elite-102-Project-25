from tkinter import *

root = Tk()
root.title("Elite 102 Project")
user_last_name = "not_set"
user_password = "not_set"

def set_login_credits(ulname, upass):
    user_last_name = ulname
    user_password = upass

def login_screen():

    welcomeLabel = Label(root, text="Welcome to my project!", padx=20, pady=5)
    loginDirectionsLabel = Label(root, text="Please enter your last name and account password.")
    u_lname = Entry(root)
    u_pass = Entry(root)

    lnameLabel = Label(root, text=user_last_name, padx=20, pady=5)
    lpassLabel = Label(root, text=user_password, padx=20, pady=5)

    submitButton = Button(root, text="Login", command=set_login_credits(u_lname.get(), u_pass.get()))
    if (user_last_name != "not_set" and user_password != "not_set"):
        return (user_last_name, user_password)

    welcomeLabel.pack()
    u_lname.pack()
    u_pass.pack()
    submitButton.pack()
    lnameLabel.pack()
    lpassLabel.pack()

    u_lname.insert(0, "Last Name")
    u_pass.insert(0, "Password")
    root.mainloop()

