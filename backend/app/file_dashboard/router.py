from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.core.security import get_user_from_access_token
from app.file_dashboard import service

router = APIRouter(prefix="/files", tags=["Files"])


# -------------------------
# ROOT
# -------------------------
@router.get("/folders")
def get_root_folders(
    db: Session = Depends(get_database),
    user = Depends(get_user_from_access_token)
):
    return service.get_root_folders(db, user.user_id)


# -------------------------
# SUBFOLDERS
# -------------------------
@router.get("/folders/{parent_graph_id}")
def get_subfolders(
    parent_graph_id: str,
    db: Session = Depends(get_database),
    user = Depends(get_user_from_access_token)
):
    return service.get_subfolders(db, user.user_id, parent_graph_id)


# -------------------------
# FILES
# -------------------------
@router.get("/{parent_graph_id}")
def get_files(
    parent_graph_id: str,
    db: Session = Depends(get_database),
    user = Depends(get_user_from_access_token)
):
    return service.get_files_in_folder(db, user.user_id, parent_graph_id)