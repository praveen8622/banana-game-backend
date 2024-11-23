from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

# Database URL retrieved from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Dependency function to create and close database sessions.
    - Yields: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
