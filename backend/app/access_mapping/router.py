from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.access_mapping import service, repository
from app.access_mapping.schemas import FileEmployeeAccessResponse

router = APIRouter(prefix="/access_mapping", tags=["access_mapping"])


# Route for getting employees with access to a file by providing its id (unique)
@router.get("/get_file_employees_with_access/{file_id}}", response_model=[FileEmployeeAccessResponse])
def get_file_employees_with_access(file_id: int, db: Session = Depends(get_database)):
    return service.get_file_employees_with_access(db, file_id)