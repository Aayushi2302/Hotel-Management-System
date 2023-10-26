import logging
import maskpass
import hashlib
import json
import sqlite3

from database import database_helper
from database.query_collector import AunthenticationQuery
import perform_admin_operations
import perform_staff_operations

logger = logging.getLogger('authentication')

class Aunthentication:
    def __init__(self) -> None:
        self.login_attempts = 3

    def invalid_login(self) -> None:
        print("Wrong password... Try Again!")
        logging.error("Invalid Login into the system.")
        self.login_attempts -= 1
        print(f"Invalid login...\nLogin attempts left : {self.login_attempts}\n")
    
    def first_time_login(username) -> None:
        logging.debug("First Login into the system successful.Change password.")
        print("\nChange your password...\n")
        new_password = maskpass.askpass(prompt="New Password : ", mask="*")
        confirm_password = ""
        while True:
            confirm_password =  maskpass.askpass(
                                    prompt="Confirm Password : ",
                                    mask="*"
                                )
            if new_password != confirm_password:
                print("Password does not match. Please enter your password again!\n")
            else:
                break
        hashed_password = hashlib.sha256(confirm_password.encode('utf-8')).hexdigest()
        database_helper.update_database(
            AunthenticationQuery.QUERY_FOR_UPDATING_DEFAULT_PASSWORD, 
            (hashed_password, 1, username)
        )
        print("Password changed successfully! Now login with your new password...\n")
    
    def valid_login(role) -> None:
        logging.debug("Successful login into the system.")
        print("Login Successful...\n")      

        role = json.loads(role)

        while True:
            print("\nYou have the following roles : ")
            i = 1
            for r in role :
                print(f"{r} : {i}")
                i += 1
            choice = int(input("Enter the number mentioned above for the role that you want to pursue : "))
            if role[choice-1] == "admin":
                perform_admin_operations.admin_operations()
            elif role[choice-1] == "staff" or choice == "reception":
                perform_staff_operations.staff_operations()
            else:
                print("Invalid input!! Enter again...")
            is_logout = int(input("Enter 1 to logout and 2 to continue : "))
            if is_logout == 1:
                logging.debug("Successful logout of the system.")
                print("Logout of the system successful....\n")
                break
    
    def user_authentication(self) -> None:
        print("Enter your credentails :")
        username = input("Username : ")
        try:
            user_data = database_helper.fetch_data_from_database(
                            AunthenticationQuery.QUERY_FOR_FETCHING_USER_CREDENTIALS, 
                            (username, )
                        )
            if not any(user_data):
                print(f"{username} does not exist. Try Again!")
                self.invalid_login()
            else:
                password_type = user_data[0][0]
                role = user_data[0][1]
                actual_password = user_data[0][2]
                if password_type == 0:
                    password = maskpass.askpass(prompt="Default Password : ", mask="*")
                    if password == actual_password:
                        self.first_time_login(username, actual_password)
                    else:
                        self.invalid_login()
                else:
                    password = maskpass.askpass(prompt="Password : ", mask="*")
                    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    if hashed_password == actual_password:
                        self.valid_login(role)
                    else:
                        self.invalid_login()
        except sqlite3.OperationalError as error:
            logging.error(error)
            print(f"Error encountered : {error}")