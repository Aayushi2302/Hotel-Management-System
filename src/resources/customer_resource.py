import shortuuid
from sqlite3 import Error
from fastapi import APIRouter, HTTPException, Path
from starlette import status

from config.app_config import AppConfig
from config.regex_pattern import RegexPattern
from schemas.customer_schema import CustomerSchemaArguments, CustomerSchemaResponse, CustomerUpdateSchema
from controllers.employee_controller import EmployeeController

router = APIRouter()

@router.post("/customer", status_code=status.HTTP_201_CREATED, response_model=CustomerSchemaResponse)
async def register_customer(customer_data: CustomerSchemaArguments):
    try:
        cust_id = "CUST" + shortuuid.ShortUUID().random(5)
        name = customer_data.name
        age = customer_data.age
        gender = customer_data.gender

        if gender in ('f', 'F'):
            gender = "Female"
        elif gender in ('m', 'M'):
            gender = "Male"
        else:
            raise HTTPException(400, detail="Invalid gender supplied. Gender can be either 'f' or 'm'.")
        email = customer_data.email
        mobile_number = customer_data.mobile_number

        cust_data = (cust_id, name, age, gender, email, mobile_number)
        employee_controller_obj = EmployeeController()
        result = employee_controller_obj.save_customer_details(cust_data)

        if not result:
            raise HTTPException(500, detail="An error occurred while creating customer.")
        
        response = {
            "cust_id" : cust_id,
            "name" : name,
            "age" : age,
            "gender" : gender,
            "email" : email,
            "mobile_number" : mobile_number,
            "status" : AppConfig.STATUS_ACTIVE
        }

        return response
    except Error:
        raise HTTPException(500, detail="Internal Server Error")

@router.get("/customer", status_code=status.HTTP_200_OK, response_model=list[CustomerSchemaResponse])
async def get_all_customers():
    employee_controller_obj = EmployeeController()
    data = employee_controller_obj.get_customer_details()
    if not data:
        raise HTTPException(404, detail="Resource not found.")
    else:
        return data

@router.patch("/customer/{customer_email}", status_code=status.HTTP_200_OK, response_model=CustomerUpdateSchema)
async def deactivate_customer(customer_email: str = Path(pattern=RegexPattern.EMAIL_REGEX)):
    try:
        employee_controller_obj = EmployeeController()
        new_status = AppConfig.STATUS_INACTIVE
        result = employee_controller_obj.deactivate_customer(customer_email, new_status)
        if result == -1:
            raise HTTPException(404, detail="Resource which you are looking for does not exist.")
        elif result == -2:
            raise HTTPException(412, detail=f"Resource is already {new_status}.")
        else:
            response = {
                "cust_email" : customer_email,
                "status" : new_status
            }
            return response
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")
