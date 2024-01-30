from sqlite3 import Error
from fastapi import APIRouter, HTTPException
from starlette import status

from controllers.auth_controller import AuthController
from schemas.auth_schema import LoginSchemaArguments

router = APIRouter()

async def create_access_token():
    pass

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(credentials: LoginSchemaArguments):
    try:
        auth_controller_obj = AuthController()
        role = auth_controller_obj.authenticate_user(credentials.username, credentials.password).upper()
        if role:
            return {"message" : "User login successfully"}
        else:
            raise HTTPException(401, detail="Invalid login.")
    except Error:
        raise HTTPException(500, detail="Internal server error.")
