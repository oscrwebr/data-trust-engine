from sqlalchemy import Column, Integer, String, Text
from ..core.database import Base

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(254), nullable=False)
    oid = Column(String(40), unique=True, index=True, nullable=False)
    refresh_token = Column(Text()) # Change this to a BLOB when using encryption
    