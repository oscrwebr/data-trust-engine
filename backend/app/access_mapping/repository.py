from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.authentication.models import User
from app.access_mapping.models import ViolationEmail
from app.roles.models import UserRole, Role, RolePermission, SensitivitySubcategory
from app.ingestion.models import UserFiles
from datetime import datetime


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


# Method for creating a violation email record
def create_violation_email_record(db: Session, time_now: datetime, admin_id: int, employee_id: int):
    violation_email = ViolationEmail(created_at=time_now, admin_id=admin_id, employee_id=employee_id)
    db.add(violation_email)
    db.commit()
    db.refresh(violation_email)
    return violation_email


# Method for getting the latest violation email for an admin
def get_latest_violation_email_for_cooldown(db: Session, admin_id: int, employee_id: int):
    return (
        db.query(ViolationEmail)
        .filter(
            ViolationEmail.admin_id == admin_id,
            ViolationEmail.employee_id == employee_id
        )
        .order_by(desc(ViolationEmail.created_at))
        .first() 
    )