from sqlalchemy.orm import Session
from app.admin_files import repository


def get_last_scanned(db: Session, file_ids: list[int]):
    return repository.get_last_scanned_for_files(db, file_ids)
    