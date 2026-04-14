from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.access_mapping import service
from app.access_mapping.schemas import FileEmployeeAccessResponse, SendViolationsEmailRequest
from typing import Annotated
from ..core.security_schemas import User
from ..core.security import get_user_from_access_token

router = APIRouter(prefix="/access_mapping", tags=["access_mapping"])


# Route for getting employees with access to a file by providing its id (unique)
@router.get("/get_file_employees_with_access/{file_id}", response_model=list[FileEmployeeAccessResponse])
def get_file_employees_with_access(file_id: int, db: Session = Depends(get_database)):
    return service.get_file_employees_with_access(db, file_id)

# Route for sending an email with the violations
@router.post("/send-violations-email")
async def send_email_with_violations(employee: SendViolationsEmailRequest, db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):
    return await service.process_data_for_violation_email_template(db, current_user.user_id, employee)
