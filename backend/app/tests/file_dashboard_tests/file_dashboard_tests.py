import pytest
from datetime import datetime

from app.file_dashboard import service, repository
from app.ingestion.models import Folder, IngestionFile


# ---------------- Helper functions ----------------

def create_folder(db, name="Folder", graph_id="g1", parent_graph_id=None):
    folder = Folder(
        name=name,
        graph_id=graph_id,
        parent_graph_id=parent_graph_id,
        drive_id="drive1"
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder

def create_file(db, name, graph_id, parent_graph_id=None):
    file = IngestionFile(
        graph_id=graph_id,
        name=name,
        extension=name.split(".")[-1],
        web_url=f"https://test.com/{graph_id}",
        parent_graph_id=parent_graph_id,
        drive_id="drive1",
        last_modified=datetime.utcnow()
    )
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


# ---------------- Folder Tests ----------------

def test_get_root_folders_service(db):
    root = create_folder(db, "Root", "root1")
    child = create_folder(db, "Child", "child1", parent_graph_id="root1")

    result = service.get_root_folders(db)

    assert len(result) == 1
    assert result[0].folder_id == root.folder_id
    assert result[0].name == "Root"


def test_get_subfolders_service(db):
    root = create_folder(db, "Root", "root1")
    child1 = create_folder(db, "Child1", "child1", parent_graph_id="root1")
    child2 = create_folder(db, "Child2", "child2", parent_graph_id="root1")

    result = service.get_subfolders(db, "root1")

    assert len(result) == 2
    names = [f.name for f in result]
    assert "Child1" in names
    assert "Child2" in names


def test_get_subfolders_empty(db):
    create_folder(db, "Root", "root1")

    result = service.get_subfolders(db, "root1")

    assert result == []


# ---------------- File Tests ----------------

def test_get_files_in_folder_service(db):
    folder = create_folder(db, "Root", "root1")

    file1 = create_file(db, "file1.txt", "f1", parent_graph_id="root1")
    file2 = create_file(db, "file2.pdf", "f2", parent_graph_id="root1")

    result = service.get_files_in_folder(db, "root1")

    assert len(result) == 2
    names = [f.name for f in result]
    assert "file1.txt" in names
    assert "file2.pdf" in names


def test_get_files_empty_folder(db):
    create_folder(db, "Root", "root1")

    result = service.get_files_in_folder(db, "root1")

    assert result == []


# ---------------- Combined Behaviour ----------------

def test_folder_and_files_are_isolated(db):
    folder1 = create_folder(db, "Folder1", "g1")
    folder2 = create_folder(db, "Folder2", "g2")

    create_file(db, "file1.txt", "f1", parent_graph_id="g1")
    create_file(db, "file2.txt", "f2", parent_graph_id="g2")

    files_folder1 = service.get_files_in_folder(db, "g1")
    files_folder2 = service.get_files_in_folder(db, "g2")

    assert len(files_folder1) == 1
    assert len(files_folder2) == 1

    assert files_folder1[0].name == "file1.txt"
    assert files_folder2[0].name == "file2.txt"


# ---------------- Edge Cases ----------------

def test_nonexistent_folder_returns_empty(db):
    result_folders = service.get_subfolders(db, "does_not_exist")
    result_files = service.get_files_in_folder(db, "does_not_exist")

    assert result_folders == []
    assert result_files == []