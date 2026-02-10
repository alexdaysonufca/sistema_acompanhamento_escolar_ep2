# Serviços do sistema escolar
# Dividido em 2 classes: ServicosDoAluno e ServicosSecretaria
from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, List, Optional

from src.domain.models import Bimester, Grade, Attendance


# --- Dataclasses auxiliares ---

@dataclass
class BoletimDisciplina:
    """Dados do boletim de uma disciplina."""
    disciplina: str
    media_1bim: Optional[float]
    media_2bim: Optional[float]
    media_3bim: Optional[float]
    media_4bim: Optional[float]
    media_anual: Optional[float]
    situacao: str  # "Aprovado", "Reprovado", "Incompleto"

    def __str__(self):
        return (
            f"\n{self.disciplina}:\n"
            f"  1º Bim: {self.media_1bim or 'N/A'}\n"
            f"  2º Bim: {self.media_2bim or 'N/A'}\n"
            f"  3º Bim: {self.media_3bim or 'N/A'}\n"
            f"  4º Bim: {self.media_4bim or 'N/A'}\n"
            f"  Média Anual: {self.media_anual or 'N/A'}\n"
            f"  Situação: {self.situacao}"
        )


@dataclass
class ExtratoPresenca:
    """Dados do extrato de presença do aluno."""
    student_id: int
    subject: str
    periodo_inicio: date
    periodo_fim: date
    total_aulas: int
    presencas: int
    faltas: int
    faltas_justificadas: int
    percentual_presenca: float

    def __str__(self):
        return (
            f"\nExtrato de Presença - {self.subject}\n"
            f"Período: {self.periodo_inicio} a {self.periodo_fim}\n"
            f"Total de Aulas: {self.total_aulas}\n"
            f"Presenças: {self.presencas}\n"
            f"Faltas: {self.faltas} ({self.faltas_justificadas} justificadas)\n"
            f"Percentual de Presença: {self.percentual_presenca:.1f}%"
        )


# --- Serviços do Aluno (notas, médias, boletim e frequência) ---

class ServicosDoAluno:
    """Tudo relacionado ao aluno: notas, médias, boletim e frequência."""

    MEDIA_APROVACAO = 6.0

    def __init__(self, grade_repo, assessment_repo, student_repo, attendance_repo):
        self.grade_repo = grade_repo
        self.assessment_repo = assessment_repo
        self.student_repo = student_repo
        self.attendance_repo = attendance_repo

    def lancar_nota(self, student_id: int, assessment_id: int, score: float, graded_by: str) -> Grade:
        """Lança nota de um aluno em uma avaliação."""
        student = self.student_repo.find_by_id(student_id)
        if not student or not student.active:
            raise ValueError(f"Estudante {student_id} não encontrado ou inativo.")

        assessment = self.assessment_repo.find_by_id(assessment_id)
        if not assessment:
            raise ValueError(f"Avaliação {assessment_id} não encontrada.")

        existing = self.grade_repo.find_by_student_and_assessment(student_id, assessment_id)
        if existing:
            raise ValueError(f"Já existe nota lançada para {student.name} nesta avaliação.")

        grade = Grade(
            student=student,
            assessment=assessment,
            score=score,
            graded_at=datetime.now(),
            graded_by=graded_by
        )
        self.grade_repo.save(grade)
        return grade

    def calcular_media_bimestral(self, student_id: int, subject: str,
                                  bimester: Bimester, year: int) -> Optional[float]:
        """Calcula média ponderada do aluno no bimestre."""
        grades = self.grade_repo.find_by_student_and_bimester(
            student_id, subject, bimester, year
        )
        if not grades:
            return None

        total_peso = 0.0
        total_nota = 0.0
        for grade in grades:
            if grade.assessment:
                peso = grade.assessment.weight
                total_nota += grade.score * peso
                total_peso += peso

        if total_peso == 0:
            return None
        return round(total_nota / total_peso, 2)

    def gerar_boletim(self, student_id: int, subject: str, year: int) -> BoletimDisciplina:
        """Gera o boletim anual de uma disciplina."""
        medias = {}
        for bimester in Bimester:
            medias[bimester] = self.calcular_media_bimestral(student_id, subject, bimester, year)

        medias_validas = [m for m in medias.values() if m is not None]

        if not medias_validas:
            media_anual = None
            situacao = "Incompleto"
        elif len(medias_validas) < 4:
            media_anual = round(sum(medias_validas) / len(medias_validas), 2)
            situacao = "Incompleto"
        else:
            media_anual = round(sum(medias_validas) / 4, 2)
            situacao = "Aprovado" if media_anual >= self.MEDIA_APROVACAO else "Reprovado"

        return BoletimDisciplina(
            disciplina=subject,
            media_1bim=medias[Bimester.PRIMEIRO],
            media_2bim=medias[Bimester.SEGUNDO],
            media_3bim=medias[Bimester.TERCEIRO],
            media_4bim=medias[Bimester.QUARTO],
            media_anual=media_anual,
            situacao=situacao
        )

    def consultar_extrato(self, student_id: int, subject: str,
                          start_date: date, end_date: date) -> ExtratoPresenca:
        """Gera extrato de presença para um período."""
        attendances = self.attendance_repo.find_by_student_and_period(
            student_id, subject, start_date, end_date
        )

        total = len(attendances)
        presencas = sum(1 for a in attendances if a.is_present)
        faltas = total - presencas
        faltas_justificadas = sum(1 for a in attendances if not a.is_present and a.justified)
        percentual = (presencas / total * 100) if total > 0 else 0.0

        return ExtratoPresenca(
            student_id=student_id,
            subject=subject,
            periodo_inicio=start_date,
            periodo_fim=end_date,
            total_aulas=total,
            presencas=presencas,
            faltas=faltas,
            faltas_justificadas=faltas_justificadas,
            percentual_presenca=round(percentual, 1)
        )


# --- Serviços de Secretaria (matrículas e vínculos) ---

class ServicosSecretaria:
    """Matrículas em turmas e vínculos responsável-aluno."""

    def __init__(self, student_repo, classroom_repo, parent_repo):
        self.student_repo = student_repo
        self.classroom_repo = classroom_repo
        self.parent_repo = parent_repo

    def matricular_aluno(self, student_id: int, classroom_id: int, academic_year: int = 2024):
        """Matricula um estudante em uma turma."""
        student = self.student_repo.find_by_id(student_id)
        if not student:
            raise ValueError(f"Estudante {student_id} não encontrado.")
        if not student.active:
            raise ValueError(f"Estudante {student.name} não está ativo.")

        classroom = self.classroom_repo.find_by_id(classroom_id)
        if not classroom:
            raise ValueError(f"Turma {classroom_id} não encontrada.")

        self.classroom_repo.add_student_to_classroom(classroom_id, student_id, academic_year)
        return classroom

    def vincular_responsavel(self, parent_id: int, student_id: int,
                             relationship_type: str = "Responsável") -> bool:
        """Vincula um responsável a um aluno."""
        parent = self.parent_repo.find_by_id(parent_id)
        if not parent:
            raise ValueError(f"Responsável {parent_id} não encontrado.")

        student = self.student_repo.find_by_id(student_id)
        if not student:
            raise ValueError(f"Estudante {student_id} não encontrado.")

        valid_types = [
            "Pai", "Mãe", "Responsável", "Tutor", "Tutora",
            "Avô", "Avó", "Tio", "Tia", "Padrasto", "Madrasta"
        ]
        if relationship_type not in valid_types:
            raise ValueError(f"Tipo de relacionamento inválido: {relationship_type}")

        return self.parent_repo.link_to_student(parent_id, student_id, relationship_type)

    def desvincular_responsavel(self, parent_id: int, student_id: int) -> bool:
        """Desvincula um responsável de um aluno."""
        return self.parent_repo.unlink_from_student(parent_id, student_id)

    def listar_alunos_do_responsavel(self, parent_id: int) -> List[int]:
        """Lista todos os alunos vinculados a um responsável."""
        parent = self.parent_repo.find_by_id(parent_id)
        if not parent:
            raise ValueError(f"Responsável {parent_id} não encontrado.")
        return self.parent_repo.get_students(parent_id)

    def listar_responsaveis_do_aluno(self, student_id: int) -> List[int]:
        """Lista todos os responsáveis vinculados a um aluno."""
        student = self.student_repo.find_by_id(student_id)
        if not student:
            raise ValueError(f"Estudante {student_id} não encontrado.")
        return self.parent_repo.get_parents_by_student(student_id)
