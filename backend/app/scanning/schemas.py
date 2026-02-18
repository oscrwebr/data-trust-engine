from pydantic import BaseModel

class ScanRequest(BaseModel):
    file_id: int

class ScanResponse(BaseModel):
    scan_id: int
    status: str