from fastapi import APIRouter, Depends, UploadFile, File, Form, Response
from app.core.database import get_database
from sqlalchemy.orm import Session
from app.workspaces.service import workspace, add_notification, get_user_notifications, del_notification, get_employees, add_pending_user_to_workspace
from typing import Annotated
from ..core.security_schemas import User
from ..core.security import get_user_from_access_token
from app.authentication import service
from app.workspaces.schema import NotificationSchema, RemoveSchema, MessageSchema
from datetime import datetime
from app.roles.models import UserRole, Role

router = APIRouter(prefix="/workspace", tags=["workspace"])

@router.post("/create-workspace")
async def create_workspace(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], name: str = Form(None),
    image: UploadFile = File(None)):

    # Checking if name is null
    if not name or name.strip().lower() == "null":
        return "name"
    
    #Checking if image is null
    if image is None:
        return "image"

    image_bytes = await image.read()
    result = workspace(name, image_bytes, db, current_user.user_id)

    return result

@router.get("/dashboard")
async def dashboard(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):
    user = service.test_route(current_user.user_id, db=db)
    if not user.workspaces:
        return {"user": {
        "firstname": user.firstname,
        "surname": user.surname,
        "email": user.email,
        "role": user.role}, "workspace":"You have not joined a workspace yet"} if user else {"message": "no user"}
    
    return {"user": {
        "firstname": user.firstname,
        "surname": user.surname,
        "email": user.email,
        "role": user.role}, "workspace":user.workspaces[0].name} if user else {"message": "no user"}

@router.post("/request-join-workspace")
async def create_notification(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], notification: NotificationSchema):
    result = add_notification(db, notification.title, notification.body, datetime.now(), current_user.user_id)
    return result

@router.post("/send-message")
async def create_notification(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], employees: MessageSchema):
    
    if employees.body is None or employees.body == "":
        return
    
    for e in employees.employees:
        result = add_notification(db, "New Message", employees.body, datetime.now(), e)

    return result

@router.get("/get-notifications")
async def get_all_notifications(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):
    result = get_user_notifications(db, current_user.user_id)
    return result

@router.post("/delete-notification")
async def delete_notification(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], remove: RemoveSchema):
    result = del_notification(db, remove.notification_id, current_user.user_id)
    return result

@router.get("/get-workspace-image")
async def get_workspace_image(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):
    user = service.test_route(current_user.user_id, db=db)
    return Response(content=user.workspaces[0].image)

@router.get("/get-employees")
async def get_all_employees(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):
    employees = get_employees(db, current_user.user_id)
    result = []
    for e in employees:

        # fetch assigned sensitivity role
        user_role = db.query(UserRole).filter(UserRole.user_id == e.user_id).first()
        role_id = user_role.role_id if user_role else None

        # optionally fetch role name
        role_name = None
        if role_id:
            role = db.query(Role).filter(Role.role_id == role_id).first()
            role_name = role.name if role else None

        result.append({
            "user": e,
            "role_name": role_name
        })
    
    return result

@router.get("/get-workspace-roles")
async def get_workspace_roles(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):

    # Access admnin user and their workspace
    user = service.test_route(current_user.user_id, db=db)
    workspace = user.workspaces

    # Pull all the roles from that workspace
    roles = db.query(Role).filter(Role.workspace_id == workspace[0].id).all()

    return roles