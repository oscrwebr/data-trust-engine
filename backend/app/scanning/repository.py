from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.scanning.models import File, NamingConvention, Scan, ScanNamingConvention, NamingConventionScanResult, Scan, ScanFile, ScanFileDetection
from datetime import datetime, timezone
from app.scanning.scan_type import ScanType


def create_scan(db: Session, scan_type: ScanType):
    scan = Scan(
        scan_type = scan_type,
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


def get_file_by_graph_id(db: Session, graph_file_id: str):
    return db.query(File).filter(File.graph_file_id == graph_file_id).first()


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

def get_all_scans(db: Session):
    return db.query(Scan).all()

def get_scan_file_count(db: Session, scan_id: int):
    return db.query(ScanFile).filter(ScanFile.scan_id == scan_id).count()

def get_scans_with_file_count(db: Session):
    return db.query(Scan, func.count(ScanFile.scan_file_id)).outerjoin(ScanFile, Scan.scan_id == ScanFile.scan_id).group_by(Scan.scan_id).all()

def get_naming_convention_scan_result_by_scan_file_id(db: Session, scan_file_id: int):
    return db.query(NamingConventionScanResult, NamingConvention.name).join(
    # Join to first get the ScanNamingConvention result
    ScanNamingConvention, NamingConventionScanResult.scan_naming_convention_id == ScanNamingConvention.scan_naming_convention_id
    ).join(
    # Then join to get the actual NamingConvention
    NamingConvention, ScanNamingConvention.naming_convention_id == NamingConvention.naming_convention_id
    # Then get the naming convention scan results for the given scan_file_id
    ).filter(NamingConventionScanResult.scan_file_id == scan_file_id).all()