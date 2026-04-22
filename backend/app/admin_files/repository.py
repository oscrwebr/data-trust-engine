from sqlalchemy.orm import Session
from sqlalchemy import func

from app.scanning.models import Scan, ScanFile
from app.ingestion.models import IngestionFile


def get_last_scanned_for_files(db: Session, file_ids: list[int]):
    results = (
        db.query(
            IngestionFile.ingestion_file_id.label("file_id"),
            IngestionFile.graph_id.label("graph_file_id"),
            func.max(Scan.finished_at).label("last_scanned")
        )
        .outerjoin(ScanFile, ScanFile.file_id == IngestionFile.ingestion_file_id)
        .outerjoin(Scan, Scan.scan_id == ScanFile.scan_id)
        .filter(IngestionFile.ingestion_file_id.in_(file_ids))
        .group_by(IngestionFile.ingestion_file_id, IngestionFile.graph_id)
        .all()
    )

    return [
        {
            "file_id": r.file_id,
            "graph_file_id": r.graph_file_id,
            "last_scanned": r.last_scanned.isoformat() if r.last_scanned else None
        }
        for r in results
    ]