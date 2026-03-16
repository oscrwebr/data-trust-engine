from sqlalchemy.orm import Session
from app.invites.models import Invite
from app.workspaces.models import Workspace
from app.authentication.models import PendingUser
from sqlalchemy import desc

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

def get_invite_for_cooldown(db: Session, workspace: Workspace, user: PendingUser):
    return (
        db.query(Invite)
        .filter(
            Invite.workspace_id == workspace.id,
            Invite.user_id == user.user_id
        )
        .order_by(desc(Invite.created_at))
        .first() 
    )
