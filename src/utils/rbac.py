from functools import wraps
from fastapi import HTTPException
from jose import jwt, JWTError
from starlette import status

from resources.auth_resource import SECRET_KEY, ALGORITHM

def role_based_access(allowed_roles: tuple):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                token = kwargs["token"]
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                role = payload["role"]
                if role in allowed_roles:
                    return func(*args, **kwargs)
                else:
                    raise HTTPException(401, detail="You don't have permission to access this functionality.")
            except JWTError:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Could not validate user.')
        return inner
    return wrapper
