import app.access_mapping.service as service
from types import SimpleNamespace
from unittest.mock import Mock

def test_get_file_employees_with_access_sets_unknown_when_file_not_scanned(monkeypatch):
    # Mock employee records
    test_employee_records = [
        SimpleNamespace(
            user_id=1,
            firstname="Szymon",
            surname="Wodkiewicz",
            email="szymon@test.com",
            role_name="PII Role"
        )
    ]

    # Mock the get_file_employees_with_access repository method
    monkeypatch.setattr(
        service.repository,
        "get_file_employees_with_access",
        lambda db, file_id: test_employee_records
    )

    # Mock the check_file_has_scan service method (simulates that it returns False)
    monkeypatch.setattr(service, "check_file_has_scan", lambda db, file_id: False)

    # Mock the get_file_latest_scan_results service method (simulates that it has no scan results at all)
    monkeypatch.setattr(service, "get_file_latest_scan_results", lambda db, file_id: [])

    result = service.get_file_employees_with_access(db=Mock(), file_id=123)

    # Ensure that access_allowed is None and there are no failed detections
    # access_allowed None means that the file has not been scanned ever 
    assert len(result) == 1
    assert result[0]["user_id"] == 1
    assert result[0]["access_allowed"] is None
    assert result[0]["failed_detections"] == []


def test_get_file_employees_with_access_returns_failed_detections_for_denied_employee(monkeypatch):
    # Mock employee records
    test_employee_records = [
        SimpleNamespace(
            user_id=1,
            firstname="Szymon",
            surname="Wodkiewicz",
            email="szymon@test.com",
            role_name="PII Role"
        )
    ]

    # Mock repository method for get_file_employees_with_access to return the mocked employee records
    monkeypatch.setattr(
        service.repository,
        "get_file_employees_with_access",
        lambda db, file_id: test_employee_records
    )

    # Mock check_file_has_scan service method to return True
    monkeypatch.setattr(service, "check_file_has_scan", lambda db, file_id: True)

    # Mock get_file_latest_scan_results service method to return 8 name detections
    monkeypatch.setattr(
        service,
        "get_file_latest_scan_results",
        lambda db, file_id: [{"subcategory": "NAME", "count": 8}]
    )
    
    # Mock get_user_role_ids service method to return role id 1
    monkeypatch.setattr(service.repository, "get_user_role_ids", lambda db, user_id: [1])

    # Mock get_role_permissions repository method to return that the user can see a maximum of 5 name detections
    monkeypatch.setattr(
        service.repository,
        "get_role_permissions",
        lambda db, role_id: [SimpleNamespace(subcategory="NAME", threshold=5)]
    )

    result = service.get_file_employees_with_access(db=Mock(), file_id=123)

    # Ensure access_allowed is false because detection count exceeds threshold
    # Ensure failed_detections contains NAME subcategory and its count & threshold
    assert len(result) == 1
    assert result[0]["access_allowed"] is False
    assert result[0]["failed_detections"] == [
        {
            "subcategory": "NAME",
            "count": 8,
            "threshold": 5
        }
    ]


def test_get_file_employees_with_access_allows_employee_when_threshold_not_exceeded(monkeypatch):
    # Mock employee records
    test_employee_records = [
        SimpleNamespace(
            user_id=1,
            firstname="Szymon",
            surname="Wodkiewicz",
            email="szymon@test.com",
            role_name="PII Role"
        )
    ]

    # Mock get_file_employees_with_access repository method to return mocked employee records
    monkeypatch.setattr(
        service.repository,
        "get_file_employees_with_access",
        lambda db, file_id: test_employee_records
    ) 

    # Mock check_file_has_scan service method to return True
    monkeypatch.setattr(service, "check_file_has_scan", lambda db, file_id: True)

    # Mock get_file_latest_scan_results service method to return 3 name detections
    monkeypatch.setattr(
        service,
        "get_file_latest_scan_results",
        lambda db, file_id: [{"subcategory": "NAME", "count": 3}]
    )
    
    # Mock get_user_role_ids repository method to return role id 1
    monkeypatch.setattr(service.repository, "get_user_role_ids", lambda db, user_id: [1])

    # Mock get_role_permissions repository method to return that the employee can see a maximum of 5 names
    monkeypatch.setattr(
        service.repository,
        "get_role_permissions",
        lambda db, role_id: [SimpleNamespace(subcategory="NAME", threshold=5)]
    )

    result = service.get_file_employees_with_access(db=Mock(), file_id=123)

    # Ensure that access allowed is true
    # Because detection count is within the permitted threshold
    # Ensure there are no failed detections
    assert len(result) == 1
    assert result[0]["access_allowed"] is True
    assert result[0]["failed_detections"] == []

