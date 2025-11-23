from .class_schema import ClassCreate, ClassRead, ClassUpdate, ClassWithStudents
from .student import StudentCreate, StudentRead, StudentUpdate
from .subject_mark import SubjectMarkCreate, SubjectMarkRead
from .teacher import TeacherCreate, TeacherRead, TeacherUpdate
from .timetable import TimetableCreate, TimetableRead

__all__ = [
    "ClassCreate",
    "ClassRead",
    "ClassUpdate",
    "ClassWithStudents",
    "StudentCreate",
    "StudentRead",
    "StudentUpdate",
    "SubjectMarkCreate",
    "SubjectMarkRead",
    "TeacherCreate",
    "TeacherRead",
    "TeacherUpdate",
    "TimetableCreate",
    "TimetableRead",
]
