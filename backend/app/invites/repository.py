from sqlalchemy.orm import Session
from app.invites.models import Invite
from app.workspaces.models import Workspace

from datetime import datetime, date

def add_invite(db: Session, createdAt:datetime, expiryDate:date, user_id:int, token:str, workspace: Workspace):
    invite = Invite(created_at=createdAt, expiry_date=expiryDate, user_id=user_id, token=token, workspace=workspace)
    db.add(invite)
    db.commit()
    db.refresh(invite)
    return invite

def get_invite(db: Session, token:str):
    invite = db.query(Invite).filter(Invite.token == token).first()
    return invite