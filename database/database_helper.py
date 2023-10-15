from .database_connection import DatabaseConnection
from database import query_collector

def create_table_customer() -> None:
    with DatabaseConnection("database\\hotel_management.db") as connection:
            cursor = connection.cursor()
            cursor.execute(query_collector.QUERY_FOR_CUSTOMER_TABLE_CREATION)

def create_table_room() -> None:
    with DatabaseConnection("database\\hotel_management.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query_collector.QUERY_FOR_ROOM_TABLE_CREATION)

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
