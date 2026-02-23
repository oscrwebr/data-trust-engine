from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean
from app.core.database import Base

class Invite(Base):
    __tablename__ = 'invites'

    invite_id = Column(Integer, primary_key=True, index=True) 
    created_at = Column(DateTime)
    token = Column(String(255), unique=True)
    expiry_date = Column(Date)
    status = Column(String(16))
    used = Column(Boolean)

    # Must also link to the users table (role type admin)
