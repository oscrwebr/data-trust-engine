from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Invite(Base):
    __tablename__ = 'invites'

    invite_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)
    expiry_date = Column(Date)
    token = Column(String(250))

    # relations
    user_id = Column(
        Integer,
        ForeignKey("pending_users.user_id", ondelete="CASCADE"),  # <- cascade here
        nullable=False
    )

    pending_user = relationship("PendingUser", back_populates="invites")

    # Must also link to the workspace table
