from .health import router as health_router
from .students import router as students_router
from .teachers import router as teachers_router
from .timetables import router as timetables_router

__all__ = [
    "health_router",
    "students_router",
    "teachers_router",
    "timetables_router",
]
