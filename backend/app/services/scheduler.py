from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas


class SchedulerService:
    """Coordinates AI-assisted timetable generation."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def generate_timetable(
        self,
        students: Sequence[schemas.StudentRead],
        teachers: Sequence[schemas.TeacherRead],
    ) -> list[schemas.TimetableRead]:
        # TODO: integrate LangChain flow per PRD; returning empty list for now.
        return []
