from room import Room

def display_admin_menu() -> None:
    user_choice = """
        Welcome to admin module :-)

        You can perfrom the below tasks :
        1. Register a room
        2 .Register an employee
        3. Remove a room
        4. Remove an employee
        5. Add login credentials
        6. Exit
    """
    print(user_choice)

def admin_operations() -> None:
    while True:
        display_admin_menu()
        admin_choice = int(input("\nEnter your choice between 1 to 6 : "))
        match admin_choice:
            case 1 : 
                room_obj = Room()
                room_obj.register_room()
            case 2 : pass
            case 3 : pass
            case 4 : pass
            case 5 : pass
            case 6 : 
                print(
                    """
                    Thank you for using the system! Hope you had a great experience :-)
                    Redirecting back to staff module....
                    """
                )
                break