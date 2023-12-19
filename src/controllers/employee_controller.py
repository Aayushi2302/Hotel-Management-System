from config.query import QueryConfig
from models.database import Database

class EmployeeController:
    def __init__(self, db: Database) -> None:
        self.db = db

    def save_customer_details(self, cust_data: tuple) -> int | None:
        last_row_id =   self.db.save_data_to_database(
                            QueryConfig.SAVE_CUSTOMER_DATA,
                            cust_data
                        )
        return last_row_id

    def get_customer_details(self) -> list:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_CUSTOMER_DATA
                )
        return data
    
    def get_customer_id_from_email(self, cust_email: str) -> list:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_CUSTOMER_ID_WITH_EMAIL,
                    (cust_email, )
                )
        return data

    def remove_customer_details(self, cust_email) -> int:
        data =  self.get_customer_id_from_email(cust_email)
        if not data:
            return -1
        else:
            cust_id = data[0][0]
            last_row_id =  self.db.save_data_to_database(
                                QueryConfig.REMOVE_CUSTOMER_DATA,
                                (cust_id, )
                            )
            if not last_row_id:
                return 0
            else:
                return 1
