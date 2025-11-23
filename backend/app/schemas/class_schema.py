from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ClassBase(BaseModel):
    """Base schema for Class."""
    name: str = Field(..., max_length=100, description="Class name (e.g., '10A', '12 Science B')")
    grade: Optional[str] = Field(None, max_length=50, description="Grade level (e.g., '10', '12')")
    section: Optional[str] = Field(None, max_length=50, description="Section (e.g., 'A', 'B', 'Science')")
    academic_year: Optional[str] = Field(None, max_length=20, description="Academic year (e.g., '2024-2025')")


class ClassCreate(ClassBase):
    """Schema for creating a new class."""
    pass


class ClassUpdate(BaseModel):
    """Schema for updating an existing class."""
    name: Optional[str] = Field(None, max_length=100)
    grade: Optional[str] = Field(None, max_length=50)
    section: Optional[str] = Field(None, max_length=50)
    academic_year: Optional[str] = Field(None, max_length=20)


class ClassRead(ClassBase):
    """Schema for reading class data."""
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class ClassWithStudents(ClassRead):
    """Schema for class with student count."""
    student_count: int = 0

    model_config = {
        "from_attributes": True,
    }
