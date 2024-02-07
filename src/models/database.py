import sqlite3

from config.app_config import AppConfig
from config.query import QueryConfig
from models.database_access import DatabaseAccess
from utils.error_handler import error_handler

class Database:

    def create_all_tables(self) -> None:
        """ 
            Method for creating all tables of database
            Parameter -> self
            Return type -> None
        """
        with DatabaseAccess(AppConfig.DATABASE_PATH) as connection:
            print(AppConfig.DATABASE_PATH)
            cursor = connection.cursor()
            cursor.execute(QueryConfig.AUTHENTICATION_TABLE_CREATION)
            cursor.execute(QueryConfig.CUSTOMER_TABLE_CREATION)
            cursor.execute(QueryConfig.ROOM_TABLE_CREATION)
            cursor.execute(QueryConfig.RESERVATION_TABLE_CREATION)
   
    def save_data_to_database(self, query: str | list, data: tuple | list) -> int:
        """
            Method for saving data to single or multiple tables in database.
            Paramter -> self, query: Union[str, list], data: Union[tuple, list]
            Return type -> int
        """
        with DatabaseAccess(AppConfig.DATABASE_PATH) as connection:
            cursor = connection.cursor()
            if isinstance(query, str):
                cursor.execute(query, data)
            else:
                for i in range(len(query)):
                    cursor.execute(query[i], data[i])
            connection.commit()
            return cursor.lastrowid

    def fetch_data_from_database(self, query: str, data: tuple = None) -> list:
        """
            Method for fetching data from single or multiple tables in database.
            Paramter -> self, query: str, data: Union[tuple, None]
            Return type -> list
        """
        with DatabaseAccess(AppConfig.DATABASE_PATH) as connection:
            cursor = connection.cursor()
            if data is None:
                cursor.execute(query)
            else:
                cursor.execute(query, data)
            return cursor.fetchall()

    def delete_operation_on_database(self, query: str) -> None:
        with DatabaseAccess(AppConfig.DATABASE_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(query)

