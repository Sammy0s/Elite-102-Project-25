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
    
    def user_update(self, c_tuple):
        # c_tuple is a user creation tuple that has namelast, namefirst, password, and email of the user (in that order.)

        self.u_lastname = c_tuple[0]
        self.u_firstname = c_tuple[1]
        self.u_password = c_tuple[2]
        self.u_email = c_tuple[3]
    
    # updates self's 
    def reset(self):
        u_tuple = get_u_tuple(self.u_id)
        self.new_assign(u_tuple)

    # returns self's user id
    def get_id(self):
        return self.u_id

    def get_lname(self):
        return self.u_lastname
    
    def get_fname(self):
        return self.u_firstname
    
    def get_pass(self):
        return self.u_password
    
    def get_bal(self):
        return self.u_balance
    
    def get_email(self):
        return self.u_email
    
    def get_u_tuple(self):
        return self.u_tuple
    
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

def add_account(c_tuple, do_commit):
    # c_tuple is a user creation tuple that has namelast, namefirst, password, and email of the user (in that order.)

    u_lastname = c_tuple[0]
    u_firstname = c_tuple[1]
    u_password = c_tuple[2]
    u_email = c_tuple[3]


    # Inserts the user info into a new row in the database
    mycursor.execute(f"INSERT INTO accounts (namelast, namefirst, password, balance, email) VALUES ('{u_lastname}', '{u_firstname}', '{u_password}', 0, '{u_email}')")
    if (do_commit):
        mydb.commit()

def update_account(c_tuple, do_commit):
    # c_tuple is a user creation tuple that has namelast, namefirst, password, and email of the user (in that order.)


    u_lastname = c_tuple[0]
    u_firstname = c_tuple[1]
    u_password = c_tuple[2]
    u_email = c_tuple[3]

    user_id = cur_user.get_id()


    # Inserts the user info into a new row in the database
    # f"UPDATE accounts SET namelast='{u_lastname}', namefirst='u_firstname', password='u_password', email='{u_email}'"
    mycursor.execute(f"UPDATE accounts SET namelast='{u_lastname}', namefirst='{u_firstname}', password='{u_password}', email='{u_email}' WHERE id = {user_id}")
    if (do_commit):
        mydb.commit()


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
        u_pass = tk.Entry(self, show="*")

        submitButton = tk.Button(self, text="Login", command = lambda: attempt_login(u_lname.get(), u_pass.get()))

        new_user_directions = tk.Label(self, pady=1, text="New user?")
        new_acc_Button = tk.Button(self, text="Create Account", command = lambda: p_create_acc.show())
        

        welcomeLabel.pack()
        loginDirectionsLabel.pack()
        u_lname.pack()
        u_pass.pack()
        submitButton.pack()
        loginErrorLabel.pack()
        
        new_user_directions.pack()
        new_acc_Button.pack()

        login_label.pack(side="top", fill="both", expand=True)
        
        u_lname.insert(0, "Last Name")
        u_pass.insert(0, "Password")

class Create_acc(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        login_label = tk.Label(self, text="This is the account creation screen")


        # building account creation screen
        createLabel = tk.Label(self, text="Welcome!", padx=20)
        createDirectionsLabel = tk.Label(self, pady=10, text="Let's get you set up.")
        
        global create_fname
        create_fname = tk.Entry(self)
        global create_lname
        create_lname = tk.Entry(self)
        global create_email
        create_email = tk.Entry(self)
        global create_pass
        create_pass = tk.Entry(self, show="*")


        # submitButton = tk.Button(self, text="Login", command = lambda: attempt_login(u_lname.get(), u_pass.get()))
        create_account = tk.Button(self, text="Create Account", command = lambda: attempt_acc_creation())
        button_logout = tk.Button(self, text="Logout", command = lambda: attempt_logout(True))


        # packing acc creation
        createLabel.pack()
        createDirectionsLabel.pack()

        create_fname.pack()
        create_lname.pack()
        create_email.pack()
        create_pass.pack()

        create_account.pack()
        button_logout.pack()


        # config acc creation
        create_fname.insert(0, "First Name")
        create_lname.insert(0, "Last Name")
        create_email.insert(0, "Email")
        create_pass.insert(0, "Pass")

class Edit_acc(Page):
   def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        edit_label = tk.Label(self, text="This is the account update/edit screen")


        # building account creation screen
        editLabel = tk.Label(self, text="Welcome!", padx=20)
        editDirectionsLabel = tk.Label(self, pady=10, text="Update any details you want to change.")
        
        global edit_fname
        edit_fname = tk.Entry(self)
        global edit_lname
        edit_lname = tk.Entry(self)
        global edit_email
        edit_email = tk.Entry(self)
        global edit_pass
        edit_pass = tk.Entry(self, show="*")


        # submitButton = tk.Button(self, text="Login", command = lambda: attempt_login(u_lname.get(), u_pass.get()))
        edit_account = tk.Button(self, text="Update Details", command = lambda: attempt_acc_update())
        button_to_dash = tk.Button(self, text="Back to Dashboard", command = lambda: p_dash.show())


        # packing acc update
        editLabel.pack()
        editDirectionsLabel.pack()

        edit_fname.pack()
        edit_lname.pack()
        edit_email.pack()
        edit_pass.pack()

        edit_account.pack()
        button_to_dash.pack()


        # config acc update
        edit_fname.insert(0, "First Name")
        edit_lname.insert(0, "Last Name")
        edit_email.insert(0, "Email")
        edit_pass.insert(0, "Pass")


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

       button_edit_acc = tk.Button(self, text="Update Account Details", command = lambda: p_update_acc.show())

       button_logout = tk.Button(self, text="Logout to sign in screen", command = lambda: attempt_logout(False))


       wel.pack()
       dis_balance.pack()

       button_deposit.pack()
       button_withdrawl.pack()
       button_edit_acc.pack()

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
       button_submit = tk.Button(self, text="Submit", command = lambda: attempt_withdraw(u_with_amm.get()))
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
       button_submit = tk.Button(self, text="Submit", command = lambda: attempt_deposit(u_dep_amm.get()))
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

class update_acc_confrim(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       global acc_up_conf
       acc_up_conf = tk.Label(self, text="This is the account update confrimation screen.")
       up_status_label = tk.Label(self, text="Account Update confrimation")
       button_to_dash = tk.Button(self, text="Back to Dashboard", command = lambda: p_dash.show())

       up_status_label.pack()
       button_to_dash.pack()
       acc_up_conf.pack(side="top", fill="both", expand=True)

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

    global u_with_amm
    txt = u_with_amm.get()
    u_with_amm.delete(0, len(txt))
    
    global u_dep_amm
    txt = u_dep_amm.get()
    u_dep_amm.delete(0, len(txt))

    # Account creation page
    global create_fname
    txt = create_fname.get()
    create_fname.delete(0, len(txt))
    create_fname.insert(0, "First Name")

    global create_lname
    txt = create_lname.get()
    create_lname.delete(0, len(txt))
    create_lname.insert(0, "Last Name")

    global create_email
    txt = create_email.get()
    create_email.delete(0, len(txt))
    create_email.insert(0, "Email")

    global create_pass
    txt = create_pass.get()
    create_pass.delete(0, len(txt))
    create_pass.insert(0, "Pass")

    # Account Update Page
    global edit_fname
    txt = edit_fname.get()
    edit_fname.delete(0, len(txt))
    edit_fname.insert(0, cur_user.get_fname())

    global edit_lname
    txt = edit_lname.get()
    edit_lname.delete(0, len(txt))
    edit_lname.insert(0, cur_user.get_lname())

    global edit_email
    txt = edit_email.get()
    edit_email.delete(0, len(txt))
    edit_email.insert(0, cur_user.get_email())

    global edit_pass
    txt = edit_pass.get()
    edit_pass.delete(0, len(txt))
    edit_pass.insert(0, cur_user.get_pass())

    # Account Update Confirmation Page
    global acc_up_conf
    acc_up_conf.config(text=f"Update Successful! \n First Name: {edit_fname.get()} \n Last Name: {edit_lname.get()} \n Email: {edit_email.get()} \n Password: {edit_pass.get()}")


def attempt_logout(confrimed):
    if (confrimed == False):
        p_log_conf.show()
    else:
        update_gui()
        p_login.show()

def attempt_acc_creation():
    # c_tuple is a user creation tuple that has namelast, namefirst, password, and email of the user (in that order.)

    # c_tuple is a user creation tuple that has namelast, namefirst, password, and email of the user (in that order.)
    global create_lname, create_fname, create_pass, create_email
    c_tuple = (create_lname.get(), create_fname.get(), create_pass.get(), create_email.get())


    # This is where any validation needs to happen for account creation.
    u_lastname = c_tuple[0]
    u_firstname = c_tuple[1]
    u_password = c_tuple[2]
    u_email = c_tuple[3]

    # calling sql function to actually create the account
    add_account(c_tuple, True)

    # Move the user back to the dashboard after creating the account
    # Should be it's own function that way validation and GUI stuff happens seperately but it's fine for now.
    p_login.show()

def attempt_acc_update():
    # c_tuple is a user creation tuple that has namelast, namefirst, password, and email of the user (in that order.)

    # c_tuple is a user creation tuple that has namelast, namefirst, password, and email of the user (in that order.)
    global edit_lname, edit_fname, edit_pass, edit_email
    c_tuple = (edit_lname.get(), edit_fname.get(), edit_pass.get(), edit_email.get())


    # This is where any validation needs to happen for account creation.
    u_lastname = c_tuple[0]
    u_firstname = c_tuple[1]
    u_password = c_tuple[2]
    u_email = c_tuple[3]

    # calling sql function to actually update the account
    update_account(c_tuple, True)

    # Move the user back to the dashboard after creating the account
    # Should be it's own function that way validation and GUI stuff happens seperately but it's fine for now.
    cur_user.user_update(c_tuple)
    update_gui()
    p_up_conf.show()

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
        w_ammount = float(ammount)
    except:
        with_conf.config(text=f"Error: Ammount to withdraw must be a float value (Must be a number)")
        update_gui()
        p_with_con.show()
    else:
        if (cur_user.u_balance < w_ammount):
            with_conf.config(text=f"Error: Insufficient funds")
            update_gui()
            p_with_con.show()
        elif(w_ammount <=0.0):
            with_conf.config(text=f"Error: Ammount to withdraw must be greater than 0")
            update_gui()
            p_with_con.show()
        elif (cur_user.u_balance > w_ammount):
            # TODO I need to make methods that will edit the database instead of just the user object
            # cur_user.u_balance = cur_user.u_balance-w_ammount
            cur_user.user_withdraw(w_ammount)
            update_gui()
            with_conf.config(text=f"Successfully withdrew {w_ammount} from your account!")
            p_with_con.show()
        else: 
            update_gui()
            with_conf.config(text=f"Hm. Something went wrong. Please try again later.")
            p_with_con.show()

def attempt_deposit(ammount):
    # Returns error/success message to be displayed on confrimation screen.
    try:
        d_ammount = float(ammount)
    except:
        dep_conf.config(text=f"Error: Ammount to withdraw must be a float value (Must be a number)")
        update_gui()
        p_dep_con.show()
    else:
        if(d_ammount > 0):
            # cur_user.u_balance = cur_user.u_balance-w_ammount
            cur_user.user_deposit(d_ammount)
            update_gui()
            dep_conf.config(text=f"Successfully deposited {d_ammount} into your account!")
            p_dep_con.show()
        else:
            dep_conf.config(text=f"Error: Ammount to withdraw must be greater than 0")
            update_gui()
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

        global p_create_acc
        p_create_acc = Create_acc(self)

        global p_update_acc
        p_update_acc = Edit_acc(self)

        global p_up_conf
        p_up_conf = update_acc_confrim(self)

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
        p_create_acc.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_update_acc.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p_up_conf.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

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

# my_user = ("Gammer", "Sally", "MC_FRRR:D", "dont_talk_to_me@joyful.org")
# add_account(my_user, False)


# mycursor.execute("INSERT INTO accounts (namelast, namefirst, password, balance, email) VALUES ('Berry', 'Straw', 'a_fruit', 0, 'pick_me_girl@yahoo.com')")
# mydb.commit()


# c_tuple is a user creation tuple that has namelast, namefirst, password, and email of the user (in that order.)


#~~~~~~~~



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