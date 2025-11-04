from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.db.session import get_session
from app.models.teacher import Teacher

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("", response_model=list[schemas.TeacherRead])
async def list_teachers(session: AsyncSession = Depends(get_session)) -> list[schemas.TeacherRead]:
    result = await session.scalars(select(Teacher).order_by(Teacher.created_at.desc()))
    teachers = result.all()
    return [schemas.TeacherRead.model_validate(teacher) for teacher in teachers]


@router.post("", response_model=schemas.TeacherRead, status_code=status.HTTP_201_CREATED)
async def create_teacher(
    payload: schemas.TeacherCreate,
    session: AsyncSession = Depends(get_session),
) -> schemas.TeacherRead:
    teacher = Teacher(**payload.model_dump())
    session.add(teacher)
    await session.commit()
    await session.refresh(teacher)
    return schemas.TeacherRead.model_validate(teacher)


@router.get("/{teacher_id}", response_model=schemas.TeacherRead)
async def get_teacher(teacher_id: int, session: AsyncSession = Depends(get_session)) -> schemas.TeacherRead:
    teacher = await session.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return schemas.TeacherRead.model_validate(teacher)


@router.patch("/{teacher_id}", response_model=schemas.TeacherRead)
async def update_teacher(
    teacher_id: int,
    payload: schemas.TeacherUpdate,
    session: AsyncSession = Depends(get_session),
) -> schemas.TeacherRead:
    teacher = await session.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(teacher, field, value)

    await session.commit()
    await session.refresh(teacher)
    return schemas.TeacherRead.model_validate(teacher)
