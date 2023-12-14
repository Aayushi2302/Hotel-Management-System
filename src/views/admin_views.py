import shortuuid
import string
import random
from typing import Optional

from config.app_config import AppConfig
from config.prompts import Prompts
from controllers.admin_controller import AdminController
from utils.input_validator.user_controller_validator import UserControllerValidator

class AdminViews:
    def __init__(self, admin_controller_obj: AdminController):
        self.admin_controller_obj = admin_controller_obj

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
    
    


