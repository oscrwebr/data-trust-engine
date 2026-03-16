from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, UniqueConstraint, Index
from ..core.database import Base
from ..authentication.models import User

class Folder(Base):
    __tablename__ = 'folder'

    folder_id = Column(Integer(), primary_key=True)
    graph_id = Column(String(100), nullable=True, index=True)
    UniqueConstraint(graph_id, name="uq_graph_id")
    name = Column(String(255), nullable=False)
    web_url = Column(Text())
    parent_graph_id = Column(String(100), ForeignKey("folder.graph_id"), index=True)


class IngestionFile(Base):
    __tablename__ = 'ingestion_file'

    ingestion_file_id = Column(Integer(), primary_key=True)
    graph_id = Column(String(100), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    extension = Column(String(255), nullable=False)
    hash = Column(Text(), nullable=True)
    hash_type = Column(String(20), nullable=True)
    last_scanned = Column(DateTime())
    last_modified = Column(DateTime(), nullable=False)
    web_url = Column(Text(), nullable=False)
    parent_graph_id = Column(ForeignKey(Folder.graph_id), index=True)

class UserFolders(Base):
    __tablename__ = 'user_folders'

    folder_id = Column(Integer(), primary_key=True)
    user_id = Column(ForeignKey(User.user_id), primary_key=True)
    Index("rev_idx_user_folders", user_id, folder_id)

class UserFiles(Base):
    __tablename__ = 'user_files'

    file_id = Column(ForeignKey(IngestionFile.ingestion_file_id), primary_key=True)
    user_id = Column(ForeignKey(User.user_id), primary_key=True)
    Index("rev_idx_user_files", user_id, file_id)
