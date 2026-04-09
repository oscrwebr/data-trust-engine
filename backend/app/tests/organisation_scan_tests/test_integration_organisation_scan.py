import pytest
from sqlalchemy import select, insert

from app.scanning import router, service, repository, models
from app.workspaces.models import Workspace
from app.authentication.models import User
from app.workspaces.models import user_workspace as UserWorkspace
from app.ingestion.models import UserFiles

def test_cannot_get_organisation_scan_endpoint(client):
    response = client.get("/scanning/organisation_scan")
    assert response.status_code == 405

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

@pytest.fixture()
def organisation_scan_setup(db):
    # Create workspace model
    workspace = Workspace(name="Test Workspace", image=b"image")
    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    # Create a user
    user = User(
        firstname="Test",
        surname="User",
        username="test.user@example.com",
        email="test.user@example.com",
        oid="test-oid",
        refresh=b"refresh",
        role="admin")
    db.add(user)
    db.commit()
    db.refresh(user)

    # Add user to workspace using UserWorkspace table
    db.execute(
        insert(UserWorkspace).values(
            user_id=user.user_id,
            workspace_id=workspace.id
        )
    )
    db.commit()

    # Create file
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
    # Add file to UserFile table
    db.add(UserFiles(
        user_id=user.user_id,
        file_id=file.ingestion_file_id
    ))
    db.commit()

    return user, workspace, file


# Test the scan creates a scan record in the database
def test_organisation_scan_creates_scan_record(db, naming_conventions, organisation_scan_setup):
    user, workspace, file = organisation_scan_setup
    initial_scans = db.execute(select(models.Scan)).scalars().all()
    initial_scan_length = len(initial_scans)

    service.perform_organisation_scan(db, user_id=user.user_id, naming_convention_ids=[1])

    new_scans = db.execute(select(models.Scan)).scalars().all()
    new_scan_length = len(new_scans)

    assert new_scan_length == initial_scan_length + 1

# Test the scan creates a scan_naming_convention record in the database (to identify what naming conventions each scan uses)
def test_organisation_scan_creates_scan_naming_convention_record(db, naming_conventions, organisation_scan_setup):
    user, workspace, file = organisation_scan_setup
    initial_scan_naming_conventions = db.execute(select(models.ScanNamingConvention)).scalars().all()
    initial_scan_naming_convention_length = len(initial_scan_naming_conventions)

    service.perform_organisation_scan(db, user_id=user.user_id, naming_convention_ids=[1])

    new_scan_naming_conventions = db.execute(select(models.ScanNamingConvention)).scalars().all()
    new_scan_naming_convention_length = len(new_scan_naming_conventions)

    assert new_scan_naming_convention_length == initial_scan_naming_convention_length + 1

# When selecting multiple naming conventions, check that the scan creates two scan_naming_convention records instead of one
def test_organisation_scan_with_two_naming_conventions_creates_scan_naming_convention_records(db, naming_conventions, organisation_scan_setup):
    user, workspace, file = organisation_scan_setup
    initial_scan_naming_conventions = db.execute(select(models.ScanNamingConvention)).scalars().all()
    initial_scan_naming_convention_length = len(initial_scan_naming_conventions)

    service.perform_organisation_scan(db, user_id=user.user_id, naming_convention_ids=[1, 2])

    new_scan_naming_conventions = db.execute(select(models.ScanNamingConvention)).scalars().all()
    new_scan_naming_convention_length = len(new_scan_naming_conventions)

    assert new_scan_naming_convention_length == initial_scan_naming_convention_length + 2
# Test that the scan creates a naming_convention_scan_result record in the database
def test_organisation_scan_creates_naming_convention_scan_result_record(db, naming_conventions, organisation_scan_setup):
    user, workspace, file = organisation_scan_setup
    initial_naming_convention_scan_results = db.execute(select(models.NamingConventionScanResult)).scalars().all()
    initial_naming_convention_scan_result_length = len(initial_naming_convention_scan_results)

    service.perform_organisation_scan(db, user_id=user.user_id, naming_convention_ids=[1])

    new_naming_convention_scan_results = db.execute(select(models.NamingConventionScanResult)).scalars().all()
    new_naming_convention_scan_result_length = len(new_naming_convention_scan_results)

    assert new_naming_convention_scan_result_length > initial_naming_convention_scan_result_length

def test_valid_file_name_passes_scan(db, naming_conventions, organisation_scan_setup):
    user, workspace, file = organisation_scan_setup
    # Create a file with a valid name for snake case
    file = repository.create_test_file(
        db,
        graph_file_id="abc123",
        file_name="employee_salary_report",
        extension=".pdf",
        hash="abc",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file.pdf",
        drive_id="drive123"
    )
    # Snake case scan (id = 2)
    service.perform_organisation_scan(db, user_id=user.user_id, naming_convention_ids=[2])

    naming_convention_scan_results = db.execute(select(models.NamingConventionScanResult)).scalars().all()
    assert len(naming_convention_scan_results) == 1
    assert naming_convention_scan_results[0].passed == True

def test_invalid_file_name_fails_scan(db, naming_conventions, organisation_scan_setup):
    user, workspace, file = organisation_scan_setup
    # Create a file with an invalid name for camel case
    file = repository.create_test_file(
        db,
        graph_file_id="abc123",
        file_name="employee_salary_report",
        extension=".pdf",
        hash="abc",
        last_modified="2024-01-01 00:00:00",
        web_url="http://example.com/test_file.pdf",
        drive_id="drive123"
    )

    db.add(UserFiles(
        user_id=user.user_id,
        file_id=file.ingestion_file_id
    ) )
    db.commit()

    # Camel case scan (id = 1)
    service.perform_organisation_scan(db, user_id=user.user_id, naming_convention_ids=[1])

    naming_convention_scan_results = db.execute(select(models.NamingConventionScanResult)).scalars().all()
    assert any(result.passed is False for result in naming_convention_scan_results)