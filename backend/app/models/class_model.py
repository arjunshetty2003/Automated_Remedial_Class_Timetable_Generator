from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.student import Student
    from app.models.timetable import Timetable


class Class(Base):
    """Represents a class/section containing multiple students."""

    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)  # e.g., "10A", "12 Science B"
    grade: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., "10", "12"
    section: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., "A", "B", "Science"
    academic_year: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # e.g., "2024-2025"
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    students: Mapped[List["Student"]] = relationship(back_populates="class_", cascade="all, delete-orphan")
    timetables: Mapped[List["Timetable"]] = relationship(back_populates="class_", cascade="all, delete-orphan")
