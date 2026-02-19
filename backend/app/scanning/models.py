from sqlalchemy import Boolean, Column, Integer, String
from app.core.database import Base

class File(Base):
    __tablename__ = 'file'

    file_id = Column(Integer, primary_key=True, index=True) 
    graph_file_id = Column(String(128))
    file_name = Column(String(128))
    file_extension = Column(String(16))
    hash = Column(String(64))
