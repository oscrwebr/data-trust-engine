import pytest
from sqlalchemy import select, insert

from app.scanning import router, service, repository, models
from app.scanning.scan_type import ScanType
from app.workspaces.models import Workspace
from app.authentication.models import User
from app.workspaces.models import user_workspace as UserWorkspace
from app.ingestion.models import UserFiles

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

def test_get_scans_with_file_count_includes_correct_file_count(db, naming_conventions, organisation_scan_setup):
    # Arrange
    user, workspace, file = organisation_scan_setup
    # Perform a scan to create a scan record
    scan = service.perform_organisation_scan(db, user_id=user.user_id, naming_convention_ids=[1])

    # Act
    act = service.get_scans_with_file_count(db)

    # Assert
    # Check file_count exists in the response
    assert "file_count" in act[0]
    # Expect only one file since we only created one file associated with the scan
    assert act[0]["file_count"] == 1