from sqlalchemy.orm import Session
from app.authentication import repository

def check_exists(oid: str, db):
    print(oid)
    res = repository.get_by_id(oid, db)
    print(f"User details:\nFirstname: {res.firstname}\nSurname: {res.surname}\nemail: {res.email}") if res else print("There is nothing there!")
    return res