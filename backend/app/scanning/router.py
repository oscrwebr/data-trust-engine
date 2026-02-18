from fastapi import APIRouter
from .schemas import ScanRequest, ScanResponse
from .service import hash_file

router = APIRouter(prefix="/scanning", tags=["scanning"])

@router.get("/hash")
def run_hash_endpoint(file_path):
    hash_result = hash_file(file_path)
    print(hash_result)

    return

