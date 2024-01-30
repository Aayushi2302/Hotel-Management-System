import string
import random
import shortuuid

from sqlite3 import Error
from fastapi import Body, APIRouter, HTTPException
from starlette import status
from config.app_config import AppConfig
from schemas.employee_schema import EmployeeSchema
from controllers.admin_controller import AdminController

router = APIRouter()

@router.post("/employee", status_code=status.HTTP_201_CREATED)
async def register_employee(employee_data: EmployeeSchema):
    try:
        emp_id = "EMP" + shortuuid.ShortUUID().random(5)
        characters = string.ascii_letters + string.digits + "@#$&%"
        emp_password = ''.join(random.choice(characters) for _ in range(8))
        username = employee_data.username
        role = employee_data.role

        emp_data = (emp_id, username, emp_password, role)

        print(emp_data)

        admin_controller_obj = AdminController()
        result = admin_controller_obj.register_emp_credentials(emp_data)

        if not result:
            raise HTTPException(500, detail="An error occurred while creating employee.")
        
        return  {
                    "employee_id" : emp_id,
                    "username" : username,
                    "password" : emp_password,
                    "role" : role,
                    "password_type" : AppConfig.DEFAULT_PASSWORD
                }
    except Error:
        raise HTTPException(500, detail="Internal server error.")