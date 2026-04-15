# app/admin_files/service.py

from sqlalchemy.orm import Session
from app.admin_files import repository


def get_admin_files(
    db: Session,
    search: str = None,
    sensitivity: str = None,
    sort: str = "desc",
    page: int = 1,
    page_size: int = 20
):
    skip = (page - 1) * page_size

    results, total = repository.get_all_files_admin(
        db, search, sensitivity, sort, skip, page_size
    )

    files = []

    for file, detection_count in results:
        files.append({
            "file_id": file.ingestion_file_id,
            "name": file.name,
            "last_scanned": file.last_scanned,
            "sensitivity": "high" if detection_count > 0 else "low"
        })

    return {
        "data": files,
        "total": total,
        "page": page,
        "page_size": page_size
    }