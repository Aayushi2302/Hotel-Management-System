import pytest

from src.controllers.admin_controller import AdminController

class TestAdminController:
    @pytest.fixture(autouse=True)
    def mock_init(self, mocker) -> None:
        self.admin_controller_obj = AdminController(mocker.Mock())

    def test_register_emp_credentials_positive(self, mocker) -> bool:
        self.admin_controller_obj.db.save_data_to_database.return_value = 1
        assert self.admin_controller_obj.register_emp_credentials(["data"]) == 1

    def test_register_emp_credentials_negative(self, mocker) -> bool:
        self.admin_controller_obj.db.save_data_to_database.return_value = 0
        assert self.admin_controller_obj.register_emp_credentials(["data"]) == 0
