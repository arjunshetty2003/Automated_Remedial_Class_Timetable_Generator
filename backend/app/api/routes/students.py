from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import schemas
from app.db.session import get_session
from app.models.student import Student

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[schemas.StudentRead])
async def list_students(session: AsyncSession = Depends(get_session)) -> list[schemas.StudentRead]:
    result = await session.scalars(
        select(Student).options(selectinload(Student.subject_marks)).order_by(Student.created_at.desc())
    )
    students = result.all()
    return [schemas.StudentRead.model_validate(student) for student in students]


@router.post("", response_model=schemas.StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(
    payload: schemas.StudentCreate,
    session: AsyncSession = Depends(get_session),
) -> schemas.StudentRead:
    student = Student(**payload.model_dump())
    session.add(student)
    await session.commit()
    await session.refresh(student)
    return schemas.StudentRead.model_validate(student)


@router.get("/{student_id}", response_model=schemas.StudentRead)
async def get_student(student_id: int, session: AsyncSession = Depends(get_session)) -> schemas.StudentRead:
    student = await session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return schemas.StudentRead.model_validate(student)


@router.patch("/{student_id}", response_model=schemas.StudentRead)
async def update_student(
    student_id: int,
    payload: schemas.StudentUpdate,
    session: AsyncSession = Depends(get_session),
) -> schemas.StudentRead:
    student = await session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(student, field, value)

    await session.commit()
    await session.refresh(student)
    return schemas.StudentRead.model_validate(student)
