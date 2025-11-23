from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import schemas
from app.db.session import get_session
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.timetable import Timetable, TimetableType
from app.services.scheduler import SchedulerService

router = APIRouter(prefix="/timetables", tags=["timetables"])


@router.get("", response_model=list[schemas.TimetableRead])
async def list_timetables(
    timetable_type: str | None = Query(default=None, description="Filter by type: regular or remedial"),
    session: AsyncSession = Depends(get_session)
) -> list[schemas.TimetableRead]:
    """List all timetables, optionally filtered by type."""
    query = select(Timetable).order_by(Timetable.slot_start)

    if timetable_type:
        query = query.where(Timetable.timetable_type == timetable_type)

    result = await session.scalars(query)
    timetables = result.all()
    return [schemas.TimetableRead.model_validate(timetable) for timetable in timetables]


@router.post("", response_model=schemas.TimetableRead, status_code=status.HTTP_201_CREATED)
async def create_timetable(
    payload: schemas.TimetableCreate,
    session: AsyncSession = Depends(get_session),
) -> schemas.TimetableRead:
    timetable = Timetable(**payload.model_dump())
    session.add(timetable)
    await session.commit()
    await session.refresh(timetable)
    return schemas.TimetableRead.model_validate(timetable)


@router.post("/auto", response_model=list[schemas.TimetableRead])
async def auto_generate_timetable(session: AsyncSession = Depends(get_session)) -> list[schemas.TimetableRead]:
    """
    Generate remedial timetable using AI.
    This will avoid conflicts with existing regular timetables.
    """
    scheduler = SchedulerService(session)

    # Get all students with their subject marks eagerly loaded
    student_records = await session.scalars(
        select(Student).options(selectinload(Student.subject_marks))
    )
    teacher_records = await session.scalars(select(Teacher))

    students = [schemas.StudentRead.model_validate(student) for student in student_records.all()]
    teachers = [schemas.TeacherRead.model_validate(teacher) for teacher in teacher_records.all()]

    # Get existing regular timetables to avoid conflicts
    existing_timetables_result = await session.scalars(
        select(Timetable).where(Timetable.timetable_type == TimetableType.REGULAR)
    )
    existing_timetables = [schemas.TimetableRead.model_validate(tt) for tt in existing_timetables_result.all()]

    suggestions = await scheduler.generate_timetable(students, teachers, existing_timetables)
    return suggestions


@router.delete("/{timetable_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timetable(timetable_id: int, session: AsyncSession = Depends(get_session)) -> None:
    timetable = await session.get(Timetable, timetable_id)
    if not timetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable not found")

    await session.delete(timetable)
    await session.commit()
