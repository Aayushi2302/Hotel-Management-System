
QUERY_FOR_CUSTOMER_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS customer(
                                        customer_id TEXT PRIMARY KEY, 
                                        name TEXT, 
                                        age INTEGER, 
                                        gender TEXT, 
                                        email TEXT UNIQUE, 
                                        mobile_number TEXT UNIQUE
                                    )"""

QUERY_FOR_ROOM_TABLE_CREATION = """CREATE TABLE IF NOT EXISTS room(
                                    room_id TEXT PRIMARY KEY, 
                                    room_no INTEGER, 
                                    floor_no INTEGER,
                                    availability TEXT, 
                                    charges REAL,
                                    customer_id TEXT, 
                                    CONSTRAINT fk_customer FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
                                )"""

QUERY_FOR_SAVING_CUSTOMER_DATA = """
                                    INSERT INTO customer(
                                        customer_id, 
                                        name, 
                                        age, 
                                        gender, 
                                        email, 
                                        mobile_number
                                    ) 
                                    VALUES(?, ?, ?, ?, ?, ?)
                                """

QUERY_FOR_FECTHING_CUSTOMER_DATA = "SELECT * FROM customer ORDER BY name"

QUERY_FOR_SAVING_ROOM_DATA = """
                                INSERT INTO room(
                                    room_id, 
                                    room_no, 
                                    floor_no, 
                                    availability, 
                                    charges, 
                                    customer_id
                                ) 
                                VALUES(?, ?, ?, ?, ?, ?)
                            """

QUERY_FOR_FECTHING_ROOM_DATA = "SELECT * FROM room ORDER BY floor_no"

QUERY_FOR_FECTHING_ROOM_WITH_USER_PREFERENCE = """
                                                    SELECT room_id, 
                                                    room_no, 
                                                    floor_no, 
                                                    charges 
                                                    FROM room WHERE charges <= ? AND availability = ? 
                                                    ORDER BY floor_no
                                                """

QUERY_FOR_FECTHING_ROOM_WITHOUT_USER_PREFERENCE = """
                                                    SELECT room_id, 
                                                    room_no, 
                                                    floor_no, 
                                                    charges 
                                                    FROM room WHERE availability = ? 
                                                    ORDER BY floor_no
                                                """

QUERY_FOR_UPDATING_ROOM_AVAILABILITY = "UPDATE room SET availability = ?, customer_id = ? WHERE room_id = ?"

QUERY_FOR_REMOVING_CUSTOMER_DATA =  "DELETE FROM customer WHERE customer_id = ?"

QUERY_FOR_FECTHING_CUSTOMER_ID_WITH_EMAIL = "SELECT customer_id FROM customer WHERE email = ?"

QUERY_FOR_FETCHING_ROOM_ID = "SELECT room_id FROM room WHERE customer_id = ? AND room_no = ? AND floor_no = ?"