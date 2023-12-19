import pytest

from src.views.admin_views import AdminViews

class TestAdminViews:
    @pytest.fixture(autouse=True)
    def mock_init(self, mocker) -> None:
        self.admin_views_obj = AdminViews(mocker.Mock(), mocker.Mock())


    def test_admin_menu_negative(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ['1', '2', '3', '4', '5', 'random'])
        mocker.patch('src.views.admin_views.RoomViews.register_room', return_value = None)
        mocker.patch('src.views.admin_views.RoomViews.activate_room', return_value = None)
        mocker.patch('src.views.admin_views.RoomViews.deactivate_room', return_value = None)
        mocker.patch('src.views.admin_views.RoomViews.view_room_details', return_value = None)
        mocker.patch('src.views.admin_views.RoomViews.view_check_in_check_out_details', return_value = None)
        # mocker.patch('src.views.admin_views.AdminViews.create_emp_credentails', return_value = None)
        for _ in range(6):
            assert self.admin_views_obj.admin_menu() is False

    def test_admin_menu_positive(self, mocker) -> bool:
        mocker.patch('builtins.input', return_value = '7')
        assert self.admin_views_obj.admin_menu() is True