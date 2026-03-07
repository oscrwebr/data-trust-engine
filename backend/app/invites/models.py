from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Invite(Base):
    __tablename__ = 'invites'

    invite_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    expiry_date = Column(Date)
    status = Column(String(16))
    used = Column(Boolean)
    user_id = Column(Integer, ForeignKey("pending_users.user_id"), nullable=False)
    user = relationship("PendingUser", backref="invites")
    token = Column(String(250))

    # Must also link to the workspace table
