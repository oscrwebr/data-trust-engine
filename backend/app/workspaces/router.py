from fastapi import APIRouter, Depends, UploadFile, File, Form, Response
from app.core.database import get_database
from sqlalchemy.orm import Session
from app.workspaces.service import workspace, add_notification, get_user_notifications, del_notification, get_employees
from typing import Annotated
from ..core.security_schemas import User
from ..core.security import get_user_from_access_token
from app.authentication import service
from app.workspaces.schema import NotificationSchema, RemoveSchema
from datetime import datetime

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
    result = get_employees(db, current_user.user_id)
    return result