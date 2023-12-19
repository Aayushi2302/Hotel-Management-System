import pytest

from src.views.employee_views import EmployeeViews

class TestEmployeeViews:
    @pytest.fixture(autouse=True)
    def mock_init(self, mocker) -> None:
        self.employee_views_obj = EmployeeViews(mocker.Mock(), mocker.Mock())


    def test_reception_or_staff_menu_negative(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ['1', '2', '3', '4', '5', '6', 'random'])
        mocker.patch('src.views.employee_views.EmployeeViews.register_customer', return_value = None)
        mocker.patch('src.views.employee_views.RoomViews.check_in_room', return_value = None)
        mocker.patch('src.views.employee_views.RoomViews.check_out_room', return_value = None)
        mocker.patch('src.views.employee_views.RoomViews.view_room_details', return_value = None)
        mocker.patch('src.views.employee_views.EmployeeViews.view_customer_details', return_value = None)
        mocker.patch('src.views.employee_views.EmployeeViews.remove_customer', return_value = None)
        for _ in range(7):
            assert self.employee_views_obj.reception_or_staff_menu() is False

    def test_reception_or_staff_menu_positive(self, mocker) -> bool:
        mocker.patch('builtins.input', return_value = '7')
        assert self.employee_views_obj.reception_or_staff_menu() is True