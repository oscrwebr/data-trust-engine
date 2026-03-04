from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = 'users'
 
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), nullable=False)