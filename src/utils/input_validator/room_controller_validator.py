"""
    Room class input validation
""" 
from config.prompts import Prompts

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
                