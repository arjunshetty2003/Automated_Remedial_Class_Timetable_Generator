"""Models package - imports all models for Alembic to detect."""

from app.models.base import Base
from app.models.class_model import Class
from app.models.student import Student
from app.models.subject_mark import SubjectMark
from app.models.teacher import Teacher
from app.models.timetable import Timetable

__all__ = [
    "Base",
    "Class",
    "Student",
    "SubjectMark",
    "Teacher",
    "Timetable",
]
