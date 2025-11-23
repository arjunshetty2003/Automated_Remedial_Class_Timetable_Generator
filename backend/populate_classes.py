"""
Script to populate classes in the database.
Run this FIRST before populating students.
"""

import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings
from app.models.class_model import Class


async def populate_classes():
    """Create initial classes."""
    settings = get_settings()
    engine = create_async_engine(settings.database_url, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # Check if classes already exist
        stmt = select(Class)
        result = await session.execute(stmt)
        existing_classes = result.scalars().all()

        if existing_classes:
            print(f"✓ {len(existing_classes)} classes already exist. Skipping...")
            for cls in existing_classes:
                print(f"  - {cls.name} (ID: {cls.id})")
            return

        # Define classes to create
        classes_data = [
            {
                "name": "10A",
                "grade": "10",
                "section": "A",
                "academic_year": "2024-2025",
            },
            {
                "name": "10B",
                "grade": "10",
                "section": "B",
                "academic_year": "2024-2025",
            },
            {
                "name": "11 Science",
                "grade": "11",
                "section": "Science",
                "academic_year": "2024-2025",
            },
            {
                "name": "12 Science A",
                "grade": "12",
                "section": "Science A",
                "academic_year": "2024-2025",
            },
            {
                "name": "12 Science B",
                "grade": "12",
                "section": "Science B",
                "academic_year": "2024-2025",
            },
        ]

        print("Creating classes...")
        created_classes = []

        for class_data in classes_data:
            new_class = Class(**class_data)
            session.add(new_class)
            created_classes.append(new_class)
            print(f"  + Creating class: {class_data['name']}")

        await session.commit()

        # Refresh to get IDs
        for cls in created_classes:
            await session.refresh(cls)

        print(f"\n✓ Successfully created {len(created_classes)} classes!")
        print("\nClasses created:")
        for cls in created_classes:
            print(f"  - {cls.name} (ID: {cls.id}, Grade: {cls.grade}, Section: {cls.section})")

    await engine.dispose()


if __name__ == "__main__":
    print("=" * 60)
    print("Populating Classes")
    print("=" * 60)
    asyncio.run(populate_classes())
    print("\n✓ Done! You can now run populate_students.py")
