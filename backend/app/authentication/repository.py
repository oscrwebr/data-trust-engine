from sqlalchemy.orm import Session
from sqlalchemy import select, update, insert
from .models import *
from datetime import datetime, timezone

def get_all(db: Session):
    return db.query(User).all()

def get_by_id(user_id: int, db: Session):
    return db.query(User).filter(User.user_id == user_id).first()

def get_by_oid(oid: str, db: Session):
    return db.query(User).filter(User.oid == oid).first()

def add_user(db: Session, email: str):
    user = User(email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_refresh(hashed_token: str, expiry: datetime, db: Session) -> Refresh:
    return db.query(Refresh).filter(Refresh.token == hashed_token).first()

def create_refresh_family(db: Session) -> RefreshFamily:
    refresh_family_item = RefreshFamily()
    db.add(refresh_family_item)
    db.commit()
    db.refresh(refresh_family_item)
    return refresh_family_item

def create_refresh(db: Session, uid:int, hashed_token: str, expiry: datetime, access_token: str, refresh_family_id: int | None):
    refresh_item = Refresh(user_id=uid, token=hashed_token, expiry=expiry, refresh_family_id=refresh_family_id, access_token = access_token)
    db.add(refresh_item)
    db.commit()
    db.refresh(refresh_item)
    return refresh_item

def get_refresh_details_by_token(db: Session, hashed_token: str) -> Refresh:
    return db.query(Refresh).filter(Refresh.token == hashed_token).first()

def get_by_refresh_family_id(db: Session, refresh_family_id: int) -> RefreshFamily:
    return db.query(RefreshFamily).filter(RefreshFamily.refresh_family_id == refresh_family_id).first()

def get_uid_from_refresh_id(db: Session, refresh_id: int) -> int:
    select_statement = select(Refresh.user_id).where(Refresh.refresh_id == refresh_id)
    return db.execute(select_statement).scalar_one_or_none()
    # return db.query(Refresh.user_id).filter(Refresh.refresh_id == refresh_id).first()

def update_prev_refresh_entry(db: Session, prev_id, new_id) -> None:
    update_statement = update(Refresh).where(Refresh.refresh_id == prev_id).values({
        Refresh.replaced_by : new_id,
        Refresh.replaced_at : datetime.now(timezone.utc)
    })
    db.execute(update_statement)
    db.commit()

def revoke_refresh_family(db: Session, refresh_family_id: int) -> None:
    update_statement = update(RefreshFamily).where(RefreshFamily.refresh_family_id == refresh_family_id).values({
        RefreshFamily.is_revoked : True
    })
    db.execute(update_statement)
    db.commit()

