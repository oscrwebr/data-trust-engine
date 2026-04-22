from sqlalchemy.orm import Session
from app.roles import repository
from datetime import datetime

def get_roles(db: Session, workspace_id=int):
    roles = repository.get_all_roles(db, workspace_id)
    result = []
    for r in roles:
        permissions = db.query(repository.RolePermission).filter(repository.RolePermission.role_id == r.role_id).all()
        r_dict = {
            "role_id": r.role_id,
            "name": r.name,
            "role_permissions": [
                {"sensitivity_subcategory_id": p.sensitivity_subcategory_id, "threshold": p.threshold}
                for p in permissions
            ],
            "last_updated":r.last_updated
        }
        result.append(r_dict)
    return result

def create_role(db: Session, name: str, thresholds: list[dict], workspace_id: int, date: datetime):
    role = repository.create_role(db, name, workspace_id, date)

    for t in thresholds:
        repository.create_role_permission(
            db, role.role_id, t["sensitivity_subcategory_id"]
        )

        db.query(repository.RolePermission).filter(
            repository.RolePermission.role_id == role.role_id,
            repository.RolePermission.sensitivity_subcategory_id == t["sensitivity_subcategory_id"]
        ).update({"threshold": t.get("threshold")})

    db.commit()
    db.refresh(role)

    return {
        "role_id": role.role_id,
        "name": role.name,
        "role_permissions": [
            {
                "sensitivity_subcategory_id": t["sensitivity_subcategory_id"],
                "threshold": t.get("threshold"),
            }
            for t in thresholds
        ],
    }

def update_role(db: Session, role_id: int, name: str, thresholds: list[dict], date: datetime):
    return repository.update_role(db, role_id, name, thresholds, date)

def delete_role(db: Session, role_id: int):
    repository.delete_role(db, role_id)

def get_sensitivity_categories(db: Session):
    return repository.get_all_sensitivity_categories(db)

def get_sensitivity_subcategories(db: Session):
    return repository.get_all_sensitivity_subcategories(db)

def get_users(db: Session, role_id: int):
    return repository.get_all_users_by_role(db, role_id)

def update_user_role(db: Session, user_id: int, role_id: int | None):
    repository.set_user_role(db, user_id, role_id)
    
def get_role_by_name(db: Session, name: str):
    return repository.get_role_by_name(db, name)
