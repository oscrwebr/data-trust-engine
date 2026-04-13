import app.access_mapping.service as service
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

    employees_dict = service.build_employees_from_records(fetched_employees_records=test_employee_records)

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

    employees_dict = service.build_employees_from_records(test_employee_records)

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

    employees = service.build_employees_from_records(test_employee_records)

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

    # Mock the get_role_permission repository method
    monkeypatch.setattr(service.repository, "get_role_permissions", mock_get_role_permissions)

    thresholds = service.build_effective_thresholds(db=Mock(), role_ids=[1])

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

    # Mock the get_role_permission repository method
    monkeypatch.setattr(service.repository, "get_role_permissions", mock_get_role_permissions)

    thresholds = service.build_effective_thresholds(db=Mock(), role_ids=[1, 2])

    # Ensure only the MOST PERMISSIVE thresholds are returned (name threshold: 5 | email threshold: 3)
    assert thresholds == {
        "NAME": 5,
        "EMAIL": 3
    }


def test_get_failed_detections_returns_only_detections_exceeding_thresholds():
    # Mock latest scan results list
    latest_scan_results = [
        {"subcategory": "NAME", "count": 6},
        {"subcategory": "EMAIL", "count": 2},
        {"subcategory": "PHONE", "count": 1}
    ]

    # Mock effective thresholds dictionary
    effective_thresholds = {
        "NAME": 5,
        "EMAIL": 2,
        "PHONE": 3
    }

    failed_detections = service.get_failed_detections(latest_scan_results, effective_thresholds)

    # Ensure failed detections are those ONLY where count is greater than threshold
    assert failed_detections == [
        {
            "subcategory": "NAME",
            "count": 6,
            "threshold": 5
        }
    ]


def test_get_failed_detections_does_not_fail_when_detection_equals_threshold():
     # Mock latest scan results list
    latest_scan_results = [
        {"subcategory": "NAME", "count": 5}
    ]

    # Mock effective thresholds dictionary
    effective_thresholds = {
        "NAME": 5
    }

    failed_detections = service.get_failed_detections(latest_scan_results, effective_thresholds)

    # Ensure theres no failed detections, because the detection count equals to the threshold, which is allowed
    assert failed_detections == []


def test_get_failed_detections_does_not_fail_when_subcategory_has_no_threshold():
    # Mock latest scan results list
    latest_scan_results = [
        {"subcategory": "NAME", "count": 999}
    ]

    # Mock effective thresholds dictionary
    effective_thresholds = {}

    failed_detections = service.get_failed_detections(latest_scan_results, effective_thresholds)

    # Ensure theres no failed detections, because no threshold exists for NAME subcategory, therefore unlimited amount of detections allowed
    assert failed_detections == []


def test_evaluate_employee_access_denies_employee_with_no_roles(monkeypatch):
    # Mock employee
    employee = {
        "user_id": 1,
        "name": "Test Account",
        "email": "testaccount@test.com",
        "roles": [],
        "access_allowed": True,
        "failed_detections": []
    }

    # Mock repository call to return roles for this user
    monkeypatch.setattr(service.repository, "get_user_role_ids", lambda db, user_id: [])

    service.evaluate_employee_access(
        db=Mock(),
        employee=employee,
        latest_scan_results=[]
    )

    # Ensure employee is not allowed access, and ensure reason is because they have no roles assigned
    assert employee["access_allowed"] is False
    assert employee["failed_detections"] == [
        {
            "subcategory": "NO_ROLES_ASSIGNED",
            "count": None,
            "threshold": None
        }
    ]


def test_evaluate_employee_access_allows_employee_when_no_failed_detections(monkeypatch):
    # Mock employee
    employee = {
        "user_id": 1,
        "name": "Test Account",
        "email": "testaccount@test.com",
        "roles": ["PII Role"],
        "access_allowed": True,
        "failed_detections": []
    }

    # Mock repository call to return a role for this user
    monkeypatch.setattr(service.repository, "get_user_role_ids", lambda db, user_id: [1])

    # Mock the build threshold logic (simulate that employee is allowed up to 10 name detections)
    monkeypatch.setattr(
        service,
        "build_effective_thresholds",
        lambda db, role_ids: {"NAME": 10}
    )

    # Mock the get failed detections logic (simulate that no detections violate employee's thresholds)
    monkeypatch.setattr(
        service,
        "get_failed_detections",
        lambda latest_scan_results, effective_thresholds: []
    )

    service.evaluate_employee_access(
        db=Mock(),
        employee=employee,
        latest_scan_results=[{"subcategory": "NAME", "count": 5}]
    )

    # Ensure access allowed is true and there are no failed detections
    assert employee["access_allowed"] is True
    assert employee["failed_detections"] == []