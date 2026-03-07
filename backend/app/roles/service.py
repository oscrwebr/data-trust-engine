from sqlalchemy.orm import Session
from app.roles import repository


from sqlalchemy.orm import Session
from app.roles import repository

# Existing functions
def get_roles(db: Session):
    roles = repository.get_all_roles(db)
    # Include role_permissions for frontend
    result = []
    for r in roles:
        permissions = db.query(repository.RolePermission).filter(repository.RolePermission.role_id == r.role_id).all()
        r_dict = {
            "role_id": r.role_id,
            "name": r.name,
            "role_permissions": [
                {"sensitivity_subcategory_id": p.sensitivity_subcategory_id, "threshold": p.threshold}
                for p in permissions
            ]
        }
        result.append(r_dict)
    return result

def create_role(db: Session, name: str, thresholds: list[dict]):
    role = repository.create_role(db, name)
    for t in thresholds:
        repository.create_role_permission(
            db, role.role_id, t["sensitivity_subcategory_id"]
        )
        # Update threshold if provided
        db.query(repository.RolePermission).filter(
            repository.RolePermission.role_id == role.role_id,
            repository.RolePermission.sensitivity_subcategory_id == t["sensitivity_subcategory_id"]
        ).update({"threshold": t.get("threshold")})
    db.commit()
    return get_roles(db)[-1]  # return newly created role

def update_role(db: Session, role_id: int, name: str, thresholds: list[dict]):
    return repository.update_role(db, role_id, name, thresholds)

def delete_role(db: Session, role_id: int):
    repository.delete_role(db, role_id)

def get_sensitivity_categories(db: Session):
    return repository.get_all_sensitivity_categories(db)

def get_sensitivity_subcategories(db: Session):
    return repository.get_all_sensitivity_subcategories(db)
