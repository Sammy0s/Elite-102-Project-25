import mysql.connector
import tkinter as tk

# For the template on how to use different pages with buttons using the pace and lift functions
# https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application
# Thank you, Bryan Oakley!!!

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Login(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        login_label = tk.Label(self, text="This is the login screen")


        # building login screen
        welcomeLabel = tk.Label(self, text="Welcome to my project!", padx=20)
        loginDirectionsLabel = tk.Label(self, pady=10, text="Please enter your last name and account password.")
        u_lname = tk.Entry(self)
        u_pass = tk.Entry(self)

        submitButton = tk.Button(self, text="Login", command = lambda: attempt_login(u_lname.get(), u_pass.get()))

        welcomeLabel.pack()
        loginDirectionsLabel.pack()
        u_lname.pack()
        u_pass.pack()
        submitButton.pack()
        login_label.pack(side="top", fill="both", expand=True)

        u_lname.insert(0, "Last Name")
        u_pass.insert(0, "Password")

class Page2(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 2")
       label.pack(side="top", fill="both", expand=True)

class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 3")
       label.pack(side="top", fill="both", expand=True)

def attempt_login(nm, pword):
    print("yay.")
    print(f"Last name: {nm}, Password: {pword}")
    p2.show()


# Globals ??
p_login = "not set"
p2 = "not set"
p3 = "not set"  

def display_p_login():
    p_login.show()

def display_p2():
    p2.show()

def display_p3():
    p3.show()



class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs) # call to parent class
        
        global p_login
        p_login = Login(self)

        global p2
        p2 = Page2(self)
        p3 = Page3(self)

        print("Set GPages")

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p_login.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        p_login.show() # shows p1 by deafult
        # p2.show()
        # p3.show()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sam's Bank of Elite 102 tm")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")


    root.mainloop()
    # Anything past this point only happens after the program is terminated. Good to know.







#### ~~~~~~~~~~~~SQL Backend stuff~~~~~~~~~~~~~~~~

# Making connection to SQL Database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="MldmAMT10/13",
    database="mydatabase"
)

mycursor = mydb.cursor()

# functions for utility ?


# TODO call whenever submit button is pressed
# prints info on user where u_lname is last name and u_pass is user password
def select_user(u_lname, u_pass):
    cmd = "SELECT * FROM accounts WHERE namelast = %s AND password = %s"
    vals = (u_lname, u_pass)
    mycursor.execute(cmd, vals)

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