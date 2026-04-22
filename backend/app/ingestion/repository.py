from sqlalchemy.orm import Session
from sqlalchemy import insert, update, delete
from .models import Folder, IngestionFile, UserFolders, UserFiles
from datetime import datetime


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


def create_ingestion_file(db: Session, graph_id: str, name: str, extension: str, last_modified: datetime, web_url: str, drive_id: str,hash: str | None = None,hash_type: str | None = None,last_scanned: datetime | None = None, parent_graph_id: str | None = None):
    ingestion_file = IngestionFile(
        graph_id=graph_id,
        name=name,
        extension=extension,
        hash=hash,
        hash_type=hash_type,
        last_scanned=last_scanned,
        last_modified=last_modified,
        web_url=web_url,
        parent_graph_id=parent_graph_id,
        drive_id=drive_id
    )

    db.add(ingestion_file)
    db.commit()
    db.refresh(ingestion_file)

    return ingestion_file


def get_all_files(db: Session):
    return db.query(IngestionFile).all()

def get_user_files(db: Session, user_id: int):
    results = (
        db.query(UserFiles, IngestionFile)
        .outerjoin(
            IngestionFile,
            IngestionFile.ingestion_file_id == UserFiles.file_id
        )
        .filter(UserFiles.user_id == user_id)
        .all()
    )

    files = []
    for user_file, file in results:
        files.append({
            "file": file
        })

    return files

def update_ingestion_file_after_name_change(db: Session, graph_id: str, name: str, web_url: str, updated_modified: datetime):
    update_statement = update(IngestionFile).where(IngestionFile.graph_id == graph_id).values({
        IngestionFile.name: name,
        IngestionFile.web_url: web_url,
        IngestionFile.last_modified: updated_modified 
    })
    db.execute(update_statement)
    db.commit()

def delete_ingestion_file(db: Session, graph_id: str) -> None:
    delete_statement = delete(IngestionFile).where(IngestionFile.graph_id == graph_id)
    db.execute(delete_statement)
    db.commit()