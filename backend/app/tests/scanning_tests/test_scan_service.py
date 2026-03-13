from app.scanning.service import *


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