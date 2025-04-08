import mysql.connector
from tkinter import *

#tk stuff
root = Tk()
root.title("Elite 102 Project")
user_last_name = "not_set"
user_password = "not_set"

# building login screen
welcomeLabel = Label(root, text="Welcome to my project!", padx=20)
loginDirectionsLabel = Label(root, pady=10, text="Please enter your last name and account password.")
u_lname = Entry(root)
u_pass = Entry(root)

submitButton = Button(root, text="Login", command= lambda: select_user(u_lname.get(), u_pass.get()))

welcomeLabel.pack()
loginDirectionsLabel.pack()
u_lname.pack()
u_pass.pack()
submitButton.pack()

u_lname.insert(0, "Last Name")
u_pass.insert(0, "Password")



# Making connection to SQL Database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MldmAMT10/13",
    database="mydatabase"
)

mycursor = mydb.cursor()


# TODO call whenever submit button is pressed
# prints info on user where u_lname is last name and u_pass is user password
def select_user(u_lname, u_pass):
    cmd = "SELECT * FROM accounts WHERE namelast = %s AND password = %s"
    vals = (u_lname, u_pass)
    mycursor.execute(cmd, vals)

    print("")
    print("mycursor")
    print(mycursor)
    print("")

    accs_found = 0
    for x in mycursor:
        accs_found = accs_found + 1
        print("Found User: ")
        print(x) # x is a touple that represents the user (prints whole touple)

        # the 3rd element of the touple x is the first name
        # the 2nd element of the touple x is the last name
        print("User's Name = " + x[2] + " " + x[1])
    print(str(accs_found) + " account(s) found.")

    # Okay- at this point I want to give some type of response
        # if accs_found != 1: Error try again
        # else: Switch to a welcome screen for user
            # Welcome, u_name!
            # *display bank account details*



# main loop for graphics
root.mainloop()
    




# TESTING


#~~~~~
# testing connection to MySQL

# mycursor.execute("SELECT * from accounts")
# for x in mycursor:
#     print(x)
#~~~~~


#~~~~~
# testing function that prints user account info
# select_user("smith", "abc123")
#~~~~~