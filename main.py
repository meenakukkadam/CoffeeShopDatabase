def accCreate():
    isValidUser = 0
    isValidPass = 0
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
        print('Account successfully created')
        return True
    else:
        print('Username or password already exist')
        return False

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
    print('to show menu')

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
    print(f"{' Welcome to COFFEE ':*^50}")
    print(f"{'':*^50}\n")

    print('Please choose an option')
    print('[1] Menu')
    print('[2] Store locations')
    print('[3] Order')
    print('[4] Sign in')
    print('[5] Sign up')

    selection = inputHandle('Enter your selection: ', int, [1, 5])
    print(f'print valid selection: {selection}')
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
        except ValueError as err:
            print(err)
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
    # print(inputHandle('input ', int))

    return()

main()