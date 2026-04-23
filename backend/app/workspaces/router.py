from fastapi import APIRouter, Depends, UploadFile, File, Form, Response
from app.core.database import get_database
from sqlalchemy.orm import Session
from app.workspaces.service import remove_employee_from_workspace, workspace, add_notification, get_user_notifications, del_notification, get_employees, get_pending_employees, get_workspaces, get_workspace_by_id, get_admin_from_workspace, add_pending_user_to_workspace, get_pending_employees_type_request
from typing import Annotated
from ..core.security_schemas import User
from ..core.security import get_user_from_access_token
from app.authentication import service
from app.workspaces.schema import NotificationSchema, RemoveSchema, MessageSchema
from app.invites.service import set_pending_user_type_invite
from app.access_mapping.service import determine_employee_risk_from_violated_files
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
        "role": user.role}, "workspace": None} if user else {"message": "no user"}
    
    return {"user": {
        "firstname": user.firstname,
        "surname": user.surname,
        "email": user.email,
        "role": user.role}, "workspace":user.workspaces[0].name, "id":user.workspaces[0].id, "image":f"/workspace/image/{user.workspaces[0].id}"} if user else {"message": "no user"}

@router.post("/invite/request-join-workspace/{pending_user_id}")
async def create_notification(pending_user_id: int, db: Annotated[Session, Depends(get_database)], notification: NotificationSchema):
    pending_user = service.get_pending_by_id(db, pending_user_id)
    admin = get_admin_from_workspace(db, notification.workspace_id)

    set_pending_user_type_invite(db, pending_user, "request")
    add_notification(db, notification.title, notification.body, datetime.now(), admin[0].user_id)

    return True

@router.post("/dashboard/request-join-workspace")
async def create_notification(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], notification: NotificationSchema):
    
    admin = get_admin_from_workspace(db, notification.workspace_id)
    workspace = get_workspace_by_id(db, notification.workspace_id)

    user = service.test_route(current_user.user_id, db=db)
    pending = service.add_pending_user(db, user.email, "request")
    add_pending_user_to_workspace(db, notification.workspace_id, pending.user_id)
    add_notification(db, notification.title, notification.body, datetime.now(), admin[0].user_id)
    add_notification(db, "Invite Request Sent", f"An invite request has been sent to {workspace.name}. You won't be able to send another request whilst the current one is pending.", datetime.now(), current_user.user_id)

    return True

@router.post("/send-message")
async def create_notification(db: Annotated[Session, Depends(get_database)], employees: MessageSchema):
    
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

@router.get("/image/{workspace_id}")
async def get_workspace_image(workspace_id: int, db: Annotated[Session, Depends(get_database)]):
    workspace = get_workspace_by_id(db, workspace_id)

    if not workspace or not workspace.image:
        return Response(status_code=404)

    return Response(
        content=workspace.image
    )

@router.get("/get-employees")
async def get_all_employees(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):
    active_employees = get_employees(db, current_user.user_id)
    pending_employees = get_pending_employees(db, current_user.user_id)

    # This returns an employees current file access history
    active_employees = determine_employee_risk_from_violated_files(db, active_employees)

    return {
        "pending": pending_employees,
        "active": active_employees
    }

@router.get("/get-workspace-roles")
async def get_workspace_roles(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):

    # Access admnin user and their workspace
    user = service.test_route(current_user.user_id, db=db)
    workspace = user.workspaces
    # Pull all the roles from that workspace
    roles = db.query(Role).filter(Role.workspace_id == workspace[0].id).all()
    return roles

@router.get("/get-pending-employees")
async def get_all_pending_employees_type_request(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):    
    result = get_pending_employees_type_request(db, current_user.user_id)
    return result or None

@router.delete("/delete-user/{user_id}")
async def delete_active_user(user_id: int, db: Annotated[Session, Depends(get_database)]):
    return remove_employee_from_workspace(db, user_id)

@router.patch("/reject-pending/{user_id}")
async def reject_pending(user_id: int, db: Annotated[Session, Depends(get_database)]):
    return service.reject_pending_user(db, user_id)

@router.get("/get-all-workspaces")
async def get_all_workspaces(db: Annotated[Session, Depends(get_database)]):
    workspaces = get_workspaces(db)
    return [
        {
            "id": workspace.id,
            "name": workspace.name,
            "image": f"/workspace/image/{workspace.id}"
        }
        for workspace in workspaces
    ]
