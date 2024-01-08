from config.query import QueryConfig
from models.database import Database

class EmployeeController:
    def __init__(self, db: Database) -> None:
        self.db = db

    # POST
    # /customer
    def save_customer_details(self, cust_data: tuple) -> int | None:
        last_row_id =   self.db.save_data_to_database(
                            QueryConfig.SAVE_CUSTOMER_DATA,
                            cust_data
                        )
        return last_row_id

    # GET
    # /cutomer
    def get_customer_details(self) -> list:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_CUSTOMER_DATA
                )
        return data
    
    # GET
    # /customer/customer_email
    def get_customer_id_from_email(self, cust_email: str) -> list:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_CUSTOMER_ID_WITH_EMAIL,
                    (cust_email, )
                )
        return data
