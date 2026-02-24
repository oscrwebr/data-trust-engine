from fastapi import FastAPI, APIRouter, Form, Depends, Request, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware import Middleware
from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv
from typing import Annotated

from app.authentication import service
from ..core.security import create_access_token, get_user_from_access_token
from ..core.security_schemas import User
from sqlalchemy.orm import Session
from app.core.database import get_database

load_dotenv()
# make this singleton!
application = ConfidentialClientApplication(client_id=os.environ.get("CLIENT_ID"), authority=os.environ.get("AUTHORITY"), client_credential=os.environ.get("CLIENT_SECRET"))

router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

@router.get("/sign-in")
async def sign_in(request: Request):
    flow = application.initiate_auth_code_flow(scopes=os.environ.get("SCOPES").split())
    # print(flow)
    request.session["flow"] = flow
    print(request.session)
    return RedirectResponse(flow['auth_uri'])

@router.get("/success/")
async def login_redirect(client_info: str, code: str, state: str, request: Request, db: Annotated[Session, Depends(get_database)]):
    result = application.acquire_token_by_auth_code_flow(
        auth_code_flow = request.session["flow"],
        auth_response = {
            "client_info": client_info,
            "code": code,
            "state": state
        }
    )
    # Flow to find out if the user exists or not
    user = service.check_exists(result['id_token_claims']['oid'], db)

    # print(result)
    if user:
        return create_access_token(data= {
            "userId": user.user_id
        })
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

@router.get("/test")
async def test_repo(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):
    print(current_user.user_id)
    # service.check_exists("Hello World!", db=db)
    return {
        "message": "This has gotten to the return at least lol!"
    }
