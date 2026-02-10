"""
Teste de integridade: verifica que todos os módulos importam corretamente
e que as classes/métodos existem após as refatorações.
"""
import pytest


def test_import_domain_models():
    """Importa todas as classes e enums do domínio."""
    from src.domain.models import (
        Student, Teacher, Parent, Classroom, Assessment, Grade, Attendance,
        Bimester, AssessmentType, EducationLevel, Shift
    )
    # Verifica que são classes
    assert callable(Student)
    assert callable(Assessment)


def test_import_services():
    """Importa todos os serviços."""
    from src.application.services import (
        ServicosDoAluno, ServicosSecretaria,
        BoletimDisciplina, ExtratoPresenca
    )
    assert callable(ServicosDoAluno)
    assert callable(ServicosSecretaria)


def test_import_infrastructure():
    """Importa repositórios e DatabaseManager."""
    from src.infrastructure.database import (
        DatabaseManager, get_database,
        StudentRepository, TeacherRepository, ParentRepository,
        ClassroomRepository, AssessmentRepository, GradeRepository, AttendanceRepository
    )
    assert callable(DatabaseManager)
    assert callable(StudentRepository)


def test_import_utils():
    """Importa funções utilitárias."""
    from src.utils import validar_cpf, validar_email, normalizar_cpf, formatar_cpf, validar_ano_letivo
    assert callable(validar_cpf)
    assert callable(validar_email)


def test_repository_methods_exist():
    """Verifica que repositórios têm os métodos esperados."""
    import inspect
    from src.infrastructure.database import StudentRepository, DatabaseManager

    db = DatabaseManager(":memory:")
    repo = StudentRepository(db)
    methods = [name for name, _ in inspect.getmembers(repo, predicate=inspect.ismethod)]

    assert 'save' in methods
    assert 'find_by_id' in methods
    assert 'list_all' in methods
    assert 'delete' in methods
