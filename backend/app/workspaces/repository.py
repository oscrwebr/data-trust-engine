from sqlalchemy.orm import Session
from app.workspaces.models import Workspace, Notification
from datetime import datetime

def add_workspace(db: Session, name:str, image:bytes, user_id:int):
    workspace = Workspace(name=name, image=image, user_id=user_id)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace

def get_workspace_by_user_id(db: Session, user_id: int):
    return db.query(Workspace).filter(Workspace.user_id == user_id).first()

def add_notification(db: Session, title: str, body: str, datetime: datetime, user_id:int):
    notification = Notification(title=title, body=body, datetime=datetime, user_id=user_id)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_all_notifications(db: Session):
    return db.query(Notification).all()

def delete_notification(db: Session, id: int):
    return db.query(Notification).filter(Notification.id == id).first()