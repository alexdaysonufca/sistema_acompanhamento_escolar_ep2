-- Estudantes
CREATE TABLE students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    registration VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_name_length CHECK (LENGTH(TRIM(name)) >= 3),
    CONSTRAINT chk_registration_length CHECK (LENGTH(TRIM(registration)) >= 3),
    CONSTRAINT chk_email_format CHECK (email LIKE '%@%')
);

-- Responsáveis
CREATE TABLE parents (
    parent_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    cpf CHAR(11) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_parent_name CHECK (LENGTH(TRIM(name)) >= 3),
    CONSTRAINT chk_cpf_length CHECK (LENGTH(cpf) = 11),
    CONSTRAINT chk_parent_email CHECK (email LIKE '%@%')
);

-- Vínculo Estudante-Responsável
CREATE TABLE student_parent (
    student_id INTEGER NOT NULL,
    parent_id INTEGER NOT NULL,
    relationship_type VARCHAR(50) DEFAULT 'Responsável',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (student_id, parent_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES parents(parent_id) ON DELETE CASCADE
);

-- Professores
CREATE TABLE teachers (
    teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_teacher_name CHECK (LENGTH(TRIM(name)) >= 3),
    CONSTRAINT chk_teacher_email CHECK (email LIKE '%@%')
);

-- Disciplinas do Professor
CREATE TABLE teacher_subjects (
    teacher_id INTEGER NOT NULL,
    subject VARCHAR(100) NOT NULL,
    
    PRIMARY KEY (teacher_id, subject),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE CASCADE
);

-- Turmas (turno e nível como texto direto)
CREATE TABLE classrooms (
    classroom_id INTEGER PRIMARY KEY AUTOINCREMENT,
    year VARCHAR(50) NOT NULL,
    identifier CHAR(1) NOT NULL,
    shift VARCHAR(20) NOT NULL,
    education_level VARCHAR(30) NOT NULL,
    teacher_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_year_length CHECK (LENGTH(TRIM(year)) >= 2),
    CONSTRAINT chk_identifier CHECK (identifier GLOB '[A-Z]'),
    CONSTRAINT chk_shift CHECK (shift IN ('MANHA', 'TARDE', 'NOITE', 'INTEGRAL')),
    CONSTRAINT chk_level CHECK (education_level IN ('INFANTIL', 'FUNDAMENTAL_I', 'FUNDAMENTAL_II', 'MEDIO')),
    FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id) ON DELETE SET NULL,
    
    UNIQUE (year, identifier, shift)
);

-- Matrículas
CREATE TABLE classroom_enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    classroom_id INTEGER NOT NULL,
    academic_year INTEGER NOT NULL,
    enrollment_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    
    CONSTRAINT chk_academic_year CHECK (academic_year >= 2000),
    CONSTRAINT chk_enrollment_status CHECK (status IN ('ACTIVE', 'TRANSFERRED', 'WITHDRAWN', 'COMPLETED')),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (classroom_id) REFERENCES classrooms(classroom_id) ON DELETE RESTRICT,
    
    UNIQUE (student_id, classroom_id, academic_year)
);

-- Avaliações (tipo e bimestre como texto direto)
CREATE TABLE assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    description TEXT,
    max_score DECIMAL(5,2) NOT NULL,
    weight DECIMAL(5,2) NOT NULL DEFAULT 1.0,
    assessment_type VARCHAR(30) NOT NULL,
    bimester VARCHAR(20) NOT NULL,
    academic_year INTEGER NOT NULL,
    assessment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_max_score CHECK (max_score > 0 AND max_score <= 10.0),
    CONSTRAINT chk_weight CHECK (weight > 0 AND weight <= 10.0),
    CONSTRAINT chk_assessment_year CHECK (academic_year >= 2000),
    CONSTRAINT chk_assessment_type CHECK (
        assessment_type IN ('PROVA', 'TRABALHO', 'SEMINARIO', 'ATIVIDADE_PRATICA', 'PARTICIPACAO', 'PROJETO')
    ),
    CONSTRAINT chk_bimester CHECK (
        bimester IN ('PRIMEIRO', 'SEGUNDO', 'TERCEIRO', 'QUARTO')
    )
);

-- Notas
CREATE TABLE grades (
    grade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    assessment_id INTEGER NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_score_positive CHECK (score >= 0),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE RESTRICT,
    
    UNIQUE (student_id, assessment_id)
);

-- Presença
CREATE TABLE attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject VARCHAR(100) NOT NULL,
    attendance_date DATE NOT NULL,
    is_present BOOLEAN NOT NULL DEFAULT 1,
    is_justified BOOLEAN NOT NULL DEFAULT 0,
    justification TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_justification_logic CHECK (
        (is_justified = 0 AND justification IS NULL) OR
        (is_justified = 1 AND justification IS NOT NULL)
    ),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    
    UNIQUE (student_id, subject, attendance_date)
);

-- Boletins (tabela única com campo opcional para descritivo)
CREATE TABLE report_cards (
    report_card_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject VARCHAR(100) NOT NULL,
    bimester VARCHAR(20) NOT NULL,
    academic_year INTEGER NOT NULL,
    education_level VARCHAR(30) NOT NULL,
    grade DECIMAL(5,2),
    development_level VARCHAR(30),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT chk_report_year CHECK (academic_year >= 2000),
    CONSTRAINT chk_bimester_report CHECK (bimester IN ('PRIMEIRO', 'SEGUNDO', 'TERCEIRO', 'QUARTO')),
    CONSTRAINT chk_level_report CHECK (education_level IN ('INFANTIL', 'FUNDAMENTAL_I', 'FUNDAMENTAL_II', 'MEDIO')),
    CONSTRAINT chk_grade_range CHECK (grade IS NULL OR (grade >= 0 AND grade <= 10.0)),
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    
    UNIQUE (student_id, subject, bimester, academic_year)
);


-- ============================================================
-- Índices para consultas frequentes
-- (As UNIQUE constraints já criam índices automaticamente;
--  estes são complementares para buscas por nome, data, etc.)
-- ============================================================

-- Busca de estudantes por nome
CREATE INDEX idx_student_name ON students(name);

-- Busca de responsáveis por nome
CREATE INDEX idx_parent_name ON parents(name);

-- Busca de professores por nome
CREATE INDEX idx_teacher_name ON teachers(name);

-- Frequência: busca por data e por aluno+disciplina
CREATE INDEX idx_attendance_date ON attendance(attendance_date);
CREATE INDEX idx_attendance_student_subject ON attendance(student_id, subject);

-- Notas: busca por aluno
CREATE INDEX idx_grade_student ON grades(student_id);

-- Avaliações: busca por disciplina e bimestre
CREATE INDEX idx_assessment_subject_bimester ON assessments(subject, bimester);

-- Matrículas: busca por aluno e por turma
CREATE INDEX idx_enrollment_student ON classroom_enrollments(student_id);
CREATE INDEX idx_enrollment_classroom ON classroom_enrollments(classroom_id);

-- Boletins: busca por aluno e ano
CREATE INDEX idx_report_student_year ON report_cards(student_id, academic_year);


