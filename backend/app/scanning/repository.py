from sqlalchemy.orm import Session
from app.scanning.models import File

def create_file(db: Session, extension: str, file_hash: str):
    file = File(file_extension=extension, hash=file_hash)
    db.add(file)
    db.commit()
    db.refresh(file)
    return file

def get_file_by_id(db: Session, file_id: int):
    return db.query(File).filter(File.file_id == file_id).first()

def get_all_files(db: Session):
    return db.query(File).all()