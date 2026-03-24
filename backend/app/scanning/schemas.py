from pydantic import BaseModel

# Placeholder classes, pydantic to be used in later feature, no need for it yet

# class ScanRequest(BaseModel):
#     file_id: int

# class ScanResponse(BaseModel):
#     scan_id: int
#     status: str


class FileResponse(BaseModel):
    file_id: int
    file_name: str
    hash: str

    class Config:
        from_attributes = True


class OrganisationScanRequest(BaseModel):
    naming_convention_ids: list[int]