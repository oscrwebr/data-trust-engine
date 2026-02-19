from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from .schemas import ScanRequest, ScanResponse
from app.scanning import service, repository

router = APIRouter(prefix="/scanning", tags=["scanning"])

@router.get("/hash")
def run_hash_endpoint(file_id):
    hash_result = service.hash_file(file_id)
    print(hash_result)

    return

@router.post("/create_test_file")
def create_test_file(file_extension: str, db: Session = Depends(get_database)):
    hash_result = service.hash_file("app/scanning/test_files/client_services_agreement.pdf")

    repository.create_file(db, file_extension, hash_result)
    
@router.get("/get_all_files")
def get_all_files(db: Session = Depends(get_database)):
    return repository.get_all_files(db=db)
