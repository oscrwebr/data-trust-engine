from sqlalchemy.orm import Session
from app.workspaces.models import Workspace, Notification, user_workspace
from app.authentication.models import User
from datetime import datetime
from sqlalchemy import desc, insert

def add_workspace(db: Session, name:str, image:bytes):
    workspace = Workspace(name=name, image=image)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace

def get_workspace_by_workspace_id(db: Session, workspace_id: int):
    return db.query(Workspace).filter(Workspace.id == workspace_id).first()

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

def add_user_workspace(db: Session, workspace_id: int, user_id: int):
    record = insert(user_workspace).values(
        user_id=user_id,
        workspace_id=workspace_id
    )
    db.execute(record)
    db.commit()
    return record


def get_all_employees(db: Session, user_id: int):
    workspace = db.query(Workspace).join(user_workspace).filter(
        user_workspace.c.user_id == user_id
    ).first()
    
    users = (
        db.query(User)
        .join(user_workspace)
        .filter(user_workspace.c.workspace_id == workspace.id)
        .filter(User.role == "employee")
        .all()
    )

    return users