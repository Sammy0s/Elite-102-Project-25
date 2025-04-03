import mysql.connector
# import gui

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="menagerie"
)

mycursor = mydb.cursor()

test = "owner = 'Josh'"

mycursor.execute("")

for x in mycursor:
    print(x)
