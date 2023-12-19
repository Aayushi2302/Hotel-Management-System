import pytest

from src.controllers.auth_controller import AuthController

class TestRoomController:
    @pytest.fixture(autouse=True)
    def mock_init(self, mocker):
        self.auth_controller_obj = AuthController(mocker.Mock(), mocker.Mock(), mocker.Mock(), mocker.Mock(), mocker.Mock())

    def test_valid_first_login_positive(self) -> bool:
        self.auth_controller_obj.common_helper_obj.create_new_password.return_value = None
        assert self.auth_controller_obj.valid_first_login("user@admin", "Admin@1234", "Admin@1234") == True

    def test_valid_first_login_negative(self) -> bool:
        assert self.auth_controller_obj.valid_first_login("user@admin", "Admin@1234", "admin1234") == False

    @pytest.mark.parametrize("roles", ["admin", "staff", "reception"])
    def test_role_based_access_positive(self, roles, mocker) -> bool:
        mocker.patch('src.controllers.auth_controller.AdminViews.admin_menu_operations', return_value = None)
        mocker.patch('src.controllers.auth_controller.EmployeeViews.employee_menu_operations', return_value = None)
        assert self.auth_controller_obj.role_based_access(roles) == True

    def test_role_based_access_negative(self) -> bool:
        assert self.auth_controller_obj.role_based_access("manager") == False

    def test_authenticate_user_positive(self, mocker) -> bool:
        self.auth_controller_obj.db.fetch_data_from_database.side_effect = [[("Admin@1234", "admin", "default")], [("Admin@1234", "admin", "permanent")]]
        mocker.patch('src.controllers.auth_controller.AuthController.valid_first_login', return_value = True)
        mocker.patch('src.controllers.auth_controller.hashlib.sha256', return_value = mocker.Mock(hexdigest = lambda : "Admin@1234"))
        mocker.patch('src.controllers.auth_controller.AuthController.role_based_access', return_value = True)
        assert self.auth_controller_obj.authenticate_user("user@admin", "Admin@1234")
        assert self.auth_controller_obj.authenticate_user("user@admin", "Admin@1234")

    def test_authenticate_user_negative(self, mocker) -> bool:
        self.auth_controller_obj.db.fetch_data_from_database.side_effect = [[], [("Admin@1234", "admin", "permanent")]]
        mocker.patch('src.controllers.auth_controller.hashlib.sha256', return_value = mocker.Mock(hexdigest = lambda : "admin@1234"))
        assert not self.auth_controller_obj.authenticate_user("user@admin", "Admin@1234")
        assert not self.auth_controller_obj.authenticate_user("user@admin", "Admin@1234")
        