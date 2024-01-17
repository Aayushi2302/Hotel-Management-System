import shortuuid
import requests
import os

from config.app_config import AppConfig
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from controllers.employee_controller import EmployeeController
from schemas.customer_schema import CustomerSchema, CustomerUpdateSchema, DemoSchema
from utils.rbac import role_based_access
from utils.role_mapping import RoleMapping
from utils.error_handler import error_handler

blp = Blueprint("customer", __name__, description="Customer operations")

def send_simple_message(to, subject, body):
    domain = os.getenv('MAILGUN_DOMAIN')
    api_key = os.getenv('MAILGUN_API_KEY')
    return requests.post(
        f"https://api.mailgun.net/v3/{domain}/messages",
        auth=("api", f"{api_key}"),
        data={"from": f"Aayushi Sharma <mailgun@{domain}>",
            "to": [to],
            "subject": subject,
            "text": body})

@blp.route("/customer")
class CustomerOperations(MethodView):
    @error_handler
    @role_based_access((RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(CustomerSchema)
    @blp.response(201, CustomerSchema)
    def post(self, customer_data):
        cust_id = "CUST" + shortuuid.ShortUUID().random(5)
        name = customer_data["name"]
        age = customer_data["age"]
        gender = customer_data["gender"]

        if gender in ('f', 'F'):
            gender = "Female"
        elif gender in ('m', 'M'):
            gender = "Male"
        else:
            abort(400, "Invalid gender supplied. Gender can be either 'f' or 'm'.")
        email = customer_data["email"]
        mobile_number = customer_data["mobile_number"]

        cust_data = (cust_id, name, age, gender, email, mobile_number)
        employee_controller_obj = EmployeeController()
        result = employee_controller_obj.save_customer_details(cust_data)

        if not result:
            abort(500, message="An error occurred while creating customer.")
        
        response = {
            "cust_id" : cust_id,
            "name" : name,
            "age" : age,
            "gender" : gender,
            "email" : email,
            "mobile_number" : mobile_number,
            "status" : AppConfig.STATUS_ACTIVE
        }

        send_simple_message(
            to=email,
            subject="Successfully registered",
            body="Thank you registering to this system."
        )

        return response

    @error_handler
    @role_based_access((RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.response(200, CustomerSchema(many=True))
    def get(self):
        employee_controller_obj = EmployeeController()
        data = employee_controller_obj.get_customer_details()
        if not data:
            abort(404, message="Resource not found.")
        else:
            return data

@blp.route("/customer/<string:customer_email>")
class CustomerOperationsID(MethodView):
    @error_handler
    @role_based_access((RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.response(200, CustomerUpdateSchema)
    def patch(self, customer_email: str):
        employee_controller_obj = EmployeeController()
        new_status = AppConfig.STATUS_INACTIVE
        result = employee_controller_obj.deactivate_customer(customer_email, new_status)
        if result == -1:
            abort(404, message="Resource which you are looking for does not exist.")
        elif result == -2:
            abort(412, message=f"Resource is already {new_status}.")
        else:
            response = {
                "cust_email" : customer_email,
                "status" : new_status
            }
            return response
