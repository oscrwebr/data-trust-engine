from sqlalchemy.orm import Session
from sqlalchemy import insert
from .models import Folder, IngestionFile


def create_folders_files(folders: dict, files: dict, db: Session) -> int:
    folders = list(folders.values())
    files = list(files.values())
    status = {"status": 200}

    try:
        db.execute(insert(Folder), folders)
        db.execute(insert(IngestionFile), files)
        db.commit()
    except Exception as e:
        status["description"] = f"An error ocurred: {type(e).__name__} - {e}"
        status["status"] = 403
        
    return status