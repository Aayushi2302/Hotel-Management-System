import random
from sqlite3 import Error, IntegrityError
import string
from fastapi import APIRouter, HTTPException
import shortuuid
from starlette import status


from config.app_config import AppConfig
from schemas.employee_schema import EmployeeSchemaArguments
from controllers.admin_controller import AdminController
from resources.auth_resource import token_dependency
from utils.rbac import role_based_access
from utils.role_mapping import RoleMapping

router = APIRouter(
    tags=["employee"]
)

@router.post("/employee", status_code=status.HTTP_201_CREATED)
@role_based_access((RoleMapping["ADMIN"], ))
def register_employee(token: token_dependency, employee_data: EmployeeSchemaArguments):
    try:
        emp_id = "EMP" + shortuuid.ShortUUID().random(5)
        characters = string.ascii_letters + string.digits + "@#$&%"
        emp_password = ''.join(random.choice(characters) for _ in range(8))
        username = employee_data.username
        role = employee_data.role

        emp_data = (emp_id, username, emp_password, role)

        admin_controller_obj = AdminController()
        result = admin_controller_obj.register_emp_credentials(emp_data)

        return  {
                    "employee_id" : emp_id,
                    "username" : username,
                    "password" : emp_password,
                    "role" : role,
                    "password_type" : AppConfig.DEFAULT_PASSWORD
                }

    except IntegrityError as error:
        raise HTTPException(409, detail="Data already exist")

    except Error as error:
        print(error)
        raise HTTPException(500, detail="Internal server error")
