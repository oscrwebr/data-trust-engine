from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.scanning.models import File, NamingConvention, Scan, ScanNamingConvention, NamingConventionScanResult, Scan, ScanFile, ScanFileDetection
from app.roles.models import SensitivityCategory, SensitivitySubcategory
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


def get_scan_by_id(db: Session, scan_id: int):
    return db.query(Scan).filter(Scan.scan_id == scan_id).first()


def get_all_scans(db: Session):
    return db.query(Scan).all()


def create_scan_file(db: Session, scan_id: int, file_id: int):
    scan_file = ScanFile(
        scan_id = scan_id,
        file_id = file_id
    )

    db.add(scan_file)
    db.commit()
    db.refresh(scan_file)

    return scan_file


def get_scan_file_by_scan_id_and_file_id(db: Session, scan_id: int, file_id: int):
    return db.query(ScanFile).filter(
        ScanFile.scan_id == scan_id, 
        ScanFile.file_id == file_id
    ).first()


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


def get_scan_file_detections_by_scan_file_id(db: Session, scan_file_id: int):
    return db.query(ScanFileDetection).filter(ScanFileDetection.scan_file_id == scan_file_id).all()


def create_file(db: Session, graph_file_id: str, file_name: str, file_hash: str):
    file = File(graph_file_id=graph_file_id, file_name=file_name, hash=file_hash)
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def get_file_by_id(db: Session, file_id: int):
    return db.query(File).filter(File.file_id == file_id).first()


def get_all_files(db: Session):
    return db.query(File).all()


def get_latest_scan_detection_summary(db: Session, file_id: int):
    latest_scan_file = (
        db.query(ScanFile.scan_file_id)
        .join(Scan, Scan.scan_id == ScanFile.scan_id)
        .filter(ScanFile.file_id == file_id)
        .order_by(Scan.finished_at.desc())
        .first() # Ensure we only get the most recent scan results (one that finished most recently)
    )

    if not latest_scan_file:
        return []
    
    return (
        db.query(
            ScanFileDetection.sensitivity_subcategory,
            func.count(ScanFileDetection.scan_file_detection_id).label("count")
        )
        .filter(ScanFileDetection.scan_file_id == latest_scan_file.scan_file_id)
        .group_by(ScanFileDetection.sensitivity_subcategory)
        .all()
    )


def get_subcategory_category_map(db: Session):
    rows = (
        db.query(
            SensitivitySubcategory.name,
            SensitivityCategory.name
        )
        .join(
            SensitivityCategory,
            SensitivitySubcategory.sensitivity_category_id == SensitivityCategory.sensitivity_category_id
        )
        .all()
    )

    return {row.subcategory_name: row.category_name for row in rows}


def get_file_by_graph_id(db: Session, graph_file_id: str):
    return db.query(File).filter(File.graph_file_id == graph_file_id).first()


def get_file_scans(db: Session, file_id: int):
    return (
        db.query(
            Scan.scan_id,
            Scan.started_at,
            Scan.finished_at,

            # Count number of detections for this file within each scan
            func.count(ScanFileDetection.scan_file_detection_id).label("detection_count")
        )
        .join(ScanFile, Scan.scan_id == ScanFile.scan_id) # Join Scan to ScanFile, links each scan to the files included in that scan
        .outerjoin( # Outerjoin ScanFile to ScanFileDetections, so that scans are included even if number of detections is 0
            ScanFileDetection,
            ScanFile.scan_file_id == ScanFileDetection.scan_file_id
        )
        .filter(ScanFile.file_id == file_id) # Filter to only include rows where ScanFile relates to the given file_id
        .group_by(Scan.scan_id, Scan.started_at, Scan.finished_at) # Group by scan to aggregate 
        .order_by(Scan.started_at.desc())
        .all()
    )


def set_file_hash(db: Session, file: File, new_hash: str):
    file.hash = new_hash
    db.commit()
    db.refresh(file)

def create_scan_naming_convention(db: Session, scan_id: int, naming_convention_id: int):
    scan_naming_convention = ScanNamingConvention(scan_id=scan_id, naming_convention_id=naming_convention_id)
    db.add(scan_naming_convention)
    db.commit()
    db.refresh(scan_naming_convention)
    return scan_naming_convention

def get_all_naming_conventions(db: Session):
    return db.query(NamingConvention).all()

def set_naming_convention_scan_result(db: Session, scan_file_id: int, scan_naming_convention_id: int, passed: bool, suggested_name: str):
    naming_convention_scan_result = NamingConventionScanResult(scan_file_id=scan_file_id, scan_naming_convention_id=scan_naming_convention_id, passed=passed, suggested_name=suggested_name)
    db.add(naming_convention_scan_result)
    db.commit()
    db.refresh(naming_convention_scan_result)
    return naming_convention_scan_result

def create_scan(db: Session):
    scan = Scan(started_at=datetime.now())
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

def end_scan(db: Session, scan: Scan):
    scan.finished_at = datetime.now()
    db.commit()
    db.refresh(scan)
    return scan

def create_scan_file(db: Session, scan_id: int, file_id: int):
    scan_file = ScanFile(scan_id=scan_id, file_id=file_id)
    db.add(scan_file)
    db.commit()
    db.refresh(scan_file)
    return scan_file

def create_scan_naming_convention(db: Session, scan_id: int, naming_convention_id: int):
    scan_naming_convention = ScanNamingConvention(scan_id=scan_id, naming_convention_id=naming_convention_id)
    db.add(scan_naming_convention)
    db.commit()
    db.refresh(scan_naming_convention)
    return scan_naming_convention

def get_scan_files_by_scan_id(db: Session, scan_id: int):
    return db.query(ScanFile).filter(ScanFile.scan_id == scan_id).all()

def get_scan_naming_convention(db: Session, scan_id: int, naming_convention_id: int):
    return db.query(ScanNamingConvention).filter(ScanNamingConvention.scan_id == scan_id, ScanNamingConvention.naming_convention_id == naming_convention_id).first()

def get_scan_naming_convention_by_scan_id(db: Session, scan_id: int):
    return db.query(ScanNamingConvention).filter(ScanNamingConvention.scan_id == scan_id).all()

def get_scan_files_with_file(db: Session, scan_id: int):
    return db.query(ScanFile, File).join(File, ScanFile.file_id == File.file_id).filter(ScanFile.scan_id == scan_id).all()

def get_naming_convention_ids(db: Session):
        return db.execute(select(NamingConvention.naming_convention_id)).scalars().all()

def create_test_file(db: Session, graph_file_id: str, file_name: str, hash: str):
    file = File(graph_file_id=graph_file_id, file_name= file_name, hash=hash)
    db.add(file)
    db.commit()
    db.refresh(file)
    return file