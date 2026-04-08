from unittest import result

import pytest

from app.scanning import router, service, repository, models
from app.scanning.scan_type import ScanType

# Create naming convention ids in test database
@pytest.fixture()
def naming_conventions(db):
    db.add_all([
        models.NamingConvention(naming_convention_id=1, name="camel_case"),
        models.NamingConvention(naming_convention_id=2, name="snake_case"),
        models.NamingConvention(naming_convention_id=3, name="pascal_case"),
        models.NamingConvention(naming_convention_id=4, name="kebab_case"),
    ])
    db.commit()


def test_scan_file_with_no_naming_results_returns_empty_list(db):
    # Arrange
    scan = repository.create_scan(db, scan_type=ScanType.ORGANISATION)
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
    repository.create_scan_file(db, scan.scan_id, file.ingestion_file_id)

    # Act

    scan = service.get_organisational_scan_details(db, scan)


    # Assert
    assert scan["files"][0]["naming_convention_scan_results"] == []

def test_scan_file_performed_with_multiple_naming_conventions_returns_results_for_all_naming_conventions(db, naming_conventions):
    # Arrange
    scan = repository.create_scan(db, scan_type=ScanType.ORGANISATION)
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

    # Create scan naming conventions with camel case (1) and snake case (2) check
    scan_naming_convention_1 = repository.create_scan_naming_convention(db, scan.scan_id, 1)
    scan_naming_convention_2 = repository.create_scan_naming_convention(db, scan.scan_id, 2)

    # Create two naming convention scan results for the file (using the scan naming convention ids)
    repository.create_naming_convention_scan_result(db, scan_file.scan_file_id, scan_naming_convention_1.scan_naming_convention_id, False, "testFile")
    repository.create_naming_convention_scan_result(db, scan_file.scan_file_id, scan_naming_convention_2.scan_naming_convention_id, True, "")

    # Act
    perform_scan = service.perform_organisation_scan(db, naming_convention_ids=[1, 2])
    scan = service.get_organisational_scan_details(db, scan)

    # Assert
    results = scan["files"][0]["naming_convention_scan_results"]
    assert len(results) == 2

def test_get_organisational_scan_details_returns_correct_number_of_results(db, naming_conventions):
    # Arrange
    scan = repository.create_scan(db, scan_type=ScanType.ORGANISATION)

    file1 = repository.create_test_file(
        db,
        graph_file_id="abc123",
        file_name="test_file",
        extension=".pdf",
        hash="abc",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file.pdf",
        drive_id="drive123"
    )
    file2 = repository.create_test_file(
        db,
        graph_file_id="def456",
        file_name="test_file_2",
        extension=".pdf",
        hash="def",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file_2.pdf",
        drive_id="drive456"
    )

    scan_file1 = repository.create_scan_file(db, scan.scan_id, file1.ingestion_file_id)
    scan_file2 = repository.create_scan_file(db, scan.scan_id, file2.ingestion_file_id)

    scan_naming_convention_1 = repository.create_scan_naming_convention(db, scan.scan_id, 1)
    scan_naming_convention_2 = repository.create_scan_naming_convention(db, scan.scan_id, 2)

    repository.create_naming_convention_scan_result(db, scan_file1.scan_file_id, scan_naming_convention_1.scan_naming_convention_id, False, "testFile")
    repository.create_naming_convention_scan_result(db, scan_file1.scan_file_id, scan_naming_convention_2.scan_naming_convention_id, True, "")
    repository.create_naming_convention_scan_result(db, scan_file2.scan_file_id, scan_naming_convention_1.scan_naming_convention_id, False, "testFile2")
    repository.create_naming_convention_scan_result(db, scan_file2.scan_file_id, scan_naming_convention_2.scan_naming_convention_id, True, "")

    # Act
    result = service.get_organisational_scan_details(db, scan)

    # Assert
    assert len(result["files"]) == 2

    for file in result["files"]:    
        assert len(file["naming_convention_scan_results"]) == 2
    