import shortuuid
from sqlite3 import Error
from fastapi import APIRouter, HTTPException, Query
from starlette import status

from config.app_config import AppConfig
from schemas.room_schema import RoomSchemaArguments, RoomSchemaResponse, RoomSchemaUpdate
from controllers.room_controller import RoomController

router = APIRouter()

@router.post("/room", status_code=status.HTTP_201_CREATED, response_model=RoomSchemaResponse)
async def create_room(room_data: RoomSchemaArguments):
    try:
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
async def get_all_rooms():
    try:
        room_controller_obj = RoomController()
        data = room_controller_obj.get_room_data()
        if not data:
            raise HTTPException(404, detail="Resource not found.")
        return data
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")

@router.patch("/room", status_code=status.HTTP_200_OK, response_model=RoomSchemaUpdate)
async def update_room_status(room_data: RoomSchemaUpdate):
    try:
        room_no = room_data.room_no
        floor_no = room_data.floor_no
        new_status = room_data.status
        room_controller_obj = RoomController()
        result = room_controller_obj.update_room_status(room_no, floor_no, new_status)
        if result == -1:
            raise HTTPException(404, detail="Resource which you are looking for does not exist.")
        elif result == -2:
            raise HTTPException(412, detail=f"Resource is already {new_status}.")
        else:
            response = {
                "room_no" : room_no,
                "floor_no" : floor_no,
                "status" : new_status
            }
            return response
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")


@router.get("/room/available", status_code=status.HTTP_200_OK, response_model=list[RoomSchemaResponse])
async def get_all_available_rooms():
    try:
        room_controller_obj = RoomController()
        data = room_controller_obj.get_available_rooms()
        if not data:
            raise HTTPException(404, detail="Resource not found.")
        return data
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")


@router.get("/room/preferred", status_code=status.HTTP_200_OK, response_model=list[RoomSchemaResponse])
async def get_preferred_price_room(price: int = Query(gt=2000)):
    try:
        room_controller_obj = RoomController()
        data = room_controller_obj.get_preferred_room(price)
        if not data:
            raise HTTPException(404, detail="Resource not found.")
        return data
    except Error:
        raise HTTPException(500, detail="Internal Server Error.")
