"""
Teste de Integração: Repositórios com banco SQLite real.

Valida que o SQL manual está correto:
- Syntax SQL válida
- Constraints funcionando
- Conversões Python <-> SQLite
- JOINs e agregações
"""
import pytest
import sqlite3
from pathlib import Path
from datetime import date, datetime

from src.infrastructure.database import (
    DatabaseManager,
    StudentRepository, TeacherRepository, ParentRepository,
    ClassroomRepository, AssessmentRepository, GradeRepository, AttendanceRepository
)
from src.domain.models import (
    Student, Teacher, Parent, Classroom, Assessment, Grade, Attendance,
    EducationLevel, Shift, Bimester, AssessmentType
)


@pytest.fixture
def db_manager(tmp_path):
    """Cria banco temporário para testes."""
    db_path = str(tmp_path / "test_school.db")
    manager = DatabaseManager(db_path)
    # Aplicar schema silenciosamente
    schema_file = Path(__file__).parent.parent.parent / "src" / "infrastructure" / "schema.sql"
    conn = manager.get_connection()
    with open(schema_file, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    yield manager


@pytest.fixture
def student_repo(db_manager):
    return StudentRepository(db_manager)


@pytest.fixture
def teacher_repo(db_manager):
    return TeacherRepository(db_manager)


@pytest.fixture
def parent_repo(db_manager):
    return ParentRepository(db_manager)


@pytest.fixture
def classroom_repo(db_manager):
    return ClassroomRepository(db_manager)


@pytest.fixture
def assessment_repo(db_manager):
    return AssessmentRepository(db_manager)


@pytest.fixture
def grade_repo(db_manager):
    return GradeRepository(db_manager)


@pytest.fixture
def attendance_repo(db_manager):
    return AttendanceRepository(db_manager)


# =============================================================================
# STUDENT REPOSITORY
# =============================================================================

def test_student_crud(student_repo):
    """CRUD completo de estudantes."""
    # CREATE
    student = Student(name="João Silva", registration="2024001", email="joao@escola.com")
    student_repo.save(student)
    assert student.id is not None

    # READ
    found = student_repo.find_by_id(student.id)
    assert found is not None
    assert found.name == "João Silva"
    assert found.registration == "2024001"
    assert found.email == "joao@escola.com"

    # UPDATE
    student.name = "João Pedro Silva"
    student_repo.save(student)
    updated = student_repo.find_by_id(student.id)
    assert updated.name == "João Pedro Silva"

    # LIST
    all_students = student_repo.list_all()
    assert len(all_students) == 1

    # DELETE
    student_repo.delete(student.id)
    deleted = student_repo.find_by_id(student.id)
    assert deleted is None


def test_student_find_by_id_inexistente(student_repo):
    """find_by_id retorna None para ID inexistente."""
    assert student_repo.find_by_id(999) is None


# =============================================================================
# TEACHER REPOSITORY
# =============================================================================

def test_teacher_com_disciplinas(teacher_repo):
    """Cria professor com disciplinas (tabela teacher_subjects)."""
    teacher = Teacher(name="Prof. Carlos", email="carlos@escola.com", subjects=["Matemática", "Física"])
    teacher_repo.save(teacher)
    assert teacher.id is not None

    found = teacher_repo.find_by_id(teacher.id)
    assert found is not None
    assert "Matemática" in found.subjects
    assert "Física" in found.subjects


def test_teacher_list_all(teacher_repo):
    """Lista todos os professores."""
    teacher_repo.save(Teacher(name="Prof. Ana", email="ana@escola.com", subjects=["História"]))
    teacher_repo.save(Teacher(name="Prof. Pedro", email="pedro@escola.com", subjects=["Geografia"]))
    all_teachers = teacher_repo.list_all()
    assert len(all_teachers) == 2


# =============================================================================
# PARENT REPOSITORY
# =============================================================================

def test_parent_crud(parent_repo):
    """CRUD de responsáveis."""
    parent = Parent(name="José Silva", email="jose@email.com", cpf="12345678909")
    parent_repo.save(parent)
    assert parent.id is not None

    found = parent_repo.find_by_id(parent.id)
    assert found is not None
    assert found.name == "José Silva"
    assert found.cpf == "12345678909"


def test_parent_link_to_student(parent_repo, student_repo):
    """Vincula responsável a aluno (tabela student_parent)."""
    student = Student(name="Lucas Silva", registration="2024003", email="lucas@escola.com")
    student_repo.save(student)
    parent = Parent(name="José Silva", email="jose@email.com", cpf="12345678909")
    parent_repo.save(parent)

    result = parent_repo.link_to_student(parent.id, student.id, "Pai")
    assert result is True

    # Verificar vínculo
    students = parent_repo.get_students(parent.id)
    assert student.id in students

    parents = parent_repo.get_parents_by_student(student.id)
    assert parent.id in parents


def test_parent_unlink_from_student(parent_repo, student_repo):
    """Desvincula responsável de aluno."""
    student = Student(name="Maria", registration="2024004", email="maria@escola.com")
    student_repo.save(student)
    parent = Parent(name="Ana", email="ana@email.com", cpf="52998224725")
    parent_repo.save(parent)

    parent_repo.link_to_student(parent.id, student.id)
    assert parent_repo.unlink_from_student(parent.id, student.id) is True
    assert parent_repo.get_students(parent.id) == []


# =============================================================================
# CLASSROOM REPOSITORY
# =============================================================================

def test_classroom_enum_handling(classroom_repo):
    """Enums (Shift, EducationLevel) são gravados como texto e reconvertidos."""
    classroom = Classroom(year="6º Ano", identifier="A", shift=Shift.MANHA, level=EducationLevel.FUNDAMENTAL_II)
    classroom_repo.save(classroom)

    found = classroom_repo.find_by_id(classroom.id)
    assert found is not None
    assert found.shift == Shift.MANHA
    assert found.level == EducationLevel.FUNDAMENTAL_II


def test_classroom_add_student(classroom_repo, student_repo):
    """Matricula estudante na turma (classroom_enrollments)."""
    student = Student(name="Pedro", registration="2024005", email="pedro@escola.com")
    student_repo.save(student)
    classroom = Classroom(year="7º Ano", identifier="B", shift=Shift.TARDE, level=EducationLevel.FUNDAMENTAL_II)
    classroom_repo.save(classroom)

    classroom_repo.add_student_to_classroom(classroom.id, student.id, 2024)
    # Sem exceção = sucesso


# =============================================================================
# ASSESSMENT REPOSITORY
# =============================================================================

def test_assessment_crud(assessment_repo):
    """CRUD de avaliações com conversão de enums."""
    assessment = Assessment(
        title="Prova de Álgebra", subject="Matemática",
        max_score=10.0, weight=3.0,
        assessment_type=AssessmentType.PROVA, bimester=Bimester.PRIMEIRO,
        academic_year=2024, assessment_date=date(2024, 3, 15)
    )
    assessment_repo.save(assessment)
    assert assessment.id is not None

    found = assessment_repo.find_by_id(assessment.id)
    assert found.title == "Prova de Álgebra"
    assert found.assessment_type == AssessmentType.PROVA
    assert found.bimester == Bimester.PRIMEIRO
    assert found.weight == 3.0
    assert found.assessment_date == date(2024, 3, 15)


def test_assessment_list_all(assessment_repo):
    """Lista todas as avaliações."""
    assessment_repo.save(Assessment(title="Prova 1", subject="Português", max_score=10.0, weight=2.0,
                                     assessment_type=AssessmentType.PROVA, bimester=Bimester.PRIMEIRO, academic_year=2024))
    assessment_repo.save(Assessment(title="Trabalho 1", subject="Português", max_score=10.0, weight=1.0,
                                     assessment_type=AssessmentType.TRABALHO, bimester=Bimester.PRIMEIRO, academic_year=2024))
    all_assessments = assessment_repo.list_all()
    assert len(all_assessments) == 2


# =============================================================================
# GRADE REPOSITORY
# =============================================================================

def test_grade_save_and_find(grade_repo, student_repo, assessment_repo):
    """Salva e busca nota por aluno+avaliação."""
    student = Student(name="Pedro Alves", registration="2024005", email="pedro@escola.com")
    student_repo.save(student)
    assessment = Assessment(title="Prova", subject="Ciências", max_score=10.0, weight=3.0,
                             assessment_type=AssessmentType.PROVA, bimester=Bimester.SEGUNDO, academic_year=2024)
    assessment_repo.save(assessment)

    grade = Grade(student=student, assessment=assessment, score=7.5)
    grade_repo.save(grade)
    assert grade.id is not None

    found = grade_repo.find_by_student_and_assessment(student.id, assessment.id)
    assert found is not None
    assert found.score == 7.5


def test_grade_find_by_bimester_com_peso(grade_repo, student_repo, assessment_repo):
    """Busca notas do bimestre com assessment populado (para calcular média ponderada)."""
    student = Student(name="Ana Costa", registration="2024006", email="ana@escola.com")
    student_repo.save(student)

    prova = Assessment(title="Prova", subject="História", max_score=10.0, weight=4.0,
                        assessment_type=AssessmentType.PROVA, bimester=Bimester.TERCEIRO, academic_year=2024)
    trabalho = Assessment(title="Trabalho", subject="História", max_score=10.0, weight=1.0,
                           assessment_type=AssessmentType.TRABALHO, bimester=Bimester.TERCEIRO, academic_year=2024)
    assessment_repo.save(prova)
    assessment_repo.save(trabalho)

    grade_repo.save(Grade(student=student, assessment=prova, score=8.0))
    grade_repo.save(Grade(student=student, assessment=trabalho, score=10.0))

    # Buscar notas do 3º bimestre em História
    grades = grade_repo.find_by_student_and_bimester(student.id, "História", Bimester.TERCEIRO, 2024)
    assert len(grades) == 2

    # Verificar que assessment está populado (para usar o peso)
    for g in grades:
        assert g.assessment is not None
        assert g.assessment.weight > 0

    # Média ponderada: (8.0 * 4 + 10.0 * 1) / (4 + 1) = 42/5 = 8.4
    total_nota = sum(g.score * g.assessment.weight for g in grades)
    total_peso = sum(g.assessment.weight for g in grades)
    media = round(total_nota / total_peso, 2)
    assert media == 8.4


# =============================================================================
# ATTENDANCE REPOSITORY
# =============================================================================

def test_attendance_save_and_find(attendance_repo, student_repo):
    """Salva e busca presença por período."""
    student = Student(name="Carlos Lima", registration="2024007", email="carlos@escola.com")
    student_repo.save(student)

    attendance = Attendance(student=student, subject="Educação Física",
                             attendance_date=date(2024, 3, 15), is_present=True)
    attendance_repo.save(attendance)
    assert attendance.id is not None

    # Buscar por período
    results = attendance_repo.find_by_student_and_period(
        student.id, "Educação Física", date(2024, 3, 1), date(2024, 3, 31)
    )
    assert len(results) == 1
    assert results[0].is_present is True
    assert results[0].attendance_date == date(2024, 3, 15)


def test_attendance_percentage(attendance_repo, student_repo):
    """Calcula percentual de presença (7 presenças em 10 aulas = 70%)."""
    student = Student(name="Fernanda Souza", registration="2024008", email="fernanda@escola.com")
    student_repo.save(student)

    # 10 aulas: primeiras 7 = presente, últimas 3 = falta
    for day in range(1, 11):
        is_present = (day <= 7)
        att = Attendance(student=student, subject="Inglês",
                          attendance_date=date(2024, 4, day), is_present=is_present)
        attendance_repo.save(att)

    results = attendance_repo.find_by_student_and_period(
        student.id, "Inglês", date(2024, 4, 1), date(2024, 4, 10)
    )
    total = len(results)
    presencas = sum(1 for a in results if a.is_present)
    percentual = (presencas / total * 100)
    assert percentual == pytest.approx(70.0, abs=0.1)


# =============================================================================
# TESTE DE FLUXO COMPLETO
# =============================================================================

def test_fluxo_academico_completo(student_repo, teacher_repo, classroom_repo,
                                   assessment_repo, grade_repo, attendance_repo):
    """Simula fluxo real: criar turma, matricular, avaliar, registrar presença."""
    # 1. Professor e turma
    teacher = Teacher(name="Prof. Roberto", email="roberto@escola.com", subjects=["Matemática"])
    teacher_repo.save(teacher)

    classroom = Classroom(year="8º Ano", identifier="C", shift=Shift.MANHA,
                           level=EducationLevel.FUNDAMENTAL_II)
    classroom_repo.save(classroom)

    # 2. Matricular aluno
    student = Student(name="Beatriz Oliveira", registration="2024009", email="beatriz@escola.com")
    student_repo.save(student)
    classroom_repo.add_student_to_classroom(classroom.id, student.id, 2024)

    # 3. Criar avaliação
    assessment = Assessment(title="Prova de Álgebra", subject="Matemática",
                             max_score=10.0, weight=5.0,
                             assessment_type=AssessmentType.PROVA, bimester=Bimester.QUARTO,
                             academic_year=2024, assessment_date=date(2024, 11, 20))
    assessment_repo.save(assessment)

    # 4. Lançar nota
    grade = Grade(student=student, assessment=assessment, score=9.5)
    grade_repo.save(grade)

    # 5. Registrar presenças
    for day in range(1, 6):
        att = Attendance(student=student, subject="Matemática",
                          attendance_date=date(2024, 11, day), is_present=True)
        attendance_repo.save(att)

    # 6. Verificações
    saved_grade = grade_repo.find_by_student_and_assessment(student.id, assessment.id)
    assert saved_grade.score == 9.5

    attendances = attendance_repo.find_by_student_and_period(
        student.id, "Matemática", date(2024, 11, 1), date(2024, 11, 5)
    )
    assert len(attendances) == 5
    assert all(a.is_present for a in attendances)
