import pytest, os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from unittest.mock import patch


from app.main import app
from app.core.database import get_database, Base

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DATABASE_USERNAME = os.getenv("DB_USERNAME")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_TEST_NAME = os.getenv("DB_TEST_NAME")

DATABASE_URL = (f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DB_HOST}:3306/{DB_TEST_NAME}")

@pytest.fixture(scope="session") # Runs once per test session (once for all the tests instead of once for each test)
def db_engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine) # creates all the tables within the db
    yield engine # Where pytest allows all the tests to run
    Base.metadata.drop_all(bind=engine) # Where the tables within the db are dropped

@pytest.fixture()
def db(db_engine):
    connection = db_engine.connect() # This opens the connection
    transaction = connection.begin() # Begins a transaction
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestingSession() # This creates the db session for each test
    try:
        yield session # This gives the test the session
    finally:
        session.close()
        transaction.rollback() # ends the transaction
        connection.close()

@pytest.fixture()
def client(db):
    def override_get_db(): # this is what will be passed into all functions that depend on 'get_database()'
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_database] = override_get_db # This is what overrides the normal 'get_database()' dependency 
    with TestClient(app) as client: # This creates a http client so that response.get, response.post can be used
        yield client # This passes that client into the test
    app.dependency_overrides.clear() # This clears the override for 'get_database'

@pytest.fixture()
def mock_delay():
    with patch("app.authentication.service.setup_ingestion_celery.delay") as mock_delay:
        yield mock_delay