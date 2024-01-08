"""
    Room class input validation
""" 
from datetime import datetime
import pytz

from config.prompts import Prompts
from config.regex_pattern import RegexPattern
from utils.common_helper import CommonHelper

class RoomControllerValidator:
    @staticmethod
    def input_room_no() -> int:
        while True:
            try:
                room_no = int(input("Room No : "))
                return room_no
            except ValueError:
                print(Prompts.INVALID_INPUT + "\n")
                

    @staticmethod
    def input_floor_no() -> int:
        while True:
            try:
                floor_no = int(input("Floor No : "))
                return floor_no
            except ValueError:
                print(Prompts.INVALID_INPUT + "\n")
                

    @staticmethod
    def input_charges() -> float:
        while True:
            try:
                charges = float(input("Charges : "))
                return charges
            except ValueError:
                print(Prompts.INVALID_INPUT + "\n")

    @staticmethod
    def input_room_id() -> str:
        while True:
            room_id = input(Prompts.INPUT_ROOM_ID).strip()
            is_valid_room_id = CommonHelper.input_validation(RegexPattern.ROOM_ID_REGEX, room_id)
            if is_valid_room_id:
                return room_id

    @staticmethod
    def input_out_date_and_time() -> str:
        while True:
            print(Prompts.INPUT_TIME_IN_24_HOUR_FORMAT + "\n")
            time_zone = pytz.timezone('Asia/Kolkata')
            out_date = input(Prompts.CUSTOMER_OUT_DATE_INPUT).strip()
            out_time = input(Prompts.CUSTOMER_OUT_TIME_INPUT).strip()
            present_date_time = datetime.now().replace(tzinfo=time_zone)
            try:
                out_date_time = datetime.strptime(out_date + " " + out_time, "%d-%m-%Y %H:%M").replace(tzinfo=time_zone)
                if out_date_time < present_date_time:
                    print(Prompts.CANNOT_INPUT_PAST_DATE_TIME + "\n")
                else:
                    return (out_date, out_time)
            except ValueError:
                print(Prompts.INVALID_INPUT + "\n")
                