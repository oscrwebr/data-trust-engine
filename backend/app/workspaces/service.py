from app.workspaces import repository
from app.core.database import get_database
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

# Checking workspace creation inputs
def validate_workspace(name:str, image: bytes, db: Session):

    # Checking if name is null
    if(name is None):
        return "name"
    
    # Checking if image is null
    if(image is None):
        return "image"
    
    # Add workspace to database
    repository.add_workspace(db, name, image)
    return True