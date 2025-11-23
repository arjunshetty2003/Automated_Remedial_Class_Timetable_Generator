from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TimetableTypeEnum(str, Enum):
    """Timetable type enum for API."""
    REGULAR = "regular"
    REMEDIAL = "remedial"


class TimetableBase(BaseModel):
    student_id: int | None = Field(default=None, description="Student ID (for individual timetables)")
    class_id: int | None = Field(default=None, description="Class ID (for class-level timetables)")
    teacher_id: int
    timetable_type: TimetableTypeEnum = Field(default=TimetableTypeEnum.REGULAR)
    slot_start: datetime
    slot_end: datetime
    location: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=1024)
    subject: str | None = Field(default=None, max_length=128, description="Subject being taught")


class TimetableCreate(TimetableBase):
    pass


class TimetableRead(TimetableBase):
    id: int

    model_config = {
        "from_attributes": True,
    }
