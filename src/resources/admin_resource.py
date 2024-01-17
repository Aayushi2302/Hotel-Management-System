import shortuuid
import string
import random

from config.app_config import AppConfig
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas.admin_schema import EmployeeSchema
from controllers.admin_controller import AdminController
from flask_jwt_extended import jwt_required
from utils.rbac import role_based_access
from utils.role_mapping import RoleMapping
from utils.error_handler import error_handler

blp = Blueprint("admin", __name__, description = "Admin operations")

@blp.route("/employee")
class AdminOperations(MethodView):

    @error_handler
    @role_based_access((RoleMapping.ADMIN_ROLE, ))
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(EmployeeSchema)
    @blp.response(201, EmployeeSchema)
    def post(self, employee_data):

        emp_id = "EMP" + shortuuid.ShortUUID().random(5)
        characters = string.ascii_letters + string.digits + "@#$&%"
        emp_password = ''.join(random.choice(characters) for _ in range(8))
        username = employee_data["username"]
        role = employee_data["role"]

        emp_data = (emp_id, username, emp_password, role)

        admin_controller_obj = AdminController()
        result = admin_controller_obj.register_emp_credentials(emp_data)

        if not result:
            abort(500, message="An error occurred while creating employee.")
        
        response = {
            "employee_id" : emp_id,
            "username" : username,
            "password" : emp_password,
            "role" : role,
            "password_type" : AppConfig.DEFAULT_PASSWORD
        }

        return response

