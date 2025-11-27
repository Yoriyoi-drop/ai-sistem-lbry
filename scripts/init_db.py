#!/usr/bin/env python3
"""
Script to initialize the database for the Infinite AI Security platform
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from apps.api.src.database.init_db import init_db


def main():
    """
    Initialize the database by creating all tables
    """
    print("Initializing database...")
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()