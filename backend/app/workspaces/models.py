from sqlalchemy import Column, Integer, String, LargeBinary
from app.core.database import Base

class Workspace(Base):
    __tablename__ = 'workspaces'
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    image = Column(LargeBinary, nullable=False)