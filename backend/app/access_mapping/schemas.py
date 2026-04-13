import os

from pydantic import BaseModel
from fastapi_mail import ConnectionConfig

from dotenv import load_dotenv


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