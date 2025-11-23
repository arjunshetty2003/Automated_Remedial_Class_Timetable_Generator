"""
Simple script to create database tables in Supabase.
Run this with: python create_tables.py
"""
import asyncio
from app.core.config import get_settings
from app.models.base import Base

# Import all models to ensure they're registered with Base
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.timetable import Timetable


async def create_tables():
    settings = get_settings()

    # Use sync engine for table creation (simpler)
    # Remove +asyncpg and use psycopg2 for sync operations
    sync_url = settings.database_url.replace('+asyncpg', '')

    print(f"Creating tables in database...")
    print(f"Connection: {sync_url.split('@')[1]}")  # Print host only, not password

    try:
        # For table creation, we can use a sync engine
        from sqlalchemy import create_engine
        from sqlalchemy.pool import NullPool

        engine = create_engine(sync_url, poolclass=NullPool, echo=True)

        # Create all tables
        Base.metadata.create_all(bind=engine)

        print("\n✓ Tables created successfully!")
        print("  - students")
        print("  - teachers")
        print("  - timetables")

        engine.dispose()

    except Exception as e:
        print(f"\n✗ Error creating tables: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(create_tables())
