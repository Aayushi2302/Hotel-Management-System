import shortuuid

from flask import request
from config.app_config import AppConfig
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from controllers.room_controller import RoomController
from schemas.reservation_schema import ReservationCheckInSchema, ReservationCheckOutSchema
from utils.rbac import role_based_access
from utils.role_mapping import RoleMapping
from utils.error_handler import error_handler
from utils.common_helper import CommonHelper

blp = Blueprint("reservation", __name__, description = "Reservation operations")

@blp.route("/reservation/check-in/<string:room_id>")
class ReservationCheckIn(MethodView):
    @error_handler
    @role_based_access((RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(ReservationCheckInSchema)
    @blp.response(201, ReservationCheckInSchema)
    def post(self, cust_data, room_id):
        reservation_id = "RESR" + shortuuid.ShortUUID().random(5)
        cust_checkin_date_time = CommonHelper.get_current_date_and_time()
        cust_email = cust_data["cust_email"]
        cust_checkout_date_time = (cust_data["cust_checkout_date"], cust_data["cust_checkout_time"])
        cust_data = (cust_email, cust_checkin_date_time, cust_checkout_date_time)
        room_controller_obj = RoomController()
        result = room_controller_obj.save_room_details_for_check_in(reservation_id, room_id, cust_data)
        if result == -1:
            abort(404, message="Customer resource not found.")
        elif result == -2:
            abort(404, message="Room resource not available.")
        elif result == 0:
            abort(500, message="Internal server error.")
        else:
            response = {
                "reservation_id" : reservation_id,
                "cust_email" : cust_email,
                "cust_checkin_date" : cust_checkin_date_time[0],
                "cust_checkin_time" : cust_checkin_date_time[1],
                "cust_checkout_date" : cust_checkout_date_time[0],
                "cust_checkout_time" : cust_checkout_date_time[1]
            }
            return response

@blp.route("/reservation/check-out/<string:room_id>")
class ReservationCheckIn(MethodView):
    @error_handler
    @role_based_access((RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
    @jwt_required()
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(ReservationCheckOutSchema)
    @blp.response(201, ReservationCheckOutSchema)
    def put(self, cust_data, room_id):
        cust_email = cust_data["cust_email"]
        cust_checkout_date_time = CommonHelper.get_current_date_and_time()
        room_controller_obj = RoomController()
        result = room_controller_obj.save_room_details_for_check_out(cust_email, room_id, cust_checkout_date_time)
        if result == -1:
            abort(404, message="Reservation resource not found for customer.")
        else:
            response = {
                "cust_email" : cust_email,
                "cust_checkout_date" : cust_checkout_date_time[0],
                "cust_checkout_time" : cust_checkout_date_time[1],
                "charges" : result
            }
            return response