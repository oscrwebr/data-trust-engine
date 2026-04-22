from sqlalchemy.orm import Session
from app.workspaces.models import Workspace, Notification, user_workspace, pending_user_workspace
from app.authentication.models import User, PendingUser
from app.invites.models import Invite
from app.roles.models import Role, UserRole
from datetime import datetime
from sqlalchemy import desc, insert, func

def add_workspace(db: Session, name:str, image:bytes):
    workspace = Workspace(name=name, image=image)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace

def get_all_workspaces(db: Session):
    return db.query(Workspace).all()

def get_workspace_by_workspace_id(db: Session, workspace_id: int):
    return db.query(Workspace).filter(Workspace.id == workspace_id).first()

def add_notification(db: Session, title: str, body: str, datetime: datetime, user_id:int):
    notification = Notification(title=title, body=body, datetime=datetime, user_id=user_id)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_all_notifications(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.user_id == user_id).order_by(desc(Notification.datetime)).all()

def delete_notification(db: Session, notification_id: int, user_id: int):
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    db.delete(notification)
    db.commit()
    return db.query(Notification).filter(Notification.user_id == user_id).all()

def add_user_workspace(db: Session, workspace_id: int, user_id: int):
    record = insert(user_workspace).values(
        user_id=user_id,
        workspace_id=workspace_id
    )
    db.execute(record)
    db.commit()
    return record

def add_pending_user_workspace(db: Session, workspace_id: int, user_id: int):
    record = insert(pending_user_workspace).values(
        user_id=user_id,
        workspace_id=workspace_id
    )
    db.execute(record)
    db.commit()
    return record

def get_workspace_admin(db: Session, workspace_id: int):
    user = (
        db.query(User)
        .join(user_workspace, User.user_id == user_workspace.c.user_id)
        .filter(user_workspace.c.workspace_id == workspace_id)
        .filter(User.role == "admin")
        .all()
    )

    return user

def get_all_employees(db: Session, user_id: int):
    workspace = db.query(Workspace).join(user_workspace).filter(
        user_workspace.c.user_id == user_id
    ).first()
    
    results = (
        db.query(User, Role.name.label("role_name"))
        .join(user_workspace, user_workspace.c.user_id == User.user_id)
        .outerjoin(UserRole, UserRole.user_id == User.user_id)
        .outerjoin(Role, Role.role_id == UserRole.role_id)
        .filter(user_workspace.c.workspace_id == workspace.id)
        .filter(User.role == "employee")
        .all()
    )

    # shape into clean response
    employees = []
    for user, role_name in results:
        employees.append({
        "user": user,
        "role_name": role_name
    })

    return employees

def get_workspace_by_user(db: Session, user_id: int) -> int | None:

    workspace_assoc = db.query(user_workspace).filter(user_workspace.c.user_id == user_id).first()
    if workspace_assoc:
        return workspace_assoc.workspace_id
    return None

def get_all_pending_employees(db: Session, user_id: int):
    workspace = db.query(Workspace).join(user_workspace).filter(
        user_workspace.c.user_id == user_id
    ).first()

    latest_invite = (
        db.query(
            Invite.user_id,
            func.max(Invite.created_at).label("datetime")
        )
        .group_by(Invite.user_id)
        .subquery()
    )
    
    results = (
        db.query(PendingUser, latest_invite.c.datetime)
        .join(pending_user_workspace, pending_user_workspace.c.user_id == PendingUser.user_id)
        .outerjoin(latest_invite, latest_invite.c.user_id == PendingUser.user_id)
        .filter(pending_user_workspace.c.workspace_id == workspace.id)
        .all()
    )

    # shape into clean response
    pending_users = []
    for pending_user, datetime_value in results:
        pending_users.append({
        "user": pending_user,
        "datetime": datetime_value
    })

    return pending_users

def get_all_pending_employees_type_request(db: Session, user_id: int):
    workspace = db.query(Workspace).join(user_workspace).filter(
        user_workspace.c.user_id == user_id
    ).first()
    
    results = (
        db.query(PendingUser)
        .join(pending_user_workspace, pending_user_workspace.c.user_id == PendingUser.user_id)
        .filter(pending_user_workspace.c.workspace_id == workspace.id)
        .filter(PendingUser.type == "request")
        .all()
    )

    # shape into clean response
    pending_users = []
    for pending_user in results:
        pending_users.append({
        "user": pending_user,
    })

    return pending_users


def get_employee_in_workspace_by_email(db: Session, email: str, workspace: Workspace):
    
    user = (
        db.query(User)
        .join(user_workspace, user_workspace.c.user_id == User.user_id)
        .filter(user_workspace.c.workspace_id == workspace.id)
        .filter(User.email == email)
        .filter(User.role == "employee")
        .first()
    )

    return user
