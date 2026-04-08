from sqlalchemy.orm import Session
from app.authentication.models import User
from app.roles.models import UserRole, Role
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