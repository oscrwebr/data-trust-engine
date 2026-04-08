import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DATABASE_USERNAME = os.getenv("DB_USERNAME")
DATABASE_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DB_HOST}:3306/{DB_NAME}")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()