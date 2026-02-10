# Relatório de Atendimento aos Requisitos - Projeto Integrado (Etapa 2)

**Estudantes:** Antonio Alex Dayson Tomaz e Maria Alexsandra Tomaz  
**Curso:** Análise e Desenvolvimento de Sistemas (UFCA)  
**Data:** 09/02/2026

---

## 1. Introdução e Compreensão do Escopo

A equipe compreendeu que o objetivo central da Etapa 2 transcendia a mera implementação de funcionalidades. O desafio consistia em evoluir o protótipo da Etapa 1 (baseado em memória) para um **sistema robusto, persistente e arquiteturalmente estruturado**, aplicando conceitos fundamentais de Engenharia de Software e Banco de Dados.

Interpretamos os requisitos como um pedido por **profissionalismo e integridade**: o sistema não deveria apenas "funcionar no caso feliz", mas ser capaz de resistir a dados inválidos, garantir a consistência das informações e ser facilmente auditável por meio de testes e documentação.

---

## 2. Detalhamento do Atendimento aos Requisitos

Abaixo, apresentamos como cada pilar do entregável foi compreendido e executado, com suas respectivas evidências no código-fonte.

### 2.1. Projeto Físico de Banco de Dados (Implementação e Integridade)

**Compreensão:** Entendemos que o banco de dados é a "fundação" do sistema. Um modelo lógico precisa ser traduzido fisicamente com regras rígidas para impedir a corrupção dos dados.

**Como Atendemos:**
- Migramos 100% da persistência para **SQLite**, abandonando listas temporárias.
- Projetamos o esquema manualmente (`SQL DDL`) em vez de usar ORMs automáticos, garantindo controle total sobre tipos e performance.
- Implementamos **Normalização** para evitar redundâncias (ex: tabelas separadas para Alunos, Responsáveis e Turmas).

**Evidências:**
- **Arquivo `src/infrastructure/schema.sql`:** Contém a definição explícita de 11 tabelas.
- **Uso de Constraints (Travas de Segurança):**
  - *Integridade de Domínio:* `CHECK (score >= 0 AND score <= 10.0)` impede notas absurdas.
  - *Integridade Referencial:* Uso de `FOREIGN KEY ... ON DELETE CASCADE` para garantir que, ao remover um aluno, suas notas não fiquem "órfãs" no sistema.
  - *Unicidade:* `UNIQUE (email)` e `UNIQUE (cpf)` impedem duplicidade de cadastros.
- **Performance:** Criação de 11 índices manuais (`CREATE INDEX`) para otimizar buscas por nome e data.

### 2.2. Arquitetura e Organização do Código

**Compreensão:** O código precisa ser legível e separado por responsabilidades. Misturar SQL com regras de negócio e interface dificulta a manutenção.

**Como Atendemos:**
Adotamos uma arquitetura em camadas inspirada em princípios de *Clean Architecture*:

1.  **Domain (`src/domain`):** As classes principais (`Student`, `Teacher`, etc.) são puras. Elas não sabem que o banco de dados existe.
2.  **Application (`src/application`):** Os serviços (`ServicosDoAluno`, `ServicosSecretaria`) orquestram as regras de negócio (ex: calcular média, gerar boletim).
3.  **Infrastructure (`src/infrastructure`):** Onde o SQL reside. Isolamos o acesso a dados aqui para que, se trocarmos o banco no futuro, o resto do sistema não quebre.

**Evidências:**
- Separação clara de pastas em `src/`.
- O arquivo `database.py` centraliza toda a lógica de conexão, utilizando o padrão **Repository Pattern** (`StudentRepository`, `GradeRepository`) para abstrair o SQL do resto do sistema.

### 2.3. Qualidade de Software e Testes

**Compreensão:** Um sistema sem testes é um sistema não confiável. A entrega exigia prova de que as funcionalidades operam corretamente sob diversas condições.

**Como Atendemos:**
Desenvolvemos uma suíte de testes automatizados utilizando o framework **pytest**.

**Evidências:**
- **60 Testes Automatizados:** Cobrindo 100% das entidades e fluxos principais.
- **Testes Unitários (`tests/unit`):** Validam regras isoladas, como o dígito verificador de um CPF (`utils.py`) ou o cálculo de média.
- **Testes de Integração (`tests/integration`):** Criam um banco de dados real em memória, inserem dados, executam operações e verificam se o resultado gravado está correto.
- **Execução:** O comando `pytest` roda toda a bateria em menos de 2 segundos, garantindo feedback rápido.

### 2.4. Documentação e Componente Extensionista

**Compreensão:** O projeto deve ser acessível. A documentação não server apenas para o professor, mas para compartilhar conhecimento com outros estudantes.

**Como Atendemos:**
- Atualizamos o `README.md` não apenas com comandos técnicos, mas com uma **seção educativa** explicando o que é um Projeto Físico de Banco de Dados de forma didática (analogia da "Planta Baixa vs. Construção").
- Criamos o `DESCRICAO_DO_PROJETO.md` com métricas detalhadas (contagem de linhas, estrutura de arquivos) para facilitar a navegação pelo corretor.

---

## 3. Conclusão

A equipe considera que os requisitos foram plenamente atendidos e superados. Entregamos não apenas um software funcional, mas um projeto de engenharia, com preocupações reais sobre performance (índices), integridade (constraints), manutenibilidade (arquitetura) e confiabilidade (testes).

O sistema está pronto para ser auditado, utilizado como base de aprendizado por colegas, ou evoluído para etapas futuras (como uma interface Web/API).


### a) Definição do Projeto Físico e Diagrama
**Como foi feita a definição:**
A transição do modelo lógico para o físico foi realizada através de um mapeamento manual e criterioso, sem o uso de ferramentas de geração automática, para garantir controle total sobre a performance e integridade.

1.  **Refinamento dos Tipos de Dados:**
    Analisamos cada atributo das classes Python (`domain/models.py`) e escolhemos o tipo SQL mais adequado:
    -   *Strings:* Usamos `VARCHAR(N)` definindo limites (ex: 200 chars para nomes) para otimizar armazenamento.
    -   *Booleans:* Como o SQLite não tem tipo boolean nativo, definimos o uso de `INTEGER (0/1)` com a abstração transparente feita pelo driver.
    -   *Decimais:* Para notas e pesos, rejeitamos o `FLOAT` em favor de `DECIMAL(5,2)` para garantir precisão exata (duas casas decimais), crítica para cálculos de média escolar.

2.  **Modelagem dos Relacionamentos (Diagrama em Código):**
    A estrutura relacional (Diagrama Físico) foi implementada em SQL puro no arquivo `schema.sql`.
    -   **Relacionamento N:N (Muitos-para-Muitos):** Identificado entre *Alunos* e *Responsáveis*. Solucionado criando a tabela associativa `student_parent` com chave primária composta `(student_id, parent_id)`.
    -   **Relacionamento 1:N (Um-para-Muitos):** Identificado entre *Professor* e *Turmas* (`classrooms`). Implementado com a FK `teacher_id` na tabela `classrooms`.
    -   **Dependência Existencial:** Tabelas como `grades` (Notas) e `attendance` (Frequência) foram definidas como dependentes de `students`. Utilizamos `ON DELETE CASCADE` para que a exclusão de um aluno limpe automaticamente seus registros associados.

3.  **Normalização:**
    Aplicamos regras de normalização para evitar redundâncias. Por exemplo, o *Endereço* ou dados detalhados do *Responsável* não são repetidos na tabela do aluno; eles residem em suas próprias tabelas, vinculados apenas por IDs.

**Evidência:**
O arquivo `src/infrastructure/schema.sql` (211 linhas) representa a concretização desse diagrama, contendo todas as definições de tabelas (DDL), chaves primárias, estrangeiras e índices.

#### b) Justificativas e Lógica Adotada (Tabelas, Tipos e Restrições)
**R:**
A lógica do banco de dados priorizou a integridade referencial, a performance em consultas e a segurança dos dados. Abaixo, detalhamos as decisões técnicas baseadas na realidade do projeto:

*   **Tabelas e Normalização:** Adotamos a Terceira Forma Normal (3FN) para evitar redundâncias, separando os atores (Student, Teacher, Parent) de suas interações acadêmicas (Grade, Attendance).
*   **Tipos de Dados:**
    *   *IDs:* Optamos por `INTEGER PRIMARY KEY AUTOINCREMENT` em vez de UUIDs. **Justificativa:** IDs numéricos sequenciais são mais eficientes para índices do SQLite e mais fáceis de ler/debugar manualmente durante o desenvolvimento acadêmico.
    *   *Booleanos:* Utilizamos `BOOLEAN` (armazenado internamente como INTEGER 0/1 pelo SQLite) para flags como `is_present`.
    *   *Valores Monetários/Notas:* Utilizamos `DECIMAL(5,2)` para notas e pesos. **Justificativa:** O ponto flutuante padrão (`FLOAT`) pode gerar imprecisões de arredondamento; o DECIMAL garante exatidão nas médias (ex: 8.62).
*   **Chaves e Relacionamentos:** Implementamos chaves estrangeiras (`FOREIGN KEY`) com cláusulas explícitas:
    *   `ON DELETE CASCADE`: Para vínculos fortes (ex: remover aluno apaga notas). Evita inconsistência e dados órfãos.
    *   `ON DELETE RESTRICT`: Para segurança (ex: não permitir apagar uma turma se houver alunos).
*   **Restrições (Constraints):** Aplicamos `CHECK` constraints críticas como a "última linha de defesa" do sistema.
    *   *Exemplos Reais:* `CHECK (score >= 0 AND score <= 10.0)` impede notas inválidas; `CHECK (length(cpf) = 11)` valida documentos no nível do banco.
*   **Índices (Performance):** Contrariando a premissa de simplificação excessiva, decidimos criar **11 índices manuais** (`CREATE INDEX`) em colunas de alta seletividade (como `idx_student_name` e `idx_attendance_date`). **Justificativa:** Garantir que buscas por nome ou data sejam performáticas mesmo com o crescimento da base.
*   **Enums como Texto Legível:** Para campos categóricos como *Turno* (`MANHA`, `TARDE`) e *Bimestre* (`PRIMEIRO`, ...), optamos por armazenar a string descritiva validada por `CHECK constraints`, em vez de números inteiros opacos. **Justificativa:** Facilita a auditoria e manutenção direta no banco (`school.db`), tornando o dado autoexplicativo sem necessidade de tabelas de domínio auxiliares ("look-up tables") para este escopo.
*   **Padronização de Datas:** Como o SQLite não possui tipo `DATE` nativo, padronizamos todas as datas no formato **ISO-8601 (YYYY-MM-DD)** armazenadas como `TEXT` ou `DATE` (alias). **Justificativa:** Esse formato garante que a ordenação cronológica funcione corretamente através da ordenação alfabética de strings, essencial para os relatórios de frequência.

**Evidência:**
As validações e tipos mencionados podem ser verificados no arquivo `src/infrastructure/schema.sql`, especificamente nas linhas de definição de `grades` (decimais e constraints) e `students` (IDs e unicidade). Além disso, os testes unitários (`tests/unit/test_entities.py`) confirmam que o sistema rejeita dados que violem essas regras lógicas antes mesmo de chegar ao banco.

### 5. Evidências de Funcionamento

- **Persistência Real:** O arquivo `main.py` serve como a principal evidência, demonstrando o ciclo completo de vida dos dados (CRUD) de todas as entidades diretamente no arquivo `school.db`.
- **Casos de Uso:** Implementamos **10 casos de uso core**, com destaque para o *Gerar Boletim Estudante*, que realiza a consolidação de notas e frequências dos quatro bimestres.
- **Validação Automatizada:** O projeto conta com **5 arquivos de testes** (totalizando 60 testes) que validam desde a criação de entidades até a integridade referencial do banco de dados.
