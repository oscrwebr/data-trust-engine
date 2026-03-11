from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, TIMESTAMP
from ..core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(254), nullable=False)
    oid = Column(String(40), unique=True, index=True, nullable=False) # Handle this!

class PendingUser(Base):
    __tablename__ = 'pending_users'

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(254), nullable=False)

    # relation
    invites = relationship(
        "Invite",
        back_populates="pending_user",
        cascade="all, delete",
        passive_deletes=True
    )

class RefreshFamily(Base):
    __tablename__ = 'refresh_family'

    refresh_family_id = Column(Integer, primary_key=True, index=True)
    is_revoked = Column(Boolean(), default=False) # Allows killing of an entire chain
    

class Refresh(Base):
    __tablename__ = 'refresh'

    refresh_id = Column(Integer, primary_key=True, index=True)
    token = Column(Text(), index=True, unique=True, nullable=False)
    expiry = Column(DateTime())
    user_id = Column(ForeignKey(User.user_id, ondelete="CASCADE"))
    refresh_family_id = Column(ForeignKey(RefreshFamily.refresh_family_id), index=True)
    replaced_by = Column(ForeignKey(refresh_id, ondelete="CASCADE"))
    replaced_at = Column(DateTime()) # To handle race conditions in case client sends multiple requests at once for access token generation
    access_token = Column(Text(), nullable=False) # Necessary for grace period