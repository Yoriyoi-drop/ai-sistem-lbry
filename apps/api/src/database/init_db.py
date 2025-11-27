from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import settings
from .connection import Base
import logging

logger = logging.getLogger(__name__)

def init_db():
    """
    Initialize the database by creating all tables
    """
    # Determine database URL based on backend
    db_url = settings.database_url_computed
    if "postgresql" in db_url and "localhost" in db_url:
        # If using PostgreSQL on localhost, switch to SQLite for development
        db_url = "sqlite:///./infinite_ai_security_dev.db"

    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20
    )
    
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")

if __name__ == "__main__":
    init_db()