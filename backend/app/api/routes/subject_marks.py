from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.db.session import get_session
from app.models.subject_mark import SubjectMark
from app.models.student import Student

router = APIRouter(prefix="/subject-marks", tags=["subject-marks"])


@router.get("", response_model=list[schemas.SubjectMarkRead])
async def list_subject_marks(
    student_id: int | None = None, session: AsyncSession = Depends(get_session)
) -> list[schemas.SubjectMarkRead]:
    """List all subject marks, optionally filtered by student_id."""
    query = select(SubjectMark)
    if student_id:
        query = query.where(SubjectMark.student_id == student_id)

    result = await session.scalars(query.order_by(SubjectMark.created_at.desc()))
    marks = result.all()
    return [schemas.SubjectMarkRead.model_validate(mark) for mark in marks]


@router.post("", response_model=schemas.SubjectMarkRead, status_code=status.HTTP_201_CREATED)
async def create_subject_mark(
    payload: schemas.SubjectMarkCreate,
    session: AsyncSession = Depends(get_session),
) -> schemas.SubjectMarkRead:
    """Create a new subject mark for a student."""
    # Verify student exists
    student = await session.get(Student, payload.student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    subject_mark = SubjectMark(**payload.model_dump())
    session.add(subject_mark)
    await session.commit()
    await session.refresh(subject_mark)
    return schemas.SubjectMarkRead.model_validate(subject_mark)


@router.get("/students-failing/{subject_name}", response_model=list[schemas.StudentRead])
async def get_students_failing_subject(
    subject_name: str, session: AsyncSession = Depends(get_session)
) -> list[schemas.StudentRead]:
    """Get all students failing a specific subject (marks < 10)."""
    result = await session.scalars(
        select(Student)
        .join(SubjectMark)
        .where(SubjectMark.subject_name == subject_name)
        .where(SubjectMark.marks < 10)
        .order_by(Student.name)
    )
    students = result.all()
    return [schemas.StudentRead.model_validate(student) for student in students]
