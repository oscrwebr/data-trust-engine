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
    access_allowed: bool
    failed_detections: list[FailedDetectionResponse]