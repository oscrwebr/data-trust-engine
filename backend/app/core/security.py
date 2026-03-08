import jwt, os, hashlib, secrets
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from functools import lru_cache
from .security_schemas import *
from datetime import datetime, timezone, timedelta
from msal import ConfidentialClientApplication
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="success")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
ALGORITHM = os.getenv("ALGORITHM")

@lru_cache
def application() -> ConfidentialClientApplication:
    return ConfidentialClientApplication(client_id=os.environ.get("CLIENT_ID"), authority=os.environ.get("AUTHORITY"), client_credential=os.environ.get("CLIENT_SECRET"))

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=15)
    signed_access_jwt = jwt.encode(payload=to_encode, key=ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
    return AccessToken(access_token=signed_access_jwt, token_type="Bearer")

def create_refresh_token():
    opaque_token = secrets.token_urlsafe(32)
    hashed_ot = hashlib.sha256(opaque_token.encode()).hexdigest()
    expiry_date = datetime.now(timezone.utc) + timedelta(days=7)
    return RefreshToken(opaque_token=opaque_token, hashed_ot=hashed_ot, expiry_date=expiry_date)

def hash_user_refresh_token(refresh_token: str):
    # print(f"\n\nthis is the refresh token: {refresh_token}\n\n")
    hashed_token = hashlib.sha256(refresh_token.encode()).hexdigest()
    return hashed_token

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
    