import shortuuid
from sqlite3 import Error
from fastapi import APIRouter, HTTPException, Query
from starlette import status

from config.app_config import AppConfig
from schemas.room_schema import RoomSchemaArguments, RoomSchemaResponse, RoomSchemaUpdate, AvailableRoomSchemaResponse
from controllers.room_controller import RoomController
from resources.auth_resource import token_dependency
from utils.rbac import role_based_access
from utils.role_mapping import RoleMapping

router = APIRouter(
    tags=["room"]
)

@router.post("/room", status_code=status.HTTP_201_CREATED, response_model=RoomSchemaResponse)
@role_based_access((RoleMapping["ADMIN"], ))
def create_room(token: token_dependency, room_data: RoomSchemaArguments):
    try:
        print(room_data)
        room_id = "ROOM" + shortuuid.ShortUUID().random(5)
        room_no = room_data.room_no
        floor_no = room_data.floor_no
        charges = room_data.charges

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

@router.get("/room", status_code=status.HTTP_200_OK, response_model=list[RoomSchemaResponse])
@role_based_access((RoleMapping["ADMIN"], RoleMapping["STAFF"], RoleMapping["RECEPTION"]))
def get_all_rooms(token: token_dependency):
    try:
        room_controller_obj = RoomController()
        data = room_controller_obj.get_room_data()
        return data
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")

@router.patch("/room", status_code=status.HTTP_200_OK, response_model=RoomSchemaUpdate)
@role_based_access((RoleMapping["ADMIN"], ))
def update_room_status(token: token_dependency, room_data: RoomSchemaUpdate):
    try:
        room_no = room_data.room_no
        floor_no = room_data.floor_no
        new_status = room_data.status
        room_controller_obj = RoomController()
        result = room_controller_obj.update_room_status(room_no, floor_no, new_status)
        if result == -1:
            raise HTTPException(404, detail="Resource which you are looking for does not exist.")
        elif result == -2:
            raise HTTPException(403, detail=f"Resource is already {new_status}.")
        else:
            response = {
                "room_no" : room_no,
                "floor_no" : floor_no,
                "status" : new_status
            }
            return response
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")


@router.get("/room/available", status_code=status.HTTP_200_OK, response_model=list[AvailableRoomSchemaResponse])
@role_based_access((RoleMapping["ADMIN"], RoleMapping["STAFF"], RoleMapping["RECEPTION"]))
def get_all_available_rooms(token: token_dependency):
    try:
        room_controller_obj = RoomController()
        data = room_controller_obj.get_available_rooms()
        return data
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")


@router.get("/room/preferred", status_code=status.HTTP_200_OK, response_model=list[AvailableRoomSchemaResponse])
@role_based_access((RoleMapping["ADMIN"], RoleMapping["STAFF"], RoleMapping["RECEPTION"]))
def get_preferred_price_room(token: token_dependency, price: int = Query(gt=2000)):
    try:
        room_controller_obj = RoomController()
        data = room_controller_obj.get_preferred_room(price)
        return data
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")
