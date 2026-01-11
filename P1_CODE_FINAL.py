"""
1P13 Project 1 - Robotic End Effector System
------------------------------------------

This program simulates a warehouse order system. It allows the user to make a unique account and a secure password which is hased using bcrypt, it authenticates the user and allows them to login, lets the user scan and order products, it commands the Q-arm to pick up ordered items, gives the user a order receipt, save all orders into a csv file, and gives the user a final summary of all their past orders.

MON-05, McMaster, Fall 2025
"""

## Modules
import random
import bcrypt

## Functions

## Main
def main():
    """
    The Main function handles user authentication, order placement loop, and prints a summary at the end, by calling the indiviual functions.
    """
    #initializes all files
    initialize_files()
    
    # Greets user
    print("Hello and Welcome to 1P13 Warehouse!")
    userID = authenticate() # Authenticate the user and return their userID as a variable
    choice = input("Do you want to place an order? (yes/no): ") # Asks if they want to place an order

    # Checks user input
    while choice != "yes" and choice != "no":
        print("Invalid Response")
        choice = input("Do you want to place an order? (yes/no): ")

    # Loops so user can place multiple orders
    while choice == "yes":
        products = scan_barcode() # Allows user to scan barcode and stores string as a variable
        products_list = lookup_products(products) # Convert product string to list with prices
        pack_products(products_list) # Calls function that controls q arm, picks up the requested items
        complete_order(userID, products_list) # Complete the order prints a receipt
        choice = input("Do you want to place another order? ") # Asks for another order
        while choice != "yes" and choice != "no":
            print("Invalid Response")
            choice = input("Do you want to place an order? (yes/no): ")

    # Gives user summary
    print("\n")
    customer_summary(userID)
    print("Thank you and have a great day!")

## sign_up - Marcus Zackrias
def sign_up():
    """
    This function handles the user sign up process by first asking for a unique UserID, validating password format (uppercase, lowercase, digit, symbol, length), hashing the password using bcrypt, storing UserID and hashed password in users.csv file.
    """


    # Lists of password character requirements used for password validation
    CAPS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

    LOWS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    NUM = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

    SMBLS = ['!', '.', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '[', ']']


    # Ask user for a UserID
    userid = input("Create a UserID: ")

    # Open CSV and loops until ID is unique
    while True:

        duplicate_found = False

        file = open("users.csv")
        for line in file:
            if userid == line.split(",")[0]: # Compares UserID from user to UserIds in file
                print("\033[31mThis UserID already exists, Please try again\033[0m")
                userid = input("Create a different UserID: ")
                duplicate_found = True
                break
        file.close()

        if not duplicate_found:
            break


    # Password requirement checks
    check_caps = True
    check_lows = True
    check_nums = True
    check_syms = True
    check_len = True

    # Ask user for a password and shows the password requirements
    print("Create a password that meets the following conditions", "At least 6 characters", "At least 1 number", "At least 1 lowercase letter", "At least 1 uppercase letter", "At least 1 special symbol", sep="\n")

    password = input("Enter your password: ")

    pswrd_list = list(password)

    # Checks if the password meets all the conditions by individually checking each character in the password to each character in the requirements lists
    for characters in pswrd_list:
        for C in CAPS:
            if characters == C:
                check_caps = False

        for L in LOWS:
            if characters == L:
                check_lows = False

        for n in NUM:
            if characters == n:
                check_nums = False

        for S in SMBLS:
            if characters == S:
                check_syms = False

    # Check minimum length
    if len(password) >= 6:
        check_len = False

    # If the password was not valid keeps asking user for a valid password
    while check_caps or check_lows or check_nums or check_syms or check_len:

        # Resets the requirement checks
        check_caps = True
        check_lows = True
        check_nums = True
        check_syms = True
        check_len = True

        # Gets new password
        print("\033[31mInvalid Password, make sure it meets the conditions above.\033[0m")

        password = input("Enter your password: ")

        pswrd_list = list(password)

        # Validates again
        for characters in pswrd_list:
            for C in CAPS:
                if characters == C:
                    check_caps = False

            for L in LOWS:
                if characters == L:
                    check_lows = False

            for n in NUM:
                if characters == n:
                    check_nums = False

            for S in SMBLS:
                if characters == S:
                    check_syms = False

        if len(password) >= 6:
            check_len = False

    print("Password created successfully")

    # Hashes the password using bcrypt
    hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt() ).decode('utf-8')

    # Store UserID and encrypted password into CSV file
    file = open("users.csv", "a")

    file.write(str(userid) + "," + str(hash) + "\n")

    file.close()

    print("Your account has been created successfully")

    return None

## authenticate - Abdullah Saleem
def authenticate():
    """
    Asks the user to log in, or sign up depending on whether they have an account or not.
    Inputs: User credentials, users.csv
    Outputs: Success or failure message
    Returns: userid if successful or None if failure.
    """
    #ask user if they have an account or not
    user_input = input("Do you already have an account? (yes/no): ")

    while user_input != "yes" and user_input != "no":
        print("\033[31mInvalid Response\033[0m")
        user_input = input("Do you already have an account? (yes/no): ")


    #if they don't call sign_up()
    if user_input == "no":
        print("Lets create one for you!")
        sign_up()
        print("Account created!.\n")

    #once they have an ccount or if they already do, start while loop
    while True:

        #ask the user to input their userid and password
        userid = input("Enter your UserID: ")
        password = input("Enter your password: ")

        #open the file
        file = open("users.csv", "r")
        found=False
        #read it line by line
        for line in file:

            parts = line.strip().split(",")

            #makes sure to only look at lines with 2 parts
            if len(parts) == 2:
                saved_user = parts[0]
                saved_hash = parts[1]

                #check if entered useid matches
                if userid == saved_user:
                    found=True
                    #checks to see if the password matches and prints success message if it doesn't'
                    if bcrypt.checkpw(password.encode("utf-8"),
                                      saved_hash.encode("utf-8")):
                        print("\n")
                        print("Login successful! Welcome,", userid)
                        file.close()
                        return userid

                    #if its false, restarts the while loop and lets the user try again
                    else:
                        print("\033[31mIncorrect password. Please try again.\033[0m\n")
                        file.close()
                        break

        file.close()

        #prints if userid did not match any line of users.csv
        if not found:
            print("\033[31mUserid not found. Please try again.\033[0m\n")


## lookup products - Charles Connor
def lookup_products(products):
    """
    Reads product names from the input string and looks them up in products.csv. Any products found in the CSV are returned as a list of [name, price] pairs. Products that do not appear in products.csv produce a warning message.

    Parameters:
        products (str): A string containing product names (separated by commas or spaces).

    Returns:
        list: A 2D list where each element is [product_name, price]. Only products found in the CSV file are included.

    Outputs:
        None
    """

    scanned = products.replace(",", " ").split()  # turn the input string into a list of product names

    product_list = []  # now a 2D list

    file = open("products.csv", "r")  # open the CSV file

    for line in file:
        line = line.strip()
        name, price = line.split(",")  # split each CSV line into name and price
        product_list.append([name, float(price)])  # store as a list inside the 2D list

    file.close()  # important: close the file

    found = []  # this will hold the matched products
    for name in scanned:
        for prod in product_list:
            if prod[0] == name:
                found.append(prod)  # add match
                break
        else:
            print(f"\033[31mWarning: Product '{name}' not found.\033[0m")  # warn when missing

    return found  # return 2D list


## complete order - Pranith Sepuri
def complete_order(userid, product_list):
    '''
    This fucntion completes the customer's order by calculating the total, applies a random discount,
    computes tax, and recordes the order in a csv file, and finally prints a receipt
    Parameters: userid(str), product_list[2-D list] split into [product_name(str), price(float)]
    Return: None
    Output: Receipt
    '''
    tax_rate = 0.13
    subtotal = 0
    for item in product_list:  #finding each item in product_list
        subtotal += item[1]        #adding the price of items (total)

    discount_percent = random.randint(5, 50) #applying random discount
    discount_amount = subtotal * (discount_percent / 100)
    subtotal_after_discount = subtotal - discount_amount


    tax = subtotal_after_discount * tax_rate #calulting tax
    total = subtotal_after_discount + tax #new subtotal


    order_count = 0

    file = open("orders.csv", "r") #counting previous orders

    for line in file:
        line = line.strip()
        parts = line.split(",")   #split into a list to check the customers order

        if parts[0] == userid:    #check for the userid
            order_count += 1
    file.close()

    product_names = []
    for item in product_list: #going through product list to extract the name of the product
        product_names.append(item[0])


    new_order = [userid, f"{total:.2f}"] #starting a new order

    for name in product_names:
        new_order.append(name) #adding the product names to the new order

    list_to_string = ""
    for i in range(len(new_order)):
        list_to_string += new_order[i] #converting the order to a string
        if i != len(new_order) - 1: #only adding a comma if it's not the last item
            list_to_string += ","


    file = open("orders.csv", "a")
    file.write(list_to_string + "\n") #writing the CSV line
    file.close()

    print("\n=======================================")
    print("            ORDER RECEIPT")
    print("=======================================\n")

    print(f"Customer: \033[34m{userid}\033[0m\n")

    print("Items Purchased:")
    print("-------------------------------")

    first_item = True
    for item in product_list:
        name = item[0]
        price = item[1]
        spaces = " " * (20 - len(name))  #spacing based on name of the item so formatting isn't messed up
        if first_item:
            print(f"{name}:{spaces}$  {price:.2f}") #only want the dollar symbol at the top so its not redundant
            first_item = False
        else:
            print(f"{name}:   {spaces}{price:.2f}")

    print("-------------------------------")
    print(f"Subtotal:               {subtotal:.2f}")
    print(f"\033[31mDiscount ({discount_percent}%):       -   {discount_amount:.2f}\033[0m")
    print(f"Tax:                    {tax:.2f}")
    print("-------------------------------")
    print(f"TOTAL:               $  {total:.2f}")
    print("-------------------------------\n")

    print("You have now made", order_count + 1, "orders. Thank you!\n")

## customer summary - Jason Saysana
def customer_summary(userID):
    """
    gets the customer summary for a given user. Loops through all the orders and adds up the total if the order's user is the one the function is looking for. Then it prints a recipt of the the user, the number of orders, the total spent, then the quantities of of the items bought.
    """
    number_of_orders = 0
    total = 0
    quantities = [0,0,0,0,0,0]
    file = open("orders.csv")
    for order in file:
        order_list = order.strip().split(",")
        if order_list[0] == userID:#check the id
            number_of_orders += 1
            total += float(order_list[1])
            for item in range(1,len(order_list)):
                #check the order for the items
                if order_list[item] == "Sponge":
                    quantities[0] += 1
                elif order_list[item] == "Bottle":
                    quantities[1] += 1
                elif order_list[item] == "Rook":
                    quantities[2] += 1
                elif order_list[item] == "D12":
                    quantities[3] += 1
                elif order_list[item] == "WitchHat":
                    quantities[4] += 1
                elif order_list[item] == "Bowl":
                    quantities[5] += 1
    file.close()
#Print summary here
    print(f"{('     USER SUMMARY     ').rjust(20)}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nUser ID: \033[34m{userID}\033[0m\nNumber of orders: {str(number_of_orders).ljust(20)}\nTotal: ${total:.2f}\n===============================")
    for i in range(len(quantities)):
        if quantities[i] != 0:
            result = ""
            if i == 0:
                result +=("Sponges:   ")
            elif i == 1:
                result +=("Bottles:   ")
            elif i == 2:
                result +=("Rooks:     ")
            elif i == 3:
                result +=("Dice:      ")
            elif i == 4:
                result +=("Witch Hats:")
            elif i == 5:
                result +=("Bowls:     ")
            result += (f"{str(quantities[i]).rjust(20)}")
            print(result)
    print("===============================")


## pack products
def pack_products(products_list):
    """
    Takes a list of products and controls Q arm making it pick up each product the prints confirmation.
    """
    for product in products_list:

        # Product is in format ["Item", price], so product[0] is name of item
        if product[0] == "Sponge":
            # Q arm commands
            
            arm.home()
            arm.rotate_gripper(180)

            arm.rotate_base(16.75)

            arm.rotate_gripper(-300)

            arm.rotate_elbow(-10)

            arm.rotate_gripper(-300)

            arm.rotate_shoulder(42)
            sleep(1)

            arm.rotate_gripper(50)
            sleep(1)

            arm.rotate_shoulder(-44)

            arm.rotate_base(-74)

            arm.rotate_elbow(40)

            arm.rotate_gripper(-90)

            arm.rotate_gripper(180)
            sleep(1)

            arm.home()
            
            print("\033[34mSponge picked up successfully\033[0m") # Gives confirmation

        elif product[0] == "Bottle":
            # Q arm commands
            
            arm.home()
            arm.rotate_gripper(180)

            arm.rotate_base(10)

            arm.rotate_gripper(-300)

            arm.rotate_elbow(-10)

            arm.rotate_shoulder(46)
            sleep(1)

            arm.rotate_gripper(50)
            sleep(1)

            arm.rotate_shoulder(-43)
            sleep(1)

            arm.rotate_base(-66)
            sleep(1)

            arm.rotate_elbow(40)

            arm.rotate_gripper(-90)
            sleep(1)

            arm.rotate_gripper(180)
            sleep(1)

            arm.home()
            

            print("\033[34mBottle picked up successfully\033[0m") # Gives confirmation

        elif product[0] == "Rook":
            # Q arm commands
            
            arm.home()
            arm.rotate_gripper(180)

            arm.rotate_base(4)

            arm.rotate_gripper(-300)

            arm.rotate_elbow(-9)

            arm.rotate_shoulder(48)
            sleep(1)

            arm.rotate_gripper(50)
            sleep(1)

            arm.rotate_shoulder(-43)
            sleep(1)

            arm.rotate_base(-61)
            sleep(1)

            arm.rotate_elbow(40)

            arm.rotate_gripper(-90)
            sleep(1)

            arm.rotate_gripper(180)
            sleep(1)

            arm.home()
            

            print("\033[34mRook picked up successfully\033[0m") # Gives confirmation

        elif product[0] == "D12":
            # Q arm commands
            
            arm.home()
            arm.rotate_gripper(180)

            arm.rotate_base(-3.5)

            arm.rotate_gripper(-300)

            arm.rotate_elbow(-6)

            arm.rotate_gripper(-300)

            arm.rotate_shoulder(49)
            sleep(1)

            arm.rotate_gripper(50)
            sleep(1)

            arm.rotate_shoulder(-43)
            sleep(1)

            arm.rotate_base(-59)
            sleep(1)

            arm.rotate_elbow(40)

            arm.rotate_gripper(-90)
            sleep(1)

            arm.rotate_gripper(180)
            sleep(1)

            arm.home()
            

            print("\033[34mD12 picked up successfully\033[0m") # Gives confirmation

        elif product[0] == "WitchHat":
            # Q arm commands
            
            arm.home()
            arm.rotate_gripper(180)

            arm.rotate_base(-10)

            arm.rotate_gripper(-300)

            arm.rotate_elbow(-10.4)

            arm.rotate_shoulder(45.3)
            sleep(1)

            arm.rotate_gripper(50)
            sleep(1)

            arm.rotate_shoulder(4)
            sleep(1)

            arm.rotate_shoulder(-43)
            sleep(1)

            arm.rotate_base(-55)
            sleep(1)

            arm.rotate_elbow(40)

            arm.rotate_gripper(-90)
            sleep(1)

            arm.rotate_gripper(180)
            sleep(1)

            arm.home()
            

            print("\033[34mWitchHat picked up successfully\033[0m") # Gives confirmation

        elif product[0] == "Bowl":
            # Q arm commands
            
            arm.home()
            arm.rotate_gripper(180)

            arm.rotate_base(-16.3)

            arm.rotate_gripper(-300)

            arm.rotate_elbow(-10)

            arm.rotate_shoulder(47.8)
            sleep(1)

            arm.rotate_gripper(50)
            sleep(1)

            arm.rotate_shoulder(-24)

            arm.rotate_elbow(20)

            arm.rotate_shoulder(-24)

            arm.rotate_elbow(20)

            arm.rotate_base(-45)

            arm.rotate_elbow(10)

            arm.rotate_gripper(-90)
            sleep(1)

            arm.rotate_gripper(180)
            sleep(1)

            arm.home()
            
            print("\033[34mBowl picked up successfully\033[0m") # Gives confirmation

## Initilize all the csv files 
def initialize_files():
    """
    This function tries opening all files needed, if that fails it makes them with the necessary contents.
    """

    # products.cvs
    try:
        # Try opening in read mode to check if it exists
       file = open("products.csv", "r")
       file.close()
    except:
        # If it fails, create it with your data
        file = open("products.csv", "w")
        file.write("Sponge,0.12\n")
        file.write("Bottle,8\n")
        file.write("Rook,612000\n")
        file.write("D12,11.99\n")
        file.write("Bowl,20\n")
        file.write("WitchHat,40\n")
        file.close()

    # user.cvs
    try:
        file = open("users.csv", "r")
        file.close()
    except:
        file = open("users.csv", "w")
        file.close()

    # orders.cvs
    try:
       file = open("orders.csv", "r")
       file.close()
    except:
        file = open("orders.csv", "w")
        file.close()

main()