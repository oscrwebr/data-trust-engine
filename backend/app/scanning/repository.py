from sqlalchemy.orm import Session
from app.scanning.models import File, NamingConvention, Scan, ScanNamingConvention, NamingConventionScanResult

def create_file(db: Session, graph_file_id:str, name: str, extension: str, file_hash: str):
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
    scan = Scan()
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan

