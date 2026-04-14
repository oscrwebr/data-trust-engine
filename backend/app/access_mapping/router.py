from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.access_mapping import service, repository
from app.access_mapping.schemas import FileEmployeeAccessResponse, SendViolationsEmailRequest
from app.roles.repository import get_category_by_subcategory_name
from app.authentication.service import test_route
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
    user = test_route(current_user.user_id, db)
    admin_name = (user.firstname + " " + user.surname)
    detections = employee.employee.failed_detections
    all_detections = []

    for detection in detections:
        dict = {}
        category = get_category_by_subcategory_name(db, detection.subcategory)
        dict["subcategory"] = detection.subcategory
        dict["count"] = detection.count
        dict["threshold"] = detection.threshold
        dict["category"] = category.name
        all_detections.append(dict)
        
    return await service.send_email_with_violations(admin_name, employee.employee.name, employee.employee.email, employee.file_name, all_detections)
