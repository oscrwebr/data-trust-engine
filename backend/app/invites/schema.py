import os

from fastapi import FastAPI
from fastapi_mail import ConnectionConfig
from pydantic import EmailStr, BaseModel
from typing import List, Optional
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

mail_password = os.getenv("MAIL_PASSWORD")

app = FastAPI()

class EmailSchema(BaseModel):
   email: List[EmailStr]

class InviteRequest(BaseModel):
    email: str
    expiry_date: Optional[datetime] = None

conf = ConnectionConfig(
   MAIL_FROM="datatrustengine@outlook.com",
   MAIL_USERNAME="datatrustengine@outlook.com",
   MAIL_PASSWORD=mail_password,
   MAIL_PORT=587,
   MAIL_FROM_NAME="Data Trust Engine",   
   MAIL_SERVER="smtp.office365.com",
   MAIL_STARTTLS=True,
   MAIL_SSL_TLS=False,
   USE_CREDENTIALS=True,
   VALIDATE_CERTS=True
)