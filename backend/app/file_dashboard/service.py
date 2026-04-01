from sqlalchemy.orm import Session
from app.file_dashboard import repository

def get_root_folders(db: Session):
    return repository.get_root_folders(db)

def get_subfolders(db: Session, parent_graph_id: str):
    return repository.get_subfolders(db, parent_graph_id)

def get_files_in_folder(db: Session, parent_graph_id: str):
    return repository.get_files(db, parent_graph_id)