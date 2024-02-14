import shortuuid
from fastapi import APIRouter, HTTPException, Path
from starlette import status

from config.regex_pattern import RegexPattern
from controllers.room_controller import RoomController
from schemas.reservation_schema import ReservationCheckInSchemaArguments, ReservationCheckInSchemaResponse, \
                                      ReservationCheckOutSchemaArguments, ReservationCheckOutSchemaResponse
from utils.common_helper import CommonHelper
from resources.auth_resource import token_dependency
from utils.rbac import role_based_access
from utils.role_mapping import RoleMapping

router = APIRouter(
    tags=["reservation"]
)

@router.post("/reservation/check-in/{room_id}",
                status_code=status.HTTP_201_CREATED, response_model=ReservationCheckInSchemaResponse)
@role_based_access((RoleMapping["STAFF"], RoleMapping["RECEPTION"]))
def check_in_room(token: token_dependency, cust_data: ReservationCheckInSchemaArguments, room_id: str = Path(pattern=RegexPattern.ROOM_ID_REGEX)):
    print(cust_data)
    reservation_id = "RESR" + shortuuid.ShortUUID().random(5)
    cust_checkin_date_time = CommonHelper.get_current_date_and_time()
    cust_email = cust_data.cust_email
    cust_checkout_date_time = (cust_data.cust_checkout_date, cust_data.cust_checkout_time)
    cust_data = (cust_email, cust_checkin_date_time, cust_checkout_date_time)
    room_controller_obj = RoomController()
    result = room_controller_obj.save_room_details_for_check_in(reservation_id, room_id, cust_data)
    if result == -1:
        raise HTTPException(404, detail="Customer not found.")
    elif result == -2:
        raise HTTPException(404, detail="Room not available.")
    elif result == 0:
       raise HTTPException(500, detail="Internal server error.")
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

@router.put("/reservation/check-out/{room_id}",
                status_code=status.HTTP_201_CREATED, response_model=ReservationCheckOutSchemaResponse)
@role_based_access((RoleMapping["STAFF"], RoleMapping["RECEPTION"]))
def check_out_room(token: token_dependency, cust_data: ReservationCheckOutSchemaArguments, room_id: str = Path(pattern=RegexPattern.ROOM_ID_REGEX)):
    cust_email = cust_data.cust_email
    cust_checkout_date_time = CommonHelper.get_current_date_and_time()
    room_controller_obj = RoomController()
    result = room_controller_obj.save_room_details_for_check_out(cust_email, room_id, cust_checkout_date_time)
    if result == -1:
        raise HTTPException(404, detail="Reservation resource not found for customer.")
    else:
        response = {
            "cust_email" : cust_email,
            "cust_checkout_date" : cust_checkout_date_time[0],
            "cust_checkout_time" : cust_checkout_date_time[1],
            "charges" : result
        }
        return response
