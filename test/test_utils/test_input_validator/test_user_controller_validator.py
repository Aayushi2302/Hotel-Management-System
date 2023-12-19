import pytest

from src.utils.input_validator.user_controller_validator import UserControllerValidator

class TestUserControllerValidator:
    def test_input_name(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect= ["123", "Aayushi"])
        assert UserControllerValidator.input_name() == "Aayushi"
    
    def test_input_username(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["123", "user@aayushi"])
        assert UserControllerValidator.input_username() == "user@aayushi"

    def test_input_age(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["abc", "12", "45"])
        assert UserControllerValidator.input_age() == 45

    def test_input_gender(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["c", "M", "F"])
        assert UserControllerValidator.input_gender() == "Male"
        assert UserControllerValidator.input_gender() == "Female"

    def test_input_role(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["123", "admin", "attendant"])
        assert UserControllerValidator.input_role() == "attendant"

    def test_input_email_address(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["123", "user@gmail.com"])
        assert UserControllerValidator.input_email_address() == "user@gmail.com"

    def test_input_mobile_number(self, mocker) -> bool:
        mocker.patch('builtins.input', side_effect = ["1234567891", "9687456325"])
        assert UserControllerValidator.input_mobile_number() == "9687456325"
        