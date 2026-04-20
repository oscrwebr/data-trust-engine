from sqlalchemy.orm import Session
from sqlalchemy import func
import random
from datetime import datetime
from app.core.database import SessionLocal
from app.ingestion.models import IngestionFile
from app.scanning.models import ScanFile, Scan


def get_admin_files(search, sensitivity, sort, page, page_size):
    db: Session = SessionLocal()

    query = (
        db.query(
            IngestionFile.ingestion_file_id.label("file_id"),
            IngestionFile.name.label("name"),
            func.max(Scan.started_at).label("last_scanned")
        )
        .outerjoin(ScanFile, ScanFile.file_id == IngestionFile.ingestion_file_id)
        .outerjoin(Scan, Scan.scan_id == ScanFile.scan_id)
        .group_by(IngestionFile.ingestion_file_id)
    )

    if search:
        query = query.filter(IngestionFile.name.ilike(f"%{search}%"))

    rows = query.all()

    processed = []

    for r in rows:
        sensitivity, detections = generate_sensitivity(r.last_scanned)

        processed.append({
            "file_id": r.file_id,
            "name": r.name,
            "last_scanned": r.last_scanned,
            "sensitivity": sensitivity,
            "detections": detections
        })

    # safe sorting (handles NULL datetime)
    from datetime import datetime

    def norm(x):
        return x["last_scanned"] or datetime.min

    processed.sort(
        key=lambda x: x["last_scanned"] or datetime.min,
        reverse=(sort == "desc")
    )

    total = len(processed)

    start = (page - 1) * page_size
    end = start + page_size

    return processed[start:end], total

def generate_sensitivity(last_scanned):
    """
    If file has been scanned, simulate detections (0-50)
    and return sensitivity level.
    """

    if not last_scanned:
        return None, 0

    detections = random.randint(0, 50)

    if detections >= 30:
        return "critical", detections
    elif detections >= 15:
        return "high", detections
    elif detections >= 5:
        return "medium", detections
    elif detections > 0:
        return "low", detections
    else:
        return "safe", detections