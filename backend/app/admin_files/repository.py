# app/admin_files/repository.py

from sqlalchemy.orm import Session
from sqlalchemy import func, desc, asc
from app.ingestion.models import IngestionFile
from app.scanning.models import ScanFile, ScanFileDetection


def get_all_files_admin(
    db: Session,
    search: str = None,
    sensitivity: str = None,
    sort: str = "desc",
    skip: int = 0,
    limit: int = 20
):
    query = db.query(
        IngestionFile,
        func.count(ScanFileDetection.scan_file_detection_id).label("detection_count")
    ).outerjoin(
        ScanFile,
        ScanFile.file_id == IngestionFile.ingestion_file_id
    ).outerjoin(
        ScanFileDetection,
        ScanFileDetection.scan_file_id == ScanFile.scan_file_id
    ).group_by(IngestionFile.ingestion_file_id)

    # 🔍 Search
    if search:
        query = query.filter(IngestionFile.name.ilike(f"%{search}%"))

    # ⚠️ Sensitivity filter
    if sensitivity == "high":
        query = query.having(func.count(ScanFileDetection.scan_file_detection_id) > 0)
    elif sensitivity == "low":
        query = query.having(func.count(ScanFileDetection.scan_file_detection_id) == 0)

    # 📅 Sorting
    if sort == "asc":
        query = query.order_by(asc(IngestionFile.last_scanned))
    else:
        query = query.order_by(desc(IngestionFile.last_scanned))

    total = query.count()

    results = query.offset(skip).limit(limit).all()

    return results, total