"""
    Queries for database operations.
"""
class TableHeader:
    AUTH_TABLE_HEADER = (
        "Employee ID",
        "Username",
        "Role",
        "Status"
    )

    CUSTOMER_TABLE_HEADER = (
        "Customer ID",
        "Customer Name",
        "Age",
        "Gender",
        "Email Address",
        "Mobile Number"
        "Status"
    )

    ROOM_TABLE_HEADER = (
        "Room ID",
        "Room No",
        "Floor No",
        "Charges",
        "Status"
    )

    AVAILABLE_ROOM_TABLE_HEADER = (
        "Room ID",
        "Room No",
        "Floor No",
        "Charges"
    )


class QueryConfig:
    # authentication table
    AUTHENTICATION_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS authentication(
                                            emp_id TEXT PRIMARY KEY, 
                                            username TEXT, 
                                            password TEXT, 
                                            role TEXT, 
                                            password_type TEXT "default",
                                            status TEXT DEFAULT "active"
                                        )"""

    SAVE_LOGIN_CREDENTIALS = """INSERT INTO authentication(
                                    emp_id, 
                                    username, 
                                    password, 
                                    role, 
                                    password_type) 
                                    VALUES(?, ?, ?, ?, ?)"""
    
    FETCH_EMPID_FROM_ROLE_AND_STATUS = """
        SELECT emp_id FROM authentication
        WHERE role = ? and status = ?
    """

    FETCH_EMPLOYEE_CREDENTIALS = """SELECT password, role, password_type
                                        FROM authentication WHERE username = ? AND status = ?"""

    UPDATE_DEFAULT_PASSWORD = "UPDATE authentication SET password = ?, password_type = ? WHERE username = ?"


    # customer table
    CUSTOMER_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS customer(
                                    customer_id TEXT PRIMARY KEY, 
                                    name TEXT, 
                                    age INTEGER, 
                                    gender TEXT, 
                                    email TEXT UNIQUE, 
                                    mobile_number TEXT UNIQUE
                                )"""
    
    SAVE_CUSTOMER_DATA = """INSERT INTO customer(
                                customer_id, 
                                name, 
                                age, 
                                gender, 
                                email, 
                                mobile_number
                            ) 
                            VALUES(?, ?, ?, ?, ?, ?)"""
    
    FETCH_CUSTOMER_DATA = "SELECT * FROM customer ORDER BY name"

    FETCH_CUSTOMER_ID_WITH_EMAIL = "SELECT customer_id FROM customer WHERE email = ?"

    REMOVE_CUSTOMER_DATA =  "DELETE FROM customer WHERE customer_id = ?"

    
    # room table
    ROOM_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS room(
                                room_id TEXT PRIMARY KEY, 
                                room_no INTEGER, 
                                floor_no INTEGER,
                                charges REAL,
                                status TEXT DEFAULT "available"
                            )"""

    SAVE_ROOM_DATA = """INSERT INTO room(
                            room_id, 
                            room_no, 
                            floor_no, 
                            charges
                        ) 
                        VALUES(?, ?, ?, ?)"""

    FETCH_ROOM_DATA = "SELECT * FROM room ORDER BY floor_no"

    FETCH_STATUS_WITH_ROOM_ID = "SELECT status FROM room WHERE room_id = ?"

    FETCH_ROOM_ID_AND_STATUS = """SELECT room_id, status FROM room
                                    WHERE floor_no = ? AND room_no = ?"""

    UPDATE_ROOM_STATUS = """UPDATE room SET status = ? WHERE room_id = ?"""

    FETCH_ROOM_ID_FROM_ROOM_DATA = "SELECT room_id FROM room WHERE room_no = ? AND floor_no = ?"

    FECTH_ROOM_WITH_USER_PREFERENCE = """SELECT room_id, 
                                            room_no, 
                                            floor_no, 
                                            charges 
                                            FROM room WHERE charges <= ? AND status = ? 
                                            ORDER BY floor_no"""

    FETCH_AVAILABLE_ROOMS = """SELECT room_id, 
                                room_no, 
                                floor_no, 
                                charges 
                                FROM room WHERE status = ? 
                                ORDER BY floor_no"""

    # reservation table
    RESERVATION_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS reservation(
                                            reservation_id TEXT PRIMARY KEY,
                                            customer_id TEXT, 
                                            room_id TEXT, 
                                            check_in_date TEXT,
                                            check_in_time TEXT,
                                            check_out_date TEXT,
                                            check_out_time TEXT,
                                            is_checkout TEXT DEFAULT "No",
                                            FOREIGN KEY(customer_id) REFERENCES customer(customer_id) ON DELETE CASCADE,
                                            FOREIGN KEY(room_id) REFERENCES room(room_id) ON DELETE CASCADE
                                        )"""

    CHECK_IN_ROOM = """INSERT INTO reservation(
                                reservation_id,
                                customer_id,
                                room_id,
                                check_in_date,
                                check_in_time,
                                check_out_date,
                                check_out_time)
                                VALUES(?, ?, ?, ?, ?, ?, ?)"""
