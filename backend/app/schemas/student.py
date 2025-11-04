from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: EmailStr
    marks: int = Field(ge=0, le=100)
    availability: str | None = Field(default=None, max_length=1024)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    marks: int | None = Field(default=None, ge=0, le=100)
    availability: str | None = Field(default=None, max_length=1024)


class StudentRead(StudentBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
