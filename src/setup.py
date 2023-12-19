from models.database import db
from controllers.auth_controller import AuthController
from controllers.admin_controller import AdminController
from controllers.employee_controller import EmployeeController
from controllers.room_controller import RoomController
from utils.common_helper import CommonHelper

class SetUp:
    common_helper_obj = CommonHelper(db)
    admin_controller_obj = AdminController(db)
    employee_controller_obj = EmployeeController(db)
    auth_controller_obj = AuthController(db, common_helper_obj, admin_controller_obj, employee_controller_obj)
    room_controller_obj = RoomController(db, employee_controller_obj)
    