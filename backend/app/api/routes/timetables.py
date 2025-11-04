from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.db.session import get_session
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.timetable import Timetable
from app.services.scheduler import SchedulerService

router = APIRouter(prefix="/timetables", tags=["timetables"])


@router.get("", response_model=list[schemas.TimetableRead])
async def list_timetables(session: AsyncSession = Depends(get_session)) -> list[schemas.TimetableRead]:
    result = await session.scalars(select(Timetable).order_by(Timetable.slot_start))
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
    scheduler = SchedulerService(session)
    student_records = await session.scalars(select(Student).where(Student.marks < 10))
    teacher_records = await session.scalars(select(Teacher))

    students = [schemas.StudentRead.model_validate(student) for student in student_records.all()]
    teachers = [schemas.TeacherRead.model_validate(teacher) for teacher in teacher_records.all()]

    suggestions = await scheduler.generate_timetable(students, teachers)
    return suggestions


@router.delete("/{timetable_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_timetable(timetable_id: int, session: AsyncSession = Depends(get_session)) -> None:
    timetable = await session.get(Timetable, timetable_id)
    if not timetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable not found")

    await session.delete(timetable)
    await session.commit()
