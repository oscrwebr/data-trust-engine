import pytest
from datetime import datetime, timezone

from app.admin_files import repository
from app.ingestion.models import IngestionFile
from app.scanning.models import Scan, ScanFile


def create_file(db, name="test.txt"):
    file = IngestionFile(
        graph_id=f"graph-{name}",
        name=name,
        extension=name.split(".")[-1],
        hash="fake-hash",
        hash_type="sha256",
        last_scanned=None,
        last_modified=datetime.now(timezone.utc),
        web_url="https://test.local/file",
        parent_graph_id=None,
        drive_id="test-drive-id"
    )

    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def create_scan_for_file(db, file):
    # create scan
    scan = Scan(
        scan_type="AUTO",
        started_at=datetime.now(timezone.utc),
        finished_at=datetime.now(timezone.utc)
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    # link scan to file
    scan_file = ScanFile(
        scan_id=scan.scan_id,
        file_id=file.ingestion_file_id
    )
    db.add(scan_file)
    db.commit()

    return scan


def test_get_last_scanned_for_single_file(db):
    file = create_file(db, "a.txt")
    create_scan_for_file(db, file)

    result = repository.get_last_scanned_for_files(
        db,
        [file.ingestion_file_id]
    )

    assert len(result) == 1
    assert result[0]["file_id"] == file.ingestion_file_id
    assert result[0]["graph_file_id"] == file.graph_id
    assert result[0]["last_scanned"] is not None


def test_get_last_scanned_returns_latest_scan(db):
    file = create_file(db, "b.txt")

    create_scan_for_file(db, file)
    create_scan_for_file(db, file)  # newer scan

    result = repository.get_last_scanned_for_files(
        db,
        [file.ingestion_file_id]
    )

    assert len(result) == 1
    assert result[0]["last_scanned"] is not None


def test_get_last_scanned_multiple_files(db):
    file1 = create_file(db, "file1.txt")
    file2 = create_file(db, "file2.txt")

    create_scan_for_file(db, file1)

    result = repository.get_last_scanned_for_files(
        db,
        [file1.ingestion_file_id, file2.ingestion_file_id]
    )

    assert len(result) == 2

    file_ids = {r["file_id"] for r in result}
    assert file1.ingestion_file_id in file_ids
    assert file2.ingestion_file_id in file_ids


def test_get_last_scanned_no_scans(db):
    file = create_file(db, "no_scan.txt")

    result = repository.get_last_scanned_for_files(
        db,
        [file.ingestion_file_id]
    )

    assert len(result) == 1
    assert result[0]["last_scanned"] is None