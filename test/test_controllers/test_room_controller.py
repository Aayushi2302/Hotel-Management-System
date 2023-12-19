import pytest

from src.controllers.room_controller import RoomController

class TestRoomController:
    @pytest.fixture(autouse=True)
    def mock_init(self, mocker) -> None:
        self.room_controller_obj = RoomController(mocker.Mock(), mocker.Mock())

    def test_save_room_details_positive(self) -> bool:
        self.room_controller_obj.db.save_data_to_database.return_value = 1
        assert self.room_controller_obj.save_room_details(("room data", )) == 1
        self.room_controller_obj.db.save_data_to_database.assert_called_once()

    def test_save_room_details_negative(self) -> bool:
        self.room_controller_obj.db.save_data_to_database.return_value = None
        assert self.room_controller_obj.save_room_details(("room data", )) == None
        self.room_controller_obj.db.save_data_to_database.assert_called_once()

    def test_get_available_rooms_positive(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = [("data", )]
        assert self.room_controller_obj.get_available_rooms() == [("data", )]
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_get_available_rooms_negative(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = []
        assert self.room_controller_obj.get_available_rooms() == []
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_get_room_data_positive(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = [("data", )]
        assert self.room_controller_obj.get_room_data() == [("data", )]
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_get_room_data_negative(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = []
        assert self.room_controller_obj.get_room_data() == []
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_is_room_available_positive(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = [("available", )]
        assert self.room_controller_obj.is_room_available("room_id") == True
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_is_room_available_negative(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.side_effect = [[], [("booked", )]]
        assert self.room_controller_obj.is_room_available("room_id") is False
        assert self.room_controller_obj.is_room_available("room_id") is False

    def test_update_room_status_positive(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = [("room_id", "available")]
        self.room_controller_obj.db.save_data_to_database.return_value = 1
        assert self.room_controller_obj.update_room_status("floor_no", "room_no", "updated_status") == 1
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()
        self.room_controller_obj.db.save_data_to_database.assert_called_once()

    def test_update_room_status_negative(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.side_effect = [[], [("room_id", "available")], [("room_id", "booked")]]
        self.room_controller_obj.db.save_data_to_database.return_value = 0
        assert self.room_controller_obj.update_room_status("floor_no", "room_no", "updated_status") == -1
        assert self.room_controller_obj.update_room_status("floor_no", "room_no", "available") == -2
        assert self.room_controller_obj.update_room_status("floor_no", "room_no", "updated_field") == 0
        self.room_controller_obj.db.save_data_to_database.assert_called_once()

    def test_get_preferred_room_positive(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = [("data", )]
        assert self.room_controller_obj.get_preferred_room(5000) == [("data", )]
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_get_preferred_room_negative(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = []
        assert self.room_controller_obj.get_preferred_room(5000) == []
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_save_room_details_for_check_in_positive(self, mocker) -> bool:
        self.room_controller_obj.employee_controller_obj.get_customer_id_from_email.return_value = [("cust data", )]
        mocker.patch('src.controllers.room_controller.RoomController.is_room_available', return_value = True)
        self.room_controller_obj.db.save_data_to_database.return_value = 1
        assert self.room_controller_obj.save_room_details_for_check_in(
            "reservation_id",
            "room_id",
            ("demo@gmail.com", ("18-12-2023", "12:15"), ("18-12-2023", "13:15"))
        ) == 1
        self.room_controller_obj.db.save_data_to_database.assert_called_once()

    def test_save_room_details_for_check_in_negative(self, mocker) -> bool:
        self.room_controller_obj.employee_controller_obj.get_customer_id_from_email.side_effect = [[], [("cust data", )], [("cust data", )]]
        mocker.patch('src.controllers.room_controller.RoomController.is_room_available', side_effect = [False, True])
        self.room_controller_obj.db.save_data_to_database.return_value = 0
        assert self.room_controller_obj.save_room_details_for_check_in(
            "reservation_id",
            "room_id",
            ("demo@gmail.com", ("18-12-2023", "12:15"), ("18-12-2023", "13:15"))
        ) == -1
        assert self.room_controller_obj.save_room_details_for_check_in(
            "reservation_id",
            "room_id",
            ("demo@gmail.com", ("18-12-2023", "12:15"), ("18-12-2023", "13:15"))
        ) == -2
        assert self.room_controller_obj.save_room_details_for_check_in(
            "reservation_id",
            "room_id",
            ("demo@gmail.com", ("18-12-2023", "12:15"), ("18-12-2023", "13:15"))
        ) == 0
        self.room_controller_obj.db.save_data_to_database.assert_called_once()

    def test_get_room_id_from_room_no_positive(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = [("data", )]
        assert self.room_controller_obj.get_room_id_from_room_no("room_no", "floor_no") == [("data", )]
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_get_room_id_from_room_no_negative(self) -> bool:
        self.room_controller_obj.db.fetch_data_from_database.return_value = []
        assert self.room_controller_obj.get_room_id_from_room_no("room_no", "floor_no") == []
        self.room_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_save_room_details_for_check_out_negative(self) -> bool:
        self.room_controller_obj.employee_controller_obj.get_customer_id_from_email.return_value = []
        assert self.room_controller_obj.save_room_details_for_check_out("demo@gmail.com", "room_no", "floor_no", "checkout_date_time") == -1