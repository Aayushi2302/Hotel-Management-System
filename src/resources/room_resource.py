import shortuuid
from sqlite3 import Error
from fastapi import Body, APIRouter, HTTPException
from starlette import status

from config.app_config import AppConfig
from controllers.room_controller import RoomController

router = APIRouter()

@router.post("/room", status_code=status.HTTP_201_CREATED)
async def create_room(room_data=Body()):
    try:
        room_id = "ROOM" + shortuuid.ShortUUID().random(5)
        room_no = room_data["room_no"]
        floor_no = room_data["floor_no"]
        charges = room_data["charges"]

        room_data = (room_id, room_no, floor_no, charges)
        room_controller_obj = RoomController()
        result = room_controller_obj.save_room_details(room_data)

        if not result:
            raise HTTPException(500, detail="An error occurred while creating employee.")
        
        response = {
            "room_id" : room_id,
            "room_no" : room_no,
            "floor_no" : floor_no,
            "charges" : charges,
            "status" : AppConfig.ROOM_STATUS_AVAILABLE
        }

        return response
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")

@router.get("/room", status_code=status.HTTP_200_OK)
def get_all_rooms():
    try:
        room_controller_obj = RoomController()
        data = room_controller_obj.get_room_data()
        if not data:
            raise HTTPException(404, detail="Resource not found.")
        return data
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")

#     @error_handler
#     @role_based_access((RoleMapping.ADMIN_ROLE, ))
#     @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
#     @blp.arguments(RoomSchemaUpdate)
#     @blp.response(200, RoomSchemaUpdate)
#     def patch(self, room_data):
#         room_no = room_data["room_no"]
#         floor_no = room_data["floor_no"]
#         new_status = room_data["status"]
#         room_controller_obj = RoomController()
#         result = room_controller_obj.update_room_status(room_no, floor_no, new_status)
#         if result == -1:
#             abort(404, message="Resource which you are looking for does not exist.")
#         elif result == -2:
#             abort(412, message=f"Resource is already {new_status}.")
#         else:
#             response = {
#                 "room_no" : room_no,
#                 "floor_no" : floor_no,
#                 "status" : new_status
#             }
#             return response

# @blp.route("/room/available")
# class RoomAvailable(MethodView):
#     @error_handler
#     @role_based_access((RoleMapping.ADMIN_ROLE, RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
#     @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
#     @blp.response(200, RoomSchema(many=True))
#     def get(self):
#         room_controller_obj = RoomController()
#         data = room_controller_obj.get_available_rooms()
#         if not data:
#             abort(404, message="Resource not found.")
#         return data

# @blp.route("/room/preferred")
# class PreferredRoom(MethodView):
#     @error_handler
#     @role_based_access((RoleMapping.ADMIN_ROLE, RoleMapping.STAFF_ROLE, RoleMapping.RECEPTION_ROLE))
#     @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
#     @blp.response(200, RoomSchema(many=True))
#     def get(self):
#         try:
#             price = float(request.args.get("price"))
#             print(price)
#             room_controller_obj = RoomController()
#             data = room_controller_obj.get_preferred_room(price)
#             if not data:
#                 abort(404, message="Resource not found.")
#             return data
#         except Exception as e:
#             print(e)
#             abort(400, message="Price should be integer or float.")
        