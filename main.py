import mysql.connector
import gui
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
    login_credits = (last_name, u_pass)
    login_select_query = "select * from accounts where namelast = %s and password = %s"
    mycursor.execute(login_select_query, login_credits)
    
    result = None
    for x in mycursor:
        result = x
    if (result == None):
        return "failed to execute"
    for x in mycursor:
        print(x)

print(gui.login_screen())


# login_attempt('smiths','abc123')
