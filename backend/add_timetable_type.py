#!/usr/bin/env python3
"""
Add timetable_type column to existing timetable table.
This migration adds a column to distinguish between regular and remedial classes.
"""
import asyncio
from sqlalchemy import text
from app.db.session import engine


async def add_timetable_type_column():
    """Add timetable_type column to timetable table."""

    async with engine.begin() as conn:
        # Check if column already exists
        result = await conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='timetable'
            AND column_name='timetable_type';
        """))

        if result.fetchone():
            print("✓ Column 'timetable_type' already exists")
            return

        # Add the column with default value
        print("Adding 'timetable_type' column...")
        await conn.execute(text("""
            ALTER TABLE timetable
            ADD COLUMN timetable_type VARCHAR(20) NOT NULL DEFAULT 'regular';
        """))

        # Create index
        print("Creating index on timetable_type...")
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_timetable_type
            ON timetable(timetable_type);
        """))

        print("✓ Migration completed successfully!")


if __name__ == "__main__":
    print("="*60)
    print("Adding timetable_type column to timetable table")
    print("="*60)
    asyncio.run(add_timetable_type_column())
    print("\nDone!")
