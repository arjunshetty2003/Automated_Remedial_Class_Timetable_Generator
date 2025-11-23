from .classes import router as classes_router
from .health import router as health_router
from .students import router as students_router
from .subject_marks import router as subject_marks_router
from .teachers import router as teachers_router
from .timetables import router as timetables_router

__all__ = [
    "classes_router",
    "health_router",
    "students_router",
    "subject_marks_router",
    "teachers_router",
    "timetables_router",
]
