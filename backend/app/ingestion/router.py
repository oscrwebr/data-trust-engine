from fastapi import APIRouter, Depends, HTTPException, status, Query
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
    access_token = auth_service.get_user_access(application=application, user_id=user.user_id, db=db)
    if access_token:
        # get and the set all the files from MS graph
        output = service.get_set_all_graph_files(access_token=access_token, id=user.user_id, db=db)
        return output
    
    return {"message": None}

@router.patch("/update-file")
async def update_file(application: Annotated[ConfidentialClientApplication, Depends(application)], user: Annotated[User, Depends(get_user_from_access_token)], db: Annotated[Session, Depends(get_database)], graph_id: str, new_name: Annotated[str, Query(max_length=255)]):
    # Ensure that only admins can access this route!
    if user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    print(f"This is the graph_id: {graph_id}")
    print(f"This is the new name: {new_name}")

    return {
        "message": "Updating!"
    }
    

@router.get("/test-download")
async def test_download(application: Annotated[ConfidentialClientApplication, Depends(application)], user: Annotated[User, Depends(get_user_from_access_token)], db: Annotated[Session, Depends(get_database)], graph_id: str):
    download_url = service.get_download_link_by_graph_id(application=application, graph_id=graph_id, db=db)
    return {
        "download_url": download_url
    }
    