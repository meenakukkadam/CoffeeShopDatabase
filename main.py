# install psycopg2-binary: https://bobbyhadz.com/blog/python-no-module-named-psycopg2
import psycopg2
import psycopg2.extras # for returning data as dictionaries
import os
from datetime import datetime # for confirming dates match format

hostname = 'localhost'
database = 'coffeeshop'
username = 'din'
pwd = '123'
port_id = 5432

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
                conn.commit()

            def login():
                #While loop to keep displaying menu until user has logged in
                while True:
                    isValidUser = False     #flag to check if user input matches a user in the database
                    passw = ''              #if user was found, keep password to check input password is correct
                    # get username
                    user = input('Enter your username: ')

                    #check if user exists in the database
                    cur.execute("SELECT customerid, passw FROM customer")
                    for record in cur.fetchall():
                        if(record['customerid'].strip() == user):
                            #if user exists, keep password and set flag to true
                            passw = record['passw']
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
                            return user
                    else: #user does not exist, return message
                        print('Username does not exist. Please try again.')


            # display drinks menu
            def menu():
                cur.execute("DROP VIEW IF EXISTS menuview")
                cur.execute("CREATE VIEW MenuView AS SELECT productid, productname, price FROM products")
                # selection for choosing category to see more
                selection = 9
                while(selection !=0):
                    clearScreen()
                    print(f"{' MENU ':*^50}")
                    print('[1]. Hot Coffees:')
                    if(selection == 1):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HC%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])
                    
                    print('[2]. Cold Coffees:')
                    if(selection == 2):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'CC%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[3]. Hot Teas:')
                    if(selection == 3):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HT%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[4]. Iced Teas:')
                    if(selection == 4):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'IT%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[5]. Frappucinos:')
                    if(selection == 5):                
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'F%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[6]. Hot Drinks:')
                    if(selection == 6):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HD%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[7]. Cold Drinks:')
                    if(selection == 7):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'CD%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])

                    print('[8]. Bakery:')
                    if(selection == 8):
                        cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'B%' OR productid LIKE 'HB%'")
                        for record in cur.fetchall():
                            print('\t', record['productname'].ljust(60, '.'), record['price'])
                    
                    print('[0]. Exit:')
                    selection = inputHandle("Select category to see more options: ", int, [0, 8])
                    if(selection == 0):
                        break
                    while selection == False:
                        print('Invalid input. Please try again.')
                        selection = inputHandle('Enter your selection: ', int, [0, 8])

            # to show stores
            def stores():
                print(f"{' Locations ':*^50}\n")
                cur.execute("DROP VIEW IF EXISTS storeview")
                cur.execute("CREATE VIEW StoreView AS SELECT shoplocation FROM shop")
                cur.execute("SELECT * FROM storeview")
                for record in cur.fetchall():
                    print(record['shoplocation'])


            # order
            def placeOrder():
                print('What drink would you like to order?')
                menu()
                selection = inputHandle('Enter your selection: ', int, [1, 100])


            # customer view / default view
            def custView():
                # print(f'{"geeks" :*>15}')
                print(f"{'':*^50}")
                print(f"{' Welcome to Postgres Coffee! ':*^50}")
                print(f"{'':*^50}\n")
                selection = 0
                user = ''

                while selection != 6:
                    print('\nPlease choose an option')
                    print('[1] Menu')
                    print('[2] Store locations')
                    print('[3] Order')
                    print('[4] Sign in')
                    print('[5] Sign up')
                    print('[6] Quit')

                    selection = inputHandle('Enter your selection: ', int, [1, 6])
                    while selection == False:
                        print('Invalid input. Please try again.')
                        selection = inputHandle('Enter your selection: ', int, [1, 6])
                        
                    if selection == 1:
                        menu()
                    elif selection == 2:
                        stores()
                    elif selection == 3:
                        if len(user) == 0:
                            print('To order, please sign in to your account.')
                        else:
                            pass
                    elif selection == 4:
                        user = login()
                    elif selection == 5:
                        accCreate()
                    elif selection == 6:
                        print('Goodbye!\n')
                
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