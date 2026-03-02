from sqlalchemy.orm import Session
from app.invites.models import Invite
from app.authentication.models import User

from datetime import datetime, date

def add_invite(db: Session, createdAt:datetime, expiryDate:date, status:str, used:bool, user_id:int):
    invite = Invite(created_at=createdAt, expiry_date=expiryDate, status=status, used=used, user_id=user_id)
    db.add(invite)
    db.commit()
    db.refresh(invite)
    return invite