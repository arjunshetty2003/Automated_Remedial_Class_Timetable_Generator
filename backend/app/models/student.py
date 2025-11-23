from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.timetable import Timetable
    from app.models.subject_mark import SubjectMark
    from app.models.class_model import Class


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    marks: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # Overall marks (kept for backward compatibility)
    availability: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    class_id: Mapped[Optional[int]] = mapped_column(ForeignKey("classes.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    # Relationships
    class_: Mapped[Optional["Class"]] = relationship(back_populates="students")
    timetables: Mapped[List["Timetable"]] = relationship(back_populates="student", cascade="all, delete-orphan")
    subject_marks: Mapped[List["SubjectMark"]] = relationship(back_populates="student", cascade="all, delete-orphan")
