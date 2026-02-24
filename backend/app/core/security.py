import jwt, datetime, os
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from .security_schemas import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="success")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=30)
    print(to_encode)
    signed_access_jwt = jwt.encode(payload=to_encode, key=ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
    return Token(access_token=signed_access_jwt, token_type="Bearer")

def get_user_from_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    token_credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "User not authorised",
        headers = { # This header is returned as part of spec
            "WWW-Authenticate": "Bearer"
        })
    try: # automatically checks for time validity with jwt.decode if 'exp' is present (it is)
        payload = jwt.decode(jwt=token, key=ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
        user_id = payload.get("userId")
        if user_id is None:
            raise token_credentials_exception
        user = User(user_id = user_id)
    except InvalidTokenError:
        raise token_credentials_exception
    return user        
    