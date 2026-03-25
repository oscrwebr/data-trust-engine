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
    prefix = "/ingestion",
    tags = ["ingestion"]
)

@router.get("/test-graph")
async def test_ingest(application: Annotated[ConfidentialClientApplication, Depends(application)], user: Annotated[User, Depends(get_user_from_access_token)], db: Annotated[Session, Depends(get_database)]):
    print(user)
    access_token = auth_service.get_user_access(application=application, user_id=user.user_id, db=db)
    print(f"\n\nThis is the access token {access_token}\n")
    if access_token:
        # get and the set all the files from MS graph
        output = service.get_set_all_graph_files(access_token=access_token, id=user.user_id, db=db)
        return output
    
    return {"message": None}

@router.get("/test-download")
async def test_download(application: Annotated[ConfidentialClientApplication, Depends(application)], user: Annotated[User, Depends(get_user_from_access_token)], db: Annotated[Session, Depends(get_database)]):
    access_token = auth_service.get_user_access(application=application, user_id=user.user_id, db=db)
    download_url = service.get_download_link_by_graph_id(graph_id="1C3872D08681F6C4!5784", access_token=access_token)
    return {
        "download_url": download_url
    }
    