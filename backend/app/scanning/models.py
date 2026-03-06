from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from app.core.database import Base

class File(Base):
    __tablename__ = 'file'

    file_id = Column(Integer, primary_key=True, index=True) 
    graph_file_id = Column(String(128))
    file_name = Column(String(128))
    hash = Column(String(64))

class Scan(Base):
    __tablename__ = 'scans'

    scan_id = Column(Integer, primary_key=True, index=True)
    started_at = Column(DateTime)
    finished_at = Column(DateTime, nullable=True)

class ScanFiles(Base):
    __tablename__ = 'scan_files'

    scan_file_id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.scan_id"), nullable=False)
    file_id = Column(Integer, ForeignKey("file.file_id"), nullable=False)

class NamingConvention(Base):
    __tablename__ = 'naming_convention'

    naming_convention_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))

class ScanNamingConvention(Base):
    __tablename__ = 'scan_naming_convention'

    scan_naming_convention_id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.scan_id"), nullable=False)
    naming_convention_id = Column(Integer, ForeignKey("naming_convention.naming_convention_id"), nullable=False)

class NamingConventionScanResult(Base):
    __tablename__ = 'naming_convention_scan_result'

    naming_convention_scan_result_id = Column(Integer, primary_key=True, index=True)
    scan_file_id = Column(Integer, ForeignKey("scan_files.scan_file_id"), nullable=False)
    scan_naming_convention_id = Column(Integer, ForeignKey("scan_naming_convention.scan_naming_convention_id"), nullable=False)
    passed = Column(Boolean, nullable=False)
    suggested_name = Column(String(128))

