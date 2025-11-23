#!/usr/bin/env python3
"""
Script to create the subject_marks table directly in the database.
Run this once to add the new table without affecting existing data.
"""
import asyncio
from sqlalchemy import text
from app.db.session import engine


async def create_subject_marks_table():
    """Create subject_marks table in database."""

    async with engine.begin() as conn:
        # Create table
        await conn.execute(text("""
            CREATE TABLE IF NOT EXISTS subject_marks (
                id SERIAL PRIMARY KEY,
                student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                subject_name VARCHAR(128) NOT NULL,
                marks INTEGER NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """))
        print("✓ subject_marks table created")

        # Create indexes
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_subject_marks_id ON subject_marks(id)
        """))
        print("✓ Index on id created")

        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_subject_marks_student_id ON subject_marks(student_id)
        """))
        print("✓ Index on student_id created")

        print("\n✅ subject_marks table created successfully!")


if __name__ == "__main__":
    asyncio.run(create_subject_marks_table())
