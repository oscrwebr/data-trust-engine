from fastapi import APIRouter, Depends, UploadFile, File, Form, Response
from app.core.database import get_database
from sqlalchemy.orm import Session
from app.workspaces.service import workspace, add_notification, get_user_notifications, del_notification, get_employees, get_pending_employees, get_workspaces, get_workspace_by_id, get_admin_from_workspace
from typing import Annotated
from ..core.security_schemas import User
from ..core.security import get_user_from_access_token
from app.authentication import service
from app.workspaces.schema import NotificationSchema, RemoveSchema, MessageSchema
from app.invites.service import get_invite_by_pending_user_id, set_pending_user_type_invite
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

@router.post("/request-join-workspace")
async def create_notification(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)], notification: NotificationSchema):
    pending_user = service.get_pending_by_id(db, current_user.user_id)
    admin = get_admin_from_workspace(db, notification.workspace_id)
    workspace = get_workspace_by_id(db, notification.workspace_id)

    if pending_user:
        set_pending_user_type_invite(db, pending_user, "request")
        add_notification(db, notification.title, notification.body, datetime.now(), admin[0].user_id)

    else:
        user = service.test_route(current_user.user_id, db=db)
        service.add_pending_user(db, user.email, "request")
        add_notification(db, notification.title, notification.body, datetime.now(), admin[0].user_id)
        add_notification(db, "Invite Request Sent", f"An invite request has been sent to {workspace.name}. You won't be able to send another request whilst the current one is pending.", datetime.now(), current_user.user_id)

    return True

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
    employees = get_employees(db, current_user.user_id)
    pending = get_pending_employees(db, current_user.user_id)

    active_employees = []
    pending_employees = []

    for e in employees:

        # fetch assigned sensitivity role
        user_role = db.query(UserRole).filter(UserRole.user_id == e.user_id).first()
        role_id = user_role.role_id if user_role else None

        # optionally fetch role name
        role_name = None
        if role_id:
            role = db.query(Role).filter(Role.role_id == role_id).first()
            role_name = role.name if role else None

        active_employees.append({"user": e, "role_name": role_name})

    for p in pending:

        # Fetch the invite associated with the pending user where possible
        invite = get_invite_by_pending_user_id(db, p.user_id)
  
        datetime = invite.created_at if invite else None
        pending_employees.append({"pending": p, "datetime": datetime})

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
async def get_all_pending_employees(db: Annotated[Session, Depends(get_database)], current_user: Annotated[User, Depends(get_user_from_access_token)]):
    user = service.test_route(current_user.user_id, db=db)
    pending_employees = []
    if user.role == "employee":
        return pending_employees
    
    if user.role == "admin":
        result = get_pending_employees(db, current_user.user_id)
        
        for p in result:
            if p.type == "request":
                pending_employees.append(p)

    return pending_employees

@router.delete("/delete-user/{user_id}")
async def delete_active_user(user_id: int, db: Annotated[Session, Depends(get_database)]):
    return service.delete_user(db, user_id)

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
