from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.scanning import service, repository

router = APIRouter(prefix="/scanning", tags=["scanning"])


@router.post("/update_file_hash")
def update_file_hash(graph_file_id: str, db: Session=Depends(get_database)):
    service.update_file_hash(graph_file_id)


# Route for creating files (for dev only)
@router.post("/create_file")
def create_file(file_extension: str, db: Session = Depends(get_database)):
    hash_result = service.get_file_hash("app/scanning/test_files/client_services_agreement.pdf")

    repository.create_file(db, file_extension, hash_result)


@router.get("/get_all_files")
def get_all_files(db: Session = Depends(get_database)):
    return repository.get_all_files(db=db)
