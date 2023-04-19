# install psycopg2-binary: https://bobbyhadz.com/blog/python-no-module-named-psycopg2
import psycopg2
import psycopg2.extras # for returning data as dictionaries
import os
from datetime import datetime # for confirming dates match format
import random

hostname = 'localhost'
database = 'CoffeeShop'
username = 'postgres'
pwd = 'admin'
port_id = 5433

menuSep = "*" * 50
seperation = "=" * 50

conn = None

try:
    with psycopg2.connect(host = hostname, dbname = database, user = username, password = pwd, port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            def accCreate():
                # While loop to keep displaying menu until user has been created
                while True:
                    #flag for valid username, take username input
                    isValidUser = True
                    user = input('Enter your preferred username (max 10 characters): ') 
                    
                    #check if username matches the size in the database
                    if(len(user) > 10):
                        print('Username greater than 10 characters, please try again.')  
                    else:
                        #check if the username already exists in the database
                        cur.execute("SELECT customerid FROM customer")
                        for record in cur.fetchall():
                            if(record['customerid'].strip() == user):
                                isValidUser = False
                                break
                        
                        #if the username is new, ask for input values
                        if(isValidUser):
                            #input password, check for correct length, and confirm password with the user
                            passw = input('Enter your preferred password: ')
                            while True:
                                if len(passw) > 30:
                                    print('Password must be less than 30 characters, please try again.')
                                    passw = input('Enter your preferred password: ')
                                else:
                                    pass2 = input('Confirm password: ')
                                    if passw != pass2:
                                        print('Passwords do not match, please try again.')
                                        passw = input('Enter your preferred password: ')
                                    else:
                                        break
                            
                            #input first name and check for correct length
                            fname = input('Enter your first name: ')
                            while True:
                                if(len(fname) > 30):
                                    print('First name must be less than 30 characters, please try again.')
                                    fname = input('Enter your first name: ')
                                else:
                                    break
                            
                            #input last name and check for correct length
                            lname = input('Enter your last name: ')
                            while True:
                                if(len(lname) > 30):
                                    print('Last name must be less than 30 characters, please try again.')
                                    lname = input('Enter your last name: ')
                                else:
                                    break
                                
                            #input addresss and check for correct length
                            addr = input('Enter your address: ')
                            while True:
                                if(len(addr) > 50):
                                    print('Address must be less than 50 characters, please try again.')
                                    addr = input('Enter your address: ')
                                else:
                                    break
                            
                            #input email and check for correct length
                            email = input('Enter your email: ')
                            while True:
                                if(len(email) > 30):
                                    print('Email must be less than 30 characters, please try again.')
                                    email = input('Enter your email: ')
                                else:
                                    break
                            
                            #input date of birth in requested format
                            dob = input('Enter your date of birth (yyyy-mm-dd): ')
                            format = "%Y-%m-%d"     #format required for database
                            validDate = False       #flag to check for valid format
                            while not validDate:
                                try:
                                    #call strptime to check for valid format, set validDate to bool value returned
                                    validDate = bool(datetime.strptime(dob, format))
                                except ValueError:
                                    #dob does not match format
                                    validDate = False
                                
                                #if dob does not match format, output message and take input again
                                if not validDate:
                                    print("Invalid input. Please try again.")
                                    dob = input('Enter your date of birth (yyyy-mm-dd): ')

                            #input phone number, check if int, and check if in range
                            phone = inputHandle('Enter your phone number (no dashes): ', int, [0000000000, 9999999999])
                            while phone is False: #validate user input
                                print('Invalid input. Please try again.')
                                phone = inputHandle('Enter your phone number (no dashes): ', int, [0000000000, 9999999999])
                            
                            #insert values into database
                            insertScript = 'INSERT INTO customer(customerid, fname, lname, customeraddress, email, dob, phonenumber, balance, passw) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                            insertValues = (user, fname, lname, addr, email, dob, phone, 0, passw)
                            cur.execute(insertScript, insertValues)
                            break
                        else:
                            #user already exists, output message
                            print('Username already exists, please try again')

                #output message and commit changes to database
                print("\nUser created successfully!\n")
                
            def login():
                print("== Customer Login ==")
                #While loop to keep displaying menu until user has logged in
                while True:
                    isValidUser = False     #flag to check if user input matches a user in the database
                    passw = ''              #if user was found, keep password to check input password is correct
                    # get username
                    user = input('Enter your username: ')
                    fname = ''
                    #check if user exists in the database
                    cur.execute("SELECT customerid, passw, fname FROM customer")
                    for record in cur.fetchall():
                        if(record['customerid'].strip() == user):
                            #if user exists, keep password and set flag to true
                            passw = record['passw']
                            fname = record['fname']
                            isValidUser = True
                            break
                    
                    #if user was found as for password
                    if(isValidUser):
                        inputPassw = input('Enter your password: ')
                        #if passwords do not match output message
                        if inputPassw != passw:
                            print("Incorrect password. Please try again.")
                        else:
                            #passwords matched, output message, and return the username
                            print("Successfully logged in!")
                            return user, fname
                    else: #user does not exist, return message
                        print('Username does not exist. Please try again.')

            def emplogin():
                print("== Employee Login ==")
                #While loop to keep displaying menu until user has logged in
                while True:
                    isValidUser = False     #flag to check if user input matches a user in the database
                    passw = ''              #if user was found, keep password to check input password is correct
                    # get username
                    ssn = inputHandle('Enter your ssn: ', int, [100000, 999999])
                    while ssn is False:
                        ssn = inputHandle('Invalid ssn. Enter your ssn: ', int, [100000, 999999])

                    fname = ''
                    #check if user exists in the database
                    cur.execute("SELECT ssn, passw, fname FROM employees")
                    for record in cur.fetchall():
                        if(record['ssn'] == ssn):
                            #if user exists, keep password and set flag to true
                            passw = record['passw']
                            fname = record['fname']
                            isValidUser = True
                            break
                    
                    #if user was found as for password
                    if(isValidUser):
                        inputPassw = input('Enter your password: ')
                        #if passwords do not match output message
                        if inputPassw != passw:
                            print("Incorrect password. Please try again.")
                        else:
                            #passwords matched, output message, and return the username
                            print("Successfully logged in!")
                            return ssn, fname
                    else: #user does not exist, return message
                        print('SSN does not exist. Please try again.')

            # display menu
            def menu():
                cur.execute("DROP VIEW IF EXISTS menuview")
                cur.execute("CREATE VIEW MenuView AS SELECT productid, productname, price FROM products")
                # selection for choosing category to see more
                selection = 0
                while(selection != 9):
                    clearScreen()
                    print(f"{' MENU ':*^50}")
                    print('[1] Hot Coffees:')
                    if(selection == 1):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HC%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])
                    
                    print('[2] Cold Coffees:')
                    if(selection == 2):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'CC%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[3] Hot Teas:')
                    if(selection == 3):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HT%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[4] Iced Teas:')
                    if(selection == 4):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'IT%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[5] Frappucinos:')
                    if(selection == 5):                
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'F%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[6] Hot Drinks:')
                    if(selection == 6):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HD%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[7] Cold Drinks:')
                    if(selection == 7):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'CD%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[8] Bakery:')
                    if(selection == 8):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'B%' OR productid LIKE 'HB%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])
                    
                    print('[9] Exit')
                    selection = inputHandle("Select category to see more options: ", int, [1, 9])
                    while selection == False:
                        print('Invalid input. Please try again.')
                        selection = inputHandle('Enter your selection: ', int, [1, 9])

            # to show stores
            def stores():
                print(f"{' Locations ':*^50}")
                cur.execute("SELECT shopID, shoplocation FROM shop")
                i = 1
                shops = []
                locations = []
                for record in cur.fetchall():
                    print(f"[{i}] {record['shoplocation']}")
                    shops.append(record['shopid'])
                    locations.append(record['shoplocation'])
                    i += 1
                
                return shops, locations

            # order
            def placeOrder(user, fname):
                print(menuSep, "Order Menu", menuSep)
                shops, locations = stores()

                selection = inputHandle("Enter the number of the store you wish to order from: ", int, [1, len(shops)])
                while selection is False:
                    selection = inputHandle("Invalid input. Enter the number of the store you wish to order from: ", int, [1, len(shops)])
                
                shopID = shops[selection-1]
                location = locations[selection-1]
            
                print(seperation)
                print(f"Ordering To: {location}")

                flag = True
                orderID = random.randint(1000000, 9999999)
                while flag:
                    orderidScript = 'SELECT orderID FROM orders WHERE orderID = %s'
                    orderid = (orderID,)
                    cur.execute(orderidScript, orderid)

                    if len(cur.fetchall()) == 0:
                        flag = False
                    else:
                        orderID = random.randint(1000000, 9999999)

                cur.execute("DROP VIEW IF EXISTS shopBaristas")
                cur.execute("DROP VIEW IF EXISTS shopCashiers")

                cur.execute("CREATE VIEW shopBaristas AS SELECT * FROM barista JOIN employees ON empid = ssn")
                cur.execute("CREATE VIEW shopCashiers AS SELECT * FROM cashiers JOIN employees ON empid = ssn")

                shopTuple = (shopID, )
                cur.execute("SELECT * FROM shopBaristas")

                baristas = []
                for record in cur.fetchall():
                    if record['storeid'] == shopID:
                        baristas.append(record['ssn'])
                
                rand = random.randint(0, len(baristas)-1)

                baristaID = baristas[rand]

                selectCashier = "SELECT * FROM shopCashiers WHERE storeID = %s"
                cur.execute(selectCashier, shopTuple)

                cashiers = []
                for record in cur.fetchall():
                    cashiers.append(record['ssn'])

                rand = random.randint(0, len(cashiers)-1)
                cashierID = cashiers[rand]

                totalprice = 0
                items = []
                quantity = []

                order = ''
                while order != 'n':
                    order = input("Enter the name of the item you wish to order: ")

                    orderScript = 'SELECT productid, price FROM products WHERE productname = %s'
                    order = (order, )
                    cur.execute(orderScript, order)

                    product = cur.fetchall()

                    prID = ''
                    price = 0
                    if len(product) == 0:
                        print('Item could not be found, please try again.')
                        continue
                    else:
                        for record in product:
                            prID = record['productid']
                            price = record['price']
                    
                    amount = inputHandle("Enter how many of this item to order: ", int, [1, 100])
                    while amount is False:
                        amount = inputHandle("Invalid input. Enter how many of this item to order: ", int, [1, 100])

                    totalprice += (price * amount)
                    items.append(prID)
                    quantity.append(amount)

                    order = input("Would you like to order more items? (y/n):")
                    order = order.lower()
                    print(seperation)
                
                dateToday = datetime.today().strftime('%Y-%m-%d')
                createOrder = 'INSERT INTO orders(orderid, customerid, storeid, dates, totalprice, cashierid, baristaid) VALUES(%s, %s, %s, %s, %s, %s, %s)'
                orderValues = (orderID, user, shopID, dateToday, totalprice, cashierID, baristaID)

                cur.execute(createOrder, orderValues)

                for (item, q) in zip(items, quantity):
                    insertScript = 'INSERT INTO contain(orid, prid, quantity) VALUES(%s, %s, %s)'
                    insertVals = (orderID, item, q)
                    cur.execute(insertScript, insertVals)

                print(f"\nYour order has been placed, {fname}! \
                      \nTotal: ${totalprice}\nYour order should be ready in about 15-20 minutes.")

            def cancelOrder(user, fname):
                functionCreation = '''CREATE OR REPLACE FUNCTION delete_from_contain()
                                    RETURNS TRIGGER LANGUAGE PLPGSQL
                                    AS
                                    $$
                                    BEGIN
                                        DELETE FROM contain WHERE orid = OLD.orderid;
                                        RETURN OLD;
                                    END;
                                    $$'''
                cur.execute(functionCreation)
                cur.execute("CREATE OR REPLACE TRIGGER trig BEFORE DELETE ON orders FOR EACH ROW EXECUTE PROCEDURE delete_from_contain()")
                
                userTuple = (user, )
                cur.execute("SELECT * FROM orders WHERE customerid = %s", userTuple)
                orders = cur.fetchall()
                orderlist = []
                if len(orders) == 0:
                    print('There are currently no orders in progress for you.')
                else:
                    print(f"Here are the orders in progress for you, {fname}:")
                    for record in orders:
                        print(f"Order: #{record['orderid']}\tDate Placed: {record['dates']}\tTotal Price: {record['totalprice']}")
                        orderlist.append(str(record['orderid']))

                    print()
                    selection = input("Enter the order number you wish to cancel (enter q to cancel): ")
                    while selection != 'q':
                        if selection not in orderlist:
                            selection = input("Order Number does not exist, please try again. \
                                              \nEnter the order number you wish to cancel (enter q to cancel): ")
                        else:
                            selecTuple = (selection, )
                            cur.execute("DELETE FROM orders WHERE orderid = %s", selecTuple)
                            print(f"\nOrder #{selection} successfully cancelled! A refund will be issued to you shortly.")
                            break
                
            # customer view / default view
            def custView():
                print(f"{'':*^50}")
                print(f"{' Welcome to Postgres Coffee! ':*^50}")
                print(f"{'':*^50}\n")
                selection = 0
                user = ''
                fname = ''
                isEmployee = False

                while selection != 7:
                    print('\n** Postgres Coffee **')
                    if len(fname) != 0:
                        print(f'Welcome Back, {fname}!')
                    print('Please choose an option')
                    print('[1] Menu')
                    print('[2] Store locations')
                    print('[3] Order')
                    print('[4] Sign in')
                    print('[5] Sign up')
                    print('[6] Cancel Order')
                    print('[7] Quit')

                    selection = inputHandle('Enter your selection: ', int, [1, 7])
                    while selection == False:
                        print('Invalid input. Please try again.')
                        selection = inputHandle('Enter your selection: ', int, [1, 7])
                    
                    print()

                    if selection == 1:
                        menu()
                        print(menuSep)
                    elif selection == 2:
                        stores()
                        print(menuSep)
                    elif selection == 3:
                        if isEmployee:
                            print('Please login to your customer account to order.')
                        elif len(user) == 0:
                            print('To order, please sign in to your account.')
                        else:
                            placeOrder(user, fname)

                        print(menuSep)
                    elif selection == 4:
                        if len(user) == 0:
                            print(seperation)
                            print('[1] Customer Login')
                            print('[2] Employee Login')
                            s = inputHandle('Enter your selection: ', int, [1, 2])
                            while s is False:
                                print('Invalid Input. Please try again.')
                                s = inputHandle('Enter your selection: ', int, [1, 2])

                            if s == 1:
                                print(seperation)
                                user, fname = login()
                            else:
                                print(seperation)
                                user, fname = emplogin()
                                isEmployee = True
                            print(menuSep)
                        else:
                            print('You are already logged in as user: ', user)
                            print(menuSep)
                    elif selection == 5:
                        accCreate()
                        print(menuSep)
                    elif selection == 6:
                        if len(user) == 0:
                            print('To cancel an order, please sign in to your account.')
                        else:
                            cancelOrder(user, fname)
                        
                        print(menuSep)
                    elif selection == 7:
                        print('Goodbye!\n')
                    
                    conn.commit()
                
            # employee view
            def empView():
                pass

            # ------------------------ HELPER FUNCTIONS ------------------------
            # clear screen
            def clearScreen():
                os.system('clear')

            # handle user selection
            def inputHandle(text, typeCast, range):
                # print(data)
                isValid = 0
                while(isValid == 0):
                    try:
                        data = input(text)
                        data = typeCast(data)
                    except ValueError:
                        return False
                    else:
                        break # break loop
                if (data >= range[0] and data <= range[1]):
                    return data
                else:
                    return False
            
            def main():
                custView()

                return()

            main()

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()