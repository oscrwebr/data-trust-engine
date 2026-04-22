from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.scanning import service, repository
from pydantic import BaseModel
from app.scanning.schemas import OrganisationScanRequest, FileResponse, FileScansResponse, FileLatestScanResultResponse, UpdateWorkspaceDetectionSensitivityRequest

from app.core.security import get_user_id_from_access_token
from app.authentication.models import User

router = APIRouter(prefix="/scanning", tags=["scanning"])


class ScanFilesRequest(BaseModel):
    graph_file_ids: list[str]


# Scanning files using provide graph file ids
@router.post("/scan_files")
def scan_files(scan_files_request: ScanFilesRequest, db: Session = Depends(get_database)):
    service.perform_scan(graph_file_ids=scan_files_request.graph_file_ids, db=db)

    return {
        "message:" f"File content scan completed successfuly for files: {scan_files_request.graph_file_ids}"
    }


@router.post("/update_file_hash")
def update_file_hash(graph_file_id: str, db: Session=Depends(get_database)):
    service.update_file_hash(db, graph_file_id)


# Route for creating files (for dev only)
@router.post("/create_file")
def create_file(graph_file_id: str, file_name: str, db: Session = Depends(get_database)):
    file = service.fetch_graph_file(graph_file_id=graph_file_id)
    hash_result = service.get_file_hash(file)

    repository.create_file(db, graph_file_id, file_name, hash_result)


# Get a file's details using its id
@router.get("/get_file/{file_id}", response_model=FileResponse)
def get_file(file_id: int, db: Session = Depends(get_database)):
    file = service.get_file(db, file_id)

    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return file


# Get a file's latest scan results using its id
@router.get("/get_file_latest_scan_results/{file_id}", response_model=list[FileLatestScanResultResponse])
def get_file_latest_scan_results(file_id: int, db: Session = Depends(get_database)):
    return service.get_file_latest_scan_results(db=db, file_id=file_id)


# Get all scans a file is part of using its id
@router.get("/get_file_scans/{file_id}", response_model=list[FileScansResponse])
def get_file_scans(file_id: int, db: Session = Depends(get_database)):
    return service.get_file_scans(db, file_id)


@router.get("/get_all_files")
def get_all_files(db: Session = Depends(get_database)):
    return repository.get_all_files(db=db)


@router.post("/organisation_scan")
def organisation_scan(organisation_scan_request: OrganisationScanRequest, db: Session = Depends(get_database), user_id: int = Depends(get_user_id_from_access_token)):
    service.perform_organisation_scan(db, user_id, organisation_scan_request.naming_convention_ids)
    return {"message": "Organisation scan completed successfully"}

@router.get("/get_all_scans")
def get_all_scans(db: Session = Depends(get_database)):
    return repository.get_all_scans(db=db)

@router.get("/get_scans_with_file_count")
def get_scans_with_file_count(db: Session = Depends(get_database), user_id: int = Depends(get_user_id_from_access_token)):
    return service.get_scans_with_file_count(db=db)

@router.get("/get_scan_by_id/{scan_id}")
def get_scan_by_id(scan_id: int, db: Session = Depends(get_database)):
    return service.get_scan_details(db=db, scan_id=scan_id)

@router.get("/get_scan_file_by_id/{scan_file_id}")
def get_scan_file_by_id(scan_file_id: int, db: Session = Depends(get_database)):
    return service.get_scan_file_details(db=db, scan_file_id=scan_file_id)

@router.get("/get_sensitivity_categories")
def get_sensitivity_categories(db: Session = Depends(get_database), user_id: int = Depends(get_user_id_from_access_token)):
    return service.get_sensitivity_subcategories(db=db, user_id=user_id)

@router.post("/update_workspace_detection_sensitivity")
def update_workspace_detection_sensitivity(update_request: UpdateWorkspaceDetectionSensitivityRequest, db: Session = Depends(get_database), user_id: int = Depends(get_user_id_from_access_token)):
    service.update_workspace_detection_sensitivity(db=db, user_id=user_id, sensitivity_subcategory_id=update_request.sensitivity_subcategory_id, is_high=update_request.is_high)
    return {"message": "Updated successfully"}