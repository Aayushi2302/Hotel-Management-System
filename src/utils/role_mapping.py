import os
from dotenv import load_dotenv

load_dotenv()

RoleMapping = {
    "ADMIN" : os.getenv("ADMIN"),
    "STAFF" : os.getenv("STAFF"),
    "RECEPTION" : os.getenv("RECEPTION")
}
