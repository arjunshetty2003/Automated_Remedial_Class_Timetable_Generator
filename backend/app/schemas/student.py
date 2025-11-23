from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field


class SubjectMarkInfo(BaseModel):
    """Subject mark information for nested responses."""

    id: int
    subject_name: str
    marks: int

    model_config = {"from_attributes": True}


class StudentBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr
    marks: int = Field(ge=0, le=30)  # Overall marks for backward compatibility (out of 30)
    availability: str | None = Field(default=None, max_length=1024)
    class_id: int | None = Field(default=None, description="ID of the class this student belongs to")


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    marks: int | None = Field(default=None, ge=0, le=30)
    availability: str | None = Field(default=None, max_length=1024)
    class_id: int | None = Field(default=None, description="ID of the class this student belongs to")


class StudentRead(StudentBase):
    id: int
    created_at: datetime
    subject_marks: List[SubjectMarkInfo] = []  # Subject-wise marks

    model_config = {
        "from_attributes": True,
    }
