from customer import Customer
import sys
import maskpass        # to hide the password
import time
import credentails_decryption
from room import Room
import perform_admin_operations

def display_menu():
    user_choice = """
        You can perfrom the below tasks :
        1. Register a customer
        2. Check in
        3. Check out
        4. Print room details
        5. Print customer details
        6. Perform admin operations
        7. Exit
    """
    print(user_choice)

if __name__ == "__main__":
    Customer.create_table_customer()
    Room.create_table_room()
    print("----- Welcome to Hotel Reservation System ------")
    print("\n\n")
    print("Enter your role and credentails :")
    role = input("Role : ")
    user_name = input("Username : ")
    password = maskpass.askpass(prompt="Password : ", mask="*")
    check = credentails_decryption.login_into_system(user_name, password, role)
    time.sleep(2)
    # check = 1
    # check_counter = 0
    try:
        if check: 
            try: 
                if role == "admin" or role == "reception": 
                    while True:
                        # menu for user choice 
                        display_menu()
                        choice = int(input("\nEnter your choice between 1 to 7 : "))
                        match choice:
                            case 1 : 
                                print("Enter customer details....\n")
                                obj = Customer()
                                obj.register_customer()
                            case 2 : 
                                room_obj = Room()
                                room_obj.check_in_room()
                            case 3 : pass
                            case 4 :
                                room_obj = Room()
                                room_obj.print_room_data_from_database()
                            case 5 : 
                                print("The customer details are :\n")
                                obj = Customer()
                                obj.print_customer_data_from_database()
                            case 6 : 
                                while True:
                                    perform_admin_operations.admin_operations()
                            case 7 : 
                                print("Thank you for using the system! Hope you had a great experience :-)")
                                break
                else:
                    raise Exception("Role not justified! Login Restricted")
            except Exception as e:
                print(e)
        else:
            raise Exception("Inavlid Login! Login Restricted")
    except Exception as e:
        print(e)
else:
   sys.exit()
















