import shortuuid

from flask import request
from config.app_config import AppConfig
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from controllers.room_controller import RoomController
from schemas.room_schema import RoomSchema, RoomSchemaUpdate
from utils.rbac import role_based_access
from utils.role_mapping import RoleMapping
from utils.error_handler import error_handler

blp = Blueprint("room", __name__, description = "Room operations")

@blp.route("/room")
class RoomOperations(MethodView):

    @error_handler
    @role_based_access((RoleMapping.ADMIN_ROLE, ))
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(RoomSchema)
    @blp.response(201, RoomSchema)
    def post(self, room_data):
        room_id = "ROOM" + shortuuid.ShortUUID().random(5)
        room_no = room_data["room_no"]
        floor_no = room_data["floor_no"]
        charges = room_data["charges"]

        room_data = (room_id, room_no, floor_no, charges)
        room_controller_obj = RoomController()
        result = room_controller_obj.save_room_details(room_data)

        if not result:
            abort(500, message="An error occurred while creating employee.")
        
        response = {
            "room_id" : room_id,
            "room_no" : room_no,
            "floor_no" : floor_no,
            "charges" : charges,
            "status" : AppConfig.ROOM_STATUS_AVAILABLE
        }

        return response

    @error_handler
    @role_based_access((RoleMapping.ADMIN_ROLE, RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.response(200, RoomSchema(many=True))
    def get(self):
        room_controller_obj = RoomController()
        data = room_controller_obj.get_room_data()
        if not data:
            abort(404, message="Resource not found.")
        return data

    @error_handler
    @role_based_access((RoleMapping.ADMIN_ROLE, ))
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(RoomSchemaUpdate)
    @blp.response(200, RoomSchemaUpdate)
    def patch(self, room_data):
        room_no = room_data["room_no"]
        floor_no = room_data["floor_no"]
        new_status = room_data["status"]
        room_controller_obj = RoomController()
        result = room_controller_obj.update_room_status(room_no, floor_no, new_status)
        if result == -1:
            abort(404, message="Resource which you are looking for does not exist.")
        elif result == -2:
            abort(412, message=f"Resource is already {new_status}.")
        else:
            response = {
                "room_no" : room_no,
                "floor_no" : floor_no,
                "status" : new_status
            }
            return response

@blp.route("/room/available")
class RoomAvailable(MethodView):
    @error_handler
    @role_based_access((RoleMapping.ADMIN_ROLE, RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.response(200, RoomSchema(many=True))
    def get(self):
        room_controller_obj = RoomController()
        data = room_controller_obj.get_available_rooms()
        if not data:
            abort(404, message="Resource not found.")
        return data

@blp.route("/room/preferred")
class PreferredRoom(MethodView):
    @error_handler
    @role_based_access((RoleMapping.ADMIN_ROLE, RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.response(200, RoomSchema(many=True))
    def get(self):
        try:
            price = float(request.args.get("price"))
            print(price)
            room_controller_obj = RoomController()
            data = room_controller_obj.get_preferred_room(price)
            if not data:
                abort(404, message="Resource not found.")
            return data
        except Exception as e:
            print(e)
            abort(400, message="Price should be integer or float.")
        