from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from ..core.database import Base

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(254), nullable=False)
    oid = Column(String(40), unique=True, index=True, nullable=False)
    refresh_token = Column(Text()) # Change this to a BLOB when using encryption

class Refresh(Base):
    __tablename__ = 'refresh'

    refresh_id = Column(Integer, primary_key=True, index=True)
    token = Column(Text(), index=True, unique=True, nullable=False)
    expiry = Column(DateTime())
    is_revoked = Column(Boolean(False), nullable=False) # Do we want to deal with this? Can just delete the entire chain if this is the case
    replaced_by = Column(ForeignKey(refresh_id, ondelete="CASCADE"))