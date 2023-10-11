"""
    Room class input validation
""" 
def input_room_no() -> int:
    # validation of room no
    while True:
        try:
            room_no = int(input("Room No : "))
            return room_no
        except Exception as e:
            print(e)

def input_floor_no() -> int:
    # validation of floor no
    while True:
        try:
            floor_no = int(input("Floor No : "))
            return floor_no
        except Exception as e:
            print(e)

def input_charges() -> float:
    # validation of charges
    while True:
        try:
            charges = float(input("Charges : "))
            return charges
        except Exception as e:
            print(e)
