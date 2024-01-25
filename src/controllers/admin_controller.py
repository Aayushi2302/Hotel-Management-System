from typing import Tuple

from config.query import QueryConfig
from models.database import db

class AdminController:

    def register_emp_credentials(self, emp_data: Tuple[str]) -> None:
        last_row_id =   db.save_data_to_database(
                            QueryConfig.SAVE_LOGIN_CREDENTIALS,
                            emp_data
                        )
        return last_row_id