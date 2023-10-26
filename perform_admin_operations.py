"""
    This file contains all the operations performed by admin.
"""
# third party imports
import shortuuid
from password_generator import PasswordGenerator
import json

# local file imports
from room import Room
from database import database_helper
from database.query_collector import AunthenticationQuery

def create_login_credentials() -> None:
    emp_id = "EMP" + shortuuid.ShortUUID().random(length = 5)
    pwo = PasswordGenerator()
    password = pwo.non_duplicate_password(7)
    role = input("Enter roles that you want to add for the employee separated by , : ").split(",")
    # role = ["admin", "staff"]
    emp_roles = json.dumps(role)
    username = input("Enter username : ")
    # username = "user@admin"
    database_helper.update_database(
        AunthenticationQuery.QUERY_FOR_SAVING_LOGIN_CREDENTIALS,
        (emp_id, username, password, emp_roles, 0)
    )
    
admin_menu = """
    Welcome to admin module :-)

    You can perfrom the below tasks :
    1. Add room
    2. Register room as under-construction
    3. Print room details
    4. Print check-in and check-out details
    5. Add login credentials
    6. Logout
"""

room_obj = Room()

def admin_operations() -> None:
    while True:
        print(admin_menu)
        admin_choice = int(input("\nEnter your choice between 1 to 6 : "))
        match admin_choice:
            case 1 : 
                room_obj.register_room()
            case 2 : 
                room_obj.register_room_as_under_construction()
            case 3 : 
                room_obj.print_room_data_from_database()
            case 4 : pass
            case 5 : 
                create_login_credentials()
            case 6 : 
                print("Logout from admin module successful...\n")
                break