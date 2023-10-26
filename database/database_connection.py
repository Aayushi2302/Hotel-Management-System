import sqlite3
from sqlite3 import Connection

class DatabaseConnection:
    def __init__(self, host) -> None:
        try:
            self.connection = None
            self.host = host
        except Exception as e:
            print(e)
    
    def __enter__(self) -> Connection:
        try:
            self.connection = sqlite3.connect(self.host)
            return self.connection
        except Exception as e:
            print(e)
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type or exc_val or exc_tb:
            print(exc_type, exc_val)
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()