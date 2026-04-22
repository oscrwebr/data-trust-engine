from sqlalchemy.orm import Session
from sqlalchemy import func
from app.ingestion.models import Folder, IngestionFile, UserFolders, UserFiles


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

def get_files(db: Session, user_id: int, parent_graph_id: str):
    if not user_id:
        return []

    shared_subquery = (
        db.query(
            UserFiles.file_id,
            func.count(UserFiles.user_id).label("user_count")
        )
        .group_by(UserFiles.file_id)
        .subquery()
    )

    results = (
        db.query(IngestionFile, shared_subquery.c.user_count)
        .join(UserFiles, UserFiles.file_id == IngestionFile.ingestion_file_id)
        .join(shared_subquery, shared_subquery.c.file_id == IngestionFile.ingestion_file_id)
        .filter(
            UserFiles.user_id == user_id,
            IngestionFile.parent_graph_id == parent_graph_id
        )
        .distinct()
        .all()
    )

    files = []
    for file, user_count in results:
        file_dict = file.__dict__.copy()
        file_dict["is_shared"] = user_count > 1
        files.append(file_dict)

    return files