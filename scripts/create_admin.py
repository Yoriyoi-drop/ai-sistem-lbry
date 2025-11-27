#!/usr/bin/env python3
"""
Script to create an admin user for the Infinite AI Security platform
"""
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import settings first to configure the database
from apps.api.src.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apps.api.src.models.user import User
from apps.api.src.utils.security import get_password_hash


def create_admin_user():
    """
    Create an admin user in the database
    """
    print("Creating admin user...")

    # Determine database URL based on backend (same logic as connection.py)
    db_url = settings.database_url_computed
    if "postgresql" in db_url and "localhost" in db_url:
        # If using PostgreSQL on localhost, switch to SQLite for development
        db_url = "sqlite:///./infinite_ai_security_dev.db"

    # Create engine with the same database URL as connection.py
    engine = create_engine(
        db_url,
        pool_pre_ping=True,
        pool_recycle=300,
        pool_size=10,
        max_overflow=20
    )

    # Import Base to ensure models are registered
    from apps.api.src.database.connection import Base

    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == "admin@infinite-ai.local").first()
        if existing_admin:
            print("Admin user already exists. Skipping creation.")
            return

        # Create hashed password (use shorter password to avoid bcrypt issues)
        password_hash = get_password_hash("Admin123")

        # Create admin user
        admin_user = User(
            email="admin@infinite-ai.local",
            username="admin",
            full_name="Admin User",
            hashed_password=password_hash,
            is_active=True,
            is_superuser=True
        )

        # Add to database
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"Admin user created successfully with ID: {admin_user.id}")
        print(f"Email: admin@infinite-ai.local")
        print(f"Password: Admin123")

    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()