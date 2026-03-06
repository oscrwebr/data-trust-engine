from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.scanning import service, repository

router = APIRouter(prefix="/scanning", tags=["scanning"])


# Scanning files using provide graph file ids
@router.post("/scan_files")
def scan_files(graph_file_ids: list[str], db: Session = Depends(get_database)):
    service.perform_scan(graph_file_ids=graph_file_ids, db=db)


@router.post("/update_file_hash")
def update_file_hash(graph_file_id: str, db: Session=Depends(get_database)):
    service.update_file_hash(db, graph_file_id)


# Route for creating files (for dev only)
@router.post("/create_file")
def create_file(graph_file_id: str, file_name: str, file_extension: str, db: Session = Depends(get_database)):
    hash_result = service.get_file_hash("app/scanning/test_files/client_services_agreement.pdf")

    repository.create_file(db, graph_file_id, file_name, file_extension, hash_result)


@router.get("/get_all_files")
def get_all_files(db: Session = Depends(get_database)):
    return repository.get_all_files(db=db)

    
