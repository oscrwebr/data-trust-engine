from sqlalchemy.orm import Session
from app.workspaces.models import Workspace, Notification
from datetime import datetime
from sqlalchemy import desc

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

def get_all_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(desc(Notification.datetime)).all()

def delete_notification(db: Session, notification_id: int, user_id: int):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    db.delete(notification)
    db.commit()
    return db.query(Notification).filter(Notification.user_id == user_id).all()