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

def insert_user_folders(folders: list, permissions_dict: dict, user_id: int, db: Session):
    status = {}
    # going through the folders in the list and adding their id to a list of folder_id
    print(f"\n\npermissions_dict:\n{permissions_dict}\n\n")

    try:
        db.execute(insert(UserFolders), folders)
        db.commit()
    except Exception as e:
        status["description"] = f"An error ocurred: {type(e).__name__} - {e}"
        status["status"] = 403
    return status