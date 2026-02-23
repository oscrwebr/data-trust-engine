from sqlalchemy.orm import Session
from app.invites.models import Invite

from datetime import datetime, date

def add_invite(db: Session, createdAt:datetime, token: str, expiryDate:date, status:str, used:bool):
    invite = Invite(created_at=createdAt, token=token, expiry_date=expiryDate, status=status, used=used)
    db.add(invite)
    db.commit()
    db.refresh(invite)
    return invite