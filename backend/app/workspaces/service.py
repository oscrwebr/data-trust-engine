from app.workspaces import repository
from app.core.database import get_database
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
import base64
from datetime import datetime

# Checking workspace creation inputs
def workspace(user_id:int, name:str, image: bytes, db: Session):

    # Add workspace to database
    image_bytes = base64.b64decode(image)
    repository.add_workspace(db, name, image_bytes, user_id)
    return True

# Checking workspace creation inputs
def add_notification(db: Session, title: str, body: str, datetime: datetime, user_id: int):
    repository.add_notification(db, title, body, datetime, user_id)
    return True