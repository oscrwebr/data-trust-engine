from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_database

from app.core.security import get_user_id_from_access_token
from app.authentication.models import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/get_recent_activity")
def get_recent_activity(db: Session = Depends(get_database), user_id: int = Depends(get_user_id_from_access_token)):
    pass