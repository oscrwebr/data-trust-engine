from app.access_mapping.service import *
from types import SimpleNamespace


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