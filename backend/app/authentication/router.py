from fastapi import FastAPI, APIRouter, Form, Depends, Request, Response, HTTPException, status, Cookie
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware import Middleware
from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv
from typing import Annotated
from datetime import datetime, timezone

from app.authentication import service
from ..core.security import application, get_user_from_access_token, encrypt_refresh
from ..core.security_schemas import User
from ..core import config
from sqlalchemy.orm import Session
from app.core.database import get_database


load_dotenv()

def get_session(request: Request):
    return request

router = APIRouter(
    prefix = "/auth",
    tags = ["auth"]
)

roles_dict = {
    1 : "admin",
    2: "employee"
}

@router.get("/sign-in")
async def sign_in(application: Annotated[ConfidentialClientApplication, Depends(application)], request: Annotated[dict, Depends(get_session)], next: str, signup: bool | None=None, role: int | None=None, workspace_id: int | None=None):
    # Protect against url manipulation!
    if not next.startswith("/"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    flow = application.initiate_auth_code_flow(scopes=config.SCOPES, redirect_uri=f"{config.REDIRECT_URI}/auth/success/")
    # print(flow)
    request.session["flow"] = flow
    request.session["next"] = next

    # Ensure that a valid role must be present at signup
    if signup and role:
        if role not in roles_dict:
            print("bad role!")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        request.session["role"] = roles_dict[role]
        request.session["signup"] = signup
        request.session["workspace_id"] = workspace_id
        print("It has been added!")
    elif signup and not role:
        print("Need both!")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    # print(f"\n\n request.session: {request.session}")
    print("This is the redirect response auth_uri: ", flow["auth_uri"])
    return RedirectResponse(flow['auth_uri'])

@router.get("/success/")
async def login_redirect(application: Annotated[ConfidentialClientApplication, Depends(application)], request: Annotated[dict, Depends(get_session)], response: Response, db: Annotated[Session, Depends(get_database)], client_info: str | None=None, code: str | None=None, state: str | None=None, error: str | None=None, error_description: str | None=None):
    if error:
        return RedirectResponse(url=f"{config.FRONTEND_BASE_URL}/error/422")

    if not request.session:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    result = application.acquire_token_by_auth_code_flow(
        auth_code_flow = request.session["flow"], # Remember to delete the session!
        auth_response = {
            "client_info": client_info,
            "code": code,
            "state": state
        }
    )
    url = request.session["next"]
    
    # getting the role from the session
    role = request.session["role"] if "role" in request.session else None

    # getting the role from the session
    workspace_id = request.session["workspace_id"] if "workspace_id" in request.session else None

    # Either create user or check if the user exists
    # Check if the user exists in the db before creating a new user, incase of repeated request
    user = service.check_get_by_oid(result['id_token_claims']['oid'], db)
    if "signup" in request.session and not user:
        user = service.create_user(db=db, details=result["id_token_claims"], refresh=result["refresh_token"], ms_access_token=result["access_token"], role=role, workspace_id=workspace_id)
    request.session.clear()
    response.delete_cookie("session") # This is to remove the cookie from the user's browser

    if user:
        # generates the refresh and access token for the user (refresh will be returned later at the end of this if block, access token is gained in another flow by the user)
        _, refresh_token, _ = service.create_access_refresh(db=db, data={"userId": user.user_id, "role": user.role})
        redirect_response = RedirectResponse(f"{config.FRONTEND_BASE_URL}{url}") # This will redirect the user back to the page that they were on originally
        redirect_response.set_cookie(key="dte_refresh_token", value=refresh_token.opaque_token, expires=refresh_token.expiry_date, httponly=True, samesite = None)
        # return {"access_token": access_token} # This is now technically irrelevant - optimised flow to save milliseconds would be to remove this entirely
        return redirect_response
    else:
        return RedirectResponse(f"{config.FRONTEND_BASE_URL}/error/403")
    
@router.get("/token/refresh")
async def refresh_access(db: Annotated[Session, Depends(get_database)], response: Response, dte_refresh_token: Annotated[str | None, Cookie()] = None):
    if dte_refresh_token:
        refresh_response = service.refresh_flow(db=db, client_refresh=dte_refresh_token, current_time=datetime.now(timezone.utc))
    else:
        print("user has no refresh token!!!")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no Refresh Token!"
        )
    # print(refresh_response)
    if "access_token" and "refresh_token" in refresh_response:
        print("This has an access token and refresh_token")
        response.set_cookie(key="dte_refresh_token", value=refresh_response["refresh_token"].opaque_token, expires=refresh_response["refresh_token"].expiry_date, httponly=True, samesite = None)
        return {
            "access_token" : refresh_response["access_token"]
        }
    elif "access_token" in refresh_response:
        print("Request within 30 seconds!")
        return {
            "access_token": refresh_response["access_token"]
        }
    else:
        # CREATE SESSION KILL CHAIN
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@router.post("/logout")
async def logout(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], response: Response, dte_refresh_token: Annotated[str | None, Cookie()] = None):
    if not dte_refresh_token:
        return # There was no refresh token to remove
    response.delete_cookie("dte_refresh_token")
    return {"details": "refresh token removed"}

@router.get("/test")
async def test_repo(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):
    print(current_user.user_id)
    print(current_user.role)
    user = service.test_route(current_user.user_id, db=db)
    pending_user = service.get_pending_by_email(db, user.email)

    pending = True
    if pending_user is None or pending_user.type == "invite":
        pending = False
    
    if user:
        return {
            "user": user,
            "pending": pending
        }
    else:
        return {
            "message": "no user",
            "pending": pending
        }
