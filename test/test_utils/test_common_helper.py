import pytest

from src.utils.common_helper import CommonHelper

class TestCommonHelper:
    @pytest.fixture(autouse=True)
    def mock_init(self, mocker) -> None:
        self.common_helper_obj = CommonHelper(mocker.Mock())

    def test_is_admin_registered_positive(self) -> bool:
        self.common_helper_obj.db.fetch_data_from_database.return_value = True
        assert self.common_helper_obj.is_admin_registered() is True
        self.common_helper_obj.db.fetch_data_from_database.assert_called_once()


    def test_is_admin_registered_negative(self) -> bool:
        self.common_helper_obj.db.fetch_data_from_database.return_value = False
        assert self.common_helper_obj.is_admin_registered() is False
        self.common_helper_obj.db.fetch_data_from_database.assert_called_once()

    def test_create_new_password_positive(self, mocker) -> bool:
        mocker.patch('maskpass.askpass', return_value = "Demo@1234")
        mocker.patch('src.utils.common_helper.CommonHelper.input_validation', return_value = True)
        mocker.patch('src.utils.common_helper.hashlib.sha256', return_value = mocker.Mock(hexdigest = lambda : "hashed password"))
        self.common_helper_obj.db.save_data_to_database.return_value = None
        assert self.common_helper_obj.create_new_password("user@aayushi") == None
        self.common_helper_obj.db.save_data_to_database.assert_called_once()

    def test_create_new_password_negative(self, mocker) -> bool:
        mocker.patch('maskpass.askpass', side_effect = ["demo@1234", "Demo@1234", "demo@1234", "Demo@1234", "Demo@1234"])
        mocker.patch('src.utils.common_helper.CommonHelper.input_validation', side_effect = [False, True, True])
        mocker.patch('src.utils.common_helper.hashlib.sha256', return_value = mocker.Mock(hexdigest = lambda : "hashed password"))
        self.common_helper_obj.db.save_data_to_database.return_value = None
        assert self.common_helper_obj.create_new_password("user@aayushi") == None
        self.common_helper_obj.db.save_data_to_database.assert_called_once()

    def test_input_validation_positive(self, mocker) -> bool:
        mocker.patch('re.match',  return_value = "True")
        assert self.common_helper_obj.input_validation("abc", "abc") is True

    def test_input_validation_negative(self, mocker) -> bool:
        mocker.patch('re.match',  return_value = None)
        assert self.common_helper_obj.input_validation("abc", "abc") is False
        