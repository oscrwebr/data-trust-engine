from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME, Table
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from app.core.database import Base
from sqlalchemy.orm import relationship

class Workspace(Base):
    __tablename__ = 'workspaces'
 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    image = Column(MEDIUMBLOB, nullable=False)
    invites = relationship("Invite", back_populates="workspace", cascade="all, delete-orphan")
    user = relationship(
        "User",
        secondary="user_workspace",
        back_populates="workspaces"
    )

    pending_users = relationship(
        "PendingUser",
        secondary="pending_user_workspace",
        back_populates="workspaces"
    )

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    body = Column(String(200), nullable=False)
    datetime = Column(DATETIME, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", backref="notifications")

user_workspace = Table(
    "user_workspace",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True),
    Column("workspace_id", Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), primary_key=True),
)

pending_user_workspace = Table(
    "pending_user_workspace",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("pending_users.user_id", ondelete="CASCADE"), primary_key=True),
    Column("workspace_id", Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), primary_key=True),
)