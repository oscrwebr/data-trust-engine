from fastapi import APIRouter, Depends, Query
from app.core.database import get_database
from sqlalchemy.orm import Session
from app.workspaces.schema import CreateWorkspace
from app.workspaces.service import validate_workspace
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/workspace", tags=["workspace"])

@router.post("/create-workspace")
def create_workspace(workspace: CreateWorkspace, db: Session=Depends(get_database)):

    result = validate_workspace(workspace.name, workspace.image, db)
    
    return result