from sqlalchemy.orm import Session
from app.authentication import repository
from ..core.security import hash_user_refresh_token
from datetime import datetime

def check_exists(oid: str, db):
    # print(oid)
    user = repository.get_by_id(oid, db)
    # print(f"User details:\nFirstname: {res.firstname}\nSurname: {res.surname}\nemail: {res.email}") if res else print("There is nothing there!")
    return user if user else None


def create_refresh(refresh_token: str, expiry_date: datetime, db: Session, is_revoked: bool=False, replaced_by: int | None=None):
    hashed_token = hash_user_refresh_token(refresh_token)
    new_entry = repository.create_refresh(hashed_token=hashed_token, expiry=expiry_date, db=db, is_revoked=is_revoked, replaced_by=replaced_by)
    return new_entry


def update_refresh(refresh_token: str, expiry_date: datetime, db):
    hashed_token = hash_user_refresh_token(refresh_token)
    print(f"refresh token from client: {refresh_token} -- hashed token: {hashed_token}")
    matched_refresh = repository.verify_refresh(hashed_token=hashed_token, expiry=expiry_date, db=db)
    # check if the refresh has been used before
    if matched_refresh.replaced_by:
        return "This has been replaced! Compromised tokens! Delete chain immediately!"
    else:
        return "We are ready to roll baby!"
