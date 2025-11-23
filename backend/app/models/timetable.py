from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.class_model import Class


class TimetableType(str, enum.Enum):
    """Enum for timetable types."""
    REGULAR = "regular"
    REMEDIAL = "remedial"


class Timetable(Base):
    __tablename__ = "timetable"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Support both individual student timetables and class-level timetables
    # For class-level: class_id is set, student_id is NULL
    # For individual: student_id is set, class_id is NULL
    # For remedial: always student_id (individual)
    student_id: Mapped[Optional[int]] = mapped_column(ForeignKey("students.id", ondelete="CASCADE"), nullable=True, index=True)
    class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("classes.id", ondelete="CASCADE"), nullable=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)

    timetable_type: Mapped[TimetableType] = mapped_column(
        Enum(TimetableType, native_enum=False, length=20),
        nullable=False,
        default=TimetableType.REGULAR,
        index=True
    )
    slot_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    slot_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    subject: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)  # Subject being taught

    # Relationships
    student = relationship("Student", back_populates="timetables")
    class_ = relationship("Class", back_populates="timetables")
    teacher = relationship("Teacher", back_populates="timetables")
