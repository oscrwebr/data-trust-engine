from app.workspaces import repository
from app.core.database import get_database
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
import base64
from datetime import datetime

# Checking workspace creation inputs
def workspace(user_id:int, name:str, image: bytes, db: Session):
    repository.add_workspace(db, name, image, user_id)
    return True

# Add a notification to database
def add_notification(db: Session, title: str, body: str, datetime: datetime, user_id: int):
    repository.add_notification(db, title, body, datetime, user_id)
    return True

# Get all notifications for a user
def get_user_notifications(db: Session, user_id: int):
    return repository.get_all_notifications(db, user_id)

def del_notification(db: Session, notification_id: int, user_id: int):
    return repository.delete_notification(db, notification_id, user_id)

def workspace_by_user_id(db: Session, user_id: int):
    return repository.get_workspace_by_user_id(db, user_id)