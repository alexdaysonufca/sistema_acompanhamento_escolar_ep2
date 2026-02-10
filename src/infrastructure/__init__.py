"""Banco de dados e repositórios."""

from .database import (
    DatabaseManager,
    get_database,
    StudentRepository,
    TeacherRepository,
    ParentRepository,
    ClassroomRepository,
    AssessmentRepository,
    GradeRepository,
    AttendanceRepository
)

__all__ = [
    'DatabaseManager',
    'get_database',
    'StudentRepository',
    'TeacherRepository',
    'ParentRepository',
    'ClassroomRepository',
    'AssessmentRepository',
    'GradeRepository',
    'AttendanceRepository',
]
