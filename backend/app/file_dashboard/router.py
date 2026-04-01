from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.file_dashboard import service

router = APIRouter(prefix="/files", tags=["Files"])

@router.get("/folders")
def get_root_folders(db: Session = Depends(get_database)):
    return service.get_root_folders(db, )

@router.get("/folders/{parent_graph_id}")
def get_subfolders(parent_graph_id: str, db: Session = Depends(get_database)):
    return service.get_subfolders(db, parent_graph_id)

@router.get("/{parent_graph_id}")
def get_files(parent_graph_id: str, db: Session = Depends(get_database)):
    return service.get_files_in_folder(db, parent_graph_id)