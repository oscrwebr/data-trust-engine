from sqlalchemy.orm import Session
from app.ingestion.models import Folder, IngestionFile, UserFolders, UserFiles


# -------------------------
# ROOT FOLDERS (USER SCOPED)
# -------------------------
def get_root_folders(db: Session, user_id: int):
    if not user_id:
        return []

    return (
        db.query(Folder)
        .join(UserFolders, UserFolders.folder_id == Folder.folder_id)
        .filter(
            UserFolders.user_id == user_id,
            Folder.parent_graph_id.is_(None)
        )
        .distinct()
        .all()
    )


# -------------------------
# SUBFOLDERS (USER SCOPED)
# -------------------------
def get_subfolders(db: Session, user_id: int, parent_graph_id: str):
    if not user_id:
        return []

    return (
        db.query(Folder)
        .join(UserFolders, UserFolders.folder_id == Folder.folder_id)
        .filter(
            UserFolders.user_id == user_id,
            Folder.parent_graph_id == parent_graph_id
        )
        .distinct()
        .all()
    )


# -------------------------
# FILES (USER SCOPED)
# -------------------------
def get_files(db: Session, user_id: int, parent_graph_id: str):
    if not user_id:
        return []

    return (
        db.query(IngestionFile)
        .join(UserFiles, UserFiles.file_id == IngestionFile.ingestion_file_id)
        .filter(
            UserFiles.user_id == user_id,
            IngestionFile.parent_graph_id == parent_graph_id
        )
        .distinct()
        .all()
    )