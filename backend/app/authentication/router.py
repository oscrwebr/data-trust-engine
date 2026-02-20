from fastapi import FastAPI, APIRouter, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
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
async def sign_in():
    result = application.initiate_auth_code_flow(scopes=os.environ.get("SCOPES").split(), response_mode='form_post')
    print(result)
    return RedirectResponse(result['auth_uri'])

@router.post("/success/")
async def login_redirect(client_info: Annotated[str, Form()], code: Annotated[str, Form()], state: Annotated[str, Form()]):

    # application.acquire_token_by_auth_code_flow()
    return {
        "client_info": client_info,
        "code": code,
        "state": state
    }

# oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # @router.get("/test")
# # async def test(token: Annotated[str, Depends(oauth_scheme)]):
# #     return {
# #         "token": token
# #     }
