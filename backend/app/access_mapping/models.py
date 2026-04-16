from sqlalchemy import Column, Integer, DateTime, ForeignKey
from ..core.database import Base

class ViolationEmail(Base):
    __tablename__ = 'violation_emails'

    violation_email_id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    admin_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"))
    employee_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"))
    