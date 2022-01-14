
def check_if_existing(db, dbCursor):
    dbCursor.execute('show databases')
    result = dbCursor.fetchall()
    check = False
    for i in result:
        if i[0] == 'pharmacy':
            check = True

    return check

def initialize_database(db, dbCursor):
    dbCursor.execute('create database pharmacy')
    dbCursor.execute('use pharmacy')
    # Table 1
    dbCursor.execute("""create table productdetails (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) UNIQUE,
        prescribed bool,
        tablet bool,
        price float NOT NULL,
        children VARCHAR(6) NOT NULL,
        accessories bool,
        stock INT
    )""")

    # Table 2
    dbCursor.execute("""create table customerdetails (
        id INT PRIMARY KEY AUTO_INCREMENT,
        contact_no VARCHAR(20) UNIQUE, 
        name VARCHAR(100)
    )""")

    # Table 3
    dbCursor.execute("""create table billextra (
        bill_id INT PRIMARY KEY UNIQUE,
        cus_id INT,
        CONSTRAINT fk_cus_id FOREIGN KEY (cus_id) REFERENCES customerdetails(id)
    )""")

    # Table 4
    dbCursor.execute("""create table bill (
        id INT,
        prod_name VARCHAR(100),
        quantity INT,
        CONSTRAINT fk_bill_id FOREIGN KEY (id) REFERENCES billextra(bill_id)
    )""")
    db.commit()