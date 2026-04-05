from app.workspaces import repository
from sqlalchemy.orm import Session
from datetime import datetime

# Checking workspace creation inputs
def workspace(name:str, image: bytes, db: Session, user_id: int):
    workspace = repository.add_workspace(db, name, image)
    repository.add_user_workspace(db, workspace.id, user_id)
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

def get_workspace_by_id(db: Session, workspace_id: int):
    return repository.get_workspace_by_workspace_id(db, workspace_id)

def get_workspaces(db: Session):
    return repository.get_all_workspaces(db)

def get_employees(db: Session, user_id: int):
    return repository.get_all_employees(db, user_id)

def get_admin_from_workspace(db: Session, workspace_id: int):
    return repository.get_workspace_admin(db, workspace_id)

def get_workspace_by_user(db: Session, user_id: int):
    return repository.get_workspace_by_user(db, user_id)
    
def get_pending_employees(db: Session, user_id: int):
    return repository.get_all_pending_employees(db, user_id)

def add_pending_user_to_workspace(db: Session, workspace_id: int, user_id: int):
    return repository.add_pending_user_workspace(db, workspace_id, user_id)
