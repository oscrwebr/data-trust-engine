from sqlalchemy.orm import Session
from app.file_dashboard import repository


def get_root_folders(db: Session, user_id: int):
    return repository.get_root_folders(db, user_id)


def get_subfolders(db: Session, user_id: int, parent_graph_id: str):
    return repository.get_subfolders(db, user_id, parent_graph_id)


def get_files_in_folder(db: Session, user_id: int, parent_graph_id: str):
    return repository.get_files(db, user_id, parent_graph_id)