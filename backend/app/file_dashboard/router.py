from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.file_dashboard import service

router = APIRouter(prefix="/files", tags=["Files"])


# -------------------------
# GET Folders
# -------------------------
@router.get("/folders")
def get_folders(db: Session = Depends(get_database)):
    return service.get_folders(db)


# -------------------------
# GET Files
# -------------------------
@router.get("/all")
def get_files(db: Session = Depends(get_database)):
    return service.get_files(db)