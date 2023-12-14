import shortuuid

from config.prompts import Prompts
from config.query import TableHeader
from controllers.room_controller import RoomController
from utils.common_helper import CommonHelper
from utils.input_validator.room_controller_validator import RoomControllerValidator

class RoomViews:
    def __init__(self, room_controller_obj: RoomController) -> None:
        self.room_controller_obj = room_controller_obj
    
    def register_room(self) -> None:
        print(Prompts.ENTER_ROOM_DETAILS + "\n")
        room_id = "ROOM" + shortuuid.ShortUUID().random(5)
        room_no = RoomControllerValidator.input_room_no()
        floor_no = RoomControllerValidator.input_floor_no()
        charges = RoomController.input_charges()
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
        pass