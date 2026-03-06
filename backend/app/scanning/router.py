from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.scanning import service, repository

router = APIRouter(prefix="/scanning", tags=["scanning"])


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


@router.get("/scan_file")
def scan_file(file_path: str, db: Session = Depends(get_database)):
    extracted_text = service.extract_text_from_pdf(file_path)

    detected_named_entities = service.detect_named_entities(extracted_text)
    detected_phone_numbers = service.detect_phone_numbers(extracted_text)

    return extracted_text
    
