from sqlalchemy import Boolean, Column, Integer, String
from app.core.database import Base

class File(Base):
    __tablename__ = 'file'

    file_id = Column(Integer, primary_key=True, index=True) 
    file_extension = Column(String(16))
    hash = Column(String(64))
