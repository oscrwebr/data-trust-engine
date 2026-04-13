from app.access_mapping.service import *
from types import SimpleNamespace
from unittest.mock import Mock


def test_build_employees_from_record_groups_roles_for_same_employee():
    # Create mock employee records
    test_employee_records = [
        SimpleNamespace(
            user_id=1,
            firstname="Test",
            surname="Account",
            email="testaccount@test.com",
            role_name="PII Role"
        ),
        SimpleNamespace(
            user_id=1,
            firstname="Test",
            surname="Acount",
            email="testaccount@test.com",
            role_name="HR Role"
        )
    ]

    employees_dict = build_employees_from_records(fetched_employees_records=test_employee_records)

    # Ensure only one employee item exists with both roles in roles list, and with all correct details
    assert len(employees_dict) == 1
    assert employees_dict[1]["user_id"] == 1
    assert employees_dict[1]["name"] == "Test Account"
    assert employees_dict[1]["email"] == "testaccount@test.com"
    assert employees_dict[1]["roles"] == ["PII Role", "HR Role"]
    assert employees_dict[1]["access_allowed"] is True
    assert employees_dict[1]["failed_detections"] == []


def test_build_employees_from_records_does_not_duplicate_same_role():
    # Create mock employee records
    test_employee_records = [
        SimpleNamespace(
            user_id=1,
            firstname="Test",
            surname="Account",
            email="testaccount@test.com",
            role_name="PII Role"
        ),
        SimpleNamespace(
            user_id=1,
            firstname="Test",
            surname="Account",
            email="testaccount@test.com",
            role_name="PII Role"
        )
    ]

    employees_dict = build_employees_from_records(test_employee_records)

    # Ensure employee only has one role (role is not duplicated)
    assert employees_dict[1]["roles"] == ["PII Role"]


def test_build_employees_from_records_handles_employee_with_no_role_name():
    # Create mock employee records
    test_employee_records = [
        SimpleNamespace(
            user_id=1,
            firstname="Test",
            surname="Account",
            email="testaccount@test.com",
            role_name=None
        )
    ]

    employees = build_employees_from_records(test_employee_records)

    # Ensure only one item in employees dictionary, ensure roles list is empty
    assert len(employees) == 1
    assert employees[1]["roles"] == []


def test_build_effective_thresholds_returns_thresholds_for_single_role(monkeypatch):
    # Mock return value of get_role_permissions function
    def mock_get_role_permissions(db, role_id):
        return [
            SimpleNamespace(subcategory="NAME", threshold=5),
            SimpleNamespace(subcategory="EMAIL", threshold=2)
        ]

    monkeypatch.setattr(repository, "get_role_permissions", mock_get_role_permissions)

    thresholds = build_effective_thresholds(db=Mock(), role_ids=[1])

    # Ensure the correct thresholds are returned
    assert thresholds == {
        "NAME": 5,
        "EMAIL": 2
    }


def test_build_effective_thresholds_keeps_most_permissive_threshold_across_roles(monkeypatch):
    # Mock return value of get_role_permissions function for both role id 1 and 2
    def mock_get_role_permissions(db, role_id):
        if role_id == 1:
            return [
                SimpleNamespace(subcategory="NAME", threshold=2),
                SimpleNamespace(subcategory="EMAIL", threshold=3)
            ]
        if role_id == 2:
            return [
                SimpleNamespace(subcategory="NAME", threshold=5),
                SimpleNamespace(subcategory="EMAIL", threshold=1)
            ]
        return []

    monkeypatch.setattr(repository, "get_role_permissions", mock_get_role_permissions)

    thresholds = build_effective_thresholds(db=Mock(), role_ids=[1, 2])

    # Ensure only the MOST PERMISSIVE thresholds are returned (name threshold: 5 | email threshold: 3)
    assert thresholds == {
        "NAME": 5,
        "EMAIL": 3
    }