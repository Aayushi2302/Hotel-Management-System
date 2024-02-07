from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from jose import jwt
import os
from sqlite3 import Error
from starlette import status
from typing import Annotated
import secrets

from controllers.auth_controller import AuthController
from schemas.auth_schema import LoginSchemaArguments
from utils.role_mapping import RoleMapping

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


router = APIRouter(
    tags=["authentication"]
)

load_dotenv()

TOKEN_EXPIRATION_TIME = int(os.getenv("ACCESS_TOKEN_EXPIRATION_TIME_IN_MINUTES"))
SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")
ALGORITHM = os.getenv("TOKEN_ENCRYPTION_ALGORITHM")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/login")
token_dependency = Annotated[dict, Depends(oauth2_bearer)]

security = HTTPBasic()
templates = Jinja2Templates(directory="templates")

def create_access_token(username: str, role: str):
    payload = {"sub" : username, "role" : RoleMapping[role]}
    expires = datetime.utcnow() + timedelta(minutes=15)
    payload["exp"] = expires
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: LoginSchemaArguments):
    try:
        auth_controller_obj = AuthController()
        role = auth_controller_obj.authenticate_user(credentials.username, credentials.password)
        if role:
            role = role.upper()
            token = create_access_token(credentials.username, role)
            return {"access_token": token, "message" : "User login successfully"}
        else:
            raise HTTPException(401, detail="Invalid login.")
    except Error as error:
        raise HTTPException(500, detail="Internal server error.")

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_username = secrets.compare_digest(credentials.username, "Aayushi2302")
    correct_password = secrets.compare_digest(credentials.password, "Aayushi@12345")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.get("/docs", response_class=HTMLResponse)
def get_docs(username: str = Depends(get_current_username)) -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs")

@router.get("/redoc", response_class=HTMLResponse)
def get_redoc(username: str = Depends(get_current_username)) -> HTMLResponse:
    return get_redoc_html(openapi_url="/api/openapi.json", title="redoc")   