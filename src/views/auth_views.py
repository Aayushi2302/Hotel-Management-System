"""
    Module for taking user login credentails as input.
    This module maintains a login attempts count for each user.
    Users are allowed only 3 valid login attempts.
"""
import time
import maskpass

from config.app_config import AppConfig
from config.prompts import Prompts
from controllers.admin_controller import AdminController
from controllers.auth_controller import AuthController
from controllers.room_controller import RoomController
from utils.common_helper import CommonHelper
from views.admin_views import AdminViews

class AuthViews:
    """
        Class containing method for taking user login credentails as input.
        ...
        Attribute
        ---------
        max_login_attempts -> Maximum login attempts with user for valid login (i.e. 3)

        Methods
        -------
        login() -> Method for taking login credentails as input.
    """

    def __init__(self, auth_controller_obj: AuthController, common_helper_obj: CommonHelper, admin_controller_obj: AdminController, room_controller_obj: RoomController) -> None:
        self.__max_login_attempts = AppConfig.MAXIMUM_LOGIN_ATTEMPTS
        self.auth_controller_obj = auth_controller_obj
        self.common_helper_obj = common_helper_obj
        self.admin_view_obj = AdminViews(admin_controller_obj, room_controller_obj)

    def login(self) -> None:
        """
            Method for taking user login credentails as input.
            Parameter -> self
            Return type -> None
        """
        while True:
            if not self.common_helper_obj.is_admin_registered():
                print(Prompts.ADMIN_NOT_FOUND + "\n")
                self.admin_view_obj.create_emp_credentials(AppConfig.ADMIN_ROLE)
                
            if self.__max_login_attempts == 0:
                print(Prompts.LOGIN_ATTEMPTS_EXHAUSTED + "\n")
                self.__max_login_attempts = AppConfig.MAXIMUM_LOGIN_ATTEMPTS
                time.sleep(10)
            else:
                print("\n" + Prompts.INPUT_CREDENTIAL)
                username = input(Prompts.INPUT_USERNAME).strip()
                password = maskpass.askpass(Prompts.INPUT_PASSWORD).strip()
                is_valid_user = self.auth_controller_obj.authenticate_user(username, password)

                if is_valid_user:
                    self.__max_login_attempts = AppConfig.MAXIMUM_LOGIN_ATTEMPTS
                else:
                    self.__max_login_attempts -= 1
                    print(Prompts.LOGIN_ATTEMPTS_LEFT.format(self.__max_login_attempts) + "\n")
                
                choice = input(Prompts.EXIT_SYSTEM + "\n")
                if choice in ("Y", "y"):
                    break
                