from sqlalchemy.orm import Session
from .models import *
from datetime import datetime

def get_all(db: Session):
    return db.query(User).all()

def get_by_id(oid: str, db: Session):
    return db.query(User).filter(User.oid == oid).first()

def add_user(db: Session, email: str):
    user = User(email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_refresh(hashed_token: str, expiry: datetime, db: Session) -> Refresh:
    return db.query(Refresh).filter(Refresh.token == hashed_token).first()

def create_refresh(hashed_token: str, expiry: datetime, db: Session, is_revoked: bool=False, replaced_by: int | None=None) -> None:
    refresh_item = Refresh(token=hashed_token, expiry=expiry, is_revoked=is_revoked, replaced_by=replaced_by)
    db.add(refresh_item)
    db.commit()
    db.refresh(refresh_item)
    return refresh_item
