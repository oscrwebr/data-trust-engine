from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_database
from app.roles import service
from app.roles.models import UserRole, Role
from app.roles.schema import UpdateUserRolesRequest
from app.authentication.models import User
from datetime import datetime

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/get")
def get_roles(db: Session = Depends(get_database)):
    return service.get_roles(db)

@router.post("/create")
def create_role(payload: dict, db: Session = Depends(get_database)):
    name = payload.get("name")
    thresholds = payload.get("thresholds", [])
    workspace_id = 1
    return service.create_role(db, name, thresholds, workspace_id, datetime.now())

@router.put("/update/{role_id}")
def update_role(role_id: int, payload: dict, db: Session = Depends(get_database)):
    name = payload.get("name")
    thresholds = payload.get("thresholds", [])
    return service.update_role(db, role_id, name, thresholds, datetime.now())

@router.delete("/delete/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_database)):
    service.delete_role(db, role_id)
    return {"message": "Role deleted successfully"}

@router.get("/sensitivity/categories")
def get_categories(db: Session = Depends(get_database)):
    return service.get_sensitivity_categories(db)

@router.get("/sensitivity/subcategories")
def get_subcategories(db: Session = Depends(get_database)):
    return service.get_sensitivity_subcategories(db)

@router.get("/users/role/{role_id}")
def get_users(role_id: int, db: Session = Depends(get_database)):
    """Fetch all users with their current role"""
    return service.get_users(db, role_id)

@router.put("/update-user-roles")
def set_user_role(roleUpdate: UpdateUserRolesRequest, db: Session = Depends(get_database)):

    for entity in roleUpdate.employees:
        if entity.role_name == 'No Role Assigned':
            service.update_user_role(db, entity.user_id, None)
            return {"message": "User role updated successfully"}

        role = service.get_role_by_name(db, entity.role_name)
        service.update_user_role(db, entity.user_id, role.role_id)

    return {"message": "User role updated successfully"}

@router.get("/users/all")
def get_all_users(db: Session = Depends(get_database)):
    users = db.query(User).all()
    result = []

    for u in users:
        # fetch assigned sensitivity role
        user_role = db.query(UserRole).filter(UserRole.user_id == u.user_id).first()
        role_id = user_role.role_id if user_role else None

        # optionally fetch role name
        role_name = None
        if role_id:
            role = db.query(Role).filter(Role.role_id == role_id).first()
            role_name = role.name if role else None

        result.append({
            "user_id": u.user_id,
            "firstname": u.firstname,
            "surname": u.surname,
            "email": u.email,
            "role_id": role_id,
            "role_name": role_name
        })

    return result
