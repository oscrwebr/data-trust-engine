from app.workspaces import repository
from app.core.database import get_database
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
import base64

# Checking workspace creation inputs
def workspace(user_id:int, name:str, image: bytes, db: Session):

    # Add workspace to database
    image_bytes = base64.b64decode(image)
    repository.add_workspace(db, name, image_bytes, user_id)
    return True