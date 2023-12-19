import shortuuid
import string
import random
from typing import Optional

from config.app_config import AppConfig
from config.prompts import Prompts
from controllers.admin_controller import AdminController
from controllers.room_controller import RoomController
from utils.error_handler import error_handler
from utils.input_validator.user_controller_validator import UserControllerValidator
from views.room_views import RoomViews

class AdminViews:
    def __init__(self, admin_controller_obj: AdminController, room_controller_obj: RoomController) -> None:
        self.admin_controller_obj = admin_controller_obj
        self.room_views_obj = RoomViews(room_controller_obj)

    def admin_menu_operations(self) -> None:
        while True:
            if self.admin_menu():
                break

    def create_emp_credentials(self, role: Optional[str] = None) -> None:
        emp_id = "EMP" + shortuuid.ShortUUID().random(5)
        username = UserControllerValidator.input_username()
        characters = string.ascii_letters + string.digits + "@#$&%"
        emp_password = ''.join(random.choice(characters) for _ in range(8))
        if not role:
            role = UserControllerValidator.input_role()
        password_type = AppConfig.DEFAULT_PASSWORD_TYPE
        emp_data = (emp_id, username, emp_password, role, password_type)
        result = self.admin_controller_obj.register_emp_credentials(emp_data)
        if result:
            print("\n" + Prompts.SUCCESSFUL_CREDENTIAL_CREATION + "\n")
        else:
            print("\n" + Prompts.UNSUCCESSFUL_CREDENTIAL_CREATION + "\n")
    
    @error_handler
    def admin_menu(self) -> bool:
        print(Prompts.ADMIN_MENU + "\n")
        choice = input(Prompts.ENTER_CHOICE)
        match choice:
            case '1':
                print(self.room_views_obj.register_room())
            case '2':
                self.room_views_obj.activate_room()
            case '3':
                self.room_views_obj.deactivate_room()
            case '4':
                self.room_views_obj.view_room_details()
            case '5':
                self.room_views_obj.view_check_in_check_out_details()
            case '6':
                self.create_emp_credentials()
            case '7':
                print(Prompts.SUCCESSFUL_LOGOUT + "\n")
                return True
            case _:
                print(Prompts.INVALID_INPUT + "\n")
        return False
