"""
    Establishing of database connection for save, update and fetch queries
"""
# local file imports
from database.database_connection import DatabaseConnection
from database.query_collector import CustomerQuery, RoomQuery, AunthenticationQuery

def create_table_login_credentials() -> None:
    with DatabaseConnection("database\\hotel_management.db") as connection:
        cursor = connection.cursor()
        cursor.execute(AunthenticationQuery.QUERY_FOR_LOGIN_CREDENTIALS_TABLE_CREATION)

def create_table_customer() -> None:
    with DatabaseConnection("database\\hotel_management.db") as connection:
            cursor = connection.cursor()
            cursor.execute(CustomerQuery.QUERY_FOR_CUSTOMER_TABLE_CREATION)

def create_table_room() -> None:
    with DatabaseConnection("database\\hotel_management.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RoomQuery.QUERY_FOR_ROOM_TABLE_CREATION)

def create_table_reservation() -> None:
    with DatabaseConnection("database\\hotel_management.db") as connection:
        cursor = connection.cursor()
        cursor.execute(RoomQuery.QUERY_FOR_RESERVATION_TABLE_CREATION)

def update_database(query: str, data: tuple) -> None:
    with DatabaseConnection("database\\hotel_management.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query, data)
        
def fetch_data_from_database(query: str, data: tuple = None) -> list:
    with DatabaseConnection("database\\hotel_management.db") as connection:
        cursor = connection.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        return cursor.fetchall()

def is_empty_login_credentials() -> bool:
    data = fetch_data_from_database(AunthenticationQuery.QUERY_FOR_FETCHING_DATA_FROM_LOGIN_CREDENTIALS)
    if data:
        return False
    else:
        return True
