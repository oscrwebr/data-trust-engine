from sqlalchemy.orm import Session
from app.roles.models import (
    Role,
    SensitivityCategory,
    SensitivitySubcategory,
    RolePermission,
    UserRole,
    PendingUserRole
)
from app.authentication.models import User

def create_role(db: Session, name: str, workspace_id: int):
    role = Role(name=name, workspace_id=workspace_id)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def get_all_roles(db: Session):
    return db.query(Role).all()

def get_role_by_name(db: Session, name: str):
    role = db.query(Role).filter(Role.name == name).first()
    return role

def delete_role(db: Session, role_id: int):
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete(synchronize_session=False)
    db.query(Role).filter(Role.role_id == role_id).delete(synchronize_session=False)
    db.commit()

def update_role(db: Session, role_id: int, name: str, thresholds: list[dict]):
    role = db.query(Role).filter(Role.role_id == role_id).first()

    if not role:
        return None

    role.name = name

    db.query(RolePermission).filter(
        RolePermission.role_id == role_id
    ).delete(synchronize_session=False)

    for t in thresholds:
        perm = RolePermission(
            role_id=role_id,
            sensitivity_subcategory_id=t["sensitivity_subcategory_id"],
            threshold=t.get("threshold")
        )
        db.add(perm)

    db.commit()
    db.refresh(role)

    return role

def create_sensitivity_category(db: Session, name: str):
    category = SensitivityCategory(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_all_sensitivity_categories(db: Session):
    return db.query(SensitivityCategory).all()

def create_sensitivity_subcategory(db: Session, name: str, category_id: int):
    subcategory = SensitivitySubcategory(
        name=name,
        sensitivity_category_id=category_id
    )
    db.add(subcategory)
    db.commit()
    db.refresh(subcategory)
    return subcategory

def get_all_sensitivity_subcategories(db: Session):
    return db.query(SensitivitySubcategory).all()

def create_role_permission(db: Session, role_id: int, subcategory_id: int):
    permission = RolePermission(
        role_id=role_id,
        sensitivity_subcategory_id=subcategory_id
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission

def get_all_users_by_role(db: Session, role_id: int):
    """
    Return all users who have a specific sensitivity role.
    role_id: the id of the sensitivity role (from Role table)
    """
    # Join UserRole to filter users with the given sensitivity role
    users = (
        db.query(User)
        .join(UserRole, User.user_id == UserRole.user_id)
        .filter(UserRole.role_id == role_id)
        .all()
    )

    # Prepare list of dicts for API response
    result = [
        {
            "user_id": u.user_id,
            "firstname": u.firstname,
            "surname": u.surname,
            "email": u.email,
            "user_level_role": u.role  # admin/employee
        }
        for u in users
    ]

    return result
    
def set_user_role(db: Session, user_id: int, role_id: int | None):
    """Assign a role to a user, or unset if role_id is None."""
    user_role = db.query(UserRole).filter(UserRole.user_id == user_id).first()
    if role_id is None:
        if user_role:
            db.delete(user_role)
            db.commit()
    else:
        if user_role:
            user_role.role_id = role_id
        else:
            new_user_role = UserRole(user_id=user_id, role_id=role_id)
            db.add(new_user_role)
        db.commit()

def migrate_pending_roles(db: Session, pending_user_id: int, new_user_id: int):
    pending_roles = db.query(PendingUserRole).filter(
        PendingUserRole.user_id == pending_user_id
    ).all()

    for pr in pending_roles:
        db.add(UserRole(
            user_id=new_user_id,
            role_id=pr.role_id
        ))

    db.query(PendingUserRole).filter(
        PendingUserRole.user_id == pending_user_id
    ).delete()

    db.commit()