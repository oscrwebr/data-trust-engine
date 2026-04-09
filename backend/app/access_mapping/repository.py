from sqlalchemy.orm import Session
from app.authentication.models import User
from app.roles.models import UserRole, Role, RolePermission, SensitivitySubcategory
from app.ingestion.models import UserFiles


# Method to get all employees with access to a specific file
def get_file_employees_with_access(db: Session, file_id: int):
    return (
        db.query(
            User.user_id,
            User.firstname,
            User.surname,
            User.email,
            Role.name.label("role_name")
        )
        .join(UserFiles, UserFiles.user_id == User.user_id)
        .outerjoin(UserRole, UserRole.user_id == User.user_id)
        .outerjoin(Role, Role.role_id == UserRole.role_id)
        .filter(UserFiles.file_id == file_id)
        .all()
    )


# Method to get the thresholds of a provided role
def get_role_thresholds(db: Session, role_id: int):
    return (
        db.query(
            SensitivitySubcategory.name.label("subcategory"),
            RolePermission.threshold
        )
        .join(
            SensitivitySubcategory,
            SensitivitySubcategory.sensitivity_subcategory_id == RolePermission.sensitivity_subcategory_id
        )
        .filter(RolePermission.role_id == role_id)
        .all()
    )