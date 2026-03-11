from fastapi import APIRouter, Depends
from typing import Annotated
from msal import ConfidentialClientApplication
import os
from sqlalchemy.orm import Session

from ..core.security import application, get_user_from_access_token
from ..core.security_schemas import User
from ..core.database import get_database
from ..core.config import SCOPES
from . import service
from ..authentication import service as auth_service



router = APIRouter(
    prefix = "/ingest",
    tags = ["ingest"]
)

@router.get("/test-graph")
async def test_ingest(application: Annotated[ConfidentialClientApplication, Depends(application)], user: Annotated[User, Depends(get_user_from_access_token)], db: Annotated[Session, Depends(get_database)]):
    print(user)
    access_token = service.get_user_access(application=application, user=user, db=db)
    return {"access_token": access_token} if access_token else {"message": None}
    