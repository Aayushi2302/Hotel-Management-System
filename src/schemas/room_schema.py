from pydantic import BaseModel, Field
from config.regex_pattern import RegexPattern

class RoomSchemaResponse(BaseModel):
    room_id : str
    room_no : int = Field(gt=0)
    floor_no : int = Field(gt=0)
    charges : float
    status : str

class AvailableRoomSchemaResponse(BaseModel):
    room_id : str
    room_no : int = Field(gt=0)
    floor_no : int = Field(gt=0)
    charges : float

class RoomSchemaArguments(BaseModel):
    room_no : int = Field(gt=0)
    floor_no : int = Field(gt=0)
    charges : float

class RoomSchemaUpdate(BaseModel):
    room_no : int
    floor_no : int
    status : str = Field(pattern=RegexPattern.ROOM_STATUS)
