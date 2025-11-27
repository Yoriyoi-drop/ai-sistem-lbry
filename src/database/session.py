"""
Database session factory for Infinite AI Security Platform
"""
from .connection import SessionLocal
from contextlib import contextmanager


@contextmanager
def get_db_session():
    """
    Context manager for database sessions
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    """
    Get database session for dependency injection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()