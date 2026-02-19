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

def get_file_by_graph_id(db: Session, graph_file_id: str):
    return db.query(File).filter(File.graph_file_id == graph_file_id).first()

def set_file_hash(db: Session, file: File, new_hash: str):
    file.hash = new_hash
    db.commit()
    db.refresh(file)




