import pytest


from src.config.query import QueryConfig
from models.database import AppConfig, Database
from resources.auth_resource import oauth2_bearer, create_access_token
from main import app
from config.app_config import AppConfig

@pytest.fixture(scope='package')
def test_db(package_mocker):
    
    package_mocker.patch.object(AppConfig, "DATABASE_PATH", AppConfig.TEST_DATABASE_PATH)

    test_db_obj = Database()
    test_db_obj.create_all_tables()

    yield test_db_obj

    test_db_obj.delete_operation_on_database("DROP TABLE authentication")
    test_db_obj.delete_operation_on_database("DROP TABLE room")
    test_db_obj.delete_operation_on_database("DROP TABLE customer")
    test_db_obj.delete_operation_on_database("DROP TABLE reservation")

@pytest.fixture(autouse=True, scope='package')
def insert_into_tables(test_db):
    test_db.save_data_to_database(QueryConfig.SAVE_LOGIN_CREDENTIALS, ("EMP12345", "user@abcde", "Abcde@12345", "admin"))
    test_db.save_data_to_database(QueryConfig.SAVE_CUSTOMER_DATA, ("CUST12345", "Dev Mishra", 25, "Male", "dev25mishra@gmail.com", "7456369852"))
    test_db.save_data_to_database(QueryConfig.SAVE_ROOM_DATA, ("ROOM12345", 15, 2, 2500))
    test_db.save_data_to_database(QueryConfig.CHECK_IN_ROOM, ("RESR12345", "CUST12345", "ROOM12345", "02-02-2024", "10:00", "03-02-2024", "10:00"))

def get_test_token_reception():
    return create_access_token("user@abc", "RECEPTION")

def get_test_token_admin():
    return create_access_token("user@abc", "ADMIN")

@pytest.fixture
def admin_dependency():
    app.dependency_overrides[oauth2_bearer] = get_test_token_admin

@pytest.fixture
def reception_dependency():
    app.dependency_overrides[oauth2_bearer] = get_test_token_reception