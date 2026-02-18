from sqlalchemy import Boolean, Column, Integer, String
from core.database import Base

class File(Base):
    __tablename__ = 'files'

    file_id = Column(Integer, primary_key=True, index=True) 
    file_extension = Column(String)
    hash = Column(String)
