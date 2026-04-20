from unittest.mock import Mock

import pytest
import app.scanning.service as service
import app.scanning.repository as repository
import app.scanning.models as models
from app.roles.models import SensitivityCategory, SensitivitySubcategory
from app.scanning.scan_type import ScanType

@pytest.fixture
def sensitivity_categories(db):
    personal = SensitivityCategory(name="Personal")
    financial = SensitivityCategory(name="Financial")
    legal = SensitivityCategory(name="Legal Case")
    db.add_all([personal, financial, legal])
    db.commit()

    db.add_all([
        SensitivitySubcategory(name="NAME", sensitivity_category_id=personal.sensitivity_category_id),
        SensitivitySubcategory(name="PHONE", sensitivity_category_id=personal.sensitivity_category_id),
        SensitivitySubcategory(name="EMAIL", sensitivity_category_id=personal.sensitivity_category_id),
        SensitivitySubcategory(name="ADDRESS", sensitivity_category_id=personal.sensitivity_category_id),
        SensitivitySubcategory(name="POSTCODE", sensitivity_category_id=personal.sensitivity_category_id),

        SensitivitySubcategory(name="IBAN", sensitivity_category_id=financial.sensitivity_category_id),
        SensitivitySubcategory(name="VAT", sensitivity_category_id=financial.sensitivity_category_id),

        SensitivitySubcategory(name="CITATION", sensitivity_category_id=legal.sensitivity_category_id),
        SensitivitySubcategory(name="ACT", sensitivity_category_id=legal.sensitivity_category_id),
        SensitivitySubcategory(name="REGULATION", sensitivity_category_id=legal.sensitivity_category_id),
        SensitivitySubcategory(name="CASE_NAME", sensitivity_category_id=legal.sensitivity_category_id),
    ])
    db.commit()

@pytest.fixture
def scan_setup(db):
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

    scan = repository.create_scan(db, ScanType.SENSITIVITY)

    scan_file = repository.create_scan_file(db, scan.scan_id, file.ingestion_file_id)

    return file, scan, scan_file


def test_get_scan_file_details_orders_by_page_number(db, sensitivity_categories, scan_setup):
    file, scan, scan_file = scan_setup

    db.add_all([
        models.ScanFileDetection(
            scan_file_id=scan_file.scan_file_id,
            sensitivity_subcategory="NAME",
            page_number=2
        ),
        models.ScanFileDetection(
            scan_file_id=scan_file.scan_file_id,
            sensitivity_subcategory="IBAN",
            page_number=1
        ),
        models.ScanFileDetection(
            scan_file_id=scan_file.scan_file_id,
            sensitivity_subcategory="POSTCODE",
            page_number=3
        )
    ])
    db.commit()

    query = repository.get_scan_file_details(db, scan_file.scan_file_id)

    page_numbers = [detection.page_number for detection, _ in query]

    # Check page numbers are correctly ordered
    assert page_numbers == [1, 2, 3]

def test_get_scan_file_details_correctly_counts_detections(db, sensitivity_categories, scan_setup):
    file, scan, scan_file = scan_setup

    db.add_all([
        models.ScanFileDetection(
            scan_file_id=scan_file.scan_file_id,
            sensitivity_subcategory="NAME",
            page_number=1
        ),
        models.ScanFileDetection(
            scan_file_id=scan_file.scan_file_id,
            sensitivity_subcategory="NAME",
            page_number=1
        ),
        models.ScanFileDetection(
            scan_file_id=scan_file.scan_file_id,
            sensitivity_subcategory="IBAN",
            page_number=1
        ),
        models.ScanFileDetection(
            scan_file_id=scan_file.scan_file_id,
            sensitivity_subcategory="VAT",
            page_number=1
        ),
        models.ScanFileDetection(
            scan_file_id=scan_file.scan_file_id,
            sensitivity_subcategory="CITATION",
            page_number=1
        )

    ])
    db.commit()

    query = service.get_scan_file_details(db, scan_file.scan_file_id)

    assert query["total_detections"] == 5
    assert query["category_counts"]["personal"] == 2
    assert query["category_counts"]["financial"] == 2
    assert query["category_counts"]["legal_case"] == 1


def test_get_scan_file_details_returns_empty_list_if_no_detections(db, sensitivity_categories, scan_setup):
    file, scan, scan_file = scan_setup

    query = service.get_scan_file_details(db, scan_file.scan_file_id)

    assert query["total_detections"] == 0
    assert query["category_counts"] == {
        "personal": 0,
        "financial": 0,
        "legal_case": 0
    }

def test_get_scan_file_details_for_organisational_scan_file_returns_none(db, sensitivity_categories, scan_setup):
    file, scan, scan_file = scan_setup

    scan.scan_type = ScanType.ORGANISATION
    db.commit()

    query = service.get_scan_file_details(db, scan_file.scan_file_id)

    assert query is None

def test_get_scan_file_details_for_invalid_scan_file_returns_none(db, sensitivity_categories):
    query = service.get_scan_file_details(db, 100000)

    assert query is None

def test_get_scan_file_details_returns_correct_detection_details(db, sensitivity_categories, scan_setup):
    file, scan, scan_file = scan_setup

    db.add(models.ScanFileDetection(
        scan_file_id=scan_file.scan_file_id,
        sensitivity_subcategory="NAME",
        page_number=1
    ))
    db.commit()

    query = service.get_scan_file_details(db, scan_file.scan_file_id)

    assert len(query["detections"]) == 1
    assert query["detections"][0]["category"] == "Personal"
    assert query["detections"][0]["subcategory"] == "NAME"
    assert query["detections"][0]["page_number"] == 1
