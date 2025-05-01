import mysql.connector
import tkinter as tk



class user():
    u_id = -1
    u_lastname = "not set"
    u_firstname = "not set"
    u_password = "not set"
    u_balance = -1
    u_email = "not set"
    u_tuple = ()

    def __init__(self, u_tuple):
        self.u_tuple = u_tuple
        self.u_id = u_tuple[0]
        self.u_lastname = u_tuple[1]
        self.u_firstname = u_tuple[2]
        self.u_password = u_tuple[3]
        self.u_balance = u_tuple[4]
        self.u_email = u_tuple[5]
    
    def new_assign(self, u_tuple):
        self.u_tuple = u_tuple
        self.u_id = u_tuple[0]
        self.u_lastname = u_tuple[1]
        self.u_firstname = u_tuple[2]
        self.u_password = u_tuple[3]
        self.u_balance = u_tuple[4]
        self.u_email = u_tuple[5]
    
    # updates self's 
    def reset(self):
        u_tuple = get_u_tuple(self.u_id)
        self.new_assign(u_tuple)

    # returns self's user id
    def get_id(self):
        return self.u_id
    
    # withdraws money from an account.
    def user_withdraw(self, amm):
        withdraw_from_account(self.u_id, amm)
        self.reset()
    
    def user_deposit(self, amm):
        deposit_into_account(self.u_id, amm)
        self.reset()
    
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

# the_user is a user object
# ammount_to_withdraw is a float/double value
# backend use only. Should only be called through the user class
def withdraw_from_account(u_id, ammount_to_withdraw):
    #first I need to find the current balance
    start_balance = get_u_tuple(u_id)[4] # index 4 is the balance
    withdraw_ammount = start_balance - ammount_to_withdraw
    cmd = "UPDATE accounts SET balance = %s WHERE id = %s"
    vals = (withdraw_ammount, u_id)
    mycursor.execute(cmd, vals)
    mydb.commit()

def deposit_into_account(u_id, ammount_to_deposit):
    #first I need to find the current balance
    start_balance = get_u_tuple(u_id)[4] # index 4 is the balance
    deposit_ammount = start_balance + ammount_to_deposit
    cmd = "UPDATE accounts SET balance = %s WHERE id = %s"
    vals = (deposit_ammount, u_id)
    mycursor.execute(cmd, vals)
    mydb.commit()
    
def get_u_tuple(u_id):
    mycursor.execute(f"SELECT * FROM accounts WHERE id = {u_id}")

    accs_found = 0
    u_tuple = ()
    for x in mycursor:
        accs_found = accs_found + 1
        # print("Found User: ")
        # print(x) # x is a tuple that represents the user (prints whole tuple)

        # the 3rd element of the tuple x is the first name
        # the 2nd element of the tuple x is the last name
        u_tuple = x

    # print(str(accs_found) + " account(s) found.")

    if (accs_found > 1):
        raise Exception("Error- Multiple accounts found. Duplicate accounts?")
    elif(accs_found == 0):
        raise Exception("Error- No accounts found. Does user id exist?")
    
    return u_tuple



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
        # print(x) # x is a tuple that represents the user (prints whole tuple)

        # the 3rd element of the tuple x is the first name
        # the 2nd element of the tuple x is the last name
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


        return cur_user
    elif (accs_found == 0):
        global loginErrorLabel
        loginErrorLabel.config(text="Incorrect name or password. Please try again.")
        return None
    return None



# Globals ??

def display_p_login():
    p_login.show()

def display_u_dashboard():
    p_dash.show()

def display_p_log_conf():
    p_log_conf.show()





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
        global loginErrorLabel
        loginErrorLabel = tk.Label(self, pady=10, text="")
        global u_lname
        u_lname = tk.Entry(self)
        global u_pass
        u_pass = tk.Entry(self)

        submitButton = tk.Button(self, text="Login", command = lambda: attempt_login(u_lname.get(), u_pass.get()))

        welcomeLabel.pack()
        loginDirectionsLabel.pack()
        u_lname.pack()
        u_pass.pack()
        submitButton.pack()
        loginErrorLabel.pack()
        login_label.pack(side="top", fill="both", expand=True)

        
        u_lname.insert(0, "Last Name")
        u_pass.insert(0, "Password")

class u_dashboard(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is the user dashboard")
       global wel
       wel = tk.Label(self, text=f"Welcome back, {cur_user.u_firstname}!!")
       global dis_balance
       dis_balance = tk.Label(self, pady=10, text=f"Your current balance is: {cur_user.u_balance}.")
       # dis_rec_trans = tk.Label(self, text=f"Your most recent transaction: \n {cur_user.get_rec_trans()}") TODO most recent transactions require transactions database
       global p_dep
       button_deposit = tk.Button(self, text="Deposit Money", command = lambda: p_dep.show())
       global p_with
       button_withdrawl = tk.Button(self, text="Withdrawl Money", command = lambda: p_with.show())

       button_logout = tk.Button(self, text="Logout to sign in screen", command = lambda: attempt_logout(False))


       wel.pack()
       dis_balance.pack()

       button_deposit.pack()
       button_withdrawl.pack()

       button_logout.pack()

       label.pack(side="top", fill="both", expand=True)

class logout_confrim(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is the logout confrimation screen")
       log_out_label = tk.Label(self, text="Are you sure you want to logout?")
       button_logout = tk.Button(self, text="Logout", command = lambda: attempt_logout(True))
       button_to_dash = tk.Button(self, text="Back to Dashboard", command = lambda: p_dash.show())

       log_out_label.pack()
       button_logout.pack()
       button_to_dash.pack()
       label.pack(side="top", fill="both", expand=True)

class withdraw(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is the withdraw page")
       withdraw_label = tk.Label(self, text="How much would you like to withdraw?")
       #TODO I need an entry box to get the ammount the user wants to withdraw: entry
       global u_with_amm
       u_with_amm = tk.Entry(self)
       button_submit = tk.Button(self, text="submit", command = lambda: attempt_withdraw(u_with_amm.get()))
       button_to_dash = tk.Button(self, text="Cancel", command = lambda: p_dash.show())

       withdraw_label.pack()
       u_with_amm.pack()
       button_submit.pack()
       button_to_dash.pack()
       label.pack(side="top", fill="both", expand=True)

class deposit(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is the deposit page")
       deposit_label = tk.Label(self, text="How much would you like to deposit?")
       #TODO I need an entry box to get the ammount the user wants to deposit: entry
       global u_dep_amm
       u_dep_amm = tk.Entry(self)
       button_submit = tk.Button(self, text="submit", command = lambda: attempt_deposit(u_dep_amm.get()))
       button_to_dash = tk.Button(self, text="Cancel", command = lambda: p_dash.show())

       deposit_label.pack()
       u_dep_amm.pack()
       button_submit.pack()
       button_to_dash.pack()
       label.pack(side="top", fill="both", expand=True)

class withdraw_confrim(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       global with_conf
       with_conf = tk.Label(self, text="This is the withdraw confrimation screen.")
       log_out_label = tk.Label(self, text="Withdraw confrimation")
       button_to_dash = tk.Button(self, text="Back to Dashboard", command = lambda: p_dash.show())

       log_out_label.pack()
       button_to_dash.pack()
       with_conf.pack(side="top", fill="both", expand=True)

class deposit_confrim(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       global dep_conf
       dep_conf = tk.Label(self, text="This is the deposit confrimation screen.")
       log_out_label = tk.Label(self, text="Deposit confrimation")
       button_to_dash = tk.Button(self, text="Back to Dashboard", command = lambda: p_dash.show())

       log_out_label.pack()
       button_to_dash.pack()
       dep_conf.pack(side="top", fill="both", expand=True)

def update_gui():
    global wel
    wel.config(text = f"Welcome back, {cur_user.u_firstname}!!")
    global dis_balance
    dis_balance.config(text=f"Your current balance is: {cur_user.u_balance}.")

    global u_lname
    txt = u_lname.get()
    u_lname.delete(0, len(txt))
    u_lname.insert(0, "Last Name")
    global u_pass
    txt = u_pass.get()
    u_pass.delete(0, len(txt))
    u_pass.insert(0, "Password")

    global with_conf
    with_conf.config(text=f"Hm. Something went wrong.")

    global u_with_amm
    txt = u_with_amm.get()
    u_with_amm.delete(0, len(txt))
    
    global u_dep_amm
    txt = u_dep_amm.get()
    u_dep_amm.delete(0, len(txt))

    global dep_conf
    dep_conf.config(text=f"Hm. Something went wrong.")


def attempt_logout(confrimed):
    if (confrimed == False):
        p_log_conf.show()
    else:
        update_gui()
        p_login.show()

def attempt_login(nm, pword):
    # print("yay.")
    # print(f"Last name: {nm}, Password: {pword}")
    if (select_user(nm, pword) != None):
        #TODO set cur_user to user that just logged in
        global cur_user
        cur_user = select_user(nm, pword)
        update_gui()

        p_dash.show()

def attempt_withdraw(ammount):
    # TODO needs to validate user input and then if it's okay it needs to withdraw funds from user account
    # Returns error/success message to be displayed on confrimation screen.
    try:
        w_ammount = int(ammount)
    except:
        with_conf.config(text=f"Error: Ammount to withdraw must be a float value (Must be a number)")
        p_with_con.show()
    if (cur_user.u_balance < w_ammount):
        with_conf.config(text=f"Error: Insufficient funds")
        p_with_con.show()
    if (cur_user.u_balance > w_ammount):
        # TODO I need to make methods that will edit the database instead of just the user object
        # cur_user.u_balance = cur_user.u_balance-w_ammount
        cur_user.user_withdraw(w_ammount)
        update_gui()
        with_conf.config(text=f"Successfully withdrew {w_ammount} from your account!")
        p_with_con.show()

def attempt_deposit(ammount):
    # Returns error/success message to be displayed on confrimation screen.
    try:
        d_ammount = int(ammount)
    except:
        dep_conf.config(text=f"Error: Ammount to withdraw must be a float value (Must be a number)")
        p_dep_con.show()
    
    # cur_user.u_balance = cur_user.u_balance-w_ammount
    cur_user.user_deposit(d_ammount)
    update_gui()
    dep_conf.config(text=f"Successfully deposited {d_ammount} into your account!")
    p_dep_con.show()
    

# ~~~~~~~~~~~~~~~~~~~~

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs) # call to parent class

        global p_login
        p_login = Login(self)

        global p_dash
        p_dash = u_dashboard(self)

        global p_log_conf
        p_log_conf = logout_confrim(self)

        global p_with
        p_with = withdraw(self)

        global p_dep
        p_dep = deposit(self)

        global p_with_con
        p_with_con = withdraw_confrim(self)

        global p_dep_con
        p_dep_con = deposit_confrim(self)

        print("Set GPages")

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p_login.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_dash.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_log_conf.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_with.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_dep.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_with_con.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_dep_con.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        p_login.show() # shows p1 by deafult
        # p2.show()
        # p_log_conf.show()
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
# print(f"This is a user account's last name: {aldair.u_tuple}")

# testing the user.reset() command. Should update info in user.u_tuple.
# cmd = "UPDATE accounts SET balance = %s WHERE id = %s"
# vals = (101, 6)
# mycursor.execute(cmd, vals)
# mydb.commit()

# print("resets")

# aldair.reset()

# testing the user.user_deposit command
# aldair.user_deposit(15)

# print(f"This is a user account's last name: {aldair.u_lastname}")
# print(f"This is a user account's last name: {aldair.u_tuple}")



# ~~~~~

#testing how to withdraw from the database. 
# I learned that commiting is important if you're changing something in the table.

# print("pre: "+str(aldair.u_balance))
# withdraw_from_account(6, 12)

# mycursor.execute("UPDATE accounts SET balance = 102 WHERE id = 6")

# mydb.commit()
# print("post: "+str(aldair.u_balance))


# backend SQL get u_tuple function
# prints the 3rd element from the u_tuple that gets returned when the user id is provided.
# print("Trying to print u_tuple for user id 6: " + str(get_u_tuple(6)[2]))
#~~``




# MAIN LOOP~~~~~

if __name__ == "__main__":
    cur_user = user((-1, "not_set", "not_set", "not_set", -1, "not_set"))

    root = tk.Tk()
    root.title("Sam's Bank of Elite 102 (trademarked)")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")

    root.mainloop()
#     # Anything past this point only happens after the program is terminated. Good to know.