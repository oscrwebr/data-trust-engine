from fastapi import FastAPI, APIRouter, Form, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware import Middleware
from msal import ConfidentialClientApplication
import os
from dotenv import load_dotenv
from typing import Annotated

load_dotenv()

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
async def login_redirect(client_info: str, code: str, state: str, request: Request):
    result = application.acquire_token_by_auth_code_flow(
        auth_code_flow = request.session["flow"],
        auth_response = {
            "client_info": client_info,
        "code": code,
        "state": state
        }
    )
    print(result)
    return {
        "message": result
    }

