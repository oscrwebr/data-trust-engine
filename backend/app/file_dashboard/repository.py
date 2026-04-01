from sqlalchemy.orm import Session
from app.ingestion.models import Folder, IngestionFile

# Get root folders (parent_graph_id is None)
def get_root_folders(db: Session):
    return db.query(Folder).filter(Folder.parent_graph_id == None).all()

# Get subfolders of a folder
def get_subfolders(db: Session, parent_graph_id: str):
    return db.query(Folder).filter(Folder.parent_graph_id == parent_graph_id).all()

# Get files in a folder
def get_files(db: Session, parent_graph_id: str):
    return db.query(IngestionFile).filter(IngestionFile.parent_graph_id == parent_graph_id).all()