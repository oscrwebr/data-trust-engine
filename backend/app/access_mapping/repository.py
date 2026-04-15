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


# Method to get all employees with access to all files provided
def get_employees_with_access_for_files(db: Session, file_ids: list[int]):
    rows = (
        db.query(
            UserFiles.file_id.label("file_id"),
            User.user_id,
            User.firstname,
            User.surname,
            User.email,
            Role.name.label("role_name")
        )
        .join(User, User.user_id == UserFiles.user_id)
        .outerjoin(UserRole, UserRole.user_id == User.user_id)
        .outerjoin(Role, Role.role_id == UserRole.role_id)
        .filter(UserFiles.file_id.in_(file_ids))
        .all()
    )

    records_by_file = {}

    for row in rows:
        if row.file_id not in records_by_file:
            records_by_file[row.file_id] = []

        records_by_file[row.file_id].append(row)

    return records_by_file


# Method to get a user's role ids
def get_user_role_ids(db: Session, user_id: int):
    rows = (
        db.query(UserRole.role_id)
        .filter(UserRole.user_id == user_id)
        .all()
    )

    return [row.role_id for row in rows]


# Method to get the permissions of a provided role
def get_role_permissions(db: Session, role_id: int):
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