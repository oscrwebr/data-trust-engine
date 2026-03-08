from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.scanning import service, repository
from app.scanning.schemas import OrganisationScanRequest

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

@router.post("/organisation_scan")
def organisation_scan(organisation_scan_request: OrganisationScanRequest, db: Session = Depends(get_database)):
    service.perform_organisation_scan(db, organisation_scan_request.naming_convention_ids)
    return {"message": "Organisation scan completed successfully"}
