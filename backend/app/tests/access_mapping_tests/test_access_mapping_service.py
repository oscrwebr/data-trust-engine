import app.access_mapping.service as service
from types import SimpleNamespace
from app.access_mapping.schemas import FileRiskDetailsResponse
from unittest.mock import Mock

def test_get_file_employees_with_access_sets_unknown_when_file_not_scanned(monkeypatch):
    # Mock employee records
    test_employee_records = [
        SimpleNamespace(
            user_id=1,
            firstname="Test",
            surname="Account",
            email="testaccount@test.com",
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
    monkeypatch.setattr(service.scanning_service, "check_file_has_scan", lambda db, file_id: False)

    # Mock the get_file_latest_scan_results service method (simulates that it has no scan results at all)
    monkeypatch.setattr(service.scanning_service, "get_file_latest_scan_results", lambda db, file_id: [])

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
            firstname="Test",
            surname="Account",
            email="testaccount@test.com",
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
    monkeypatch.setattr(service.scanning_service, "check_file_has_scan", lambda db, file_id: True)

    # Mock get_file_latest_scan_results service method to return 8 name detections
    monkeypatch.setattr(
        service.scanning_service,
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
            firstname="Test",
            surname="Account",
            email="testaccount@test.com",
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
    monkeypatch.setattr(service.scanning_service, "check_file_has_scan", lambda db, file_id: True)

    # Mock get_file_latest_scan_results service method to return 3 name detections
    monkeypatch.setattr(
        service.scanning_service,
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


def test_get_file_employees_with_access_from_data_sets_unknown_when_not_scanned(monkeypatch):
    # Mock employee records
    test_employee_records = [
        SimpleNamespace(
            user_id=1,
            firstname="Test",
            surname="Account",
            email="testaccount@test.com",
            role_name="PII Role"
        )
    ]

    # Mock employees dictionary
    employees_dict = {
        1: {
            "user_id": 1,
            "name": "Test Account",
            "email": "testaccount@test.com",
            "roles": ["PII Role"],
            "failed_detections": []
        }
    }

    # Mock build_employees_from_records method to return mocked employees dictionary
    monkeypatch.setattr(service, "build_employees_from_records", lambda records: employees_dict)

    result = service.get_file_employees_with_access_from_data(
        db=None,
        fetched_employees_records=test_employee_records,
        has_been_scanned=False,
        latest_scan_results=[]
    )

    # Ensure access allowed is Unknown since file has never been scanned
    assert len(result) == 1
    assert result[0]["access_allowed"] is None


def test_get_file_employees_with_access_from_data_evaluates_access_when_scanned(monkeypatch):
    # Mock test employee record
    test_employee_records = [
        SimpleNamespace(
            user_id=1,
            firstname="Test",
            surname="Account",
            email="testaccount@test.com",
            role_name="PII Role"
        )
    ]

    # Mock employees dictionary
    employees_dict = {
        1: {
            "user_id": 1,
            "name": "Test Account",
            "email": "testaccount@test.com",
            "roles": ["PII Role"],
            "failed_detections": []
        }
    }

    def fake_evaluate_employee_access(db, employee, latest_scan_results):
        employee["access_allowed"] = False
        employee["failed_detections"] = ["EMAIL"]

    # Mock service method to return mocked employees dictionary
    monkeypatch.setattr(service, "build_employees_from_records", lambda records: employees_dict)

    # Mock evaluate_employee_access method to return employee access evaluaton results
    monkeypatch.setattr(service, "evaluate_employee_access", fake_evaluate_employee_access)

    result = service.get_file_employees_with_access_from_data(
        db=None,
        fetched_employees_records=test_employee_records,
        has_been_scanned=True,
        latest_scan_results=[{"category": "Personal", "subcategory": "EMAIL", "count": 2}]
    )

    # Ensure access allowed is False and that EMAIL failed detection exists
    assert len(result) == 1
    assert result[0]["access_allowed"] is False
    assert result[0]["failed_detections"] == ["EMAIL"]


def test_get_file_risk_details_from_data_calculates_values_correctly(monkeypatch):
    # Mock employee access_allowed values
    mock_employees = [
        {"access_allowed": True},
        {"access_allowed": False},
        {"access_allowed": False},
    ]

    # Mock get_file_employes_with_access_from_data method to return mock employees access_allowed values
    monkeypatch.setattr(
        service,
        "get_file_employees_with_access_from_data",
        lambda db, fetched_employees_records, has_been_scanned, latest_scan_results: mock_employees
    )

    latest_scan_results = [
        {"category": "Personal", "subcategory": "NAME", "count": 3},
        {"category": "Personal", "subcategory": "EMAIL", "count": 1},
    ]

    result = service.get_file_risk_details_from_data(
        db=None,
        file_id=10,
        file_name="contract.pdf",
        latest_scan_results=latest_scan_results,
        fetched_employees_records=[],
        has_been_scanned=True
    )

    # Ensure the file risk details are all correct, with correctly calculated access percentage as well as correct risk score
    assert result.file_id == 10
    assert result.file_name == "contract.pdf"
    assert result.employees_with_access_count == 3
    assert result.valid_access_count == 1
    assert result.invalid_access_count == 2
    assert result.valid_access_percentage == 33.33
    assert result.invalid_access_percentage == 66.67
    assert result.detection_count == 4
    assert result.risk_score == 70.87


def test_get_highest_risk_files_returns_sorted_paginated_results(monkeypatch):
    # Create mock files 
    mock_files = [
        SimpleNamespace(ingestion_file_id=1, name="file_a.pdf"),
        SimpleNamespace(ingestion_file_id=2, name="file_b.pdf"),
        SimpleNamespace(ingestion_file_id=3, name="file_c.pdf"),
    ]

    # Mock get_all_files method to return the mocked files
    monkeypatch.setattr(service.ingestion_repository, "get_all_files", lambda db: mock_files)

    # Mock get_latest_scan_results_for_files method
    monkeypatch.setattr(
        service.scanning_service,
        "get_latest_scan_results_for_files",
        lambda db, file_ids: {1: [], 2: [], 3: []}
    )
    
    # Mock get_scan_statues_for_all_files to return True for all ids
    monkeypatch.setattr(
        service.scanning_service,
        "get_scan_statuses_for_all_files",
        lambda db, file_ids: {1: True, 2: True, 3: True}
    )

    # Mock get_employees_with_access_for_files method
    monkeypatch.setattr(
        service.repository,
        "get_employees_with_access_for_files",
        lambda db, file_ids: {1: [], 2: [], 3: []}
    )

    def fake_get_file_risk_details_from_data(
        db,
        file_id,
        file_name,
        latest_scan_results,
        fetched_employees_records,
        has_been_scanned
    ):
        scores = {
            1: 10.0,
            2: 50.0,
            3: 30.0,
        }

        return FileRiskDetailsResponse(
            file_id=file_id,
            file_name=file_name,
            employees_with_access_count=0,
            valid_access_count=0,
            invalid_access_count=0,
            valid_access_percentage=0.0,
            invalid_access_percentage=0.0,
            detection_count=0,
            risk_score=scores[file_id]
        )

    # Mock get_file_risk_details_from_data method to return mocked method results
    monkeypatch.setattr(service, "get_file_risk_details_from_data", fake_get_file_risk_details_from_data)

    result = service.get_highest_risk_files(db=None, limit=2, offset=0)

    assert result.total == 3
    assert result.limit == 2
    assert result.offset == 0
    assert len(result.items) == 2
    assert result.items[0].file_id == 2
    assert result.items[1].file_id == 3


def test_get_highest_risk_files_applies_offset_and_limit(monkeypatch):
    # Mock files for test
    mock_files = [
        SimpleNamespace(ingestion_file_id=1, name="file_a.pdf"),
        SimpleNamespace(ingestion_file_id=2, name="file_b.pdf"),
        SimpleNamespace(ingestion_file_id=3, name="file_c.pdf"),
    ]

    # Mock get_all_files method to return mock files
    monkeypatch.setattr(service.ingestion_repository, "get_all_files", lambda db: mock_files)

    # Mock get_latest_scan_results_for_files method
    monkeypatch.setattr(
        service.scanning_service,
        "get_latest_scan_results_for_files",
        lambda db, file_ids: {1: [], 2: [], 3: []}
    )

    # Mock get_scan_statuses_for_all_files method to return True for all files
    monkeypatch.setattr(
        service.scanning_service,
        "get_scan_statuses_for_all_files",
        lambda db, file_ids: {1: True, 2: True, 3: True}
    )

    # Mock get_employees_with_access_for_files method
    monkeypatch.setattr(
        service.repository,
        "get_employees_with_access_for_files",
        lambda db, file_ids: {1: [], 2: [], 3: []}
    )

    def fake_get_file_risk_details_from_data(
        db,
        file_id,
        file_name,
        latest_scan_results,
        fetched_employees_records,
        has_been_scanned
    ):
        scores = {
            1: 10.0,
            2: 50.0,
            3: 30.0,
        }

        return FileRiskDetailsResponse(
            file_id=file_id,
            file_name=file_name,
            employees_with_access_count=0,
            valid_access_count=0,
            invalid_access_count=0,
            valid_access_percentage=0.0,
            invalid_access_percentage=0.0,
            detection_count=0,
            risk_score=scores[file_id]
        )

    # Mock get_file_risk_details_from_data method to return mocked method returns
    monkeypatch.setattr(service, "get_file_risk_details_from_data", fake_get_file_risk_details_from_data)

    result = service.get_highest_risk_files(db=None, limit=1, offset=1)

    # Ensure limit and offset is applied correctly, only file_id 3 should be returned
    assert result.total == 3
    assert result.limit == 1
    assert result.offset == 1
    assert len(result.items) == 1
    assert result.items[0].file_id == 3


def test_get_highest_risk_files_returns_empty_list_when_no_files(monkeypatch):
    # Mock methods to take no file_ids provided
    monkeypatch.setattr(service.ingestion_repository, "get_all_files", lambda db: [])
    monkeypatch.setattr(service.scanning_service, "get_latest_scan_results_for_files", lambda db, file_ids: {})
    monkeypatch.setattr(service.scanning_service, "get_scan_statuses_for_all_files", lambda db, file_ids: {})
    monkeypatch.setattr(service.repository, "get_employees_with_access_for_files", lambda db, file_ids: {})

    result = service.get_highest_risk_files(db=None, limit=10, offset=0)

    # Ensure result is empty cause no files have been provided in any of the mocked methods
    assert result.items == []
    assert result.total == 0
    assert result.limit == 10
    assert result.offset == 0


# Test that get employee violated files returns employees with correct file mapping (access_allowed=True)
def test_get_employee_violated_files_access_allowed_true(monkeypatch):
    mock_employee = [{"user": SimpleNamespace(user_id=1)}]

    def mock_employee_files(db, user_id):
        return [
            {"file": SimpleNamespace(ingestion_file_id=101)},
            {"file": SimpleNamespace(ingestion_file_id=102)}
        ]

    def mock_employee_files_with_access(db, file_id):
        return [
            {"user_id": 1, "access_allowed": True}
        ]

    monkeypatch.setattr(service.ingestion_repository, "get_user_files", mock_employee_files)
    monkeypatch.setattr(service, "get_file_employees_with_access", mock_employee_files_with_access)

    result = service.get_employee_violated_files(db=None, employees=mock_employee)

    assert len(result[0]["files"]) == 2
    assert result[0]["files"][0]["access_allowed"] is True

# Test that get employee violated files returns employees with correct file mapping (access_allowed=False)
def test_get_employee_violated_files_access_allowed_false(monkeypatch):
    mock_employee = [{"user": SimpleNamespace(user_id=1)}]

    def mock_employee_files(db, user_id):
        return [
            {"file": SimpleNamespace(ingestion_file_id=101)},
            {"file": SimpleNamespace(ingestion_file_id=102)}
        ]

    def mock_employee_files_with_access(db, file_id):
        return [
            {"user_id": 1, "access_allowed": False}
        ]

    monkeypatch.setattr(service.ingestion_repository, "get_user_files", mock_employee_files)
    monkeypatch.setattr(service, "get_file_employees_with_access", mock_employee_files_with_access)

    result = service.get_employee_violated_files(db=None, employees=mock_employee)

    assert len(result[0]["files"]) == 2
    assert result[0]["files"][0]["access_allowed"] is False

# Test determine_employee_risk_from_violated_files when employee has no files
def test_employee_access_allowed_no_files(monkeypatch):
    mock_employee = [{"user": SimpleNamespace(user_id=1)}]

    def mock_get_employee_violated_files(db, employees):
        return [
            {"user": employees[0]["user"], "files": []}
        ]

    monkeypatch.setattr(
        service,
        "get_employee_violated_files",
        mock_get_employee_violated_files
    )

    result = service.determine_employee_risk_from_violated_files(None, mock_employee)

    assert result[0]["files"]["id"] == 1
    assert result[0]["files"]["status"] == "No files found"


# Test determine_employee_risk_from_violated_files when access_allowed is None
def test_employee_access_allowed_all_none(monkeypatch):
    mock_employee = [{"user": SimpleNamespace(user_id=1)}]

    def mock_get_employee_violated_files(db, employees):
        return [
            {
                "user": employees[0]["user"],
                "files": [
                    {"access_allowed": None},
                    {"access_allowed": None}
                ]
            }
        ]

    monkeypatch.setattr(service, "get_employee_violated_files", mock_get_employee_violated_files)

    result = service.determine_employee_risk_from_violated_files(None, mock_employee)

    assert result[0]["files"]["id"] == 2
    assert result[0]["files"]["status"] == "Files not scanned yet"

# Test determine_employee_risk_from_violated_files when access_allowed is False
def test_employee_access_allowed_any_false(monkeypatch):
    mock_employee = [{"user": SimpleNamespace(user_id=1)}]

    def mock_get_employee_violated_files(db, employees):
        return [
            {
                "user": employees[0]["user"],
                "files": [
                    {"access_allowed": True},
                    {"access_allowed": False},
                    {"access_allowed": None}
                ]
            }
        ]

    monkeypatch.setattr(service, "get_employee_violated_files", mock_get_employee_violated_files)

    result = service.determine_employee_risk_from_violated_files(None,  mock_employee)

    assert result[0]["files"]["id"] == 3
    assert result[0]["files"]["status"] == "Risk Detected"
    assert len(result[0]["files"]["flagged_files"]) == 1

# Test determine_employee_risk_from_violated_files when access_allowed is True (no false)
def test_employee_access_allowed_true_no_false(monkeypatch):
    mock_employee = [{"user": SimpleNamespace(user_id=1)}]

    def mock_get_employee_violated_files(db, employees):
        return [
            {
                "user": employees[0]["user"],
                "files": [
                    {"access_allowed": True},
                    {"access_allowed": True}
                ]
            }
        ]

    monkeypatch.setattr(service, "get_employee_violated_files", mock_get_employee_violated_files)

    result = service.determine_employee_risk_from_violated_files(None, mock_employee)

    assert result[0]["files"]["id"] == 4
    assert result[0]["files"]["status"] == "No Risk Detected"
    assert result[0]["files"]["flagged_files"] == []
