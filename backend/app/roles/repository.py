from sqlalchemy.orm import Session
from app.roles.models import (
    Role,
    SensitivityCategory,
    SensitivitySubcategory,
    RolePermission
)


# -------- ROLES --------

def create_role(db: Session, name: str):
    role = Role(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_all_roles(db: Session):
    return db.query(Role).all()

def delete_role(db: Session, role_id: int):
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete(synchronize_session=False)
    db.query(Role).filter(Role.role_id == role_id).delete(synchronize_session=False)
    db.commit()

def update_role(db: Session, role_id: int, name: str, thresholds: list[dict]):
    role = db.query(Role).filter(Role.role_id == role_id).first()

    if not role:
        return None

    # 🔹 Update role name
    role.name = name

    # 🔹 Remove old permissions
    db.query(RolePermission).filter(
        RolePermission.role_id == role_id
    ).delete(synchronize_session=False)

    # 🔹 Add new permissions
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

# -------- SENSITIVITY CATEGORIES --------

def create_sensitivity_category(db: Session, name: str):
    category = SensitivityCategory(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_all_sensitivity_categories(db: Session):
    return db.query(SensitivityCategory).all()


# -------- SUBCATEGORIES --------

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


# -------- ROLE PERMISSIONS --------

def create_role_permission(db: Session, role_id: int, subcategory_id: int):
    permission = RolePermission(
        role_id=role_id,
        sensitivity_subcategory_id=subcategory_id
    )
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission
