from cryptography.fernet import Fernet  # to encrypt the username and password
from database.database_connection import DatabaseConnection

key = Fernet.generate_key()
with open('utils\\filekey.key', 'wb') as filekey :
    filekey.write(key)

with open('utils\login_system.txt', 'rb') as file :
    original = file.read()

fernet = Fernet(key)

encrypted = fernet.encrypt(original)
with DatabaseConnection("database\\hotel_management.db") as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS login_credentials(key text, role text, credentials text)")
        cursor.execute("INSERT INTO login_credentials(key, role, credentials) VALUES(?, ?, ?)", (key, "reception", encrypted))





















"""
        Room class is for handling room related functionalities in Hotel Reservation System.
        Here this class represent a Room

        ...
        Attributes
        ----------
        room_id : str
            unique room id generated for each room using third party library shortuuid
            this is also a primary key in room table in the database
        room_no : int
            room_no of room
        floor_no : int
            floor_no of floor where the room is present
        available : str
            if the room is available for booking. By default it is "Yes" for all rooms
        customer_id : str
            unique customer id generated from shortuuid and taken from customer table for customer who wnat to register a room
            this is also a foreign key in room table in the database
        charges : float
            per night stay charges for room
        
        Methods
        -------
        save_room_Data_to_database() : None
            save room data to hotel_management.db database
        print_room_data_from_database() : None
            fetches room data from database and print on console using tabulate library
        check_in_room : None
            check in the customer into the room and set available field in room table to No
        check_out_room : None
            check out the customer from the room and set available field in room table to Yes again

    """