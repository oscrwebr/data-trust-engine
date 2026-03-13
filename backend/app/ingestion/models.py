from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, BLOB
from ..core.database import Base

class Folder(Base):
    __tablename__ = 'folder'

    folder_id = Column(Integer(), primary_key=True, index=True)
    graph_id = Column(Text(), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(ForeignKey(folder_id), index=True)

class IngestionFile(Base):
    __tablename__ = 'ingestion_file'

    ingestion_file_id = Column(Integer(), primary_key=True, index=True)
    graph_id = Column(Text(), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    extension = Column(String(255), nullable=False)
    hash = Column(Text(), nullable=True)
    hash_type = Column(String(20), nullable=True)
    last_scanned = Column(DateTime())
    last_modified = Column(DateTime(), nullable=False)
    web_url = Column(Text(), nullable=False)
    parent_id = Column(ForeignKey(Folder.folder_id), index=True)


