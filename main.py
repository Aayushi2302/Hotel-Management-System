"""
    This is the main module for Hotel-Reservation-System
"""
# pylint: disable=C0103

# third party imports
import logging
import hashlib
import time
import sqlite3
import maskpass

# local file imports
from room import Room
import perform_admin_operations
from database import database_helper
from database.query_collector import AunthenticationQuery
from authentication import Aunthentication

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    level = logging.DEBUG,
                    filename = 'logs.txt')
logger = logging.getLogger('main')

# global variable
invalid_login_attempts = 3

authentication_obj = Aunthentication()

if __name__ == "__main__":

    # connection = sqlite3.connect("database\\hotel_management.db")
    # cursor = connection.cursor()
    # # cursor.execute("DROP TABLE login_credentials")
    # cursor.execute("DROP TABLE reservation")

    print("----- Welcome to Hotel Reservation System ------")

    logger.info("Starting with the hotel management system.")
    database_helper.create_table_customer()
    database_helper.create_table_room()
    database_helper.create_table_login_credentials()
    database_helper.create_table_reservation()
    
    # creation of the first admin of the system
    if database_helper.is_empty_login_credentials():
        perform_admin_operations.create_login_credentials()

    logging.info("Establishing database connection for system login.")
    while True:
        if authentication_obj.login_attempts == 0:
            print("Login attempts exhausted! Please login after some time...\n")
            authentication_obj.login_attempts = 3
            time.sleep(10)
        else :
            authentication_obj.user_authentication()
else:
    logger.debug("Wrong file run. Run main.py for running the program.")