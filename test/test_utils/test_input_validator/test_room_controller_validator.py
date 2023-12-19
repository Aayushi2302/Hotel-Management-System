import pytest

from src.utils.input_validator.room_controller_validator import RoomControllerValidator

class TestRoomControllerValidator:
    def test_input_room_no(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["abc", 123])
        assert RoomControllerValidator.input_room_no() == 123

    def test_input_floor_no(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["abc", 123])
        assert RoomControllerValidator.input_floor_no() == 123

    def test_input_charges(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["abc", 123.12])
        assert RoomControllerValidator.input_charges() == 123.12

    def test_input_room_id(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["random", "ROOM12dg4"])
        assert RoomControllerValidator.input_room_id() == "ROOM12dg4"
        