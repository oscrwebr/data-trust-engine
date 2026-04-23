import pytest
import secrets
from datetime import datetime

from sqlalchemy import insert

from app.authentication.models import User
from app.workspaces.models import Workspace

from app.ingestion.models import Folder, IngestionFile, UserFolders, UserFiles
from app.file_dashboard import service, repository

def create_admin_user(db, email="admin@test.com"):
    oid = secrets.token_hex(8)

    stmt = insert(User).values(
        firstname="Admin",
        surname="User",
        username=email,
        email=email,
        oid=oid,
        refresh=b"refresh",
        role="admin"
    )

    result = db.execute(stmt)
    db.commit()

    user_id = result.inserted_primary_key[0]
    return db.query(User).filter(User.user_id == user_id).first()


def create_user(db, email="user@test.com"):
    user = User(
        firstname="Test",
        surname="User",
        username=email,
        email=email,
        oid=secrets.token_hex(8),
        refresh=b"refresh",
        role="employee",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_folder(db, name="Folder", graph_id="g1", parent_graph_id=None):
    folder = Folder(
        name=name,
        graph_id=graph_id,
        parent_graph_id=parent_graph_id,
        drive_id="drive-x",
    )
    db.add(folder)
    db.commit()
    db.refresh(folder)
    return folder


def create_file(db, name="file.txt", graph_id="f1", parent_graph_id=None):
    file = IngestionFile(
        name=name,
        extension="txt",
        graph_id=graph_id,
        parent_graph_id=parent_graph_id,
        last_modified=datetime.utcnow(),
        web_url="http://test",
        drive_id="drive-x",
    )
    db.add(file)
    db.commit()
    db.refresh(file)
    return file


def link_folder(db, folder_id, user_id):
    db.add(UserFolders(folder_id=folder_id, user_id=user_id))
    db.commit()


def link_file(db, file_id, user_id):
    db.add(UserFiles(file_id=file_id, user_id=user_id))
    db.commit()


def test_get_root_folders(db):
    user = create_user(db)

    f1 = create_folder(db, "Root1", "r1")
    f2 = create_folder(db, "Root2", "r2", parent_graph_id="r1")  # subfolder

    link_folder(db, f1.folder_id, user.user_id)
    link_folder(db, f2.folder_id, user.user_id)

    result = service.get_root_folders(db, user.user_id)

    assert any(f.graph_id == "r1" for f in result)



def test_get_subfolders(db):
    user = create_user(db)

    parent = create_folder(db, "Parent", "p1")
    child = create_folder(db, "Child", "c1", parent_graph_id="p1")

    link_folder(db, parent.folder_id, user.user_id)
    link_folder(db, child.folder_id, user.user_id)

    result = service.get_subfolders(db, user.user_id, "p1")

    assert len(result) == 1
    assert result[0].graph_id == "c1"



def test_get_files_in_folder(db):
    user = create_user(db)

    create_folder(db, "Root", "r1")

    file1 = create_file(db, "file1.txt", "f1", parent_graph_id="r1")
    file2 = create_file(db, "file2.pdf", "f2", parent_graph_id="r1")

    link_file(db, file1.ingestion_file_id, user.user_id)
    link_file(db, file2.ingestion_file_id, user.user_id)

    result = service.get_files_in_folder(db, user.user_id, "r1")

    assert len(result) == 2
    assert {f.name for f in result} == {"file1.txt", "file2.pdf"}


def test_folder_and_files_are_isolated(db):
    user = create_user(db)

    f1 = create_folder(db, "F1", "g1")
    f2 = create_folder(db, "F2", "g2")

    file1 = create_file(db, "a.txt", "a", "g1")
    file2 = create_file(db, "b.txt", "b", "g2")

    link_folder(db, f1.folder_id, user.user_id)
    link_folder(db, f2.folder_id, user.user_id)

    link_file(db, file1.ingestion_file_id, user.user_id)
    link_file(db, file2.ingestion_file_id, user.user_id)

    r1 = service.get_files_in_folder(db, user.user_id, "g1")
    r2 = service.get_files_in_folder(db, user.user_id, "g2")

    assert len(r1) == 1
    assert len(r2) == 1