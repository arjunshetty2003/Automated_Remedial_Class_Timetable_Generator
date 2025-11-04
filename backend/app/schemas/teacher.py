from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TeacherBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr
    subject: str | None = Field(default=None, max_length=128)
    availability: str | None = Field(default=None, max_length=1024)


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    subject: str | None = Field(default=None, max_length=128)
    availability: str | None = Field(default=None, max_length=1024)


class TeacherRead(TeacherBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
