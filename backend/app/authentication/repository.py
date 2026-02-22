from sqlalchemy.orm import Session
from .models import User

def get_all(db: Session):
    return db.query(User).all()

def get_by_id(oid: str, db: Session):
    return db.query(User).filter(User.oid == oid).first()

def add_user(db: Session, email: str):
    user = User(email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user