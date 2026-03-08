from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.core.database import get_database
from sqlalchemy.orm import Session
from app.workspaces.schema import CreateWorkspace
from app.workspaces.service import workspace
from fastapi.responses import RedirectResponse
from typing import Annotated
from ..core.security_schemas import User
from ..core.security import create_access_token, get_user_from_access_token

router = APIRouter(prefix="/workspace", tags=["workspace"])

@router.post("/create-workspace")
async def create_workspace(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], name: str = Form(None),
    image: UploadFile = File(None)):

    # Checking if name is null
    if not name or name.strip().lower() == "null":
        return "name"
    
    #Checking if image is null
    if image is None:
        return "image"

    image_bytes = await image.read()
    result = workspace(current_user.user_id, name, image_bytes, db)

    return result