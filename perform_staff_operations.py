"""
    This file contains all the operations performed by staff or admin.
"""

# local file imports
from customer import Customer
from room import Room

reception_or_staff_menu = """
    Welcome to staff module :-)

    You can perfrom the below tasks :
    1. Register a customer
    2. Check in
    3. Check out
    4. Print room details
    5. Print customer details
    6. Delete customer 
    7. Logout
"""
cust_obj = Customer()
room_obj = Room()

def staff_operations() -> bool:
    while True:
        print(reception_or_staff_menu)
        choice = int(input("Enter your choice (1-7) : "))
        match choice:
            case 1 : 
                cust_obj.register_customer()
            case 2 : pass
            case 3 : pass
            case 4 : 
                room_obj.print_room_data_from_database()
            case 5 : 
                cust_obj.print_customer_data_from_database()
            case 6 :
                cust_obj.remove_customer_data_from_database()
            case 7 : 
                print("Logout from staff module successful...\n")
                break
