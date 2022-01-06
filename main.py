import db_connector
import mysql.connector as conn

def log_in(username, password):
    try:
        DB_OBJECT = conn.connect(user=username, password=password)
        DB_CURSOR = DB_OBJECT.cursor()
    except conn.errors.ProgrammingError:
        print("Error : Incorrect Username or Password")
    else:
        check_if_new_user(DB_OBJECT, DB_CURSOR)
        home_page()

def check_if_new_user(db, cursor):
    if db_connector.check_if_existing(db, cursor) == False:
        db_connector.initialize_database(db, cursor)

def home_page():
    print("""
    ---Home Page---
    1. Enter Bill
    2. Add Product
    3. Exit
    """)
    choice = input("Enter Your Choice : ")
    if choice == '1':
        print("Enter Bill")
    elif choice == '2':
        print("Add Product")
    elif choice == '3':
        pass
    else:
        print("Error : Invalid Option!")
        home_page()

usernameFromUser = input("Enter your MySql Username : ")
passwordFromUser = input("Enter your MySql Password : ")

log_in(usernameFromUser, passwordFromUser)