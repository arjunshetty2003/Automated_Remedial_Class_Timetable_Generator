from datetime import datetime

from pydantic import BaseModel, Field


class TimetableBase(BaseModel):
    student_id: int
    teacher_id: int
    slot_start: datetime
    slot_end: datetime
    location: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=1024)


class TimetableCreate(TimetableBase):
    pass


class TimetableRead(TimetableBase):
    id: int

    model_config = {
        "from_attributes": True,
    }
