from sqlalchemy.orm import Session
from app.scanning.models import File, Scan, ScanFile, ScanFileDetection
from datetime import datetime, timezone


def create_scan(db: Session):
    scan = Scan(
        started_at = datetime.now(timezone.utc),
        finished_at = None
    )

    db.add(scan)
    db.commit()
    db.refresh(scan)

    return scan


def create_scan_file(db: Session, scan_id: int, graph_file_id: str):
    scan_file = ScanFile(
        scan_id = scan_id,
        graph_file_id = graph_file_id
    )

    db.add(scan_file)
    db.commit()
    db.refresh(scan_file)

    return scan_file


def create_scan_file_detection(db: Session, scan_file_id: int, sensitivity_subcategory: str, page_number: int):
    scan_file_detection = ScanFileDetection(
        scan_file_id = scan_file_id,
        sensitivity_subcategory = sensitivity_subcategory,
        page_number = page_number
    )

    db.add(scan_file_detection)
    db.commit()
    db.refresh(scan_file_detection)

    return scan_file_detection


def create_file(db: Session, graph_file_id: str, name: str, extension: str, file_hash: str):
    file = File(graph_file_id=graph_file_id, file_name=name, file_extension=extension, hash=file_hash)
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




