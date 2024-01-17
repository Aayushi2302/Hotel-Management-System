from config.query import QueryConfig
from models.database import db
from utils.common_helper import CommonHelper

class EmployeeController:
    # def __init__(self, db: Database) -> None:
    #     self.db = db

    # POST
    # /customer
    def save_customer_details(self, cust_data: tuple) -> int | None:
        last_row_id =   db.save_data_to_database(
                            QueryConfig.SAVE_CUSTOMER_DATA,
                            cust_data
                        )
        return last_row_id

    # GET
    # /cutomer
    def get_customer_details(self) -> list:
        data =  db.fetch_data_from_database(
                    QueryConfig.FETCH_CUSTOMER_DATA
                )
        keys = ['room_id', 'name', 'age', 'gender', 'email', 'mobile_number', 'status']
        return CommonHelper.jsonify_data(data, keys)
    
    # GET
    # /customer/customer_email
    def get_customer_id_from_email(self, cust_email: str) -> list:
        data =  db.fetch_data_from_database(
                    QueryConfig.FETCH_CUSTOMER_ID_AND_STATUS_FROM_EMAIL,
                    (cust_email, )
                )
        return data

    def deactivate_customer(self, cust_email: str, new_status: str):
        data = self.get_customer_id_from_email(cust_email)
        if not data:
            return -1
        cust_id = data[0][0]
        status = data[0][1]

        if status == new_status:
            return -2

        db.save_data_to_database(
            QueryConfig.UPDATE_CUSTOMER_STATUS,
            (new_status, cust_id)
        )
        return 1
