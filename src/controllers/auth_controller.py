"""
    Module for authenticating users(both admin and employee) based on their credentials.
    The user password is stored in hashed format.
    The default password of the user is changed on 1st login of user.
"""
import hashlib

from config.app_config import AppConfig
from config.query import QueryConfig
from models.database import Database
from controllers.admin_controller import AdminController
from controllers.employee_controller import EmployeeController
from controllers.room_controller import RoomController
from utils.common_helper import CommonHelper
from views.admin_views import AdminViews
from views.employee_views import EmployeeViews

class AuthController:
    """
        Class containing methods for authenticating user based on their credentails.
        This class also grant role based access to user.
        ...
        Methods
        -------
        first_login() -> Method for granting access to user on 1st login.
        role_based_access() -> Method for granting role based access to user based on credentails.
        authenticate_user() -> Method for validating user based on credentials.
    """
    def __init__(self):
        self.db = Database()
    
    def authenticate_user(self, username: str, password: str) -> bool:
        """
            Method for validating user based on credentials.
            Parameter -> username: str, password: str
            Return type -> bool
        """
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_EMPLOYEE_CREDENTIALS,
                    (username, AppConfig.STATUS_ACTIVE)
                )
        if data:
            actual_password = data[0][0]
            role = data[0][1]
            password_type = data[0][2]
            if password_type != AppConfig.DEFAULT_PASSWORD:
                password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    
            if password == actual_password:
                return role
        return None
                    
