"""
Testes das classes do domínio (models.py).
Valida criação, validações e métodos das entidades.
"""
import pytest
from datetime import date

from src.domain.models import (
    Student, Teacher, Parent, Classroom, Assessment, Grade, Attendance,
    Bimester, AssessmentType, EducationLevel, Shift
)


class TestStudent:
    """Testes para Student."""

    def test_criar_aluno_valido(self):
        student = Student(name="João Silva", registration="2024001", email="joao@escola.com")
        assert student.name == "João Silva"
        assert student.registration == "2024001"
        assert student.email == "joao@escola.com"
        assert student.active is True
        assert student.id is None

    def test_matricula_vazia_rejeita(self):
        with pytest.raises(ValueError, match="Matrícula não pode estar vazia"):
            Student(name="João Silva", registration="")

    def test_email_invalido_rejeita(self):
        with pytest.raises(ValueError, match="Email inválido"):
            Student(name="João Silva", registration="2024001", email="email_invalido")

    def test_email_normaliza_minusculo(self):
        student = Student(name="João", registration="2024001", email="JOAO@ESCOLA.COM")
        assert student.email == "joao@escola.com"

    def test_add_parent(self):
        student = Student(name="João Silva", registration="2024001")
        parent = Parent(name="Maria Silva", email="maria@email.com", cpf="12345678909")
        student.add_parent(parent)
        assert len(student.parents) == 1
        assert parent in student.parents

    def test_add_parent_duplicado_rejeita(self):
        student = Student(name="João Silva", registration="2024001")
        parent = Parent(name="Maria Silva", email="maria@email.com", cpf="12345678909")
        student.add_parent(parent)
        with pytest.raises(ValueError, match="já vinculado"):
            student.add_parent(parent)

    def test_deactivate_activate(self):
        student = Student(name="João", registration="2024001")
        assert student.active is True
        student.deactivate()
        assert student.active is False
        student.activate()
        assert student.active is True


class TestTeacher:
    """Testes para Teacher."""

    def test_criar_professor_valido(self):
        teacher = Teacher(name="Prof. Carlos", email="carlos@escola.com", subjects=["Matemática"])
        assert teacher.name == "Prof. Carlos"
        assert "Matemática" in teacher.subjects

    def test_add_subject(self):
        teacher = Teacher(name="Prof. Ana", email="ana@escola.com")
        teacher.add_subject("História")
        assert "História" in teacher.subjects

    def test_add_subject_duplicada_rejeita(self):
        teacher = Teacher(name="Prof. Ana", email="ana@escola.com", subjects=["História"])
        with pytest.raises(ValueError, match="já cadastrada"):
            teacher.add_subject("História")

    def test_teaches_subject(self):
        teacher = Teacher(name="Prof. Ana", email="ana@escola.com", subjects=["História"])
        assert teacher.teaches_subject("História") is True
        assert teacher.teaches_subject("Matemática") is False


class TestParent:
    """Testes para Parent (Responsável)."""

    def test_criar_responsavel_com_cpf_valido(self):
        parent = Parent(name="José Silva", email="jose@email.com", cpf="12345678909")
        assert parent.cpf == "12345678909"

    def test_cpf_invalido_rejeita(self):
        with pytest.raises(ValueError, match="CPF inválido"):
            Parent(name="José Silva", email="jose@email.com", cpf="11111111111")

    def test_cpf_formatado_normaliza(self):
        parent = Parent(name="José", email="jose@email.com", cpf="123.456.789-09")
        assert parent.cpf == "12345678909"


class TestClassroom:
    """Testes para Classroom (Turma)."""

    def test_criar_turma_valida(self):
        classroom = Classroom(year="6º Ano", identifier="A", shift=Shift.MANHA, level=EducationLevel.FUNDAMENTAL_II)
        assert classroom.year == "6º Ano"
        assert classroom.identifier == "A"
        assert classroom.shift == Shift.MANHA

    def test_get_full_name(self):
        classroom = Classroom(year="9º Ano", identifier="B", shift=Shift.MANHA, level=EducationLevel.FUNDAMENTAL_II)
        name = classroom.get_full_name()
        assert "9º Ano" in name
        assert "B" in name

    def test_identificador_invalido_rejeita(self):
        with pytest.raises(ValueError, match="única letra"):
            Classroom(year="6º Ano", identifier="AB", shift=Shift.MANHA, level=EducationLevel.FUNDAMENTAL_II)

    def test_add_remove_student(self):
        classroom = Classroom(year="6º Ano", identifier="A", shift=Shift.MANHA, level=EducationLevel.FUNDAMENTAL_II)
        classroom.add_student(1)
        assert 1 in classroom.students
        classroom.remove_student(1)
        assert 1 not in classroom.students


class TestAssessment:
    """Testes para Assessment (Avaliação)."""

    def test_criar_avaliacao_valida(self):
        assessment = Assessment(
            title="Prova Bimestral", subject="Matemática",
            assessment_type=AssessmentType.PROVA, max_score=10.0,
            weight=2.0, bimester=Bimester.PRIMEIRO
        )
        assert assessment.title == "Prova Bimestral"
        assert assessment.max_score == 10.0
        assert assessment.weight == 2.0

    def test_nota_maxima_invalida_rejeita(self):
        with pytest.raises(ValueError, match="Nota máxima"):
            Assessment(title="Prova", subject="Matemática", max_score=0, weight=1.0, bimester=Bimester.PRIMEIRO)

    def test_peso_invalido_rejeita(self):
        with pytest.raises(ValueError, match="Peso"):
            Assessment(title="Prova", subject="Matemática", max_score=10.0, weight=0, bimester=Bimester.PRIMEIRO)

    def test_is_valid_score(self):
        assessment = Assessment(title="Prova", subject="Matemática", max_score=10.0, weight=1.0, bimester=Bimester.PRIMEIRO)
        assert assessment.is_valid_score(8.5) is True
        assert assessment.is_valid_score(10.0) is True
        assert assessment.is_valid_score(11.0) is False
        assert assessment.is_valid_score(-1.0) is False


class TestGrade:
    """Testes para Grade (Nota)."""

    def test_criar_nota_valida(self):
        student = Student(name="Ana Costa", registration="2024002")
        assessment = Assessment(title="Prova", subject="Matemática", max_score=10.0, weight=1.0, bimester=Bimester.PRIMEIRO)
        grade = Grade(student=student, assessment=assessment, score=8.5)
        assert grade.score == 8.5

    def test_nota_excede_maximo_rejeita(self):
        student = Student(name="Ana Costa", registration="2024002")
        assessment = Assessment(title="Prova", subject="Matemática", max_score=10.0, weight=1.0, bimester=Bimester.PRIMEIRO)
        with pytest.raises(ValueError, match="excede o máximo permitido"):
            Grade(student=student, assessment=assessment, score=12.0)

    def test_nota_negativa_rejeita(self):
        with pytest.raises(ValueError, match="não pode ser negativa"):
            Grade(score=-1.0)


class TestAttendance:
    """Testes para Attendance (Frequência)."""

    def test_criar_presenca(self):
        student = Student(name="Carla Souza", registration="2024004")
        attendance = Attendance(student=student, attendance_date=date(2024, 3, 1), subject="Matemática", is_present=True)
        assert attendance.is_present is True
        assert attendance.justified is False

    def test_criar_falta(self):
        student = Student(name="Carla Souza", registration="2024004")
        attendance = Attendance(student=student, attendance_date=date(2024, 3, 1), subject="Matemática", is_present=False)
        assert attendance.is_present is False

    def test_justificar_falta(self):
        student = Student(name="Carla Souza", registration="2024004")
        attendance = Attendance(student=student, attendance_date=date(2024, 3, 1), subject="Matemática", is_present=False)
        attendance.justify("Atestado médico")
        assert attendance.justified is True
        assert attendance.justification == "Atestado médico"

    def test_justificar_presenca_rejeita(self):
        student = Student(name="Carla Souza", registration="2024004")
        attendance = Attendance(student=student, attendance_date=date(2024, 3, 1), subject="Matemática", is_present=True)
        with pytest.raises(ValueError, match="justificar presença"):
            attendance.justify("Motivo")

    def test_presente_com_justificativa_rejeita(self):
        student = Student(name="Carla Souza", registration="2024004")
        with pytest.raises(ValueError, match="presente não pode ter justificativa"):
            Attendance(student=student, attendance_date=date(2024, 3, 1), subject="Matemática", is_present=True, justified=True)
