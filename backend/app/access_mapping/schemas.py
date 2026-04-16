import os

from pydantic import BaseModel
from fastapi_mail import ConnectionConfig

from dotenv import load_dotenv

from datetime import datetime


load_dotenv()

mail_password = os.getenv("MAIL_PASSWORD")


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
    last_sent: datetime | None = None


class SendViolationsEmailRequest(BaseModel):
    file_name: str
    employee: FileEmployeeAccessResponse


conf = ConnectionConfig(
   MAIL_FROM="datatrustengine@gmail.com",
   MAIL_USERNAME="datatrustengine@gmail.com",
   MAIL_PASSWORD=mail_password,
   MAIL_PORT=587,
   MAIL_FROM_NAME="Data Trust Engine",   
   MAIL_SERVER="smtp.gmail.com",
   MAIL_STARTTLS=True,
   MAIL_SSL_TLS=False,
   USE_CREDENTIALS=True,
   VALIDATE_CERTS=True
)
