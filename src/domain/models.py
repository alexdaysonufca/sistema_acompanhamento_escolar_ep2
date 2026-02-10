"""
Modelos do sistema - Alunos, professores, turmas, etc.
Inclui os enums e as classes principais.
"""
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from src.utils import validar_cpf, validar_email, normalizar_cpf


# --- Enums (tipos fixos) ---

class Bimester(Enum):
    """Os 4 bimestres do ano letivo."""
    PRIMEIRO = "PRIMEIRO"
    SEGUNDO = "SEGUNDO"
    TERCEIRO = "TERCEIRO"
    QUARTO = "QUARTO"

    def __str__(self):
        return self.value


class AssessmentType(Enum):
    """Tipos de avaliação (prova, trabalho, seminário, etc)."""
    PROVA = "PROVA"
    TRABALHO = "TRABALHO"
    SEMINARIO = "SEMINARIO"
    PARTICIPACAO = "PARTICIPACAO"
    ATIVIDADE_PRATICA = "ATIVIDADE_PRATICA"
    PROJETO = "PROJETO"

    def __str__(self):
        return self.value


class EducationLevel(Enum):
    """Níveis de ensino (Infantil, Fundamental I/II, Médio)."""
    INFANTIL = "INFANTIL"
    FUNDAMENTAL_I = "FUNDAMENTAL_I"
    FUNDAMENTAL_II = "FUNDAMENTAL_II"
    MEDIO = "MEDIO"

    def __str__(self):
        return self.value


class Shift(Enum):
    """Turnos escolares disponíveis."""
    MANHA = "MANHA"
    TARDE = "TARDE"
    NOITE = "NOITE"
    INTEGRAL = "INTEGRAL"

    def __str__(self):
        return self.value


# --- Alunos, Professores, Responsáveis ---

class Student:
    """Dados do aluno."""

    def __init__(
        self,
        name: str = "",
        email: str = "",
        registration: str = "",
        student_id: Optional[int] = None,
        active: bool = True,
        classroom_id: Optional[int] = None
    ):
        self.id = student_id
        self.name = name.strip() if name else ""
        self.active = active
        self.classroom_id = classroom_id
        self.parents: List['Parent'] = []

        # Validação de email
        if email:
            email_limpo = email.strip().lower()
            if not validar_email(email_limpo):
                raise ValueError(f"Email inválido: '{email}'")
            self.email = email_limpo
        else:
            self.email = ""

        # Validação de matrícula
        if not registration or not registration.strip():
            raise ValueError("Matrícula não pode estar vazia.")
        self.registration = registration.strip()

    def add_parent(self, parent: 'Parent') -> None:
        if parent in self.parents:
            raise ValueError("Responsável já vinculado a este estudante.")
        self.parents.append(parent)

    def remove_parent(self, parent: 'Parent') -> None:
        if parent not in self.parents:
            raise ValueError("Responsável não está vinculado a este estudante.")
        self.parents.remove(parent)

    def deactivate(self):
        self.active = False

    def activate(self):
        self.active = True

    def __repr__(self):
        return (
            f"Student(id={self.id}, name={self.name}, "
            f"registration={self.registration}, active={self.active})"
        )


class Teacher:
    """Dados do professor."""

    def __init__(
        self,
        name: str = "",
        email: str = "",
        registration: Optional[str] = None,
        subjects: Optional[List[str]] = None,
        teacher_id: Optional[int] = None
    ):
        self.id = teacher_id
        self.name = name.strip() if name else ""
        self.subjects: List[str] = subjects.copy() if subjects else []
        self.registration = registration.strip() if registration else ""

        # Validação de email
        if email:
            email_limpo = email.strip().lower()
            if not validar_email(email_limpo):
                raise ValueError(f"Email inválido: '{email}'")
            self.email = email_limpo
        else:
            self.email = ""

    def add_subject(self, subject: str) -> None:
        subject = subject.strip()
        if not subject:
            raise ValueError("Nome da disciplina não pode estar vazio.")
        if subject in self.subjects:
            raise ValueError(f"Disciplina '{subject}' já cadastrada para este professor.")
        self.subjects.append(subject)

    def remove_subject(self, subject: str) -> None:
        if subject not in self.subjects:
            raise ValueError(f"Disciplina '{subject}' não encontrada para este professor.")
        self.subjects.remove(subject)

    def teaches_subject(self, subject: str) -> bool:
        return subject in self.subjects

    def __repr__(self):
        subjects_str = ", ".join(self.subjects) if self.subjects else "Nenhuma"
        return (
            f"Teacher(id={self.id}, name={self.name}, "
            f"registration={self.registration}, subjects=[{subjects_str}])"
        )


class Parent:
    """Dados do responsável (pai, mãe, etc)."""

    def __init__(
        self,
        name: str = "",
        email: str = "",
        cpf: Optional[str] = None,
        phone: Optional[str] = None,
        parent_id: Optional[int] = None
    ):
        self.id = parent_id
        self.name = name
        self.email = email
        self.phone = phone.strip() if phone else None
        self.students: List['Student'] = []

        # Validação de CPF
        if cpf:
            if not validar_cpf(cpf):
                raise ValueError(f"CPF inválido: '{cpf}'")
            self.cpf = normalizar_cpf(cpf)
        else:
            self.cpf = None

    def add_student(self, student: 'Student') -> None:
        if student in self.students:
            raise ValueError("Estudante já vinculado a este responsável.")
        self.students.append(student)

    def remove_student(self, student: 'Student') -> None:
        if student not in self.students:
            raise ValueError("Estudante não está vinculado a este responsável.")
        self.students.remove(student)

    def __repr__(self):
        return (
            f"Parent(id={self.id}, name={self.name}, "
            f"email={self.email}, cpf={self.cpf})"
        )


# --- Turmas ---

class Classroom:
    """Dados da turma."""

    def __init__(
        self,
        year: str,
        identifier: str,
        shift: Shift,
        level: EducationLevel,
        teacher_id: Optional[int] = None,
        classroom_id: Optional[int] = None
    ):
        self.id = classroom_id
        self.shift = shift
        self.level = level
        self.teacher_id = teacher_id
        self.students: List[int] = []

        # Validação de ano/série
        if not year or len(year.strip()) < 2:
            raise ValueError("Ano/série deve ter pelo menos 2 caracteres.")
        self.year = year.strip()

        # Validação do identificador (uma letra)
        identifier = identifier.strip().upper()
        if len(identifier) != 1 or not identifier.isalpha():
            raise ValueError("Identificador deve ser uma única letra.")
        self.identifier = identifier

    def add_student(self, student_id: int) -> None:
        if student_id in self.students:
            raise ValueError("Estudante já matriculado nesta turma.")
        self.students.append(student_id)

    def remove_student(self, student_id: int) -> None:
        if student_id not in self.students:
            raise ValueError("Estudante não está matriculado nesta turma.")
        self.students.remove(student_id)

    def get_full_name(self) -> str:
        """Retorna nome completo da turma."""
        return f"{self.year} {self.identifier} - {self.shift} - {self.level}"

    def __str__(self):
        return self.get_full_name()


# --- Avaliações, Notas, Frequência ---

class Assessment:
    """Dados de uma prova/trabalho."""

    def __init__(
        self,
        assessment_id: Optional[int] = None,
        title: str = "",
        description: str = "",
        subject: str = "",
        assessment_type: AssessmentType = AssessmentType.PROVA,
        max_score: float = 10.0,
        weight: float = 1.0,
        bimester: Bimester = Bimester.PRIMEIRO,
        assessment_date: Optional[date] = None,
        academic_year: Optional[int] = None
    ):
        self.id = assessment_id
        self.assessment_type = assessment_type
        self.bimester = bimester
        self.assessment_date = assessment_date
        self.description = description.strip() if description else ""

        # Ano letivo (usa o informado ou o ano atual)
        self.academic_year = academic_year or date.today().year

        # Validação do título
        if not title or len(title.strip()) < 3:
            raise ValueError("Título deve ter pelo menos 3 caracteres.")
        self.title = title.strip()

        # Validação da disciplina
        if not subject or not subject.strip():
            raise ValueError("Disciplina não pode estar vazia.")
        self.subject = subject.strip()

        # Validação da nota máxima
        if max_score <= 0 or max_score > 100:
            raise ValueError("Nota máxima deve estar entre 0 e 100.")
        self.max_score = float(max_score)

        # Validação do peso
        if weight <= 0 or weight > 10:
            raise ValueError("Peso deve estar entre 0 e 10.")
        self.weight = float(weight)

    def is_valid_score(self, score: float) -> bool:
        """Verifica se a nota está dentro do permitido."""
        return 0 <= score <= self.max_score

    def __str__(self):
        return (
            f"Assessment({self.title}, {self.subject}, "
            f"{self.assessment_type}, Bimestre: {self.bimester})"
        )


class Grade:
    """Nota do aluno em uma avaliação."""

    def __init__(
        self,
        grade_id: Optional[int] = None,
        student: Optional['Student'] = None,
        assessment: Optional['Assessment'] = None,
        score: float = 0.0,
        graded_at: Optional[datetime] = None,
        graded_by: Optional[str] = None
    ):
        self.id = grade_id
        self.student = student
        self.assessment = assessment
        self.graded_at = graded_at or datetime.now()
        self.graded_by = graded_by

        # Validação simples da nota
        if score < 0:
            raise ValueError("Nota não pode ser negativa.")
        if assessment and not assessment.is_valid_score(score):
            raise ValueError(
                f"Nota {score} excede o máximo permitido "
                f"({assessment.max_score}) para esta avaliação."
            )
        self.score = float(score)

    def __str__(self):
        student_name = self.student.name if self.student else "N/A"
        assessment_title = self.assessment.title if self.assessment else "N/A"
        return f"Grade({student_name}, {assessment_title}, {self.score})"


class Attendance:
    """Registro de presença/falta do aluno."""

    def __init__(
        self,
        attendance_id: Optional[int] = None,
        student: Optional['Student'] = None,
        attendance_date: Optional[date] = None,
        subject: str = "",
        is_present: bool = True,
        justified: bool = False,
        justification: Optional[str] = None,
        recorded_at: Optional[datetime] = None
    ):
        self.id = attendance_id
        self.student = student
        self.attendance_date = attendance_date
        self.is_present = is_present
        self.justified = justified
        self.justification = justification
        self.recorded_at = recorded_at or datetime.now()

        # Validação de disciplina
        if not subject or not subject.strip():
            raise ValueError("Disciplina não pode estar vazia.")
        self.subject = subject.strip()

        # Validação de consistência
        if self.is_present and (self.justified or self.justification):
            raise ValueError("Aluno presente não pode ter justificativa de falta.")

    def justify(self, justification_text: str) -> None:
        """Justifica uma falta."""
        if self.is_present:
            raise ValueError("Não é possível justificar presença.")
        if self.justified:
            raise ValueError("Falta já foi justificada anteriormente.")
        if not justification_text or not justification_text.strip():
            raise ValueError("Justificativa não pode estar vazia.")

        self.justified = True
        self.justification = justification_text.strip()

    def __str__(self):
        student_name = self.student.name if self.student else "N/A"
        status = "Presente" if self.is_present else (
            "Falta Justificada" if self.justified else "Falta"
        )
        return f"Attendance({student_name}, {self.subject}, {self.attendance_date}, {status})"
