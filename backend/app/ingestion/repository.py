from sqlalchemy.orm import Session
from sqlalchemy import insert
from .models import Folder, IngestionFile, UserFolders, UserFiles


def create_folders_files(folders: dict, files: dict, db: Session) -> int:
    folders = list(folders.values())
    files = list(files.values())
    status = {"status": 200}

    try:
        folder_exec = db.execute(insert(Folder).returning(Folder.folder_id, Folder.graph_id), folders)
        file_exec = db.execute(insert(IngestionFile).returning(IngestionFile.ingestion_file_id, IngestionFile.graph_id), files)
        db.commit()
        status["data"] = {
            "folder": folder_exec.all(),
            "file": file_exec.all()
        }
    except Exception as e:
        status["description"] = f"An error ocurred: {type(e).__name__} - {e}"
        status["status"] = 403
    
    return status

def insert_user_folders(user_folders: list, db: Session):
    status = {
        "status": 200
    }
    try:
        db.execute(insert(UserFolders), user_folders)
        db.commit()
    except Exception as e:
        status["description"] = f"An error ocurred: {type(e).__name__} - {e}"
        status["status"] = 403
    return status

def insert_user_files(user_files: list, db: Session):
    status = {
        "status": 200
    }
    try:
        db.execute(insert(UserFiles), user_files)
        db.commit()
    except Exception as e:
        status["description"] = f"An error ocurred: {type(e).__name__} - {e}"
        status["status"] = 403
    return status

def get_drive_id_by_graph_id(graph_id: str, db: Session):
    return db.query(IngestionFile.drive_id).where(IngestionFile.graph_id == graph_id).first()


def get_ingestion_file_by_graph_id(graph_id: str, db: Session):
    return db.query(IngestionFile).filter(IngestionFile.graph_id == graph_id).first()