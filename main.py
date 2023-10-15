# third party imports
import sys
import maskpass        
import time
import logging

# local file imports
import credentails_decryption
from room import Room
import perform_admin_operations
import database.database_helper as database_helper
from customer import Customer

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    level = logging.DEBUG,
                    filename = 'logs.txt')

logger = logging.getLogger('main')

def display_menu() -> None:
    user_choice = """
        Welcome to staff module :-)

        You can perfrom the below tasks :
        1. Register a customer
        2. Check in
        3. Check out
        4. Print room details
        5. Print customer details
        6. Delete customer details
        7. Perform admin operations
        8. Exit
    """
    print(user_choice)

if __name__ == "__main__":
    logger.info("Starting with the hotel management system.")
    database_helper.create_table_customer()
    logger.debug("customer table created successfully.")
    database_helper.create_table_room()
    logger.debug("room table created successfully.")
    print("----- Welcome to Hotel Reservation System ------")
    print("\n\n")
    print("Enter your role and credentails :")
    check = 1
    invalid_login_attempts = 0
    while True:
        try:
            if invalid_login_attempts == 3:
                sys.exit()
            role = input("Role : ")
            if role == "admin" or role == "reception":  
                try: 
                    user_name = input("Username : ")
                    password = maskpass.askpass(prompt="Password : ", mask="*")
                    # check = credentails_decryption.login_into_system(user_name, password, role)
                    logger.debug("Login credentails fecthed from database.")
                    time.sleep(2)
                    if check:
                        while True:
                            # menu for user choice 
                            display_menu()
                            choice = int(input("\nEnter your choice between 1 to 7 : "))
                            match choice:
                                case 1 : 
                                    obj = Customer()
                                    obj.register_customer()
                                case 2 : 
                                    room_obj = Room()
                                    room_obj.check_in_room()
                                case 3 : 
                                    room_obj = Room()
                                    room_obj.check_out_room()
                                case 4 :
                                    room_obj = Room()
                                    room_obj.print_room_data_from_database()
                                case 5 : 
                                    obj = Customer()
                                    obj.print_customer_data_from_database()
                                case 6 :
                                    print("Enter details of customer to delete : ")
                                    obj  = Customer()
                                    obj.remove_customer_data_from_database()
                                case 7 : 
                                    perform_admin_operations.admin_operations()
                                case 8 : 
                                    print("Thank you for using the system! Hope you had a great experience :-)")
                                    sys.exit()
                    else:
                        invalid_login_attempts += 1
                        if invalid_login_attempts == 3:
                            raise Exception("Login attempts exhausted. Please login after some time!!")
                        else:
                            print(f"Inavlid Login! Login Restricted\nLogin attempts left : {3-invalid_login_attempts}")
                except Exception as e:
                    print(e)
            else:
                invalid_login_attempts += 1
                if invalid_login_attempts == 3:
                    raise Exception("Login attempts exhausted. Please login after some time!!")
                else:
                    print(f"Role not justified! Login Restricted\nLogin attempts left : {3-invalid_login_attempts}")
        except Exception as e:
            logger.debug(e)
            print(e)
else:
    logger.debug("Wrong file run. Run main.py for running the program.")
    sys.exit()
















