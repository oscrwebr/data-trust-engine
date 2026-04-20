import pytest
import secrets
from sqlalchemy import insert
from datetime import datetime
from app.roles import service, repository
from app.roles.models import Role, RolePermission, SensitivityCategory, SensitivitySubcategory, UserRole
from app.authentication.models import User
from app.workspaces.models import Workspace
from app.workspaces.repository import add_user_workspace
# ---------------- Helper functions ----------------
def create_admin_user(db, email="admin@test.com"):
    """Create a user who can own a workspace"""
    oid = secrets.token_hex(8)
    stmt = insert(User).values(
        firstname="Admin",
        surname="User",
        username=email,
        email=email,
        oid=oid,
        refresh="ms-refresh".encode(),
        role="admin"
    )
    result = db.execute(stmt)
    db.commit()
    user_id = result.inserted_primary_key[0]
    return db.query(User).filter(User.user_id == user_id).first()

def create_workspace(db, user=None, name="Test Workspace", image=b"fake-image-bytes"):
    """Create a workspace owned by a valid user"""
    if not user:
        user = create_admin_user(db)
    workspace = Workspace(
        name=name,
        image=image,
    )
    db.add(workspace)
    db.commit()
    db.refresh(workspace)
    return workspace

def create_user(db, workspace=None, email="user@test.com"):
    """Create a normal user and optionally associate with workspace."""
    oid = secrets.token_hex(8)
    user = User(
        firstname="Test",
        surname="User",
        username=email,
        email=email,
        oid=oid,
        refresh="ms-refresh".encode(),
        role="employee"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # If a workspace is provided and has no owner, assign this user as owner
    user_workspace = user.workspaces
    if workspace and user_workspace is None:
        workspace.user_id = user.user_id
        db.commit()

    return user

def create_role(db, workspace, name="Test Role", date='2024-01-15 09:30:00'):
    """Create a role in a workspace."""
    role = Role(name=name, workspace_id=workspace.id, last_updated=date)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role
    
# ---------------- Role Tests ----------------
def test_create_role_service(db):
    admin = create_user(db, email="admin1@test.com")
    workspace = create_workspace(db)
    add_user_workspace(db, workspace.id, admin.user_id)
    category = repository.create_sensitivity_category(db, "PII")
    sub = repository.create_sensitivity_subcategory(db, "Emails", category.sensitivity_category_id)

    thresholds = [{"sensitivity_subcategory_id": sub.sensitivity_subcategory_id, "threshold": 42}]
    result = service.create_role(db, "Test Role", thresholds, workspace.id, '2024-01-15 09:30:00')

    assert result["name"] == "Test Role"
    assert len(result["role_permissions"]) == 1
    assert result["role_permissions"][0]["threshold"] == 42

    db_role = db.query(Role).filter(Role.name == "Test Role").first()
    assert db_role is not None

    db_perm = db.query(RolePermission).filter(RolePermission.role_id == db_role.role_id).first()
    assert db_perm.threshold == 42

def test_get_roles_service(db):
    admin = create_user(db, email="admin2@test.com")
    workspace = create_workspace(db)
    add_user_workspace(db, workspace.id, admin.user_id)
    category = repository.create_sensitivity_category(db, "Legal")
    sub = repository.create_sensitivity_subcategory(db, "Contracts", category.sensitivity_category_id)

    role = create_role(db, workspace, "Law Role", '2024-01-15 09:30:00')
    repository.update_role(db, role.role_id, name="Law Role", date='2024-01-15 09:30:00',
                           thresholds=[{"sensitivity_subcategory_id": sub.sensitivity_subcategory_id, "threshold": 10}])

    result = service.get_roles(db)
    assert len(result) >= 1
    found = next(r for r in result if r["role_id"] == role.role_id)
    assert found["name"] == "Law Role"
    assert found["role_permissions"][0]["threshold"] == 10

def test_update_role_service(db):
    admin = create_user(db, email="admin3@test.com")
    workspace = create_workspace(db)
    add_user_workspace(db, workspace.id, admin.user_id)
    category = repository.create_sensitivity_category(db, "Financial")
    sub = repository.create_sensitivity_subcategory(db, "IBANs", category.sensitivity_category_id)

    role = create_role(db, workspace, "Finance Role", '2024-01-15 09:30:00')

    service.update_role(db, role.role_id, name="Finance Role", date='2024-01-15 09:30:00',
                        thresholds=[{"sensitivity_subcategory_id": sub.sensitivity_subcategory_id, "threshold": 5}])
    perm = db.query(RolePermission).filter(RolePermission.role_id == role.role_id).first()
    assert perm.threshold == 5

    service.update_role(db, role.role_id, name="Finance Role", date='2024-01-15 09:30:00',
                        thresholds=[{"sensitivity_subcategory_id": sub.sensitivity_subcategory_id, "threshold": 99}])
    perm_updated = db.query(RolePermission).filter(RolePermission.role_id == role.role_id).first()
    assert perm_updated.threshold == 99

def test_delete_role_service(db):
    admin = create_user(db, email="admin4@test.com")
    workspace = create_workspace(db)
    add_user_workspace(db, workspace.id, admin.user_id)
    role = create_role(db, workspace, "Delete Me", '2024-01-15 09:30:00')
    role_id = role.role_id

    service.delete_role(db, role_id)
    deleted = db.query(Role).filter(Role.role_id == role_id).first()
    assert deleted is None

# ---------------- Category/Subcategory Tests ----------------
def test_get_categories_service(db):
    repository.create_sensitivity_category(db, "PII")
    repository.create_sensitivity_category(db, "Legal")
    categories = service.get_sensitivity_categories(db)
    assert len(categories) >= 2

def test_get_subcategories_service(db):
    cat = repository.create_sensitivity_category(db, "PII")
    repository.create_sensitivity_subcategory(db, "Emails", cat.sensitivity_category_id)
    subs = service.get_sensitivity_subcategories(db)
    assert len(subs) >= 1
    assert subs[0].name == "Emails"

# ---------------- User Tests ----------------
def test_update_user_role_assigns_role(db):
    admin = create_user(db, email="admin3@test.com")
    workspace = create_workspace(db)
    add_user_workspace(db, workspace.id, admin.user_id)
    role = create_role(db, workspace, "Manager")

    employee = create_user(db, workspace=workspace, email="employee2@test.com")
    service.update_user_role(db, employee.user_id, role.role_id)

    assignment = db.query(UserRole).filter(UserRole.user_id == employee.user_id).first()
    assert assignment is not None
    assert assignment.role_id == role.role_id

def test_update_user_role_changes_role(db):
    admin = create_user(db, email="admin4@test.com")
    workspace = create_workspace(db)
    add_user_workspace(db, workspace.id, admin.user_id)
    role1 = create_role(db, workspace, "Role1")
    role2 = create_role(db, workspace, "Role2")

    employee = create_user(db, workspace=workspace, email="employee3@test.com")
    service.update_user_role(db, employee.user_id, role1.role_id)
    service.update_user_role(db, employee.user_id, role2.role_id)

    assignment = db.query(UserRole).filter(UserRole.user_id == employee.user_id).first()
    assert assignment.role_id == role2.role_id

def test_update_user_role_removes_role(db):
    admin = create_user(db, email="admin5@test.com")
    workspace = create_workspace(db)
    add_user_workspace(db, workspace.id, admin.user_id)
    role = create_role(db, workspace, "TempRole")

    employee = create_user(db, workspace=workspace, email="employee4@test.com")
    service.update_user_role(db, employee.user_id, role.role_id)
    service.update_user_role(db, employee.user_id, None)

    assignment = db.query(UserRole).filter(UserRole.user_id == employee.user_id).first()
    assert assignment is None