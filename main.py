import mysql.connector
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

    submitButton = Button(root, text="Login", command= lambda: login_attempt(u_lname.get(), u_pass.get()))
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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import==

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MldmAMT10/13",
    database="mydatabase"
)

mycursor = mydb.cursor()

test = "owner = 'Josh'"

# mycursor.execute("")

# for x in mycursor:
#     print(x)

def login_attempt(last_name, u_pass):
    set_login_credits(last_name, u_pass)
    login_credits = (last_name, u_pass)
    login_select_query = "select * from accounts where namelast = %s and password = %s"
    mycursor.execute(login_select_query, login_credits)
    

    for x in mycursor:
        print(x)
        

def start():
    login_screen()

start()

# login_attempt('smiths','abc123')
