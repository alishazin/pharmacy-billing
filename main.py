import db_connector
import mysql.connector as conn
from prettytable import PrettyTable

import os

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
    DB_CURSOR.execute("use pharmacy")

def add_accessory_interface():
    while True:
        name = strip_input("Enter name of the accessory : ")
        if len(name) == 0:
            print("Error : Name cannot be NULL")
            continue
        elif check_if_product_exist(name):
            print(f"Error : Product '{name}' already exist")
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
    DB_CURSOR.execute(f"""
    insert into productdetails(name, price, children, accessories, stock) 
    VALUES ('{name}', '{price}', '{convert_accessibility(accessibility)}', True, '{stock}')
    """)
    DB_OBJECT.commit()

def add_medicine_interface():
    while True:
        name = strip_input("Enter name of the medicine : ")
        if len(name) == 0:
            print("Error : Name cannot be NULL")
            continue
        elif check_if_product_exist(name):
            print(f"Error : Product '{name}' already exist")
            continue
        else:
            break

    while True:
        prescribed = strip_input("Enter if prescribed or not (yes / no) : ")
        if prescribed.lower() not in ['yes', 'no']:
            print("Error : Should be one of 'yes' or 'no'")
            continue
        else:
            break

    while True:
        tablet = strip_input("Enter 'yes' for tablet and 'no' for syrup : ")
        if tablet.lower() not in ['yes', 'no']:
            print("Error : Should be one of 'yes' or 'no'")
            continue
        else:
            break
    
    while True:
        price = strip_input("Enter price of the medicine : ")
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
        stock = strip_input("Enter initial stock of the medicine : ")
        if stock.isnumeric():
            break
        else:
            print("Error : Stock should be numeric (it can also be zero)")
            continue

    add_medicine_to_database(name, prescribed, tablet, price, accessibility, stock)
    print(f"Info : Medicine '{name}' added")
    add_product_page()

def add_medicine_to_database(name, prescribed, tablet, price, accessibility, stock):
    DB_CURSOR.execute(f"""
    insert into productdetails(name, prescribed, tablet, price, children, accessories, stock) 
    VALUES ('{name}', {convert_yes_or_no_to_bool(prescribed)}, {convert_yes_or_no_to_bool(tablet)},'{price}', '{convert_accessibility(accessibility)}', False, '{stock}')
    """)
    DB_OBJECT.commit()

def convert_yes_or_no_to_bool(text):
    replaceDict = {
        'yes' : True,
        'no' : False,
    }
    return replaceDict[text.lower()]

def convert_accessibility(text):

    replaceDict = {
        'children' : 'True',
        'adult' : 'False',
        'common' : 'common',
    }
    return replaceDict[text.lower()]

def convert_back_accessibility(text):
    replaceDict = {
        'True' : 'children',
        'False' : 'adult',
        'common' : 'common',
    }
    return replaceDict[text]

def convert_bool_to_prescribed(text):
    replaceDict = {
        True : 'prescribed',
        False : 'unprescribed',
    }
    return replaceDict[text]

def convert_bool_to_tablet(text):
    replaceDict = {
        True : 'tablet',
        False : 'syrup',
    }
    return replaceDict[text]

def view_accessories():
    DB_CURSOR.execute('select id, name, price, children, stock from productdetails where accessories = True')
    result = DB_CURSOR.fetchall()

    table = PrettyTable(['id', 'name', 'price', 'children', 'stock'])
    for row in result:
        table.add_row([row[0], row[1], row[2], convert_back_accessibility(row[3]), row[4]])
    print(table)

    input("Press enter to continue : ")
    view_product_page()

def view_medicines():
    DB_CURSOR.execute('select id, name, prescribed, tablet, price, children, stock from productdetails where accessories = False')
    result = DB_CURSOR.fetchall()

    table = PrettyTable(['id', 'name', 'prescribed', 'tablet', 'price', 'children', 'stock'])
    for row in result:
        table.add_row([row[0], row[1], convert_bool_to_prescribed(row[2]), convert_bool_to_tablet(row[3]), row[4], convert_back_accessibility(row[5]), row[6]])
    print(table)

    input("Press enter to continue : ")
    view_product_page()

def view_product_page():
    print("""
    ---View Products Page---
    1. View Accessories
    2. View Medicines
    3. Go Back To Home Page
    """)
    choice = input("Enter Your Choice : ")
    if choice == '1':
        view_accessories()
    elif choice == '2':
        view_medicines()
    elif choice == '3':
        home_page()
    else:
        print("Error : Invalid Option!")
        view_product_page()

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
        add_medicine_interface()
    elif choice == '3':
        home_page()
    else:
        print("Error : Invalid Option!")
        add_product_page()

def enter_customer_details_interface():
    
    while True:
        customerContactNumber = strip_input("Enter contact number of the customer : ")
        if not customerContactNumber.isnumeric():
            print("Error : Contact number should be numeric")
            continue
        break

    if check_if_customer_exist(customerContactNumber) == False:
        print("Customer is a new one!")
        
        while True:
            customerName = strip_input("Enter name of the customer : ")
            if len(customerName) == 0:
                print("Error : Name cannot be empty!")
                continue

            add_customer_to_database(customerContactNumber, customerName)
            print(f"Customer '{customerName}' is added")
            break

    enter_bill_interface(customerContactNumber, get_name_from_contact_no(customerContactNumber))

def enter_bill_interface(customerContactNo, customerName):
    
    productDict = {}

    while True:

        childList = []
        
        while True:
            productName = strip_input("Enter product name : ")
            if len(productName) == 0:
                print("Error : Product name cannot be empty!")
                continue
            elif not check_if_product_exist(productName):
                print("Error : Product does not exist!")
                continue
            childList.append(productName.lower())
            break

        while True:
            productQuantity = strip_input("Enter quantity of the product : ")
            if not productQuantity.isnumeric():
                print("Error : Quantity should be numeric")
                continue
            elif productQuantity == 0:
                print("Error : Quantity cannot be zero")
                continue
            elif not check_if_required_stock_left(productName, productQuantity, productDict):
                print("Error : Remaining stock number exceeded!")
                continue
            childList.append(int(productQuantity))
            break

        try:
            productDict[childList[0]] += childList[1]
        except:
            productDict[childList[0]] = childList[1]
        
        loopCommand = ''

        while True:
            confirmation = strip_input("Enter 1 to continue adding to the bill, 0 to end the bill : ")
            if confirmation == '1':
                loopCommand = 'continue'
                break
            elif confirmation == '0':
                loopCommand = 'end'
                break
            else:
                print("Error : Invalid Input!")
                continue

        if loopCommand == 'continue':
            continue
        elif loopCommand == 'end':
            break

    billId = add_data_to_bill_extra(customerContactNo)
    add_data_to_bill(billId, productDict)
    reduce_from_stock(productDict)
    calculate_bill(productDict, customerContactNo, customerName, billId)

def calculate_bill(productDict, customerContactNo, customerName, billID):
    count = 1
    allTotal = 0
    table = PrettyTable(['S.No', 'Name', 'Quantity', 'Price', 'Total'])
    for name, quantity in productDict.items():
        price = get_price_from_product_name(name)
        total = quantity * price
        table.add_row([count, name, quantity, price, total])
        count += 1
        allTotal += total
    display_bill(table, allTotal, customerContactNo, customerName, billID)

def display_bill(table, total, cusCon, cusName, billID):
    with open('bill.txt', 'w') as file:
        file.write(f"Bill ID : {billID}\nCustomer Name : {cusName}\nContact Number : {cusCon}\n\n{table}\n\nTotal : {total}")

    os.popen('bill.txt')
    print("Bill Displayed Successfully")
    input("Press enter to continue : ")
    home_page()

def get_price_from_product_name(name):
    DB_CURSOR.execute(f"select price from productdetails where name = '{name}'")
    result = DB_CURSOR.fetchall()[0][0]
    return result

def reduce_from_stock(productDict):
    for key, values in productDict.items():
        DB_CURSOR.execute(f"select stock from productdetails where name = '{key}'")
        currentStock = DB_CURSOR.fetchall()[0][0]
        DB_CURSOR.execute(f"update productdetails SET stock = '{currentStock - values}' WHERE name = '{key}'")
    DB_OBJECT.commit()

def add_data_to_bill_extra(conNo):
    billId = get_latest_bill_id() + 1
    cusId = get_cus_id_from_contact_no(conNo)
    DB_CURSOR.execute(f"insert into billextra values({billId},{cusId})")
    DB_OBJECT.commit()
    return billId

def add_data_to_bill(id, productDict):
    for key, value in productDict.items():
        DB_CURSOR.execute(f"insert into bill values({id},'{key}', {value})")
    DB_OBJECT.commit()

def get_cus_id_from_contact_no(conNo):
    DB_CURSOR.execute(f"select id from customerdetails where contact_no = '{conNo}'")
    result = DB_CURSOR.fetchall()[0][0]
    return result

def get_latest_bill_id():
    DB_CURSOR.execute("select MAX(bill_id) from billextra")
    result = DB_CURSOR.fetchall()[0][0]
    if result == None:
        return 0
    return result

def check_if_required_stock_left(productName, productQuantity, productDict):
    DB_CURSOR.execute(f"select stock from productdetails where name = '{productName}'")
    result = DB_CURSOR.fetchall()[0][0]

    try:
        existing = productDict[productName]
    except:
        existing = 0
    
    if result >= (int(productQuantity) + int(existing)):
        return True
    return False 

def check_if_product_exist(productName):
    DB_CURSOR.execute(f"select id from productdetails where name = '{productName.lower()}'")
    result = DB_CURSOR.fetchall()

    if len(result) == 0:
        return False
    return True

def get_name_from_contact_no(conNo):
    DB_CURSOR.execute(f"select name from customerdetails where contact_no = '{conNo}'")
    result = DB_CURSOR.fetchall()
    return result[0][0]

def add_customer_to_database(conNo, name):
    DB_CURSOR.execute(f"insert into customerdetails(contact_no, name) values ('{conNo}','{name.title()}')")
    DB_OBJECT.commit()

def check_if_customer_exist(conNo):
    DB_CURSOR.execute(f"select id from customerdetails where contact_no = '{conNo}'")
    result = DB_CURSOR.fetchall()

    if len(result) == 0:
        return False
    return True

def view_bill_interface():

    while True:
        billID = strip_input("Enter ID of the bill : ")
        if not billID.isnumeric():
            print("Error : ID should be numeric")
            continue
        else:
            cusID = check_if_bill_exists(billID)
            if cusID == False:
                print(f"Error : Bill with ID '{billID}' does not exist")
                continue
            break

    calculate_older_bill(cusID, billID)

def view_latest_bill():
    billID = get_latest_bill_id()
    cusID = check_if_bill_exists(billID)
    calculate_older_bill(cusID, billID)

def calculate_older_bill(cusID, billID):
    customerDetails = get_customer_details_from_id(cusID)
    customerContactNumber = customerDetails[0]
    customerName = customerDetails[1]

    productDict = get_bill_details_from_id(billID)
    calculate_bill(productDict, customerContactNumber, customerName, billID)

def get_customer_details_from_id(id):
    DB_CURSOR.execute(f"select contact_no, name from customerdetails where id = '{id}'")
    result = DB_CURSOR.fetchall()
    return [result[0][0], result[0][1]]

def get_bill_details_from_id(id):
    DB_CURSOR.execute(f"select prod_name, quantity from bill where id = '{id}'")
    result = DB_CURSOR.fetchall()

    returnDict = {}
    for row in result:
        returnDict[row[0]] = row[1]
    return returnDict

def check_if_bill_exists(id):
    DB_CURSOR.execute(f"select cus_id from billextra where bill_id = '{id}'")
    result = DB_CURSOR.fetchall()
    if len(result) > 0:
        return result[0][0]
    return False

def bill_page():
    if get_latest_bill_id() == 0:
        print("Error : There are no existing bills!")
        input("Press enter to continue : ")
        home_page()
    else:
        print("""
    ---Bill Page---
    1. View Latest Bill
    2. View Bill Using ID
    3. Go Back To Home Page
        """)
        choice = input("Enter Your Choice : ")
        if choice == '1':
            view_latest_bill()
        elif choice == '2':
            view_bill_interface()
        elif choice == '3':
            home_page()
        else:
            print("Error : Invalid Option!")
            bill_page()

def add_stock_using_id_interface():
    while True:
        productID = strip_input("Enter ID of the Product : ")
        if not productID.isnumeric():
            print("Error : ID should be numeric")
            continue
        else:
            currentStock = check_if_product_id_exists(productID)
            if currentStock == False:
                print(f"Error : Product with ID '{productID}' does not exist")
                continue
            break

    add_stock_interface(productID, currentStock)

def add_stock_using_name_interface():
    while True:
        productName = strip_input("Enter Name of the Product : ")
        if len(productName) == 0:
            print("Error : Product Name should not be NULL")
            continue
        else:
            currentStock = check_if_product_name_exists(productName)
            if currentStock == False:
                print(f"Error : Product with Name '{productName}' does not exist")
                continue
            break

    add_stock_interface(productName, currentStock, True)

def check_if_product_name_exists(name):
    DB_CURSOR.execute(f"select stock from productdetails where name = '{name}'")
    result = DB_CURSOR.fetchall()
    if len(result) > 0:
        return result[0][0]
    return False

def add_stock_interface(IDOrName, currentStock, using_name = False):
    if using_name:
        print(f"Product with Name '{IDOrName}' has '{currentStock}' stocks remaining")
    else:
        print(f"Product with ID '{IDOrName}' has '{currentStock}' stocks remaining")

    while True:
        stockAdd = strip_input("Enter number of stock to add : ")
        if not stockAdd.isnumeric():
            print("Error : Stock should be numeric")
            continue
        break

    if using_name:
        DB_CURSOR.execute(f"update productdetails set stock = '{currentStock + int(stockAdd)}' where name = '{IDOrName}'")
    else:
        DB_CURSOR.execute(f"update productdetails set stock = '{currentStock + int(stockAdd)}' where id = '{IDOrName}'")

    DB_OBJECT.commit()
    print(f"Stock is successfully updated to {currentStock + int(stockAdd)}")
    input("Press enter to continue : ")
    home_page()

def check_if_product_id_exists(id):
    DB_CURSOR.execute(f"select stock from productdetails where id = '{id}'")
    result = DB_CURSOR.fetchall()
    if len(result) > 0:
        return result[0][0]
    return False

def stock_page():
    print("""
    ---Stock Page---
    1. Add Stock Using ID
    2. Add Stock Using Name
    3. Go Back To Home Page
    """)
    choice = input("Enter Your Choice : ")
    if choice == '1':
        add_stock_using_id_interface()
    elif choice == '2':
        add_stock_using_name_interface()
    elif choice == '3':
        home_page()
    else:
        print("Error : Invalid Option!")
        bill_page()

def home_page():
    print("""
    ---Home Page---
    1. Enter Bill
    2. Add Product
    3. View Products
    4. View Older Bills
    5. Add Stock
    6. Exit
    """)
    choice = input("Enter Your Choice : ")
    if choice == '1':
        enter_customer_details_interface()
    elif choice == '2':
        add_product_page()
    elif choice == '3':
        view_product_page()
    elif choice == '4':
        bill_page()
    elif choice == '5':
        stock_page()
    elif choice == '6':
        pass
    else:
        print("Error : Invalid Option!")
        home_page()

usernameFromUser = input("Enter your MySql Username : ")
passwordFromUser = input("Enter your MySql Password : ")

log_in(usernameFromUser, passwordFromUser)
