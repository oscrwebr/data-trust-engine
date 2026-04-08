import pytest

from app.scanning import router, service, repository, models
from app.scanning.scan_type import ScanType

from app.roles import models as role_models

@pytest.fixture()
def sensitivity_categories(db):
    db.add_all([
        role_models.SensitivityCategory(sensitivity_category_id=1, name="Personal"),
        role_models.SensitivityCategory(sensitivity_category_id=2, name="Financial"),
        role_models.SensitivityCategory(sensitivity_category_id=3, name="Legal Case"),
    ])

    db.add_all([
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=1, sensitivity_category_id=1, name="NAME"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=2, sensitivity_category_id=1, name="PHONE"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=3, sensitivity_category_id=1, name="EMAIL"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=4, sensitivity_category_id=1, name="ADDRESS"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=5, sensitivity_category_id=1, name="POSTCODE"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=6, sensitivity_category_id=2, name="IBAN"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=7, sensitivity_category_id=2, name="VAT"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=8, sensitivity_category_id=3, name="CITATION"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=9, sensitivity_category_id=3, name="ACT"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=10, sensitivity_category_id=3, name="REGULATION"),
        role_models.SensitivitySubcategory(sensitivity_subcategory_id=11, sensitivity_category_id=3, name="CASE_NAME"),
    ])

    db.commit()

def test_sensitivity_scan_with_no_detections_returns_zero_counts(db, sensitivity_categories):
    # Arrange
    scan = repository.create_scan(db, scan_type=ScanType.SENSITIVITY)

    file = repository.create_test_file(
        db,
        graph_file_id="abc123",
        file_name="test_file",
        extension=".pdf",
        hash="abc",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file.pdf",
        drive_id="drive123"
    )
    scan_file = repository.create_scan_file(db, scan.scan_id, file.ingestion_file_id)

    # Act
    scan = service.get_sensitivity_scan_details(db, scan)

    # Assert
    assert scan["detection_counts"]["personal"] == 0
    assert scan["detection_counts"]["financial"] == 0
    assert scan["detection_counts"]["legal_case"] == 0

def test_get_sensitivity_scan_details_correctly_counts_detection_categories(db, sensitivity_categories):
    # Arrange
    scan = repository.create_scan(db, scan_type=ScanType.SENSITIVITY)

    file = repository.create_test_file(
        db,
        graph_file_id="abc123",
        file_name="test_file",
        extension=".pdf",
        hash="abc",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file.pdf",
        drive_id="drive123"
    )

    scan_file = repository.create_scan_file(
        db,
        scan_id=scan.scan_id,
        file_id=file.ingestion_file_id
    )

    # Personal detections
    repository.create_scan_file_detection(db, scan_file.scan_file_id, "NAME", 1)
    repository.create_scan_file_detection(db, scan_file.scan_file_id, "EMAIL", 1)
    # Financial detection
    repository.create_scan_file_detection(db, scan_file.scan_file_id, "IBAN", 1)

    # Act
    scan = service.get_sensitivity_scan_details(db, scan)

    # Assert
    assert "detection_counts" in scan
    assert scan["detection_counts"]["personal"] == 2
    assert scan["detection_counts"]["financial"] == 1
    assert scan["detection_counts"]["legal_case"] == 0

def test_get_sensitivity_scan_details_returns_unique_subcategories(db, sensitivity_categories):
    # Arrange
    scan = repository.create_scan(db, scan_type=ScanType.SENSITIVITY)

    file = repository.create_test_file(
        db,
        graph_file_id="abc123",
        file_name="test_file",
        extension=".pdf",
        hash="abc",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file.pdf",
        drive_id="drive123"
    )
    scan_file = repository.create_scan_file(db, scan.scan_id, file.ingestion_file_id)

    # Create multiple 'NAME' detections (multiple subcategories)
    repository.create_scan_file_detection(db, scan_file.scan_file_id, "NAME", 1)
    repository.create_scan_file_detection(db, scan_file.scan_file_id, "NAME", 2)
    repository.create_scan_file_detection(db, scan_file.scan_file_id, "NAME", 3)

    # Act
    scan = service.get_sensitivity_scan_details(db, scan)

    # Assert
    results = scan["files"][0]["sensitivity_scan_results"]

    # Should only show 'NAME' once
    assert len(results) == 1
    assert results[0]["subcategory_name"] == "NAME"

def test_get_sensitivity_scan_details_returns_subcategories_with_correct_category(db, sensitivity_categories):
    # Arrange
    scan = repository.create_scan(db, scan_type=ScanType.SENSITIVITY)

    file = repository.create_test_file(
        db,
        graph_file_id="abc123",
        file_name="test_file",
        extension=".pdf",
        hash="abc",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file.pdf",
        drive_id="drive123"
    )
    scan_file = repository.create_scan_file(db, scan.scan_id, file.ingestion_file_id)
    # Create one detection for each category
    repository.create_scan_file_detection(db, scan_file.scan_file_id, "NAME", 1)
    repository.create_scan_file_detection(db, scan_file.scan_file_id, "IBAN", 1)
    repository.create_scan_file_detection(db, scan_file.scan_file_id, "CITATION", 1)

    # Act
    scan = service.get_sensitivity_scan_details(db, scan)

    # Assert
    results = scan["files"][0]["sensitivity_scan_results"]

    map = {result["subcategory_name"]: result["category"] for result in results}

    assert map["NAME"] == "Personal"
    assert map["IBAN"] == "Financial"
    assert map["CITATION"] == "Legal Case"

def test_get_sensitivity_scan_details_correctly_counts_detections_with_multiple_files(db, sensitivity_categories):
    # Arrange
    scan = repository.create_scan(db, scan_type=ScanType.SENSITIVITY)

    file1 = repository.create_test_file(
        db,
        graph_file_id="abc123",
        file_name="test_file1",
        extension=".pdf",
        hash="abc",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file1.pdf",
        drive_id="drive123"
    )
    scan_file1 = repository.create_scan_file(db, scan.scan_id, file1.ingestion_file_id)

    file2 = repository.create_test_file(
        db,
        graph_file_id="def456",
        file_name="test_file2",
        extension=".pdf",
        hash="def",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file2.pdf",
        drive_id="drive456"
    )

    scan_file2 = repository.create_scan_file(db, scan.scan_id, file2.ingestion_file_id)

    # Create two personal detections, one financial and one legal detection
    repository.create_scan_file_detection(db, scan_file1.scan_file_id, "NAME", 1)
    repository.create_scan_file_detection(db, scan_file1.scan_file_id, "IBAN", 1)

    repository.create_scan_file_detection(db, scan_file2.scan_file_id, "NAME", 1)
    repository.create_scan_file_detection(db, scan_file2.scan_file_id, "CITATION", 1)

    # Act
    scan = service.get_sensitivity_scan_details(db, scan)

    # Assert
    assert "detection_counts" in scan
    assert scan["detection_counts"]["personal"] == 2
    assert scan["detection_counts"]["financial"] == 1
    assert scan["detection_counts"]["legal_case"] == 1