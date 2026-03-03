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


class ScanFileResult(Base):
    __tablename__ = 'scan_file_result'

    scan_file_result_id = Column(Integer, primary_key=True, index=True)
    scan_file_id = Column(Integer, ForeignKey("scan_files.scan_file_id"))

    # Counts
    name_count = Column(Integer, nullable=False, default=0)
    phone_count = Column(Integer, nullable=False, default=0)
    email_count = Column(Integer, nullable=False, default=0)
    address_count = Column(Integer, nullable=False, default=0)
    postcode_count = Column(Integer, nullable=False, default=0)
    number_plate_count = Column(Integer, nullable=False, default=0)
    iban_count = Column(Integer, nullable=False, default=0)
    vat_count = Column(Integer, nullable=False, default=0)