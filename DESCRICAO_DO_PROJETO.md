# Descrição do Projeto - Sistema de Acompanhamento Escolar

## Visão Geral

**Nome:** Painel de Acompanhamento Escolar
**Objetivo:** Sistema para gerenciar alunos, professores, responsáveis, turmas, avaliações, notas e frequência de uma escola
**Linguagem:** Python 3.12+
**Banco de Dados:** SQLite (IDs inteiros com autoincremento)
**Testes:** pytest
**Total de arquivos Python (src/):** 8 arquivos
**Total de linhas de código (src/):** 1.716 linhas

---

## O que o sistema faz

1. Cadastro de estudantes, professores e responsáveis
2. Organização de turmas com turno e nível de ensino
3. Matrícula de alunos em turmas e vínculos com responsáveis
4. Lançamento de notas com peso e nota máxima
5. Cálculo de média bimestral ponderada
6. Geração de boletim anual (aprovado/reprovado, média >= 6.0)
7. Registro de presença/falta com justificativa
8. Consulta de extrato de frequência por disciplina e período

---

## Estrutura do Projeto

```
etapa_2-v2/
├── main.py                          # Script de demonstração (465 linhas)
├── requirements.txt                 # Dependências (8 linhas)
├── README.md                        # Documentação principal (99 linhas)
├── DESCRICAO_DO_PROJETO.md          # Este arquivo
├── .gitignore                       # Arquivos ignorados pelo git (158 linhas)
├── .python-version                  # Versão do Python (3.12)
│
├── src/                             # Código-fonte (8 arquivos Python)
│   ├── __init__.py                  # Pacote principal (3 linhas)
│   ├── utils.py                     # Validação de CPF, email, ano (131 linhas)
│   │
│   ├── domain/                      # Modelos e regras de negócio
│   │   ├── __init__.py              # Exporta classes e enums (32 linhas)
│   │   └── models.py               # 7 classes + 4 enums (397 linhas)
│   │
│   ├── application/                 # Serviços / casos de uso
│   │   ├── __init__.py              # Exporta serviços (6 linhas)
│   │   └── services.py             # 2 serviços + 2 dataclasses (232 linhas)
│   │
│   └── infrastructure/              # Banco de dados e repositórios
│       ├── __init__.py              # Exporta tudo (25 linhas)
│       ├── database.py             # DatabaseManager + 7 repositórios (679 linhas)
│       └── schema.sql              # 11 tabelas + 11 índices (211 linhas)
│
└── tests/                           # Testes (5 arquivos de teste)
    ├── __init__.py                  # (5 linhas)
    ├── unit/
    │   ├── __init__.py              # (vazio)
    │   ├── test_entities.py         # Testes das classes do domínio (206 linhas)
    │   ├── test_cpf_validation.py   # Validação de CPF (39 linhas)
    │   └── test_passing_grade.py    # Teste de aprovação (20 linhas)
    └── integration/
        ├── __init__.py              # (vazio)
        ├── test_integrity.py        # Integridade do projeto (59 linhas)
        └── test_manual_repositories.py  # CRUD completo com banco real (385 linhas)
```

---

## Arquivos na Raiz

### main.py (465 linhas)

Script que demonstra o sistema funcionando de ponta a ponta. Inclui funções auxiliares de formatação (`print_header`, `print_separator`, `print_success`, `print_error`) e de criação de dados de exemplo (`create_sample_student`, `create_sample_classroom`, `create_sample_assessment`).

**O que faz:**
1. Cria o banco de dados SQLite (school.db)
2. Cadastra 3 estudantes, 1 professor com disciplinas, 2 responsáveis com CPF
3. Cria 1 turma e matricula os 3 alunos via ServicosSecretaria
4. Vincula responsáveis aos alunos (relationship_type: Pai, Mãe)
5. Cria 2 avaliações (prova peso 3, trabalho peso 1) e lança notas via ServicosDoAluno
6. Calcula média bimestral ponderada: (8.5 × 3 + 9.0 × 1) / 4 = 8.62
7. Registra presença e falta, justifica falta com "Atestado médico"
8. Consulta extrato de frequência via ServicosDoAluno.consultar_extrato()
9. Gera boletim anual via ServicosDoAluno.gerar_boletim()
10. Consulta vínculos (alunos do responsável, responsáveis do aluno)
11. Desvincula responsável e verifica resultado
12. Testa find_by_id() e list_all()
13. Desativa e reativa aluno, verifica contagem de ativos
14. Mostra estatísticas completas do banco (10 tabelas com registros)

**Como rodar:**
```bash
python main.py
```

---

### requirements.txt (8 linhas)

Só tem uma dependência externa:
```
pytest>=7.4.0
```
O resto do projeto usa apenas bibliotecas padrão do Python (sqlite3, datetime, re, os, pathlib, enum, dataclasses).

---

### README.md (99 linhas)

Documentação resumida do projeto com estrutura de pastas, funcionalidades, casos de uso, organização do código e instruções de execução.

---

### .gitignore (158 linhas)

Ignora arquivos de cache Python (`__pycache__/`, `*.pyc`), ambientes virtuais (`.venv/`), banco de dados (`*.db`), arquivos de IDE e builds.

---

### .python-version (1 linha)

Define a versão do Python como `3.12`.

---

## src/ - Código-Fonte

### src/__init__.py (3 linhas)

Docstring simples: "Painel de Acompanhamento Escolar - MVP".

---

### src/utils.py (131 linhas)

Funções de validação usadas pelas classes do domínio:

- `validar_cpf(cpf)` — Valida CPF com algoritmo completo dos dois dígitos verificadores. Remove formatação, verifica 11 dígitos, rejeita dígitos iguais, calcula e confere dígitos.
- `validar_email(email)` — Valida formato de email com regex (`algo@dominio.extensão`). Verifica tamanho total (5-254 chars) e parte local (máximo 64 chars).
- `normalizar_cpf(cpf)` — Remove pontos e traço, retorna só números.
- `formatar_cpf(cpf)` — Formata como `123.456.789-09`.
- `validar_ano_letivo(ano)` — Verifica se o ano é inteiro, >= 2000 e não mais que 2 anos no futuro.

---

## src/domain/ - Modelos e Regras

### src/domain/__init__.py (32 linhas)

Exporta todos os enums e classes do models.py via `__all__`.

---

### src/domain/models.py (397 linhas)

Arquivo único com tudo do domínio: os 4 enums e as 7 classes do sistema. Os IDs começam como `None` e são preenchidos pelo SQLite após o primeiro `save()` (INTEGER PRIMARY KEY AUTOINCREMENT). Todos os atributos são públicos. Validações são feitas no `__init__`.

**Imports:** `date`, `datetime`, `Enum`, `List`, `Optional`, `validar_cpf`, `validar_email`, `normalizar_cpf`.

**Enums:**

- **Bimester** — PRIMEIRO, SEGUNDO, TERCEIRO, QUARTO
- **AssessmentType** — PROVA, TRABALHO, SEMINARIO, PARTICIPACAO, ATIVIDADE_PRATICA, PROJETO
- **EducationLevel** — INFANTIL, FUNDAMENTAL_I, FUNDAMENTAL_II, MEDIO
- **Shift** — MANHA, TARDE, NOITE, INTEGRAL

Todos os enums têm `__str__` retornando o valor.

**Classes:**

#### 1. Student (Estudante)
- **Campos:** id, name, email, registration, active, classroom_id, parents (lista)
- **Construtor:** `student_id=None, name="", email="", registration="", active=True, classroom_id=None`
- **Validações:** email via `validar_email()` (normaliza para minúsculo), matrícula não pode ser vazia
- **Métodos:** `add_parent(parent)`, `remove_parent(parent)`, `activate()`, `deactivate()`, `__repr__`

#### 2. Teacher (Professor)
- **Campos:** id, name, email, registration, subjects (lista)
- **Construtor:** `teacher_id=None, name="", email="", registration=None, subjects=None`
- **Validações:** email via `validar_email()`
- **Métodos:** `add_subject(subject)`, `remove_subject(subject)`, `teaches_subject(subject) -> bool`, `__repr__`

#### 3. Parent (Responsável)
- **Campos:** id, name, email, cpf, phone, students (lista)
- **Construtor:** `parent_id=None, name="", email="", cpf=None, phone=None`
- **Validações:** CPF via `validar_cpf()`, normaliza com `normalizar_cpf()`
- **Métodos:** `add_student(student)`, `remove_student(student)`, `__repr__`

#### 4. Classroom (Turma)
- **Campos:** id, year, identifier (letra A-Z), shift, level, teacher_id, students (lista de IDs)
- **Construtor:** `year, identifier, shift, level, teacher_id=None, classroom_id=None`
- **Validações:** year >= 2 chars, identifier deve ser uma única letra maiúscula
- **Métodos:** `add_student(student_id)`, `remove_student(student_id)`, `get_full_name() -> str`, `__str__`

#### 5. Assessment (Avaliação)
- **Campos:** id, title, description, subject, assessment_type, max_score, weight, bimester, assessment_date, academic_year
- **Construtor:** `assessment_id=None, title="", description="", subject="", assessment_type=PROVA, max_score=10.0, weight=1.0, bimester=PRIMEIRO, assessment_date=None, academic_year=None`
- **Validações:** título >= 3 chars, disciplina não vazia, max_score entre 0-100, peso entre 0-10
- **Métodos:** `is_valid_score(score) -> bool`, `__str__`

#### 6. Grade (Nota)
- **Campos:** id, student, assessment, score, graded_at, graded_by
- **Construtor:** `grade_id=None, student=None, assessment=None, score=0.0, graded_at=None, graded_by=None`
- **Validações:** score >= 0, se assessment fornecido verifica `is_valid_score()`
- **Métodos:** `__str__`

#### 7. Attendance (Frequência)
- **Campos:** id, student, attendance_date, subject, is_present, justified, justification, recorded_at
- **Construtor:** `attendance_id=None, student=None, attendance_date=None, subject="", is_present=True, justified=False, justification=None, recorded_at=None`
- **Validações:** disciplina não vazia, presença + justificativa é inconsistente
- **Métodos:** `justify(justification_text)`, `__str__`

---

## src/application/ - Serviços

### src/application/__init__.py (6 linhas)

Exporta os 2 serviços e as 2 dataclasses.

---

### src/application/services.py (232 linhas)

Arquivo com todos os serviços do sistema, organizados em 2 classes + 2 dataclasses auxiliares.

**Imports:** `dataclass`, `date`, `datetime`, `Dict`, `List`, `Optional`, `Bimester`, `Grade`, `Attendance`.

**Dataclasses auxiliares:**

- **BoletimDisciplina** — disciplina, media_1bim, media_2bim, media_3bim, media_4bim, media_anual, situacao. Com `__str__` formatado.
- **ExtratoPresenca** — student_id, subject, periodo_inicio, periodo_fim, total_aulas, presencas, faltas, faltas_justificadas, percentual_presenca. Com `__str__` formatado.

**Serviços:**

#### 1. ServicosDoAluno
Recebe `grade_repo`, `assessment_repo`, `student_repo`, `attendance_repo`. Constante `MEDIA_APROVACAO = 6.0`.

- `lancar_nota(student_id, assessment_id, score, graded_by) -> Grade` — Verifica: aluno ativo, avaliação existente, nota não duplicada. Cria Grade e salva.
- `calcular_media_bimestral(student_id, subject, bimester, year) -> Optional[float]` — Busca notas do bimestre, calcula média ponderada: `soma(nota × peso) / soma(pesos)`. Retorna `None` se sem notas.
- `gerar_boletim(student_id, subject, year) -> BoletimDisciplina` — Calcula médias dos 4 bimestres. Se 4 médias: aprovado/reprovado (>= 6.0). Se < 4: "Incompleto".
- `consultar_extrato(student_id, subject, start_date, end_date) -> ExtratoPresenca` — Busca presenças do período, calcula totais, faltas, faltas justificadas e percentual.

#### 2. ServicosSecretaria
Recebe `student_repo`, `classroom_repo`, `parent_repo`.

- `matricular_aluno(student_id, classroom_id, academic_year) -> Classroom` — Verifica aluno ativo e turma existente, insere em classroom_enrollments.
- `vincular_responsavel(parent_id, student_id, relationship_type) -> bool` — Valida tipos permitidos (Pai, Mãe, Responsável, Tutor, Tutora, Avô, Avó, Tio, Tia, Padrasto, Madrasta). Insere em student_parent.
- `desvincular_responsavel(parent_id, student_id) -> bool` — Remove de student_parent.
- `listar_alunos_do_responsavel(parent_id) -> List[int]` — Retorna IDs dos alunos.
- `listar_responsaveis_do_aluno(student_id) -> List[int]` — Retorna IDs dos responsáveis.

---

## src/infrastructure/ - Banco de Dados e Repositórios

### src/infrastructure/__init__.py (25 linhas)

Exporta DatabaseManager, get_database e os 7 repositórios via `__all__`.

---

### src/infrastructure/database.py (679 linhas)

Arquivo que contém a classe DatabaseManager e os 7 repositórios SQL.

**Imports:** `sqlite3`, `Path`, `List`, `Optional`, `datetime`, `date`, todas as classes e enums de models.py.

**DatabaseManager:**
- `__init__(db_path=None)` — Se não informado, usa `<diretório_do_arquivo>/school.db`
- `get_connection()` — Retorna conexão com `PRAGMA foreign_keys = ON` e `row_factory = sqlite3.Row`
- `initialize_database()` — Lê o schema.sql e executa com `executescript()`
- `reset_database()` — Remove o arquivo do banco
- `_show_tables()` — Lista tabelas criadas (uso interno, com print)

Função `get_database(db_path=None)` — Singleton: retorna sempre a mesma instância de DatabaseManager.

**Padrão dos repositórios:**
- `save(entity)` — Se `entity.id` existe: UPDATE (com fallback INSERT). Se `None`: INSERT, depois `entity.id = cursor.lastrowid`
- `find_by_id(id)` — SELECT por chave primária, reconstrói o objeto Python
- `list_all()` — SELECT sem filtro, ordenado
- `delete(id)` — DELETE por ID (apenas StudentRepository)
- Cada método abre conexão, executa, commita e fecha

**Repositórios:**

1. **StudentRepository** — save (UPDATE + fallback INSERT para evitar CASCADE), find_by_id, list_all (só ativos, `WHERE active = 1`), delete

2. **TeacherRepository** — save (com `DELETE + INSERT` em teacher_subjects), find_by_id (2 queries: teacher + subjects), list_all (com subjects por professor)

3. **ParentRepository** — save, find_by_id, list_all, link_to_student (INSERT em student_parent, trata IntegrityError), unlink_from_student (DELETE de student_parent), get_students (lista IDs de alunos), get_parents_by_student (lista IDs de responsáveis)

4. **ClassroomRepository** — save (grava turno/nível como texto via `.value`), find_by_id (reconstrói enums via `Shift()` e `EducationLevel()`), add_student_to_classroom (INSERT em classroom_enrollments, ignora IntegrityError), list_all

5. **AssessmentRepository** — save (grava tipo/bimestre como texto via `.value`, data como ISO string), find_by_id (reconstrói enums e data), list_all (ordenado por assessment_date DESC)

6. **GradeRepository** — save (ON CONFLICT DO UPDATE), find_by_student_and_assessment (retorna Grade simples), find_by_student_and_bimester (JOIN com assessments, retorna Grade com Assessment populado incluindo peso), list_all

7. **AttendanceRepository** — save (ON CONFLICT DO UPDATE por student_id+subject+attendance_date), find_by_student_and_period (filtra por data BETWEEN, ordenado), list_all

---

### src/infrastructure/schema.sql (211 linhas)

Define toda a estrutura do banco com 11 tabelas e 11 índices para consultas frequentes. Todas as chaves primárias usam `INTEGER PRIMARY KEY AUTOINCREMENT`. Tipos (turno, nível, bimestre, tipo de avaliação) são armazenados como texto, com CHECK constraints garantindo valores válidos.

**Tabelas:**

1. **students** — student_id, name, registration (UNIQUE), email (UNIQUE), active, created_at. CHECKs: nome >= 3 chars, matrícula >= 3 chars, email com @
2. **parents** — parent_id, name, email (UNIQUE), cpf (UNIQUE, 11 dígitos), created_at. CHECKs: nome >= 3 chars, email com @
3. **student_parent** — PK composta (student_id, parent_id), relationship_type, created_at. CASCADE em ambas as FKs
4. **teachers** — teacher_id, name, email (UNIQUE), created_at. CHECKs: nome >= 3 chars, email com @
5. **teacher_subjects** — PK composta (teacher_id, subject). CASCADE na FK
6. **classrooms** — classroom_id, year, identifier (A-Z), shift, education_level, teacher_id, created_at. CHECKs nos valores de shift e education_level. UNIQUE (year, identifier, shift). FK teacher_id ON DELETE SET NULL
7. **classroom_enrollments** — enrollment_id, student_id, classroom_id, academic_year, enrollment_date, status. CHECK status IN (ACTIVE, TRANSFERRED, WITHDRAWN, COMPLETED). UNIQUE (student_id, classroom_id, academic_year). FK CASCADE + RESTRICT
8. **assessments** — assessment_id, title, subject, description, max_score (0-10), weight (0-10), assessment_type, bimester, academic_year, assessment_date, created_at. CHECKs nos valores de assessment_type e bimester
9. **grades** — grade_id, student_id, assessment_id, score (>= 0), graded_at. UNIQUE (student_id, assessment_id). FK CASCADE + RESTRICT
10. **attendance** — attendance_id, student_id, subject, attendance_date, is_present, is_justified, justification, created_at. CHECK de consistência justificativa (justificada implica texto). UNIQUE (student_id, subject, attendance_date). FK CASCADE
11. **report_cards** — report_card_id, student_id, subject, bimester, academic_year, education_level, grade (0-10), development_level, description, created_at. UNIQUE (student_id, subject, bimester, academic_year). FK CASCADE

**Índices (11):**
- idx_student_name, idx_parent_name, idx_teacher_name — Busca por nome
- idx_attendance_date — Busca de frequência por data
- idx_attendance_student_subject — Busca de frequência por aluno+disciplina
- idx_grade_student — Busca de notas por aluno
- idx_assessment_subject_bimester — Busca de avaliações por disciplina+bimestre
- idx_enrollment_student, idx_enrollment_classroom — Busca de matrículas
- idx_report_student_year — Busca de boletins por aluno+ano

---

## tests/ - Testes

Total: **5 arquivos de teste**, **60 testes**, todos passando.

### tests/__init__.py (5 linhas)
Docstring: "Testes Automatizados - Painel de Acompanhamento Escolar. Execute com: pytest tests/"

### tests/unit/test_entities.py (206 linhas) — 30 testes
Testa as 7 classes do domínio organizadas em 7 classes de teste:
- **TestStudent** (7 testes): criação válida, matrícula vazia, email inválido, email normaliza minúsculo, add_parent, add_parent duplicado, deactivate/activate
- **TestTeacher** (4 testes): criação, add_subject, add_subject duplicada, teaches_subject
- **TestParent** (3 testes): CPF válido, CPF inválido rejeita, CPF formatado normaliza
- **TestClassroom** (4 testes): criação, get_full_name, identificador inválido, add/remove_student
- **TestAssessment** (4 testes): criação, nota máxima inválida, peso inválido, is_valid_score
- **TestGrade** (3 testes): criação, nota excede máximo, nota negativa
- **TestAttendance** (5 testes): presença, falta, justificar falta, justificar presença rejeita, presente com justificativa rejeita

### tests/unit/test_cpf_validation.py (39 linhas) — 6 testes
Testa as funções de CPF do utils.py:
- CPFs válidos aceitos, dígitos errados rejeitados, todos iguais rejeitados, tamanho errado rejeitado, normalizar_cpf, formatar_cpf

### tests/unit/test_passing_grade.py (20 linhas) — 3 testes
Testa a constante `MEDIA_APROVACAO = 6.0` do ServicosDoAluno:
- Média é 6.0, nota 6.0 aprova, nota 5.9 reprova

### tests/integration/test_integrity.py (59 linhas) — 5 testes
Testa que os módulos importam corretamente e que classes/métodos existem:
- Importa domain.models (classes e enums), services (2 serviços + 2 dataclasses), infrastructure (DatabaseManager e 7 repos), utils (5 funções)
- Existência de métodos no StudentRepository (save, find_by_id, list_all, delete)

### tests/integration/test_manual_repositories.py (385 linhas) — 16 testes
Teste mais completo — cria banco SQLite temporário (via `tmp_path`), aplica schema.sql, faz CRUD com todos os 7 repositórios:
- **StudentRepository** (2 testes): CRUD completo, find_by_id inexistente
- **TeacherRepository** (2 testes): com disciplinas (teacher_subjects), list_all
- **ParentRepository** (3 testes): CRUD, link_to_student com verificação, unlink_from_student
- **ClassroomRepository** (2 testes): gravação/leitura de enums, add_student (enrollment)
- **AssessmentRepository** (2 testes): CRUD com enums e data, list_all
- **GradeRepository** (2 testes): save + find_by_student_and_assessment, find_by_bimester com média ponderada (8.0×4 + 10.0×1) / 5 = 8.4
- **AttendanceRepository** (2 testes): save + find_by_period, percentual de presença (7/10 = 70%)
- **Fluxo completo** (1 teste): cria turma, matricula, avalia, registra presença, verifica tudo

---

## Casos de Uso (10)

### Cadastro (3)
1. ManterCadastroAluno — CRUD de estudante (via StudentRepository)
2. ManterCadastroProfessor — CRUD de professor (via TeacherRepository)
3. ManterCadastroResponsavel — CRUD de responsável (via ParentRepository)

### Vínculos e Matrícula (2) — ServicosSecretaria
4. matricular_aluno — Matricula aluno na turma (classroom_enrollments)
5. vincular_responsavel — Liga responsável ao aluno (student_parent)

### Notas e Boletim (3) — ServicosDoAluno
6. lancar_nota — Registra nota com validações
7. calcular_media_bimestral — Calcula média ponderada por peso
8. gerar_boletim — Boletim anual com situação (aprovado/reprovado/incompleto)

### Frequência (1) — ServicosDoAluno
9. consultar_extrato — Resumo de frequência por período

### Presença (via repositório direto)
10. RegistrarPresenca — Registra presença/falta (AttendanceRepository.save)

---

## Métricas

### Linhas de Código (src/)
```
src/infrastructure/database.py           679 linhas  (DatabaseManager + 7 repositórios)
src/domain/models.py                     397 linhas  (4 enums + 7 classes)
src/application/services.py              232 linhas  (2 serviços + 2 dataclasses)
src/infrastructure/schema.sql            211 linhas  (11 tabelas + 11 índices)
src/utils.py                             131 linhas  (validações)
src/__init__.py + domain + app + infra    66 linhas  (exportações)
------------------------------------------------------
Código-fonte total (src/):             1.716 linhas
```

### Demonstração
```
main.py                                  465 linhas
------------------------------------------------------
Total com demonstração:                2.181 linhas
```

### Testes
```
test_manual_repositories.py              385 linhas  (16 testes)
test_entities.py                         206 linhas  (30 testes)
test_integrity.py                         59 linhas  (5 testes)
test_cpf_validation.py                    39 linhas  (6 testes)
test_passing_grade.py                     20 linhas  (3 testes)
tests/__init__.py + unit + integration     5 linhas
------------------------------------------------------
Testes total:                            714 linhas  (60 testes)
```

### Banco de Dados
```
Tabelas:                    11
Índices explícitos:         11
Chaves primárias:           INTEGER AUTOINCREMENT
Foreign keys:               CASCADE / RESTRICT / SET NULL
CHECK constraints:          18
UNIQUE constraints:         11
------------------------------------------------------
Total de tabelas:           11
```

---

## Como Executar

### Instalação
```bash
cd etapa_2-v2
python -m venv .venv
.venv\Scripts\activate       # Windows
source .venv/bin/activate    # Linux/Mac
pip install -r requirements.txt
```

### Rodar a Demonstração
```bash
python main.py
```

### Rodar os Testes
```bash
pytest tests/ -v
```

---

## Tecnologias

- **Python 3.12+** — Linguagem principal
- **SQLite** — Banco de dados embutido (não precisa instalar nada)
- **pytest** — Framework de testes
- **Bibliotecas padrão:** sqlite3, datetime, re, os, pathlib, enum, dataclasses
