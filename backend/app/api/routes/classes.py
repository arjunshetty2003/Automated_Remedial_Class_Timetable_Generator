from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.db.session import get_session
from app.models.class_model import Class
from app.models.student import Student

router = APIRouter(prefix="/classes", tags=["classes"])


@router.post("/", response_model=schemas.ClassRead, status_code=status.HTTP_201_CREATED)
async def create_class(
    class_in: schemas.ClassCreate,
    session: AsyncSession = Depends(get_session),
) -> Class:
    """Create a new class."""
    # Check if class with same name already exists
    stmt = select(Class).where(Class.name == class_in.name)
    result = await session.execute(stmt)
    existing_class = result.scalar_one_or_none()

    if existing_class:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Class with name '{class_in.name}' already exists",
        )

    new_class = Class(**class_in.model_dump())
    session.add(new_class)
    await session.commit()
    await session.refresh(new_class)
    return new_class


@router.get("/", response_model=List[schemas.ClassWithStudents])
async def list_classes(
    session: AsyncSession = Depends(get_session),
) -> List[dict]:
    """List all classes with student count."""
    stmt = (
        select(Class, func.count(Student.id).label("student_count"))
        .outerjoin(Student, Student.class_id == Class.id)
        .group_by(Class.id)
        .order_by(Class.name)
    )
    result = await session.execute(stmt)
    rows = result.all()

    classes_with_count = []
    for class_obj, student_count in rows:
        class_dict = {
            "id": class_obj.id,
            "name": class_obj.name,
            "grade": class_obj.grade,
            "section": class_obj.section,
            "academic_year": class_obj.academic_year,
            "created_at": class_obj.created_at,
            "student_count": student_count,
        }
        classes_with_count.append(class_dict)

    return classes_with_count


@router.get("/{class_id}", response_model=schemas.ClassRead)
async def get_class(
    class_id: int,
    session: AsyncSession = Depends(get_session),
) -> Class:
    """Get a specific class by ID."""
    stmt = select(Class).where(Class.id == class_id)
    result = await session.execute(stmt)
    class_obj = result.scalar_one_or_none()

    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {class_id} not found",
        )

    return class_obj


@router.get("/{class_id}/students", response_model=List[schemas.StudentRead])
async def get_class_students(
    class_id: int,
    session: AsyncSession = Depends(get_session),
) -> List[Student]:
    """Get all students in a specific class."""
    # Check if class exists
    stmt = select(Class).where(Class.id == class_id)
    result = await session.execute(stmt)
    class_obj = result.scalar_one_or_none()

    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {class_id} not found",
        )

    # Get students
    stmt = select(Student).where(Student.class_id == class_id).order_by(Student.name)
    result = await session.execute(stmt)
    students = result.scalars().all()

    return list(students)


@router.put("/{class_id}", response_model=schemas.ClassRead)
async def update_class(
    class_id: int,
    class_update: schemas.ClassUpdate,
    session: AsyncSession = Depends(get_session),
) -> Class:
    """Update a class."""
    stmt = select(Class).where(Class.id == class_id)
    result = await session.execute(stmt)
    class_obj = result.scalar_one_or_none()

    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {class_id} not found",
        )

    # Update fields
    update_data = class_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(class_obj, field, value)

    await session.commit()
    await session.refresh(class_obj)
    return class_obj


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    class_id: int,
    session: AsyncSession = Depends(get_session),
) -> None:
    """Delete a class."""
    stmt = select(Class).where(Class.id == class_id)
    result = await session.execute(stmt)
    class_obj = result.scalar_one_or_none()

    if not class_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Class with id {class_id} not found",
        )

    await session.delete(class_obj)
    await session.commit()
