from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from app.core.database import Base
from sqlalchemy.orm import relationship

class Workspace(Base):
    __tablename__ = 'workspaces'
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    image = Column(MEDIUMBLOB, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    user = relationship("User", backref="workspaces")

    invites = relationship("Invite", back_populates="workspace", cascade="all, delete-orphan")