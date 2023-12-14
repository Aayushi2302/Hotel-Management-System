import sqlite3

from config.app_config import AppConfig
from config.query import QueryConfig
from utils.error_handler import error_handler

class Database:
    """
        This class contains methods for executing database queries fetched from QueryConfig.
        ...
        Attributes
        ---------
        connection -> sqlite3.Connection
        cursor -> sqlite3.Cursor

        Methods
        -------
        __init__() -> Method for creating connection and cursor object.
        create_all_tables() -> Method for creating all database tables.
        save_data_to_database() -> Method for saving data to single or multiple tables in database.
        fetch_data_from_database() -> Method for fetching data from database tables.   
    """
    @error_handler
    def __init__(self) -> None:
        """
            Method for initializing the sqlite3 connection and cursor object
            Parameter -> self
            Return type -> None
        """
        try:
            self.connection = sqlite3.connect(AppConfig.DATABASE_PATH)
            self.cursor = self.connection.cursor()
        except Exception:
            raise sqlite3.Error

    def create_all_tables(self) -> None:
        """ 
            Method for creating all tables of database
            Parameter -> self
            Return type -> None
        """
        self.cursor.execute(QueryConfig.AUTHENTICATION_TABLE_CREATION)
        self.cursor.execute(QueryConfig.CUSTOMER_TABLE_CREATION)
        self.cursor.execute(QueryConfig.ROOM_TABLE_CREATION)
        self.cursor.execute(QueryConfig.RESERVATION_TABLE_CREATION)
   
    def save_data_to_database(self, query: str | list, data: tuple | list) -> int:
        """
            Method for saving data to single or multiple tables in database.
            Paramter -> self, query: Union[str, list], data: Union[tuple, list]
            Return type -> int
        """
        if isinstance(query, str):
            self.cursor.execute(query, data)
        else:
            for i in range(len(query)):
                self.cursor.execute(query[i], data[i])
        self.connection.commit()
        return self.cursor.lastrowid

    def fetch_data_from_database(self, query: str, data: tuple = None) -> list:
        """
            Method for fetching data from single or multiple tables in database.
            Paramter -> self, query: str, data: Union[tuple, None]
            Return type -> list
        """
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)
        return self.cursor.fetchall()

db = Database()
