import shortuuid

from config.app_config import AppConfig
from config.prompts import Prompts
from config.query import TableHeader
from controllers.employee_controller import EmployeeController
from controllers.room_controller import RoomController
from utils.common_helper import CommonHelper
from utils.input_validator.room_controller_validator import RoomControllerValidator
from utils.input_validator.user_controller_validator import UserControllerValidator

class RoomViews:
    def __init__(self, room_controller_obj: RoomController) -> None:
        self.room_controller_obj = room_controller_obj

    def register_room(self) -> None:
        print(Prompts.ENTER_ROOM_DETAILS + "\n")

        room_id = "ROOM" + shortuuid.ShortUUID().random(5)
        room_no = RoomControllerValidator.input_room_no()
        floor_no = RoomControllerValidator.input_floor_no()
        charges = RoomControllerValidator.input_charges()
        room_data = (room_id, room_no, floor_no, charges)
        result = self.room_controller_obj.save_room_details(room_data)

        if result:
            print(Prompts.SUCCESSFUL_ROOM_CREATION + "\n")
        else:
            print(Prompts.UNSUCCESSFUL_ROOM_CREATION + "\n")

    def view_room_details(self) -> None:
        data = self.room_controller_obj.get_room_data()
        if not data:
            print(Prompts.ZERO_RECORD.format("Room") + "\n")
        else:
            header = TableHeader.ROOM_TABLE_HEADER
            CommonHelper.display_table(data, header)
    
    def deactivate_room(self) -> None:
        floor_no = RoomControllerValidator.input_floor_no()
        room_no = RoomControllerValidator.input_room_no()
        result = self.room_controller_obj.update_room_status(floor_no, room_no, AppConfig.ROOM_STATUS_INACTIVE)
        if result == -1:
            print(Prompts.ROOM_DOES_NOT_EXIST + "\n")
        elif result == -2:
            print(Prompts.ROOM_ALREADY_INACTIVE + "\n")
        elif result == 0:
            print(Prompts.UNSUCCESSFUL_ROOM_DEACTIVATION + "\n")
        else:
            print(Prompts.SUCCESSFUL_ROOM_DEACTIVATION + "\n")
    
    def activate_room(self) -> None:
        floor_no = RoomControllerValidator.input_floor_no()
        room_no = RoomControllerValidator.input_room_no()
        result = self.room_controller_obj.update_room_status(floor_no, room_no, AppConfig.ROOM_STATUS_AVAILABLE)
        if result == -1:
            print(Prompts.ROOM_DOES_NOT_EXIST + "\n")
        elif result == -2:
            print(Prompts.ROOM_ALREADY_ACTIVE + "\n")
        elif result == 0:
            print(Prompts.UNSUCCESSFUL_ROOM_ACTIVATION + "\n")
        else:
            print(Prompts.SUCCESSFUL_ROOM_ACTIVATION + "\n")

    def view_available_rooms(self) -> list:
        data = self.room_controller_obj.get_available_rooms()
        if not data:
            print(Prompts.NO_ROOMS_AVAILABLE + "\n")
        else:
            header = TableHeader.AVAILABLE_ROOM_TABLE_HEADER
            CommonHelper.display_table(data, header)
        return data
    
    def view_room_for_check_in(self, cust_prefered_price: float) -> None:
        prefered_room_exist =  self.room_controller_obj.get_preferred_room(cust_prefered_price)
        if not prefered_room_exist:
            print(Prompts.PREFERRED_ROOM_NOT_EXIST + "\n")
            choice = input(Prompts.INPUT_RESERVE_OTHER_ROOM + "\n")
            if choice not in ('n' or 'N'):
                return self.view_available_rooms()
        else:
            header = TableHeader.AVAILABLE_ROOM_TABLE_HEADER
            CommonHelper.display_table(prefered_room_exist, header)
        return prefered_room_exist

    def check_in_room(self) -> None:
        reservation_id = "RESR" + shortuuid.ShortUUID().random(5)
        cust_email = UserControllerValidator.input_email_address()
        cust_prefered_price = RoomControllerValidator.input_charges()
        room_data = self.view_room_for_check_in(cust_prefered_price)
        if not room_data:
            return
        room_id = RoomControllerValidator.input_room_id()
        cust_checkin_date_time = CommonHelper.get_current_date_and_time()
        cust_checkout_date_time = RoomControllerValidator.input_out_date_and_time()
        cust_data = (cust_email, cust_checkin_date_time, cust_checkout_date_time)
        result = self.room_controller_obj.save_room_details_for_check_in(reservation_id, room_id, cust_data)
        if result == -1:
            print(Prompts.CUSTOMER_DOES_NOT_EXIST + "\n")
        elif result == -2:
            print(Prompts.ROOM_DOES_NOT_EXIST + "\n")
        elif result == 0:
            print(Prompts.UNSUCCESSFUL_CHECK_IN + "\n")
        else:
            print(Prompts.SUCCESSFUL_CHECK_IN + "\n")

    def check_out_room(self) -> None:
        cust_email = UserControllerValidator.input_email_address()
        room_no = RoomControllerValidator.input_room_no()
        floor_no = RoomControllerValidator.input_floor_no()
        checkout_date_time = CommonHelper.get_current_date_and_time()
        result = self.room_controller_obj.save_room_details_for_check_out(cust_email, room_no, floor_no, checkout_date_time)
        
    def view_check_in_check_out_details(self) -> None:
        pass
            