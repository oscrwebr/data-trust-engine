from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Invite(Base):
    __tablename__ = 'invites'

    invite_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    expiry_date = Column(Date, nullable=False)
    token = Column(String(250), nullable=False)
    used = Column(Boolean, nullable=False)

    # Relationship to user
    user_id = Column(
        Integer,
        ForeignKey("pending_users.user_id", ondelete="CASCADE"),  # <- cascade here
        nullable=False
    )
    pending_users = relationship("PendingUser", back_populates="invites")

    # Relationship to workspace
    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id"),
        nullable=False
    )
    workspace = relationship("Workspace", back_populates="invites")

    
