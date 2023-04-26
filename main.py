''' Ryan Martinez, Van Dinh Le, Meena Kukkadam, Last Edited: 04/25/2023
Purpose: This program creates the interface for a coffee shop named Postgres Coffee with over 20 stores nationwide. 
It allows for interaction with a database that holds information about the customers, employees, products, shops, etc.
Guests can view the menu, shop locations, and choose to sign in or sign up. Once signed in, Customers can place orders or
delete existing orders they have placed. Employees can view orders assigned to them and edit their information. Managers
can order more stock from suppliers. 
'''
# this program uses the psycopg2 library to connect to a postgres database
# install psycopg2-binary: https://bobbyhadz.com/blog/python-no-module-named-psycopg2
import psycopg2
import psycopg2.extras  # for returning data as dictionaries
import os   # for clearing the terminal screen
from datetime import datetime   # for confirming dates match format
import random   # for creating random ids
import re       # for checking email
import time     # for simulating tiny delays at login, logout, and account creation

# database information for use in connection
hostname = 'localhost'
database = 'CoffeeShop'
username = 'postgres'
pwd = 'admin'
port_id = 5433

# seperators
menuSep = "*" * 50
seperation = "=" * 50

# initialize connection variable
conn = None

# try-catch block to catch errors including failed connection
try:
    # initialize conn variable as the connection to the database with information passed in
    with psycopg2.connect(host = hostname, dbname = database, user = username, password = pwd, port = port_id) as conn:

        # initialize cursor to run queries and fetch returned data from database
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            
            # function to create a customer account
            def accCreate():
                clearScreen()
                print(menuSep, " Postgres Coffee ", menuSep)
                # While loop to keep displaying menu until user has been created
                while True:
                    # flag for valid username
                    isValidUser = True
                    # ask user for the username they wish to use, and verify user input
                    user = inputHandle('Enter your preferred username (max 10 characters): ', str, [1,10])
                    while user is False:
                        user = inputHandle('Invalid Input. Enter your preferred username (max 10 characters): ', str, [1,10])
                    
                    #check if the username already exists in the database
                    cur.execute("SELECT customerid FROM customer")
                    for record in cur.fetchall():
                        if(record['customerid'].strip() == user):
                            #if user name has been found, set flag to false and break
                            isValidUser = False
                            break
                    
                    #if the username was not found, ask for input values
                    if(isValidUser):
                        #input password, check for correct length, and confirm password with the user
                        passw = inputHandle('Enter your preferred password (max 30 characters): ', str, [1,30])
                        while True:
                            if passw is False:
                                passw = inputHandle('Invalid Input. Enter your preferred password (max 30 characters): ', str, [1,30])
                            else:
                                pass2 = input('Confirm password: ')
                                if passw != pass2:
                                    print('Passwords do not match, please try again.')
                                    passw = inputHandle('Enter your preferred password: ', str, [1,30])
                                else:
                                    break
                        
                        #input first name and check for correct length
                        fname = inputHandle('Enter your first name (max 30 characters): ', str, [1,30])
                        while fname is False:
                            fname = inputHandle('Invalid Input. Enter your first name (max 30 characters): ', str, [1,30])
                            
                        
                        #input last name and check for correct length
                        lname = inputHandle('Enter your last name (max 30 characters): ', str, [1,30])
                        while lname is False:
                            lname = inputHandle('Invalid Input. Enter your last name (max 30 characters): ', str, [1,30])
                            
                            
                        #input addresss and check for correct length
                        addr = inputHandle('Enter your address (max 50 characters): ', str, [1,50])
                        while addr is False:
                            addr = inputHandle('Invalid Input. Enter your address (max 50 characters): ', str, [1,50])
                        
                        # input email and check for correct length and format
                        regex = '[^@]+@[^@]+\.[^@]+'
                        email = inputHandle('Enter your email (max 30 characters): ', str, [1,30])
                        while email is False or not re.search(regex, email):
                            email = inputHandle('Invalid Email. Enter your email (max 30 characters): ', str, [1,30])
                        
                        #input date of birth in requested format
                        dob = input('Enter your date of birth (yyyy-mm-dd): ')
                        format = "%Y-%m-%d"     #format required for database
                        validDate = False       #flag to check for valid format
                        #while loop to check for correct format
                        while not validDate:
                            # try block to catch errors returned by datetime
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

                        #input phone number, check if it is an int value, and check if in range
                        phone = inputHandle('Enter your phone number (no dashes): ', int, [0000000000, 9999999999])
                        while phone is False:
                            phone = inputHandle('Invalid Input. Enter your phone number (no dashes): ', int, [0000000000, 9999999999])
                        
                        #insert values into database
                        insertScript = 'INSERT INTO customer(customerid, fname, lname, customeraddress, email, dob, phonenumber, balance, passw) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                        insertValues = (user, fname, lname, addr, email, dob, phone, 0, passw)
                        cur.execute(insertScript, insertValues)
                        break
                    else:
                        #user already exists, output message
                        print('Username already exists, please try again')

                print("Creating account...\n")
                time.sleep(2)
                #output message and commit changes to database
                print("User created successfully!\n")
            
            # functions for customer login, returns username and first name of the customer
            def login():
                clearScreen()                
                print(menuSep, " Postgres Coffee ", menuSep)
                print("== Customer Login ==")
                # while loop to keep displaying menu until user has logged in or decided to quit
                quit = 'y'
                while quit != 'n':
                    isValidUser = False     # flag to check if user input matches a user in the database
                    passw = ''              # if user was found, keep password to check input password is correct
                    # ask user for their username
                    user = input('Enter your username: ')

                    fname = '' 
                    #check if user exists in the database
                    cur.execute("SELECT customerid, passw, fname FROM customer")
                    for record in cur.fetchall():
                        if(record['customerid'].strip() == user):
                            #if user exists, keep password and first name and set flag to true
                            passw = record['passw']
                            fname = record['fname']
                            isValidUser = True
                            break
                    
                    #if user was found, ask for their password
                    if(isValidUser):
                        inputPassw = input('Enter your password: ')
                        #if passwords do not match, output message
                        if inputPassw != passw:
                            print("Incorrect password. Please try again.")
                            quit = input("Would you like to try again? Enter 'n' to quit: ")
                            quit.lower()
                        else:
                            print("Logging in...\n")
                            time.sleep(2)
                            #passwords matched, output message, and return the username and first name
                            print("Successfully logged in!")
                            return user, fname
                    else: # if user does not exist, output message
                        print('Username does not exist. Please try again.')
                        quit = input("Would you like to try again? Enter 'n' to quit: ")
                        quit.lower()
                
                # user chose to quit, return empty strings
                return '', ''

            # function for employee login, returns employee ssn, first name, and bool value that is True if logged in, False otherwise
            def emplogin():
                clearScreen()
                print(menuSep, " Postgres Coffee ", menuSep)

                print("== Employee Login ==")
                # While loop to keep displaying menu until user has logged in or decided to quit
                quit = 'y'
                while quit != 'n':
                    isValidUser = False     #flag to check if user input matches ssn in the database
                    passw = ''              # if employee was found, keep password to check input password is correct
                    # ask employee for their ssn
                    ssn = inputHandle('Enter your ssn: ', int, [100000, 999999])
                    while ssn is False:
                        ssn = inputHandle('Invalid ssn. Enter your ssn: ', int, [100000, 999999])

                    fname = ''
                    # check if ssn exists in the database
                    cur.execute("SELECT ssn, passw, fname FROM employees")
                    for record in cur.fetchall():
                        if(record['ssn'] == ssn):
                            # if ssn exists, keep password and first name, and set flag to true
                            passw = record['passw']
                            fname = record['fname']
                            isValidUser = True
                            break
                    
                    # if ssn was found, ask for password
                    if(isValidUser):
                        inputPassw = input('Enter your password: ')
                        #if passwords do not match output message
                        if inputPassw != passw:
                            print("Incorrect password. Please try again.")
                            quit = input("Would you like to try again? Enter 'n' to quit: ")
                            quit.lower()
                        else:
                            print("Logging in...\n")
                            time.sleep(2)
                            # passwords matched, output message, and return the ssn, first name, and True
                            print("Successfully logged in!")
                            return ssn, fname, True
                    else: #user does not exist, return message
                        print('SSN does not exist. Please try again.')
                        quit = input("Would you like to try again? Enter 'n' to quit: ")
                        quit.lower()
                
                # if user decided to quit, return empty strings for ssn, first name, and return False
                return '', '', False

            # display menu
            def menu():
                # Drop view if exists to make sure duplicate views are not created
                cur.execute("DROP VIEW IF EXISTS menuview")
                # Create view to get only the product id, name, and price of each product
                cur.execute("CREATE VIEW MenuView AS SELECT productid, productname, price FROM products")
                # selection for choosing menu category 
                selection = 0
                # if 9 is entered, exit the menu
                while(selection != 9):
                    clearScreen()
                    print(f"{' MENU ':*^50}")
                    print('[1] Hot Coffees:')
                    # if 1 was entered, display hot coffees
                    if(selection == 1):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HC%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])
                    
                    print('[2] Cold Coffees:')
                     # if 2 was entered, display cold coffees
                    if(selection == 2):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'CC%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[3] Hot Teas:')
                     # if 3 was entered, display hot teas
                    if(selection == 3):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HT%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[4] Iced Teas:')
                     # if 4 was entered, display iced teas
                    if(selection == 4):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'IT%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[5] Frappucinos:')
                     # if 5 was entered, display frappucinos
                    if(selection == 5):                
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'F%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[6] Hot Drinks:')
                     # if 6 was entered, display hot drinks
                    if(selection == 6):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HD%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[7] Cold Drinks:')
                     # if 7 was entered, display cold drinks
                    if(selection == 7):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'CD%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[8] Bakery:')
                     # if 8 was entered, display bakery ites
                    if(selection == 8):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'B%' OR productid LIKE 'HB%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])
                    
                    print('[9] Exit')
                    
                    # ask user which menu category they would like to see
                    selection = inputHandle("Select category to see more options: ", int, [1, 9])
                    while selection == False:
                        print('Invalid input. Please try again.')
                        selection = inputHandle('Enter your selection: ', int, [1, 9])

            # function to show store locations, returns a list of shop id's and locations
            def stores():
                clearScreen()
                print(menuSep, " Postgres Coffee ", menuSep)

                print(f"{' Locations ':*^50}")
                # get shop ids and locations from database
                cur.execute("SELECT shopID, shoplocation FROM shop")
                i = 1
                shops = []
                locations = []
                # loop through returned shop information
                for record in cur.fetchall():
                    # display shop locations with index 
                    print(f"[{i}] {record['shoplocation']}")
                    # append shop id and location to lists
                    shops.append(record['shopid'])
                    locations.append(record['shoplocation'])
                    # update index
                    i += 1
                
                # return shop id list and location list
                return shops, locations

            # function for customer to place an order
            def placeOrder(user, fname):
                clearScreen()
                print(menuSep, " Postgres Coffee ", menuSep)

                print(menuSep, "Order Menu", menuSep)
                # display store locations, and get shop ids and locations
                shops, locations = stores()

                # ask user which store they would like to order from
                selection = inputHandle("Enter the number of the store you wish to order from: ", int, [1, len(shops)])
                while selection is False:
                    selection = inputHandle("Invalid input. Enter the number of the store you wish to order from: ", int, [1, len(shops)])
                
                # get shop id and location of selected store
                shopID = shops[selection-1]
                location = locations[selection-1]
            
                print(seperation)
                # display message
                print(f"Ordering To: {location}")

                flag = True # flag to check if order id already exists
                orderID = random.randint(1000000, 9999999) # generate random order id
                # verify order id does not already exist
                while flag:
                    # check if order id exists
                    orderidScript = 'SELECT orderID FROM orders WHERE orderID = %s'
                    orderid = (orderID,)
                    cur.execute(orderidScript, orderid)

                    # if it does not exist, set flag to false
                    if len(cur.fetchall()) == 0:
                        flag = False
                    else:
                        # if it does exist, regenerate order id
                        orderID = random.randint(1000000, 9999999)

                # Drop views to avoid creating duplicate views
                cur.execute("DROP VIEW IF EXISTS shopBaristas")
                cur.execute("DROP VIEW IF EXISTS shopCashiers")

                # create views to get the selected store's baristas and cashiers
                cur.execute("CREATE VIEW shopBaristas AS SELECT * FROM barista JOIN employees ON empid = ssn WHERE storeID = %s", (shopID, ))
                cur.execute("CREATE VIEW shopCashiers AS SELECT * FROM cashiers JOIN employees ON empid = ssn WHERE storeID = %s", (shopID, ))    
                
                # get all baristas from view
                cur.execute("SELECT * FROM shopBaristas")
                baristas = []
                # add all baristas to a list
                for record in cur.fetchall():
                    baristas.append(record['ssn'])
                # define a random number to randomly assign the order to a barista
                rand = random.randint(0, len(baristas)-1)
                baristaID = baristas[rand]
                
                # get all cashiers from view
                cur.execute("SELECT * FROM shopCashiers")
                cashiers = []
                # add all cashiers to a list
                for record in cur.fetchall():
                    cashiers.append(record['ssn'])
                # define a random number to randomly assign the order to a cashier
                rand = random.randint(0, len(cashiers)-1)
                cashierID = cashiers[rand]

                totalprice = 0      # holds the total price of the order
                productCosts = 0    # holds the total product costs of the order
                items = []          # list that will hold tuples containing product IDs and the quanitity of each product
                
                order = ''
                # while loop until user enters 'n' to quit
                while order != 'n':
                    # ask user to input the name of the item they would like to purchase
                    order = inputHandle("Enter the name of the item you wish to order: ", str, [1, 999999999])
                    while order is False: # validate user input
                        order = inputHandle("Invalid input. Enter the name of the item you wish to order: ", str, [1, 999999999])
                    
                    # retrieve product information from database
                    orderScript = 'SELECT productid, price, productcost, stock FROM products WHERE productname = %s'
                    orderTuple = (order, )
                    cur.execute(orderScript, orderTuple)

                    product = cur.fetchall()    # holds all information returned from database

                    # if product was not found, display message
                    if len(product) == 0:
                        print('Item could not be found, please try again.')
                        order = input("Would you like to order more items? (y/n):")
                        order = order.lower()
                        continue
                    # if product is out of stock, display message
                    elif product[0][3] == 0:
                        print(f"We're sorry, our {order}s are out of stock at the moment.\nPlease try ordering something else.")
                        order = input("Would you like to order more items? (y/n):")
                        order = order.lower()
                        continue
                    
                    # define variables from returned information
                    prID = product[0][0]
                    price = product[0][1]
                    cost = product[0][2]
                    
                    # output the amount in stock
                    print("Amount in stock: ", product[0][3])
                    # ask for the amount they wish to order and verify the amount entered is in stock
                    amount = inputHandle("Enter how many of this item to order: ", int, [1, product[0][3]])
                    while amount is False:
                        amount = inputHandle("Invalid input. Enter how many of this item to order: ", int, [1, product[0][3]])

                    # calculate product cost and total price
                    productCosts += (cost * amount)
                    totalprice += (price * amount)

                    # check if customer already ordered this item 
                    inItems = False
                    for i in items:
                        # if item has already been ordered, update the amount to be ordered
                        if i[0] == prID:
                            amt = i[1] + amount
                            items.remove(i)
                            items.append((prID, amt))
                            inItems = True
                    
                    # if item has not already been ordered, add the tuple containing product Id and amount ot the items list
                    if not inItems:
                        items.append((prID, amount))

                    # calculate the new stock amount of the product by removing the amount ordered from the current stock
                    newstock = product[0][3] - amount

                    # update stock amount in database
                    cur.execute("UPDATE products SET stock = %s WHERE productid = %s", (newstock, prID))
                    conn.commit()

                    # ask user if they would like to input more items
                    order = input("Would you like to order more items? (y/n): ")
                    order = order.lower()
                    print(seperation)

                # if the total price is greater than zero, create the order
                if totalprice > 0:
                    dateToday = datetime.today().strftime('%Y-%m-%d')   # get today's date

                    # Insert values into orders table in database
                    createOrder = 'INSERT INTO orders(orderid, customerid, storeid, dates, totalprice, cashierid, baristaid) VALUES(%s, %s, %s, %s, %s, %s, %s)'
                    orderValues = (orderID, user, shopID, dateToday, totalprice, cashierID, baristaID)
                    cur.execute(createOrder, orderValues)

                    # insert all the items the customer ordered into the contain table along with the amount of each item
                    for i in items:
                        insertScript = 'INSERT INTO contain(orid, prid, quantity) VALUES(%s, %s, %s)'
                        insertVals = (orderID, i[0], i[1])
                        cur.execute(insertScript, insertVals)

                    # calculate the profit from this order by removing product costs from the price
                    profit = totalprice - productCosts
                    
                    # get the shops revenue
                    cur.execute("SELECT revenue FROM shop WHERE shopid = %s", (shopID,))
                    fetch = cur.fetchall()
                    revenue = fetch[0][0]
                    # calculate the new shop revenue and update the database 
                    newrevenue = revenue + profit
                    cur.execute("UPDATE shop SET revenue = %s WHERE shopID = %s", (newrevenue, shopID))
                    
                    # output receipt including 
                    print(f"\nYour order has been placed, {fname}! \
                          \nOrder #{orderID}\tTotal: ${totalprice}\nYour order should be ready in about 15-20 minutes.")
                else: # if order total is not greater than zero, no items have been ordered, output message
                    print("No order has been created.")
            
            # function to cancel an existing order, takes the customer's username and first name
            def cancelOrder(user, fname):
                clearScreen()
                print(menuSep, " Postgres Coffee ", menuSep)

                # create function to delete from contain table
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
                # create trigger to call delete_from_contain() function before delete from orders table
                cur.execute("CREATE OR REPLACE TRIGGER trig BEFORE DELETE ON orders FOR EACH ROW EXECUTE PROCEDURE delete_from_contain()")
                
                # retrive all orders made by the current user
                cur.execute("SELECT * FROM orders WHERE customerid = %s", (user, ))
                orders = cur.fetchall()
                # if no orders have been made, output message
                if len(orders) == 0:
                    print('There are currently no orders in progress for you.')
                else:
                    print(f"Here are the orders in progress for you, {fname}:")
                    orderlist = []
                    # display orders and append order id's to list
                    for record in orders:
                        print(f"Order: #{record['orderid']}\tDate Placed: {record['dates']}\tTotal Price: {record['totalprice']}")
                        orderlist.append(str(record['orderid']))

                    print()
                    # ask user for the order id of the order to cancel
                    selection = input("Enter the order number you wish to cancel (enter q to cancel): ")
                    # while loop until order is cancelled or user wants to quit
                    while selection != 'q':
                        # if user inputs an order id that is not theirs, output message and retake input
                        if selection not in orderlist:
                            selection = input("Order Number does not exist, please try again. \
                                              \nEnter the order number you wish to cancel (enter q to cancel): ")
                        else:
                            # if user inputs an order id that is theirs, delete order from orders table
                            cur.execute("DELETE FROM orders WHERE orderid = %s", (selection, ))
                            # display message and break from loop
                            print(f"\nOrder #{selection} successfully cancelled! A refund will be issued to you shortly.")
                            break

            # customer menu, takes in username and first name of the customer logged in
            def custView(user, fname):
                selection = 0
                signOut = False

                while selection != 6:
                    print('\n** Postgres Coffee **')
                    if len(fname) != 0:
                        print(f'Welcome Back, {fname}!')
                    print('Please choose an option')
                    print('[1] Menu')
                    print('[2] Store locations')
                    print('[3] Order')
                    print('[4] Cancel Order')
                    print('[5] Sign Out')
                    print('[6] Quit')

                    selection = inputHandle('Enter your selection: ', int, [1, 6])
                    while selection == False:
                        print('Invalid input. Please try again.')
                        selection = inputHandle('Enter your selection: ', int, [1, 6])
                    
                    print()

                    if selection == 1:
                        menu()
                    elif selection == 2:
                        stores()
                    elif selection == 3:
                        placeOrder(user, fname)
                    elif selection == 4:
                        cancelOrder(user, fname)
                    elif selection == 5:
                        print('Signing Out...\n')
                        signOut = True
                        time.sleep(3)
                        break
                    elif selection == 6:
                        print('Goodbye!\n')
                    
                    print(menuSep)
                    conn.commit()
                
                if signOut:
                    clearScreen()
                    guestView()

            # guest view / default view
            def guestView():
                # display welcome message
                print(f"{'':*^50}")
                print(f"{' Welcome to Postgres Coffee! ':*^50}")
                print(f"{'':*^50}\n")
                selection = 0           # hold user selection
                user = ''               # hold username
                fname = ''              # hold first name
                isEmployee = False      # bool to check if user is an employee
                
                # loop until quit, or user has signed in
                while selection != 5 and len(fname) == 0:
                    # display menu options
                    print('\n** Postgres Coffee **')
                    print('Please choose an option')
                    print('[1] Menu')
                    print('[2] Store locations')
                    print('[3] Sign in')
                    print('[4] Sign up')
                    print('[5] Quit')

                    # ask user for selection and handle input
                    selection = inputHandle('Enter your selection: ', int, [1, 5])
                    while selection == False:
                        print('Invalid input. Please try again.')
                        selection = inputHandle('Enter your selection: ', int, [1, 5])
                    
                    print()

                    if selection == 1:
                        # show menu
                        menu()
                    elif selection == 2:
                        # show store locations
                        stores()
                    elif selection == 3: # sign in
                        print(seperation)
                        # ask user if they want to log in as employee or customer
                        print('[1] Customer Login')
                        print('[2] Employee Login')
                        # handle user selection
                        s = inputHandle('Enter your selection: ', int, [1, 2])
                        while s is False:
                            print('Invalid Input. Please try again.')
                            s = inputHandle('Enter your selection: ', int, [1, 2])
                        
                        if s == 1:
                            # if 1, call customer login function
                            print(seperation)
                            user, fname = login()
                        else:
                            # if 2, call employee login function
                            print(seperation)
                            user, fname, isEmployee = emplogin()
                    elif selection == 4:
                        # create an account
                        accCreate()
                    elif selection == 5:
                        print('Goodbye!\n')
                    
                    # print decor and commit changes to db
                    print(menuSep)
                    conn.commit()
                
                # check if an employee logged in
                if isEmployee:
                    # check if employee is a manager
                    cur.execute('SELECT * FROM managers WHERE managerid = %s', (user, ))
                    if len(cur.fetchall()) != 0:
                        # if employee is a manager, open manager menu
                        managerView(user, fname)
                    else:
                        # if a regular employee, open employee menu
                        empView(user, fname)
                elif len(fname) != 0:
                    # if a customer logged in, open customer menu
                    custView(user, fname)

            # manager view, takes the manager's ssn and first name
            def managerView(ssn, fname):
                selection = 0       # hold user selection
                signOut = False     # bool to check if user wants to sign out
                while selection != 7:
                    # display menu options
                    print('\n** Postgres Coffee **')
                    if len(fname) != 0:
                            print(f'Welcome Back, {fname}!')
                    print('\nPlease choose an option')
                    print('[1] Menu')
                    print('[2] View Order')
                    print('[3] Cancel Order')
                    print('[4] Profile')
                    print('[5] Request Stock from Supplier')
                    print('[6] Sign Out')
                    print('[7] Quit')

                    # ask user selection and handle input
                    selection = inputHandle('Enter your selection: ', int, [1, 7])
                    while selection == False:
                            print('Invalid input. Please try again.')
                            selection = inputHandle('Enter your selection: ', int, [1, 7])
                    
                    print()

                    if selection == 1:
                        # see menu
                        menu()
                    elif selection == 2:
                        #see orders in the stores
                        emplViewOrder(ssn)
                    elif selection == 3:
                        #cancel order
                        emplCancelOrderView(ssn)
                    elif selection == 4:
                        #see profile
                        emplProfile(ssn)
                        cur.execute("SELECT fname FROM employees WHERE ssn = %s", (ssn, ))
                        fname = cur.fetchone()['fname']
                    elif selection == 5:
                        # request restock from supplier
                        requestStock(ssn)
                    elif selection == 6:
                        # sign out
                        print('Signing Out...\n')
                        signOut = True
                        time.sleep(3)
                        break
                    elif selection == 7:
                        #quit
                        print('Goodbye!\n')
                    
                    # print decor and commit changes to db
                    print(menuSep)
                    conn.commit()
                    
                # if user decided to sign out, clear screen and return to the guest menu
                if signOut:
                    clearScreen()
                    guestView()

            # employee view, takes employee ssn and first name
            def empView(ssn, fname):
                selection = 0       # menu input
                signOut = False     # bool to check if user wants to sign out
                while selection != 6:
                    # display menu options
                    print('\n** Postgres Coffee **')
                    if len(fname) != 0:
                            print(f'Welcome Back, {fname}!')
                    print('\nPlease choose an option')
                    print('[1] Menu')
                    print('[2] View Order')
                    print('[3] Cancel Order')
                    print('[4] Profile')
                    print('[5] Sign Out')
                    print('[6] Quit')

                    # input selection, and handle user input
                    selection = inputHandle('Enter your selection: ', int, [1, 6])
                    while selection == False:
                            print('Invalid input. Please try again.')
                            selection = inputHandle('Enter your selection: ', int, [1, 6])
                    
                    print()

                    if selection == 1:
                        # see menu
                        menu()
                    elif selection ==2:
                        #see orders in the stores
                        emplViewOrder(ssn)
                    elif selection ==3:
                        #cancel order
                        emplCancelOrderView(ssn)
                    elif selection == 4:
                        #see profile
                        emplProfile(ssn)
                        cur.execute("SELECT fname FROM employees WHERE ssn = %s", (ssn, ))
                        fname = cur.fetchone()['fname']
                    elif selection ==5:
                        #sign out
                        print('Signing Out...\n')
                        signOut = True
                        time.sleep(3)
                        break
                    elif selection ==6:
                        #quit
                        print('Goodbye!\n')
                    
                    # print decor and commit changes to db
                    print(menuSep)
                    conn.commit()
                
                # if user has chosen to sign out, clear screen and return to guest menu
                if signOut:
                    clearScreen()
                    guestView()

            # function for a manager to request stock from a supplier, takes in manager ssn
            def requestStock(ssn):
                # clear screen and display decor
                clearScreen()
                print(menuSep, " Postgres Coffee ", menuSep)
                print("=" * 15, "Requesting Stock", "=" * 15)

                today = datetime.today().strftime('%Y-%m-%d') # get today's date

                # display supplier information, and append ids to list
                print("Suppliers:")
                suppliers = []
                cur.execute("SELECT * FROM supplier")
                for record in cur.fetchall():
                    print("{:<10} {:<50} {:<12}".format(record['supplierid'],record['suppaddress'],record['fname']))
                    suppliers.append(str(record['supplierid']))

                # ask user which supplier they wish to order from, handle user input
                suppID = input("Enter the supplier id to order from (enter q to quit): ")
                while suppID not in suppliers:
                    if suppID == 'q':
                        return
                    else:
                        suppID = input("Invalid input. Enter the supplier id to order from (enter q to quit): ")

                # get first name of supplier and display message
                cur.execute("SELECT fname FROM supplier WHERE supplierid = %s", (suppID, ))
                print(f"Ordering stock from {cur.fetchall()[0][0]}:")

                quit = False    # bool to check if user wants to quit
                product = ''    # hold product id to restock
                restock = []    # holds product ids and amounts to restock
                while not quit:
                    # ask user for the product id
                    product = input('Enter the product id to restock (enter q to stop): ')
                    # get stock from db
                    cur.execute("SELECT stock FROM products WHERE productid = %s", (product, ))
                    item = cur.fetchall()
                    # check if item was found
                    while len(item) == 0:
                        # if user decided to stop, set quit bool to True and break
                        if product == 'q':
                            quit = True
                            break
                        else:
                            # if item was not found, ask user for re-input
                            product = input('Invalid product id. Enter the product id to restock (enter q to stop): ')
                            cur.execute("SELECT productid, productname, stock FROM products WHERE productid = %s", (product, ))
                            item = cur.fetchall()

                    # check if the user decided to quit
                    if not quit:
                        # if not, check if the product has already been restocked by the selected supplier today
                        checkScript = "SELECT * FROM supplies WHERE supplierid = %s AND productid = %s AND restockdate = %s"
                        cur.execute(checkScript, (suppID, product, today))
                        # if the supplier did restock this product today, display message
                        if len(cur.fetchall()) != 0:
                            print("This supplier has already restocked this product today. Please try again tomorrow.")
                        else:
                            # if not, display amount in stock
                            print(f"Currently In Stock: {item[0][0]}")
                            # ask user for the amount to restock the item and handle user input
                            amount = inputHandle('Enter the amount to restock this item: ', int, [0, 99999999999999])
                            while amount is False:
                                amount = inputHandle('Invalid amount. Enter the amount to restock this item: ', int, [0, 99999999999999])
                            # calculate the new stock
                            newStock = item[0][0] + amount
                            # update stock in db and display message
                            cur.execute('UPDATE products SET stock = %s WHERE productid = %s', (newStock, product))
                            print(f"\nSuccessfully restocked product {product} by {amount}.\n")
                            
                            # check if item is already in the restock list
                            inRestock = False
                            for i in restock:
                                # if item has been restocked in this order, update the amount to be restocked
                                if i[0] == product:
                                    amt = i[1] + amount
                                    restock.remove(i)
                                    restock.append((product, amt))
                                    inRestock = True
                            
                            # if item has not already been restocked in this order, add the tuple containing product Id and amount to the restock list
                            if not inRestock:
                                restock.append((product, amount))
                
                # loop through the restock list
                for i in restock:
                    # insert supplierid, each product id, today's date, and the amount for each product to the supplier table
                    insertScript = "INSERT INTO supplies(supplierid, productid, restockdate, restockamnt) VALUES(%s, %s, %s, %s)"
                    insertValues = (suppID, i[0], today,  i[1])
                    cur.execute(insertScript, insertValues)
            
            # function to display all orders currently at a signed-in employee's store, takes in employee ssn
            def emplViewOrder(ssn):
                clearScreen()
                print(menuSep, " Postgres Coffee ", menuSep)

                # get the storeID of the employee
                cur.execute("SELECT storeid FROM employees WHERE ssn = %s", (ssn, ))
                print("*" * 19, "View Order", "*" * 19)
                storeID = cur.fetchone()['storeid']#clear space
                # get store location
                cur.execute("SELECT shoplocation FROM shop WHERE shopid = %s", (storeID,))
                location = cur.fetchone()['shoplocation']
                print("Orders at store:", location, "\n")
                # get orders at store
                order = "SELECT orderid, fname, customerid, totalprice, cashierid, baristaid, dates FROM orders NATURAL JOIN customer WHERE storeid = %s"
                # table from this query
                #  orderid | customerid | storeid |   dates    | totalprice | cashierid | baristaid | customerid | passw  |  fname  | lname | customeraddress |          email          |    dob     | phonenumber | balance 
                #  6223451 | 100002     |    6542 | 2023-04-24 |       2.75 |    312993 |    312994 | 100002     | abc123 | Michael | Smith | 456 Oak Ave     | michael.smith@gmail.com | 1988-08-20 |  5552345678 | 2500.00
                cur.execute(order,(storeID, ))
                orders = cur.fetchall()
                # check if there are orders at the store
                if len(orders) != 0:
                    # print orders
                    print(f"{'Order #':<10} {'Order Date':<12} {'Customer Name':<35} {'Customer ID':<12} {'Total':<12} {'CashierID':<12} {'BaristaID':<12}")
                    print('-' * 112)
                    for record in orders:
                        print("{:<10} {}   {:<35} {:<12} ${:<11} {:<12} {:<12}".format(record['orderid'],record['dates'],record['fname'], record['customerid'],record['totalprice'],record['cashierid'],record['baristaid']))
                    # if orders were found and printed, return true
                    return True
                else:
                    # if no orders found, print message and return false
                    print("No current ongoing orders at this store.")
                    return False

            # func for employees to cancel order at their store, needs employee's SSN
            def emplCancelOrderView(ssn):
                clearScreen()
                print(menuSep, " Postgres Coffee ", menuSep)

                # Display the current menu first
                flag = emplViewOrder(ssn)
                if flag:
                    # create function to delete from contain table
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
                    # create trigger to call delete_from_contain() function before delete from orders table
                    cur.execute("CREATE OR REPLACE TRIGGER trig BEFORE DELETE ON orders FOR EACH ROW EXECUTE PROCEDURE delete_from_contain()")
                    
                    # this part is to get all order numbers and store in orderlist
                    # get store of the emplyee
                    cur.execute("SELECT storeid FROM employees WHERE ssn = %s", (ssn, ))
                    storeID = cur.fetchone()['storeid']
                    # get orders at store
                    order = "SELECT orderid FROM orders o, customer c WHERE storeID = %s AND o.customerid = c.customerid"
                    #  orderid | customerid | storeid |   dates    | totalprice | cashierid | baristaid | customerid | passw  |  fname  | lname | customeraddress |          email          |    dob     | phonenumber | balance 
                    #  6223451 | 100002     |    6542 | 2023-04-24 |       2.75 |    312993 |    312994 | 100002     | abc123 | Michael | Smith | 456 Oak Ave     | michael.smith@gmail.com | 1988-08-20 |  5552345678 | 2500.00
                    cur.execute(order,(storeID, ))
                    # create list of order in store
                    orderlist = []
                    # store order numbers of this store in the list
                    for record in cur.fetchall():
                        orderlist.append(str(record['orderid'])) 

                    print()
                    # employee enter order id to canel, q to exit
                    selection = input("Enter order ID to cancel (enter q to quit): ")
                    while selection != 'q':
                        # not valid order, re enter
                        if selection not in orderlist:
                            selection = input("Invalid order ID, please enter order ID again to cancel: (enter q to quit): ")
                        else:
                            # success deleting
                            selecTuple = (selection, )
                            cur.execute("DELETE FROM orders WHERE orderid = %s", selecTuple)
                            print(f"\nOrder #{selection} successfully cancelled! A refund will be issued to the customer shortly.")
                            break
            
            # function for employees to view their profile, parameter: SSN
            def emplProfile(ssn):
                clearScreen()
                print(menuSep, " Postgres Coffee ", menuSep)

                cur.execute("DROP VIEW IF EXISTS emplProfileView")
                cur.execute("CREATE VIEW emplProfileView AS SELECT ssn, fname, lname, empaddress, email, dob, phonenumber, storeid, passw, salary FROM employees, employs WHERE ssn = %s AND empid = %s", (ssn,ssn, ))
                # table of view
#                  ssn   |  fname  | lname |              empaddress              |          email          |    dob     | phonenumber | storeid |    passw     | salary  
#                --------+---------+-------+--------------------------------------+-------------------------+------------+-------------+---------+--------------+---------
#                 312993 | William | Jones | 98637 Maple Avenue, Fresno, CA 90005 | William.Jones@gmail.com | 1992-01-18 |  3125550195 |    6542 | 123456qwerty | 5000.00
                
                # decoration
                print("Your profile information is:\n")

                # print profile
                cur.execute("SELECT * FROM emplProfileView")
                profile = cur.fetchone()
                for index, (key, value) in enumerate(profile.items()):
                    print("[{}]".format(index if index < len(profile)-1 and index > 0 else " "),key, ": ", value)
                # print following:
                # [ ] ssn :  312993
                # [1] fname :  William
                # [2] lname :  Jones
                # [3] empaddress :  98637 Maple Avenue, Fresno, CA 90005
                # [4] email :  William.Jones@gmail.com
                # [5] dob :  1992-01-18
                # [6] phonenumber :  3125550195
                # [7] storeid :  6542
                # [8] passw :  hellokitty
                # [ ] salary :  5000.00

                # choose whether want to update profile
                selection = inputHandle("Enter the number of the information you wish to update (0 to exit): ", int, [0, len(profile)-1])
                while selection is False:
                    selection = inputHandle("Inavlid Input\nEnter the number of the information you wish to update (0 to exit): ", int, [0, len(profile)-1])
                
                if(selection != 0):
                    # update first name, handle user input
                    if(selection == 1):
                        update = inputHandle("Enter you first name: ", str, [1, 30])
                        if update == False:
                            print("Name is too long or too short.")
                        else:
                            cur.execute("UPDATE employees SET fname = %s WHERE ssn = %s", (update, ssn,))
                            print("Successfully updated")
                    # update last name, handle user input
                    elif(selection == 2):
                        update = inputHandle("Enter your last name: ", str, [1, 30])
                        if update == False:
                            print("Name is too long or too short.")
                        else:
                            cur.execute("UPDATE employees SET lname = %s WHERE ssn = %s", (update, ssn,))
                            print("Successfully updated")
                    # update address, handle user input
                    elif(selection == 3):
                        update = inputHandle("Enter you address: ", str, [1, 50])
                        if update == False:
                            print("Address is too long or too short")
                        else:
                            cur.execute("UPDATE employees SET empaddress = %s WHERE ssn = %s", (update, ssn,))
                            print("Successfully updated")
                    # update email, handle user input
                    elif(selection == 4):
                        update = inputHandle("Enter you email: ", str, [1, 50])
                        if update == False:
                            print("Email is too long or too short")
                        else:
                            # regex matching an email (online src)
                            regex = '[^@]+@[^@]+\.[^@]+'

                            if(re.search(regex,update)):
                                cur.execute("UPDATE employees SET email = %s WHERE ssn = %s", (update, ssn,))
                                print("Successfully updated")
                            else:   
                                print("Invalid Email")
                    # update DOB, handle user input
                    elif(selection == 5):
                        update = input('Enter your date of birth (yyyy-mm-dd): ')
                        format = "%Y-%m-%d"     #format required for database
                        validDate = False       #flag to check for valid format
                        # try block to catch errors returned by datetime
                        try:
                            #call strptime to check for valid format, set validDate to bool value returned
                            validDate = bool(datetime.strptime(update, format))
                        except ValueError:
                            #dob does not match format
                            validDate = False
                        
                        #if dob does not match format, output message and take input again
                        if not validDate:
                            print("Provided date is in incorrect format.")
                        else:
                            cur.execute("UPDATE employees SET dob = %s WHERE ssn = %s", (update, ssn,))
                            print("Successfully updated")
                    # update phonenumber, 10 numbers, handle user input
                    elif(selection == 6):
                        update = inputHandle('Enter your phone number (no dashes): ', int, [0000000000, 9999999999])
                        if update is False:
                            print("Phone number is too long or too short")
                        else:
                            print("New phone number is: ", update)
                            cur.execute("UPDATE employees SET phonenumber = %s WHERE ssn = %s", (update, ssn,))
                            print("Successfully updated")
                    # employer update this field
                    elif(selection == 7):
                        print("Please contact employer to update this field")
                    # update password, handle user input
                    elif(selection == 8):
                        # input password, check for correct length, and confirm password with the user
                        # q for exit
                        passw = inputHandle('Enter your preferred password (max 30 characters) (q to exit): ', str, [1,30])
                        # while input != q
                        while passw != 'q':
                            if passw is False:
                                passw = inputHandle('Invalid Input. Enter your preferred password (max 30 characters): ', str, [1,30])
                            else:
                                pass2 = input('Confirm password: ')
                                if passw != pass2:
                                    print('Passwords do not match, please try again.')
                                    passw = inputHandle('Enter your preferred password (q to exit): ', str, [1,30])
                                else:
                                    break
                        # if input != q
                        if passw != 'q':
                            cur.execute("UPDATE employees SET passw = %s WHERE ssn = %s", (passw, ssn,))
                            print("Successfully updated")
                        
            # ------------------------ HELPER FUNCTIONS ------------------------
            # clear screen
            def clearScreen():
                os.system('clear')
            
            # handle user input, takes in message to display, type to cast the input as, and range for the values
            def inputHandle(text, typeCast, range):
                # try-except block to catch casting error
                try:
                    # display message and take user input
                    data = input(text)
                    # try casting data
                    data = typeCast(data)
                except ValueError:
                    # if input could not be cast, return False
                    return False
                else:   # if value could be cast
                    # if desired input is int, check if input is in the given range
                    if typeCast == int and (range[0] <= data <= range[1]):
                        # if input is in the range, return input
                        return data
                    # if desired input is string, check if length is in the given range
                    elif typeCast == str and (range[0] <= len(data) <= range[1]):
                        # if it is in the given range, check if '--' is in the string
                        # this is to prevent sql injections
                        if '--' in data:
                            # if '--' was found, return false
                            return False
                        else:
                            # if not found, return input
                            return data
                    else:
                        # value was not in the given range, return False
                        return False
            
            # call guest view
            guestView()

# catch any errors in program
except Exception as error:
    print(error)
finally:
    # close connection once user has decided to quit
    if conn is not None:
        conn.close()