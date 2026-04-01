from sqlalchemy.orm import Session
from app.file_dashboard import repository


# -------------------------
# Helpers
# -------------------------
def map_folder(folder):
    return {
        "folder_id": folder.folder_id,
        "name": folder.name,
        "parent_graph_id": folder.parent_graph_id,
        "graph_id": folder.graph_id,
        "drive_id": folder.drive_id,
    }


def map_file(file):
    return {
        "file_id": file.ingestion_file_id,
        "file_name": file.name,
        "extension": file.extension,
        "parent_graph_id": file.parent_graph_id,
        "graph_id": file.graph_id,
        "last_modified": file.last_modified,
    }


# -------------------------
# Services
# -------------------------
def get_folders(db: Session):
    folders = repository.get_all_folders(db)

    # map graph_id → folder_id
    graph_to_id = {f.graph_id: f.folder_id for f in folders}

    result = []
    for f in folders:
        result.append({
            "folder_id": f.folder_id,
            "name": f.name,
            "parent_graph_id": graph_to_id.get(f.parent_graph_id),
        })

    return result
    
    
def get_folders(db: Session):
    folders = repository.get_all_folders(db)

    # map graph_id → folder_id
    graph_to_id = {f.graph_id: f.folder_id for f in folders}

    result = []
    for f in folders:
        result.append({
            "folder_id": f.folder_id,
            "name": f.name,
            "parent_graph_id": graph_to_id.get(f.parent_graph_id),
        })

    return result


def get_files(db: Session):
    files = repository.get_all_files(db)
    folders = repository.get_all_folders(db)

    graph_to_id = {f.graph_id: f.folder_id for f in folders}

    result = []
    for file in files:
        result.append({
            "file_id": file.ingestion_file_id,
            "file_name": file.name,
            "parent_graph_id": graph_to_id.get(file.parent_graph_id),
        })

    return result