from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from typing import Generator
import os
from dotenv import load_dotenv
from app.models.user import User 

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with connection pool settings
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=5,  # Maximum number of permanent connections
    max_overflow=10,  # Maximum number of additional connections
    pool_timeout=30,  # Timeout in seconds for getting connection from pool
    pool_recycle=1800,  # Recycle connections after 30 minutes
)

# session factory
SessionFactory = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

# thread-safe scoped session
SessionLocal = scoped_session(SessionFactory)

def init_db() -> None:
    """Initialize the database, creating tables if they don't exist."""

    # Creates user table 
    User.metadata.create_all(bind=engine)

def get_session() -> Session:
    """Get the global session instance."""
    return SessionLocal()

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that provides a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Provide a transactional scope around a series of operations."""
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

if __name__ == "__main__":
    init_db()