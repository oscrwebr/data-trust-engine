from pydantic import BaseModel


class FailedDetectionResponse(BaseModel):
    subcategory: str
    count: int | None = None
    threshold: int | None = None


class FileEmployeeAccessResponse(BaseModel):
    user_id: int
    name: str
    email: str
    roles: list[str]
    access_allowed: bool | None
    failed_detections: list[FailedDetectionResponse]


class FileRiskDetailsResponse(BaseModel):
    file_id: int
    file_name: str
    employees_with_access_count: int
    valid_access_count: int
    invalid_access_count: int
    valid_access_percentage: float
    invalid_access_percentage: float
    detection_count: int
    risk_score: float


class PaginatedFileRiskDetailsResponse(BaseModel):
    items: list[FileRiskDetailsResponse]
    total: int
    limit: int
    offset: int