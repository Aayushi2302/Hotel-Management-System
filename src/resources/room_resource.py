import shortuuid

from config.app_config import AppConfig
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from controllers.room_controller import RoomController
from schemas.room_schema import RoomSchema
from utils.rbac import role_based_access
from utils.role_mapping import RoleMapping
from utils.error_handler import error_handler

blp = Blueprint("room", __name__, description = "Room operations")

@blp.route("/room")
class RoomOperations(MethodView):

    @error_handler
    @role_based_access(RoleMapping.ADMIN_ROLE)
    @jwt_required()
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

