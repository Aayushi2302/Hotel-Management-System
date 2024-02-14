from datetime import datetime

from config.app_config import AppConfig
from config.query import QueryConfig
from models.database import Database
from controllers.employee_controller import EmployeeController
from utils.common_helper import CommonHelper

class RoomController:
    def __init__(self) -> None:
        self.db = Database()
        self.employee_controller_obj = EmployeeController()

    def save_room_details(self, room_data: tuple) -> int | None:
        last_row_id =   self.db.save_data_to_database(
                            QueryConfig.SAVE_ROOM_DATA,
                            room_data
                        )
        return last_row_id

    def get_available_rooms(self) -> list:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_AVAILABLE_ROOMS,
                    ("available", )
                )
        keys = ['room_id', 'room_no', 'floor_no', 'charges']
        return CommonHelper.jsonify_data(data, keys)

    def get_room_data(self) -> dict:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_ROOM_DATA
                )
        keys = ['room_id', 'room_no', 'floor_no', 'charges', 'status']
        return CommonHelper.jsonify_data(data, keys)


    def is_room_available(self, room_id: str) -> bool:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_STATUS_WITH_ROOM_ID,
                    (room_id, )
                )
        if not data:
            return False
        else:
            status = data[0][0]
            if status != AppConfig.ROOM_STATUS_AVAILABLE:
                return False
            else:
                return True

    def update_room_status(self, room_no: int, floor_no: int, updated_status: str) -> int:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_ROOM_ID_AND_STATUS,
                    (floor_no, room_no)
                )
        if not data:
            return -1
        else:
            room_id = data[0][0]
            status = data[0][1]

            if status == updated_status:
                return -2

            self.db.save_data_to_database(
                QueryConfig.UPDATE_ROOM_STATUS,
                (updated_status, room_id)
            )
            return 1

    def get_preferred_room(self, cust_preferred_price: float) -> list:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FECTH_ROOM_WITH_USER_PREFERENCE,
                    (cust_preferred_price, "available")
                )
        keys = ['room_id', 'room_no', 'floor_no', 'charges', 'status']
        return CommonHelper.jsonify_data(data, keys)

    def get_reservation_id(self, cust_id: str, room_id: str) -> str:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_RESER_ID_FROM_CUST_AND_ROOM,
                    (cust_id, room_id)
                )
        return data

    def calculate_charges(self, room_id: str, in_date: str, out_date: str) -> float:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_CHARGES_FROM_ROOM_ID,
                    (room_id, )
                )
        charges = data[0][0]
        in_date_obj = datetime.strptime(in_date, "%d-%m-%Y")
        out_date_obj = datetime.strptime(out_date, "%d-%m-%Y")
        delta = (out_date_obj - in_date_obj).days
        return charges * delta

    def save_room_details_for_check_in(self, reservation_id: str, room_id: str, cust_data: tuple) -> int:
        cust_email = cust_data[0]
        data = self.employee_controller_obj.get_customer_id_from_email(cust_email)
        if not data:
            return -1
        else:
            cust_id = data[0][0]
            room_exist = self.is_room_available(room_id)
            if not room_exist:
                return -2
            else:
                cust_checkin_date_time = cust_data[1]
                cust_checkout_date_time = cust_data[2]
                cust_checkin_date = cust_checkin_date_time[0]
                cust_checkin_time = cust_checkin_date_time[1]
                cust_checkout_date = cust_checkout_date_time[0]
                cust_checkout_time = cust_checkout_date_time[1]
    
                reservation_data = (reservation_id, cust_id, room_id, cust_checkin_date, cust_checkin_time, cust_checkout_date, cust_checkout_time)
                room_table_data = (AppConfig.ROOM_STATUS_BOOKED, room_id)
                last_row_id = self.db.save_data_to_database(
                                    [QueryConfig.CHECK_IN_ROOM, QueryConfig.UPDATE_ROOM_STATUS],
                                    [reservation_data, room_table_data]
                                )
                if not last_row_id:
                    return 0
                else:
                    return 1

    def get_room_id_from_room_no(self, room_no: int, floor_no: int) -> list:
        data =  self.db.fetch_data_from_database(
                    QueryConfig.FETCH_ROOM_ID_FROM_ROOM_DATA,
                    (room_no, floor_no)
                )
        return data

    def save_room_details_for_check_out(self, cust_email: str, room_id: str, checkout_date_time: str) -> int:
        cust_data = self.employee_controller_obj.get_customer_id_from_email(cust_email)
        if not cust_data:
            return -1
        else:
            cust_id = cust_data[0][0]
            reservation_data = self.get_reservation_id(cust_id, room_id)
            if not reservation_data:
                return -1
            else:
                reservation_id = reservation_data[0][0]
                in_date = reservation_data[0][1]
                out_date = checkout_date_time[0]
                out_time = checkout_date_time[1]
                charges = self.calculate_charges(room_id, in_date, out_date)
                reservation_data = (out_date, out_time, charges, "Yes", reservation_id)
                room_table_data = (AppConfig.ROOM_STATUS_AVAILABLE, room_id)
                last_row_id_reservation =  self.db.save_data_to_database(
                                    [QueryConfig.CHECK_OUT_ROOM, QueryConfig.UPDATE_ROOM_STATUS],
                                    [reservation_data, room_table_data]
                                )
                return charges
