from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.access_mapping import service, repository

router = APIRouter(prefix="/access_mapping", tags=["access_mapping"])

# Route for getting employees with access to a file by providing its id (unique)
@router.get("/get_file_employees_with_access/{file_id}}")
def get_file_employees_with_access(file_id: int, db: Session = Depends(get_database)):
    pass