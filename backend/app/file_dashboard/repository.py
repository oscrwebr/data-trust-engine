from sqlalchemy.orm import Session
from app.ingestion.models import Folder, IngestionFile


# -------------------------
# Folders
# -------------------------
def get_all_folders(db: Session):
    return db.query(Folder).all()


# -------------------------
# Files
# -------------------------
def get_all_files(db: Session):
    return db.query(IngestionFile).all()