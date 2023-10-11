# ROOM MODULE
import input_validation.room_input_validation as room_input_validation
import input_validation.customer_input_validation as customer_input_validation
import shortuuid
from database_connection import DatabaseConnection
from tabulate import tabulate

class Room :
    @classmethod
    def create_table_room(cls):
        with DatabaseConnection("hotel_management.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS room(
                        room_id TEXT PRIMARY KEY, 
                        room_no INTEGER, 
                        floor_no INTEGER,
                        availability TEXT, 
                        charges REAL,
                        customer_id TEXT, 
                        CONSTRAINT fk_customer FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
                )"""
            )

    def register_room(self):
        try:
            self.room_id = "R"+ shortuuid.ShortUUID().random(length = 5)
            self.room_no = room_input_validation.input_room_no()
            self.available = "Yes"
            self.customer_id = "None"
            self.floor_no = room_input_validation.input_floor_no()
            self.charges = room_input_validation.input_charges()
            self.save_room_data_to_database()
        except:
            raise Exception("Error with registration system, try again!!")
    
    def save_room_data_to_database(self):
        with DatabaseConnection("hotel_management.db") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO room(room_id, room_no, floor_no, availability, charges, customer_id) VALUES(?, ?, ?, ?, ?, ?)",
                (self.room_id, self.room_no, self.floor_no, self.available, self.charges, self.customer_id)
            )
    
    def print_room_data_from_database(self):
        with DatabaseConnection("hotel_management.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM room ORDER BY floor_no")
            room_data = cursor.fetchall()
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

    def check_in_room(self):
        try:
            user_email = customer_input_validation.input_email_address()
            with DatabaseConnection("hotel_management.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT customer_id FROM customer WHERE email = ?", (user_email, ))
                customer_id = cursor.fetchall()[0][0]

                user_prefered_price = float(input("Enter preference for price : "))
                cursor.execute(
                    """SELECT room_id, 
                       room_no, 
                       floor_no, 
                       charges 
                       FROM room WHERE charges <= ? AND availability = ? 
                       ORDER BY floor_no""", 
                       (user_prefered_price, "Yes")
                )
                room_data = cursor.fetchall()
                if not any(room_data):
                    print("Really sorry :-( No room available of your choice")
                    temp_input = input("Do you want to book any other room (Y/N) ? : ").lower()
                    if temp_input == "n":
                        print("Thank you for coming!!")
                        return
                    elif temp_input == "y":
                        cursor.execute(
                            """SELECT room_id, 
                               room_no, 
                               floor_no, 
                               charges 
                               FROM room WHERE availability = ? 
                               ORDER BY floor_no""", 
                               ("Yes", )
                        )
                        room_data = cursor.fetchall()
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
                cursor.execute("UPDATE room SET availability = ?, customer_id = ? WHERE room_id = ?", ("No", customer_id, room_id))

        except Exception as e:
            print(e)

    

    


    