import shortuuid

from config.prompts import Prompts
from config.query import TableHeader
from controllers.employee_controller import EmployeeController
from controllers.room_controller import RoomController
from utils.common_helper import CommonHelper
from utils.error_handler import error_handler
from utils.input_validator.user_controller_validator import UserControllerValidator
from views.room_views import RoomViews

class EmployeeViews:
    def __init__(self, employee_controller_obj: EmployeeController, room_controller_obj: RoomController) -> None:
        self.employee_controller_obj = employee_controller_obj
        self.room_views_obj = RoomViews(room_controller_obj)

    def employee_menu_operations(self) -> None:
        while True:
            if self.reception_or_staff_menu():
                break

    def register_customer(self) -> None:
        print(Prompts.ENTER_CUSTOMER_DETAILS + "\n")
        cust_id = "CUST" + shortuuid.ShortUUID().random(5)
        cust_name = UserControllerValidator.input_name()
        cust_age = UserControllerValidator.input_age()
        cust_gender = UserControllerValidator.input_gender()
        cust_email = UserControllerValidator.input_email_address()
        cust_mobile_number = UserControllerValidator.input_mobile_number()
        cust_data = (cust_id, cust_name, cust_age, cust_gender, cust_email, cust_mobile_number)
        result = self.employee_controller_obj.save_customer_details(cust_data)
        if result:
            print(Prompts.SUCESSFUL_CUSTOMER_CREATION + "\n")
        else:
            print(Prompts.UNSUCCESSFUL_CUSTOMER_CREATION + "\n")
    
    def view_customer_details(self) -> None:
        data = self.employee_controller_obj.get_customer_details()
        if not data:
            print(Prompts.ZERO_RECORD.format("Customer"))
        else:
            header = TableHeader.CUSTOMER_TABLE_HEADER()
            CommonHelper.display_table(data, header)

    def remove_customer(self) -> None:
        cust_email = UserControllerValidator.input_email_address()
        result = self.employee_controller_obj.remove_customer_details(cust_email)
        if result == -1:
            print(Prompts.CUSTOMER_DOES_NOT_EXIST + "\n")
        elif result == 0:
            print(Prompts.SUCCESSFUL_CUSTOMER_REMOVAL + "\n")
        else:
            print(Prompts.UNSUCCESSFUL_CUSTOMER_REMOVAL + "\n")

    @error_handler
    def reception_or_staff_menu(self) -> bool:
        print(Prompts.STAFF_OR_RECEPTION_MENU + "\n")
        choice = input(Prompts.ENTER_CHOICE)
        match choice:
            case '1':
                self.register_customer()
            case '2':
                self.room_views_obj.check_in_room()
            case '3':
                self.room_views_obj.check_out_room()
            case '4':
                self.room_views_obj.view_room_details()
            case '5':
                self.view_customer_details()
            case '6':
                self.remove_customer()
            case '7':
                print(Prompts.SUCCESSFUL_LOGOUT + "\n")
                return True
            case _:
                print(Prompts.INVALID_INPUT + "\n")
        return False
