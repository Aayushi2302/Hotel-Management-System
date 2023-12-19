import pytest

from src.controllers.employee_controller import EmployeeController

class TestEmployeeController:
    @pytest.fixture(autouse=True)
    def mock_init(self, mocker) -> None:
        self.employee_controller_obj = EmployeeController(mocker.Mock())

    def test_save_customer_details_positive(self) -> bool:
        self.employee_controller_obj.db.save_data_to_database.return_value = 1
        assert self.employee_controller_obj.save_customer_details(["data"]) == 1
        self.employee_controller_obj.db.save_data_to_database.assert_called_once()

    def test_save_customer_details_negative(self) -> bool:
        self.employee_controller_obj.db.save_data_to_database.return_value = 0
        assert self.employee_controller_obj.save_customer_details(["data"]) == 0
        self.employee_controller_obj.db.save_data_to_database.assert_called_once()
    
    def test_get_customer_details(self) -> bool:
        self.employee_controller_obj.db.fetch_data_from_database.return_value = ["data"]
        assert self.employee_controller_obj.get_customer_details() == ["data"]
        self.employee_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_get_customer_id_from_email(self) -> bool:
        self.employee_controller_obj.db.fetch_data_from_database.return_value = ["data"]
        assert self.employee_controller_obj.get_customer_id_from_email("demo@gmail.com") == ["data"]
        self.employee_controller_obj.db.fetch_data_from_database.assert_called_once()

    def test_remove_customer_details_positive(self, mocker) -> bool:
        mocker.patch('src.controllers.employee_controller.EmployeeController.get_customer_id_from_email', return_value = [("data",)])
        self.employee_controller_obj.db.save_data_to_database.return_value = 1
        assert self.employee_controller_obj.remove_customer_details("demo@gmail.com") == 1
        self.employee_controller_obj.db.save_data_to_database.assert_called_once()

    def test_remove_customer_details_negative(self, mocker) -> bool:
        mocker.patch('src.controllers.employee_controller.EmployeeController.get_customer_id_from_email', side_effect = [[], [("data", )]])
        self.employee_controller_obj.db.save_data_to_database.return_value = 0
        assert self.employee_controller_obj.remove_customer_details("demo@gmail.com") == -1
        assert self.employee_controller_obj.remove_customer_details("demo@gmail.com") == 0
        self.employee_controller_obj.db.save_data_to_database.assert_called_once()
    