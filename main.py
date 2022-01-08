import db_connector
import mysql.connector as conn

def strip_input(text):
    return input(text).strip()

def log_in(username, password):
    try:
        global DB_OBJECT
        global DB_CURSOR
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

def add_accessory_interface():
    while True:
        name = strip_input("Enter name of the accessory : ")
        if len(name) == 0:
            print("Error : Name cannot be NULL")
            continue
        else:
            break
    
    while True:
        price = strip_input("Enter price of the accessory : ")
        try:
            price = float(price)
            break
        except:
            print("Error : Price should be numeric")
            continue
        
    while True:
        accessibility = strip_input("Choose between children / adult / common : ")
        if accessibility.lower() in ['children', 'adult', 'common']:
            break
        else:
            print("Error : Should be one of children / adult / common.")
            continue

    while True:
        stock = strip_input("Enter initial stock of the accessory : ")
        if stock.isnumeric():
            break
        else:
            print("Error : Stock should be numeric (it can also be zero)")
            continue

    add_accessory_to_database(name, price, accessibility, stock)
    print(f"Info : Accessory '{name}' added")
    add_product_page()

def add_accessory_to_database(name, price, accessibility, stock):
    DB_CURSOR.execute("use pharmacy")
    DB_CURSOR.execute(f"""
    insert into productdetails(name, price, children, accessories, stock) 
    VALUES ('{name}', '{price}', '{convert_accessibility(accessibility)}', True, '{stock}')
    """)
    DB_OBJECT.commit()

def convert_accessibility(text):
    replaceDict = {
        'children' : True,
        'adult' : False,
        'common' : 'common',
    }
    return replaceDict[text.lower()]

def add_product_page():
    print("""
    ---Add Product Page---
    1. Add Accessory
    2. Add Medicine
    3. Go Back To Home Page
    """)
    choice = input("Enter Your Choice : ")
    if choice == '1':
        add_accessory_interface()
    elif choice == '2':
        print("Add Medicine")
    elif choice == '3':
        home_page()
    else:
        print("Error : Invalid Option!")
        add_product_page()


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
        add_product_page()
    elif choice == '3':
        pass
    else:
        print("Error : Invalid Option!")
        home_page()

# usernameFromUser = input("Enter your MySql Username : ")
# passwordFromUser = input("Enter your MySql Password : ")

# log_in(usernameFromUser, passwordFromUser)
log_in('root', 'physicssucks')