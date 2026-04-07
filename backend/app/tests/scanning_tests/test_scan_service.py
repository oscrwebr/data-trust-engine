from app.scanning.service import *
from unittest.mock import Mock, patch
from app.ingestion.repository import create_ingestion_file

from datetime import datetime

def test_perform_scan_creates_scan_record(db):
    # Get number of scans before running perform_scan
    scan_counts_before = len(repository.get_all_scans(db))

    # Get result of perform_scan method
    result = perform_scan(db=db, graph_file_ids=["abc123"])

    # Get number of scans after running perform_scan
    scan_counts_after = len(repository.get_all_scans(db))

    # Get created scan record
    scan = repository.get_scan_by_id(db=db, scan_id=result["scan_id"])

    # Ensure that scan was created
    assert scan is not None
    assert scan.scan_id == result["scan_id"]

    # Ensure that number of scans after is 1 bigger than before
    assert scan_counts_after == scan_counts_before + 1


def test_perform_scan_returns_correct_files_requested_count(db):
    # Get result of perform_scan method
    result = perform_scan(db=db, graph_file_ids=["abc123", "def456", "ghi789"])

    # Ensure that 3 files were requested
    assert result["files_requested"] == 3


def test_perform_scan_sets_started_and_finished_timestamps(db):
    # Get result of perform_scan method
    result = perform_scan(db=db, graph_file_ids=["abc123"])

     # Get created scan record
    scan = repository.get_scan_by_id(db=db, scan_id=result["scan_id"])

    # Ensure that scan started_at and finished_at time were updated
    assert scan.started_at is not None
    assert scan.finished_at is not None

    # Ensure that scan finished_at time is equal to or greater than started_at time
    assert scan.finished_at >= scan.started_at


@patch("app.scanning.service.requests.get")
@patch("app.scanning.service.extract_text_from_pdf")
@patch("app.scanning.service.get_download_link_by_graph_id")
def test_scan_file_method_creates_scan_file_record_for_each_file(mock_get_download_link, mock_extract_text, mock_requests_get, db):
    # Mock the file download link to be returned
    mock_get_download_link.return_value = "https://example.com/test_file.pdf"

    # Mock the HTTP response
    mock_response = Mock()
    mock_response.content = b"fake-test-file-bytes"
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response

    # Mock return value of text extraction
    mock_extract_text.return_value = {
        1: "This page contains legal text"
    }

    # Create a test scan record
    scan = repository.create_scan(db=db, scan_type=ScanType.SENSITIVITY)

    # Create a test file record
    test_file = create_ingestion_file(
        db=db,
        graph_id="lc111",
        name="legal_case_report_1.pdf",
        extension="pdf",
        hash="dummyhash",
        hash_type="sha256",
        last_modified=datetime.now(),
        web_url="https://example.com/legal_case_report_1.pdf",
        drive_id="test-drive-id"
    )

    # Scan the test file
    scan_file(db=db, graph_file_id="lc111", scan_id=scan.scan_id)

    # Fetch the scan_file_record which should be created
    scan_file_record = repository.get_scan_file_by_scan_id_and_file_id(
        db=db, 
        scan_id=scan.scan_id, 
        file_id=test_file.ingestion_file_id
    )

    # Ensure scan_file_record has been created
    assert scan_file_record is not None
    assert scan_file_record.scan_id == scan.scan_id
    assert scan_file_record.file_id == test_file.ingestion_file_id


@patch("app.scanning.service.requests.get")
@patch("app.scanning.service.extract_text_from_pdf")
@patch("app.scanning.service.get_download_link_by_graph_id")
def test_scan_file_method_creates_scan_file_detections_for_scan_file(mock_get_download_link, mock_extract_text, mock_requests_get, db):
    # Mock file download link
    mock_get_download_link.return_value = "https://example.com/test_file.pdf"

    # Mock the HTTP response
    mock_response = Mock()
    mock_response.content = b"fake-test-file-bytes"
    mock_response.raise_for_status.return_value = None
    mock_requests_get.return_value = mock_response

    # Mock extracted text
    mock_extract_text.return_value = {
        1: "John Smith johnsmith@email.com [2024] UKSC 1"
    }

    # Create a test scan record
    scan = repository.create_scan(db=db, scan_type=ScanType.SENSITIVITY)

    # Create a test file record
    test_file = create_ingestion_file(
        db=db,
        graph_id="lc111",
        name="legal_case_report_1.pdf",
        extension="pdf",
        hash="dummyhash",
        hash_type="sha256",
        last_modified=datetime.now(),
        web_url="https://example.com/legal_case_report_1.pdf",
        drive_id="test-drive-id"
    )

    # Scan the test file (has graph_file_id lc111)
    scan_file(db=db, graph_file_id="lc111", scan_id=scan.scan_id)

    # Fetch the scan_file_record which should be created
    scan_file_record = repository.get_scan_file_by_scan_id_and_file_id(
        db=db, 
        scan_id=scan.scan_id, 
        file_id=test_file.ingestion_file_id
    )
    
    # Fetch the scan_file_detection records which should be created
    detection_records = repository.get_scan_file_detections_by_scan_file_id(
        db=db,
        scan_file_id=scan_file_record.scan_file_id
    )

    # Ensure that it has created detection records
    assert len(detection_records) > 0                          