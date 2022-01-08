
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
    db.commit()