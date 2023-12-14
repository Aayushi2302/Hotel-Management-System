import re
import hashlib
import maskpass
import tabulate

from config.app_config import AppConfig
from config.prompts import Prompts
from config.regex_pattern import RegexPattern
from config.query import QueryConfig
from models.database import Database

class CommonHelper:
    def __init__(self, db: Database) -> None:
        self.db = db

    def is_admin_registered(self) -> None:
        user_data = self.db.fetch_data_from_database(
                    QueryConfig.FETCH_EMPID_FROM_ROLE_AND_STATUS,
                    (AppConfig.ADMIN_ROLE, AppConfig.STATUS_ACTIVE)
                )
        if user_data:
            return True
        else:
            return False
            
    def create_new_password(self, username: str) -> None:
        """
            Method for creating new password for the user following strong password recommendation.
            Parameter -> self, username: str
            Return type -> None
        """
        while True:
            print(Prompts.CHANGE_PASSWORD + "\n")
            print(Prompts.STRONG_PASSWORD_REQUIREMENTS + "\n")
            input_password = maskpass.askpass(Prompts.INPUT_NEW_PASSWORD)
            is_strong_password = CommonHelper.input_validation(
                                    RegexPattern.PASSWORD_PATTERN,
                                    input_password
                                )
            if not is_strong_password:
                print(Prompts.WEAK_PASSWORD_INPUT + "\n")

            else:

                confirm_password = maskpass.askpass(Prompts.INPUT_CONFIRM_PASSWORD)
                if input_password != confirm_password:
                    print(Prompts.PASSWORD_NOT_MATCH + "\n")
                    continue
                hashed_password = hashlib.sha256(confirm_password.encode('utf-8')).hexdigest()
                
                self.db.save_data_to_database(
                    QueryConfig.UPDATE_DEFAULT_PASSWORD,
                    (hashed_password, AppConfig.PERMANENT_PASSWORD, username)
                )
                print(Prompts.PASSWORD_CHANGE_SUCCESSFUL + "\n")
                break

    @staticmethod
    def input_validation(regular_exp: str, input_field: str) -> bool:
        result = re.match(regular_exp, input_field)
        if result is not None:
            return True
        else:
            print(Prompts.INVALID_INPUT + "\n")
            return False
    
    @staticmethod
    def display_table(data: list, headers: list) -> None:
        row_id = [i for i in range(1, len(data) + 1)]
        print(
            tabulate(
                data,
                headers,
                showindex = row_id,
                tablefmt = "simple_grid"
            )
        )