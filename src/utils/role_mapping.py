import os
from dotenv import load_dotenv

load_dotenv()

class RoleMapping:
    ADMIN_ROLE = os.getenv('ADMIN')
    STAFF_ROLE = os.getenv('STAFF')
    RECEPTION_ROLE = os.getenv('RECEPTION')

    @classmethod
    def get_mapped_role(cls, role: str):
        if role == "ADMIN":
            return cls.ADMIN_ROLE
        elif role == "STAFF":
            return cls.STAFF_ROLE
        else:
            return cls.RECEPTION_ROLE
