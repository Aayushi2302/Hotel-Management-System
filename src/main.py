"""
    This is the main module for Hotel-Reservation-System
"""
import logging

from config.app_config import AppConfig
from config.prompts import Prompts
from models.database import db
from views.auth_views import AuthViews
from setup import SetUp

db.create_all_tables()

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    level = logging.DEBUG,
                    filename = AppConfig.LOG_FILE_PATH)

logger = logging.getLogger(__name__)

if __name__ == "__main__":

    print(Prompts.WELCOME_MESSAGE)

    auth_views_obj = AuthViews(SetUp.auth_controller_obj, SetUp.common_helper_obj)
    auth_views_obj.login()

    db.connection.close()
    print(Prompts.EXIT_MESSAGE)

else:
    pass
