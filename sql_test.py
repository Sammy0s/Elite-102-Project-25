import mysql.connector
import tkinter as tk



class user():
    u_id = -1
    u_lastname = "not set"
    u_firstname = "not set"
    u_password = "not set"
    u_balance = -1
    u_email = "not set"

    def __init__(self, u_tuple):
        self.u_id = u_tuple[0]
        self.u_lastname = u_tuple[1]
        self.u_firstname = u_tuple[2]
        self.u_password = u_tuple[3]
        self.u_balance = u_tuple[4]
        self.u_email = u_tuple[5]
    
    def new_assign(self, u_tuple):
        self.u_id = u_tuple[0]
        self.u_lastname = u_tuple[1]
        self.u_firstname = u_tuple[2]
        self.u_password = u_tuple[3]
        self.u_balance = u_tuple[4]
        self.u_email = u_tuple[5]
    
    def __str__(self):
        return f"User: lastname: {self.u_lastname}, acc id: {self.u_id}"




def test_user_object(user_obj, user_id):
        mycursor.execute(f"Select * from accounts where id = {user_id}")
        global test_user
        test_user = None
        for x in mycursor:
            print(x)
            test_user = user(x)
        
        if("first names are equal: " + str(user_obj.u_firstname == test_user.u_firstname)):
            if("last names are equal: " + str(user_obj.u_lastname == test_user.u_lastname)):
                if("passwords are equal: " + str(user_obj.u_password == test_user.u_password)):
                    return True
        return False 



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
    u_tuple = ()
    for x in mycursor:
        accs_found = accs_found + 1
        # print("Found User: ")
        # print(x) # x is a touple that represents the user (prints whole touple)

        # the 3rd element of the touple x is the first name
        # the 2nd element of the touple x is the last name
        print("User's Name = " + x[2] + " " + x[1])
        u_tuple = x

    print(str(accs_found) + " account(s) found.")

    if (accs_found > 1):
        print("Error- Multiple accounts found. Duplicate accounts?")
        return None
    elif (accs_found == 1):
        global cur_user
        cur_user.new_assign(u_tuple)
        
        print(cur_user)
        print("test cur_user: " + str(test_user_object(cur_user, 6)))
        print("Welcome, " + cur_user.u_firstname + "!!")

        global wel
        wel.config(text = f"Welcome back, {cur_user.u_firstname}!!")
        global dis_balance
        dis_balance.config(text=f"Your current balance is: {cur_user.u_balance}.")

        return cur_user
    elif (accs_found == 0):
        return None
    return None



# Globals ??

def display_p_login():
    p_login.show()

def display_u_dashboard():
    p_dash.show()

def display_p3():
    p3.show()





# For the template on how to use different pages with buttons using the place and lift functions
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

class u_dashboard(Page):
   def __init__(self, *args, **kwargs):
       global cur_user
       print(cur_user)
       
       t_cur_user = cur_user

       print("Set name to: " + cur_user.u_firstname)

       print("Set balance to: " + str(cur_user.u_balance))
       

       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is the user dashboard")
       global wel
       wel = tk.Label(self, text=f"Welcome back, {cur_user.u_firstname}!!")
       global dis_balance
       dis_balance = tk.Label(self, pady=10, text=f"Your current balance is: {cur_user.u_balance}.")
       # dis_rec_trans = tk.Label(self, text=f"Your most recent transaction: \n {cur_user.get_rec_trans()}") TODO most recent transactions require transactions database
       button_deposit = tk.Button(self, text="Deposit Money", command = lambda: print("Deposit Money Button Pressed"))
       button_withdrawl = tk.Button(self, text="Withdrawl Money", command = lambda: print("Withdrawl Money Button Pressed"))

       button_logout = tk.Button(self, text="Logout to sign in screen", command = lambda: print("Logout Button Pressed"))


       wel.pack()
       dis_balance.pack()

       button_deposit.pack()
       button_withdrawl.pack()

       button_logout.pack()

       label.pack(side="top", fill="both", expand=True)

class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 3")
       label.pack(side="top", fill="both", expand=True)

def attempt_login(nm, pword):
    print("yay.")
    print(f"Last name: {nm}, Password: {pword}")
    if (select_user(nm, pword) != None):
        #TODO set cur_user to user that just logged in
        global cur_user
        cur_user = select_user(nm, pword)

        p_dash.show()
    

# ~~~~~~~~~~~~~~~~~~~~

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs) # call to parent class
        
        global the_user_object_plz_work
        print(the_user_object_plz_work)

        global p_login
        p_login = Login(self)

        global p_dash
        p_dash = u_dashboard(self)

        global p3
        p3 = Page3(self)

        print("Set GPages")

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p_login.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_dash.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        p_login.show() # shows p1 by deafult
        # p2.show()
        # p3.show()
# end of graphics section


# TESTING


import unittest

class TestUserClass(unittest.TestCase):
    

    def test_new_user_object(self):
        mycursor.execute("Select * from accounts where namelast = 'Mendez-Tigre'")
        global aldair
        aldair = None
        for x in mycursor:
            print(x)
            aldair = user(x)
        self.assertEqual(aldair.u_firstname, "Aldair")
        self.assertEqual(aldair.u_lastname, "Mendez-Tigre")
        self.assertEqual(aldair.u_password, "123bird")

    


# if __name__ == '__main__':
#     unittest.main()
     

# print("TestUserObj Test Success?: " + str(test_user_object(worldwide.cur_user, 6)))
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

# testing the new user class~~~
# mycursor.execute("Select * from accounts where namelast = 'Mendez-Tigre'")
# aldair = None
# for x in mycursor:
#     print(x)
#     aldair = user(x)
# print("testt")
# # user()
# print(f"This is a user account's last name: {aldair.u_lastname}")
# ~~~~~


# MAIN LOOP~~~~~

if __name__ == "__main__":
    cur_user = user((-1, "not_set", "not_set", "not_set", -1, "not_set"))
    the_user_object_plz_work = "ah yes this is working"


    root = tk.Tk()
    root.title("Sam's Bank of Elite 102 (trademarked)")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")

    root.mainloop()
    # Anything past this point only happens after the program is terminated. Good to know.