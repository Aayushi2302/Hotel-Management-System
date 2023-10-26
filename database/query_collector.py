"""
    Queries for database operations.
"""
class AunthenticationQuery:
    QUERY_FOR_LOGIN_CREDENTIALS_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS login_credentials(
                                                    emp_id TEXT PRIMARY KEY, 
                                                    username TEXT, 
                                                    password TEXT, 
                                                    role TEXT, 
                                                    password_type INTEGER
                                                )"""

    QUERY_FOR_SAVING_LOGIN_CREDENTIALS = """INSERT INTO login_credentials(
                                            emp_id, 
                                            username, 
                                            password, 
                                            role, 
                                            password_type) 
                                            VALUES(?,?,?,?,?)"""

    QUERY_FOR_FETCHING_DATA_FROM_LOGIN_CREDENTIALS = "SELECT * FROM login_credentials"

    QUERY_FOR_FETCHING_USER_CREDENTIALS = """SELECT password_type, role, password
                                        FROM login_credentials WHERE username = ?"""

    QUERY_FOR_UPDATING_DEFAULT_PASSWORD = "UPDATE login_credentials SET password = ?, password_type = ? WHERE username = ?"

class CustomerQuery:
    QUERY_FOR_CUSTOMER_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS customer(
                                        customer_id TEXT PRIMARY KEY, 
                                        name TEXT, 
                                        age INTEGER, 
                                        gender TEXT, 
                                        email TEXT UNIQUE, 
                                        mobile_number TEXT UNIQUE
                                    )"""
    
    QUERY_FOR_SAVING_CUSTOMER_DATA = """INSERT INTO customer(
                                        customer_id, 
                                        name, 
                                        age, 
                                        gender, 
                                        email, 
                                        mobile_number
                                    ) 
                                    VALUES(?, ?, ?, ?, ?, ?)"""
    
    QUERY_FOR_FETCHING_CUSTOMER_DATA = "SELECT * FROM customer ORDER BY name"

    QUERY_FOR_REMOVING_CUSTOMER_DATA =  "DELETE FROM customer WHERE customer_id = ?"

    QUERY_FOR_FETCHING_CUSTOMER_ID_WITH_EMAIL = "SELECT customer_id FROM customer WHERE email = ?"

class RoomQuery:
    QUERY_FOR_ROOM_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS room(
                                        room_id TEXT PRIMARY KEY, 
                                        room_no INTEGER, 
                                        floor_no INTEGER,
                                        availability TEXT, 
                                        charges REAL
                                    )"""

    QUERY_FOR_SAVING_ROOM_DATA = """INSERT INTO room(
                                    room_id, 
                                    room_no, 
                                    floor_no, 
                                    availability, 
                                    charges, 
                                    customer_id
                                ) 
                                VALUES(?, ?, ?, ?, ?)"""

    QUERY_FOR_FETCHING_ROOM_DATA = "SELECT * FROM room ORDER BY floor_no"

    QUERY_FOR_FECTHING_ROOM_WITH_USER_PREFERENCE = """SELECT room_id, 
                                                    room_no, 
                                                    floor_no, 
                                                    charges 
                                                    FROM room WHERE charges <= ? AND availability = ? 
                                                    ORDER BY floor_no"""

    QUERY_FOR_FETCHING_ROOM_WITHOUT_USER_PREFERENCE = """SELECT room_id, 
                                                    room_no, 
                                                    floor_no, 
                                                    charges 
                                                    FROM room WHERE availability = ? 
                                                    ORDER BY floor_no"""

    QUERY_FOR_UPDATING_ROOM_AVAILABILITY = """UPDATE room SET availability = ? WHERE room_id = ?"""

    QUERY_FOR_FETCHING_ROOM_ID = """SELECT room_id FROM room 
                                WHERE floor_no = ? AND room_no = ?"""

    QUERY_FOR_RESERVATION_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS reservation(
                                            reservation_id TEXT PRIMARY KEY,
                                            customer_id TEXT, 
                                            room_id TEXT, 
                                            check_in_date TEXT,
                                            check_in_time TEXT,
                                            check_out_date TEXT,
                                            check_out_time TEXT,
                                            is_checkout INTEGER,
                                            FOREIGN KEY(customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
                                            FOREIGN KEY(room_id) REFERENCES room(room_id) ON DELETE CASCADE
                                        )"""

    QUERY_FOR_CHECK_IN_ROOM = """INSERT INTO reservation(
                                reservation_id,
                                customer_id,
                                room_id,
                                check_in_date,
                                check_in_time,
                                check_out_date,
                                check_out_time,
                                is_checkout)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""