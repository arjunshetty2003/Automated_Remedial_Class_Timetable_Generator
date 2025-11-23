from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubjectMarkBase(BaseModel):
    """Base schema for subject marks."""

    subject_name: str
    marks: int  # Marks out of 30


class SubjectMarkCreate(SubjectMarkBase):
    """Schema for creating a subject mark."""

    student_id: int


class SubjectMarkRead(SubjectMarkBase):
    """Schema for reading a subject mark."""

    id: int
    student_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
