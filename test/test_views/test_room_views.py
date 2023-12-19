import pytest 

from src.views.room_views import RoomViews

class TestRoomViews:
    @pytest.fixture(autouse=True)
    def mock_init(self, mocker) -> None:
        self.room_views_obj = RoomViews(mocker.Mock())

    
    def test_register_room_positive(self, mocker) -> bool:
        mocker.patch('shortuuid.ShortUUID.random', return_value = "abc12")
        mocker.patch('src.views.room_views.RoomControllerValidator.input_room_no', return_value = 412)
        mocker.patch('src.views.room_views.RoomControllerValidator.input_floor_no', return_value = 4)
        mocker.patch('src.views.room_views.RoomControllerValidator.input_charges', return_value = 5500)
        self.room_views_obj.room_controller_obj.save_room_details.return_value = True
        assert self.room_views_obj.register_room() is None

    def test_register_room_negative(self, mocker) -> bool:
        mocker.patch('shortuuid.ShortUUID.random', return_value = "abc12")
        mocker.patch('src.views.room_views.RoomControllerValidator.input_room_no', return_value = 412)
        mocker.patch('src.views.room_views.RoomControllerValidator.input_floor_no', return_value = 4)
        mocker.patch('src.views.room_views.RoomControllerValidator.input_charges', return_value = 5500)
        self.room_views_obj.room_controller_obj.save_room_details.return_value = False
        assert self.room_views_obj.register_room() is None

    def test_view_room_details_positive(self) -> bool:
        self.room_views_obj.room_controller_obj.get_room_data.return_value = [("data", )]
        assert self.room_views_obj.view_room_details() is None

    def test_view_room_details_negative(self) -> bool:
        self.room_views_obj.room_controller_obj.get_room_data.return_value = []
        assert self.room_views_obj.view_room_details() is None

    def test_decativate_room_positive(self, mocker) -> bool:
        mocker.patch('src.views.room_views.RoomControllerValidator.input_floor_no', return_value = 12)
        mocker.patch('src.views.room_views.RoomControllerValidator.input_room_no', return_value = 1201)
        self.room_views_obj.room_controller_obj.update_room_status.return_value = 1
        assert self.room_views_obj.deactivate_room() is None

    def test_deactivate_room_negative(self, mocker) -> bool:
        mocker.patch('src.views.room_views.RoomControllerValidator.input_floor_no', return_value = 12)
        mocker.patch('src.views.room_views.RoomControllerValidator.input_room_no', return_value = 1201)
        self.room_views_obj.room_controller_obj.update_room_status.side_effect = ['-1', '-2', '0']
        assert self.room_views_obj.deactivate_room() is None
        assert self.room_views_obj.deactivate_room() is None
        assert self.room_views_obj.deactivate_room() is None

    def test_actiavte_room_positive(self, mocker) -> bool:
        mocker.patch('src.views.room_views.RoomControllerValidator.input_floor_no', return_value = 12)
        mocker.patch('src.views.room_views.RoomControllerValidator.input_room_no', return_value = 1201)
        self.room_views_obj.room_controller_obj.update_room_status.return_value = 1
        assert self.room_views_obj.activate_room() is None

    def test_actiavte_room_negative(self, mocker) -> bool:
        mocker.patch('src.views.room_views.RoomControllerValidator.input_floor_no', return_value = 12)
        mocker.patch('src.views.room_views.RoomControllerValidator.input_room_no', return_value = 1201)
        self.room_views_obj.room_controller_obj.update_room_status.side_effect = ['-1', '-2', '0']
        assert self.room_views_obj.activate_room() is None
        assert self.room_views_obj.activate_room() is None
        assert self.room_views_obj.activate_room() is None

    def test_view_availabl_rooms_positive(self) -> bool:
        self.room_views_obj.room_controller_obj.get_available_rooms.return_value = [("data", )]
        assert self.room_views_obj.view_available_rooms() == [("data", )]

    def test_view_availabl_rooms_negative(self) -> bool:
        self.room_views_obj.room_controller_obj.get_available_rooms.return_value = []
        assert self.room_views_obj.view_available_rooms() == []

    def test_view_rooms_for_check_in_positive(self) -> bool:
        self.room_views_obj.room_controller_obj.get_preferred_room.return_value = [("data", )]
        assert self.room_views_obj.view_room_for_check_in(5000) == [("data", )]