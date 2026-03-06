from sqlalchemy.orm import Session
from app.authentication.models import User

from datetime import datetime, date

def add_user(db: Session, email: str):
    user = User(email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user