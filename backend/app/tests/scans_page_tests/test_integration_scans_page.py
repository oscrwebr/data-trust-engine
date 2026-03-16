import pytest
from sqlalchemy import select

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


def test_get_scans_with_file_count_gets_all_scans(db, naming_conventions):
    # Arrange
    scan1 = repository.create_scan(db, scan_type=ScanType.ORGANISATION)
    scan2 = repository.create_scan(db, scan_type=ScanType.ORGANISATION)
    scan3 = repository.create_scan(db, scan_type=ScanType.SENSITIVITY)

    # Act
    act = service.get_scans_with_file_count(db)

    # Assert
    # Check that all three scans are returned
    assert len(act) == 3
    assert act[0]["scan_id"] == scan1.scan_id
    assert act[1]["scan_id"] == scan2.scan_id
    assert act[2]["scan_id"] == scan3.scan_id

def test_get_scans_with_file_count_includes_correct_file_count(db, naming_conventions):
    # Arrange
    # Perform a scan to create a scan record
    scan = service.perform_organisation_scan(db, naming_convention_ids=[1])
    # Create a file
    file = repository.create_test_file(db, graph_file_id="test_graph_file_id", file_name="employee_salary_report", hash="testhash")
    # Create a scan_file record to associate the file with the scan
    repository.create_scan_file(db, scan_id=scan.scan_id, file_id=file.file_id)

    # Act
    act = service.get_scans_with_file_count(db)

    # Assert
    # Check file_count exists in the response
    assert "file_count" in act[0]
    # Expect only one file since we only created one file associated with the scan
    assert act[0]["file_count"] == 1

def test_get_scans_with_file_count_returns_zero_for_scans_with_no_files(db, naming_conventions):
    # Arrange
    # Perform a scan to create a scan record
    service.perform_organisation_scan(db, naming_convention_ids=[1])

    # Act
    act = service.get_scans_with_file_count(db)

    # Assert
    # Expect no files since we didn't create any files associated with the scan
    assert act[0]["file_count"] == 0