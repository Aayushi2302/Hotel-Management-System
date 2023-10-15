"""
    This is a room module of the Hotel Reservation System project.
    This module is contains a Room class which has method to handle following functionalities :
    1. Registering of room
    2. Saving Room details to database
    3. Printing Room details
    4. Check in room
    5. Check out room
"""

# third party imports
import shortuuid
from tabulate import tabulate
import logging

# local files imports
from input_validation import room_input_validation
from input_validation import customer_input_validation
from database import database_helper
from database import query_collector

logger = logging.getLogger('main.room')

class Room :

    def register_room(self) -> None:
        try:
            logger.info("Getting room details from admin.")
            self.room_id = "R"+ shortuuid.ShortUUID().random(length = 5)
            self.room_no = room_input_validation.input_room_no()
            self.floor_no = room_input_validation.input_floor_no()
            self.available = "Yes"
            self.customer_id = "None"
            self.charges = room_input_validation.input_charges()
            self.save_room_data_to_database()
            logger.debug("Room details taken successfully.")
        except:
            raise Exception("Error with registration system, try again!!")
    
    def save_room_data_to_database(self) -> None:
        logger.info("Adding room details to database.")
        query = query_collector.QUERY_FOR_SAVING_ROOM_DATA
        data = (self.room_id, self.room_no, self.floor_no, self.available, self.charges, self.customer_id)
        database_helper.update_database(query, data)
        logger.debug("Room details added successfully.")
    
    def print_room_data_from_database(self) -> None:
        logger.info("Fetching room data from database.")
        query = query_collector.QUERY_FOR_FECTHING_ROOM_DATA
        room_data = database_helper.fetch_data_from_database(query)
        logger.debug("Room data feteched successfully.")
        if not any(room_data):
            print("0 records found in room table. Please enter some records!")
            return
        row_id = [i for i in range(1,len(room_data)+1)]
        print(
            tabulate(
                room_data, 
                headers = ["Room ID", "Room No", "Floor No", "Availability", "Charges", "Customer ID"], 
                showindex = row_id, 
                tablefmt = "simple_grid"
            )
        )

    def check_in_room(self) -> None:
        try:
            user_email = customer_input_validation.input_email_address()
            query = query_collector.QUERY_FOR_FECTHING_CUSTOMER_ID_WITH_EMAIL
            data = (user_email, )
            customer_id = database_helper.fetch_data_from_database(query, data)[0][0]

            user_prefered_price = float(input("Enter preference for price : "))
            query = query_collector.QUERY_FOR_FECTHING_ROOM_WITH_USER_PREFERENCE
            data = (user_prefered_price, "Yes")
            room_data = database_helper.fetch_data_from_database(query, data)

            if not any(room_data):
                print("Really sorry :-( No room available of your choice")
                temp_input = input("Do you want to book any other room (Y/N) ? : ").lower()
                if temp_input == "n":
                    print("Thank you for coming!!")
                    return
                elif temp_input == "y":
                    query = query_collector.QUERY_FOR_FECTHING_ROOM_WITHOUT_USER_PREFERENCE
                    data = ("Yes", )
                    room_data = database_helper.fetch_data_from_database(query, data)
                else:
                    print("Sorry wrong input!!")
                    return
                
            print("Room available for booking are : ")
            row_id = [i for i in range(1,len(room_data)+1)]
            print(
                tabulate(
                    room_data, 
                    headers = ["Room ID", "Room No", "Floor No", "Charges"], 
                    showindex = row_id, 
                    tablefmt = "simple_grid"
                )
            )
            room_id = input("Enter Room ID for the room you wish to register : ")
            query = query_collector.QUERY_FOR_UPDATING_ROOM_AVAILABILITY
            data = ("No", customer_id, room_id)
            database_helper.update_database(query, data)
        except Exception as e:
            print(e)

    def check_out_room(self) -> None:
        print("Enter the room details to checkout : ")
        room_no = room_input_validation.input_room_no()
        floor_no = room_input_validation.input_floor_no()
        print("\nEnter the customer details to checkout : ")
        customer_email = customer_input_validation.input_email_address()

        query_to_get_customer_id = query_collector.QUERY_FOR_FECTHING_CUSTOMER_ID_WITH_EMAIL
        customer_id = database_helper.fetch_data_from_database(query_to_get_customer_id, (customer_email, ))[0][0]

        if not any(customer_id):
            print(f"{customer_email} not found!")
            return
        else:
            query_to_get_room_id = query_collector.QUERY_FOR_FETCHING_ROOM_ID
            room_id = database_helper.fetch_data_from_database(query_to_get_room_id, (customer_id, room_no, floor_no))[0][0]

            if not any(room_id):
                print("Room not booked for the customer")
                return
            else:
                query_for_check_out = query_collector.QUERY_FOR_UPDATING_ROOM_AVAILABILITY
                database_helper.update_database(query_for_check_out, ("Yes", "None", room_id))
                print("Check out done successfully!")

        
        



    


    