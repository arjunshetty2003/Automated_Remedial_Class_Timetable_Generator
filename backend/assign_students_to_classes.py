"""
Script to assign existing students to classes.
Run this after populate_classes.py if you already have students in the database.
"""

import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.models.class_model import Class
from app.models.student import Student


async def assign_students_to_classes():
    """Assign existing students to classes."""
    settings = get_settings()
    engine = create_async_engine(settings.database_url, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Get all classes
        stmt = select(Class).order_by(Class.id)
        result = await session.execute(stmt)
        classes = result.scalars().all()

        if not classes:
            print("✗ No classes found! Please run populate_classes.py first.")
            return

        print(f"Found {len(classes)} classes:")
        for cls in classes:
            print(f"  - {cls.name} (ID: {cls.id})")

        # Get all students
        stmt = select(Student).order_by(Student.id)
        result = await session.execute(stmt)
        students = result.scalars().all()

        if not students:
            print("\n✗ No students found! Please create students first.")
            return

        print(f"\nFound {len(students)} students")

        # Distribute students evenly across classes
        print("\nAssigning students to classes...")
        for i, student in enumerate(students):
            class_index = i % len(classes)
            assigned_class = classes[class_index]
            student.class_id = assigned_class.id
            print(f"  - {student.name} → {assigned_class.name}")

        await session.commit()

        # Show summary
        print(f"\n✓ Successfully assigned {len(students)} students to {len(classes)} classes!")
        print("\nClass distribution:")
        for cls in classes:
            stmt = select(Student).where(Student.class_id == cls.id)
            result = await session.execute(stmt)
            students_in_class = result.scalars().all()
            print(f"  - {cls.name}: {len(students_in_class)} students")

    await engine.dispose()


if __name__ == "__main__":
    print("=" * 60)
    print("Assigning Students to Classes")
    print("=" * 60)
    asyncio.run(assign_students_to_classes())
    print("\n✓ Done!")
