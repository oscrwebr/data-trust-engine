from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey


class File(Base):
    __tablename__ = 'file'

    file_id = Column(Integer, primary_key=True, index=True) 
    graph_file_id = Column(String(128))
    file_name = Column(String(128))
    file_extension = Column(String(16))
    hash = Column(String(64))


class Scan(Base):
    __tablename__ = 'scans'

    scan_id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)


class ScanFiles(Base):
    __tablename__ = 'scan_files'

    scan_file_id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.scan_id"), nullable=False)
    file_id = Column(Integer, ForeignKey("file.file_id"), nullable=False)


class ScanFileDetection(Base):
    __tablename__ = 'scan_file_detection'

    scan_file_detection_id = Column(Integer, primary_key=True, index=True)
    scan_file_id = Column(Integer, ForeignKey("scan_files.scan_file_id"))

    sensitivity_subcategory = Column(String(64))
    page_number = Column(Integer)
