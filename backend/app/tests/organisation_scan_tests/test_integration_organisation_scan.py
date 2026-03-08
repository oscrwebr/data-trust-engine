import pytest
from sqlalchemy import select

from app.scanning import router, service, repository, models

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

def test_organisation_scan_creates_scan_record(db, naming_conventions):
    initial_scans = db.execute(select(models.Scan)).scalars().all()
    initial_scan_length = len(initial_scans)

    service.perform_organisation_scan(db, naming_convention_ids=[1])

    new_scans = db.execute(select(models.Scan)).scalars().all()
    new_scan_length = len(new_scans)

    assert new_scan_length == initial_scan_length + 1