# install psycopg2-binary: https://bobbyhadz.com/blog/python-no-module-named-psycopg2
import psycopg2
import psycopg2.extras # this is for returning data as dictionaries

hostname = 'localhost'
database = 'CoffeeShop'
username = 'postgres'
pwd = 'admin'
port_id = 5433

conn = None

try:
    with psycopg2.connect(host = hostname, dbname = database, user = username, password = pwd, port = port_id) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            def accCreate():
                isValidUser = False
                while not isValidUser:
                    user = input('Enter your preferred username (max 10 characters): ') 

                    if(len(user) > 10):
                        print('Username greater than 10 characters, please try again.')  
                        accCreate()
                    
                    cur.execute("SELECT customerid FROM customer")
                    for record in cur.fetchall():
                        if(record['customerid'] == user):
                                isValidUser = 0
                                break
                    

                    if(isValidUser):
                        fname = input('Enter your first name: ')
                        lname = input('Enter your last name: ')
                        addr = input('Enter your address: ')
                        email = input('Enter your email: ')
                        dob = input('Enter your date of birth (yyyy-mm-dd): ')
                        phone = input('Enter your phone number (no dashes): ')
                        insertScript = 'INSERT INTO customer(customerid, fname, lname, customeraddress, email, dob, phonenumber, balance) VALUES(%s, %s, %s, %s, %s, %s, %s, 0)'
                        insertValues = [(user, fname, lname, addr, email, dob, phone),]
                        cur.execute(insertScript, insertValues)
                        return
                    else:
                        print('Username already exist, please try again')
                        accCreate()

            def login(user, passw):
                privilege = 0
                isValidUser = 0
                isValidPass = 0
                # get username, passw
                user = input('Enter the username: ')   
                passw = input('Enter sthe password: ')

                # compare with user from db
                if(user == 'a'):
                    isValidUser = 1
                else:
                    return False
                
                # compare with corresponding passw from db
                if(passw == 'b'):
                    isValidPass = 1
                else:
                    return False
                
                if(isValidUser and isValidPass):
                    print('Successfully logged in')
                    return True
                else:
                    print('Invalid user or password')
                    return False

            # display drinks menu
            def menu():
                cur.execute("DROP VIEW IF EXISTS menuview")
                cur.execute("CREATE VIEW MenuView AS SELECT productid, productname, price FROM products")
                print('Hot Coffees:')
                cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HC%'")
                for record in cur.fetchall():
                    print('\t', record['productname'].ljust(60), record['price'])
                
                print('Cold Coffees:')
                cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'CC%'")
                for record in cur.fetchall():
                    print('\t', record['productname'].ljust(60), record['price'])

                print('Hot Teas:')
                cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HT%'")
                for record in cur.fetchall():
                    print('\t', record['productname'].ljust(60), record['price'])

                print('Iced Teas:')
                cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'IT%'")
                for record in cur.fetchall():
                    print('\t', record['productname'].ljust(60), record['price'])

                print('Frappucinos:')
                cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'F%'")
                for record in cur.fetchall():
                    print('\t', record['productname'].ljust(60), record['price'])

                print('Hot Drinks:')
                cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'HD%'")
                for record in cur.fetchall():
                    print('\t', record['productname'].ljust(60), record['price'])

                print('Cold Drinks:')
                cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'CD%'")
                for record in cur.fetchall():
                    print('\t', record['productname'].ljust(60), record['price'])

                print('Bakery:')
                cur.execute("SELECT * FROM MenuView WHERE productid LIKE 'B%' OR productid LIKE 'HB%'")
                for record in cur.fetchall():
                    print('\t', record['productname'].ljust(60), record['price'])
                    

            # to show stores
            def stores():
                print('to show locations')

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

                while selection != 6:
                    print('\nPlease choose an option')
                    print('[1] Menu')
                    print('[2] Store locations')
                    print('[3] Order')
                    print('[4] Sign in')
                    print('[5] Sign up')
                    print('[6] Quit')

                    selection = inputHandle('Enter your selection: ', int, [1, 6])
                    if selection == 1:
                        menu()
                    elif selection == 2:
                        stores
                    elif selection == 3:
                        pass
                    elif selection == 4:
                        login('empty', 'empty')
                    elif selection == 5:
                        accCreate()
                
            # employee view
            def empView():
                pass

            # handle user selection
            def inputHandle(text, typeCast, range):
                # print(data)
                isValid = 0
                while(isValid == 0):
                    try:
                        data = input(text)
                        data = typeCast(data)
                    except ValueError:
                        print('Invalid input')
                    else:
                        break # break loop
                if (data >= range[0] and data <= range[1]):
                    return data
                else:
                    print('Input out of range')

                # if (type(data) is not typeCast ):
                #     print('invalid input')
                # else:
                #     data = typeCast(data)
            
            def main():
                custView()

                return()

            main()

except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()