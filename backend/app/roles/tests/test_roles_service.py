import pytest
from app.roles import service, repository
from app.roles.models import (
    Role,
    RolePermission,
    SensitivityCategory,
    SensitivitySubcategory,
)

def test_create_role_service(db):
    category = repository.create_sensitivity_category(db, "PII")
    sub = repository.create_sensitivity_subcategory(db, "Emails", category.sensitivity_category_id)

    thresholds = [
        {"sensitivity_subcategory_id": sub.sensitivity_subcategory_id, "threshold": 42}
    ]

    result = service.create_role(db, "Test Role", thresholds)

    assert result["name"] == "Test Role"
    assert len(result["role_permissions"]) == 1
    assert result["role_permissions"][0]["threshold"] == 42

    db_role = db.query(Role).filter(Role.name == "Test Role").first()
    assert db_role is not None

    db_perm = db.query(RolePermission).filter(
        RolePermission.role_id == db_role.role_id
    ).first()
    assert db_perm.threshold == 42

def test_get_roles_service(db):
    category = repository.create_sensitivity_category(db, "Legal")
    sub = repository.create_sensitivity_subcategory(db, "Contracts", category.sensitivity_category_id)

    role = repository.create_role(db, "Law Role")
    
    # Pass the current role name to avoid NOT NULL error
    repository.update_role(
        db,
        role.role_id,
        name=role.name,  
        thresholds=[{"sensitivity_subcategory_id": sub.sensitivity_subcategory_id, "threshold": 10}]
    )

    result = service.get_roles(db)

    assert len(result) == 1
    assert result[0]["name"] == "Law Role"
    assert result[0]["role_permissions"][0]["threshold"] == 10

def test_update_role_service(db):
    category = repository.create_sensitivity_category(db, "Financial")
    sub = repository.create_sensitivity_subcategory(db, "IBANs", category.sensitivity_category_id)

    role = repository.create_role(db, "Finance Role")

    # Initial update
    service.update_role(
        db,
        role.role_id,
        thresholds=[{"sensitivity_subcategory_id": sub.sensitivity_subcategory_id, "threshold": 5}],
        name=role.name  # use current role name
    )

    perm = db.query(RolePermission).filter(
        RolePermission.role_id == role.role_id
    ).first()
    assert perm.threshold == 5

    # Update again (replace previous)
    service.update_role(
        db,
        role.role_id,
        thresholds=[{"sensitivity_subcategory_id": sub.sensitivity_subcategory_id, "threshold": 99}],
        name=role.name
    )

    perm_updated = db.query(RolePermission).filter(
        RolePermission.role_id == role.role_id
    ).first()
    assert perm_updated.threshold == 99

def test_delete_role_service(db):
    role = repository.create_role(db, "Delete Me")
    role_id = role.role_id
    service.delete_role(db, role_id)
    deleted = db.query(Role).filter(Role.role_id == role_id).first()
    assert deleted is None

def test_get_categories_service(db):
    repository.create_sensitivity_category(db, "PII")
    repository.create_sensitivity_category(db, "Legal")

    categories = service.get_sensitivity_categories(db)
    assert len(categories) == 2

def test_get_subcategories_service(db):
    cat = repository.create_sensitivity_category(db, "PII")
    repository.create_sensitivity_subcategory(db, "Emails", cat.sensitivity_category_id)

    subs = service.get_sensitivity_subcategories(db)
    assert len(subs) == 1
    assert subs[0].name == "Emails"