# Sprint 2: Sistema de Gestão de Atléticas

## Visão Geral

Esta sprint tem como foco a definição da fundação técnica do **Sistema de Gestão de Atléticas**. A partir do levantamento de requisitos, validações e fluxos de interações mapeados na Sprint 1, estabelecemos a arquitetura, os padrões de projeto e as convenções de código Python que guiarão o desenvolvimento das funcionalidades de cadastro de atletas, gerenciamento de treinos e campeonatos.

---

## 1. Arquitetura: Monolito Modular

Para o desenvolvimento do sistema em Python (utilizando frameworks como FastAPI, Flask ou Django), adotaremos a arquitetura de **Monolito Modular**.

- **Justificativa:** Como o sistema lida com um domínio bem delimitado (Atlética, Atletas, Treinos e Campeonatos), o monolito facilita o desenvolvimento inicial, o _deploy_ e a manutenção. A modularidade garante que o código seja organizado por contextos de negócio (módulos ou _Blueprints_/_Apps_ independentes), permitindo que, no futuro, o sistema possa ser facilmente escalado ou fatiado em microsserviços.
- **Divisão de Módulos (Baseada nos fluxos da Sprint 1):**
- Módulo de Gestão de Pessoas (Atlética e Atletas).
- Módulo de Gestão de Treinos (Treinadores, Locais e Horários).
- Módulo de Campeonatos (Inscrições, Modalidades e Transporte).

---

## 2. Padrões de Projeto (Design Patterns)

Para garantir um código Python limpo, testável e de fácil manutenção, utilizaremos os seguintes padrões:

### 2.1. Service Layer (Camada de Serviço)

- **Objetivo:** Isolar as regras de negócio das rotas (controllers/views) e do acesso a dados.
- **Aplicação:** Toda a lógica descrita nas histórias de usuário, como verificar se um CPF/RA está duplicado ao cadastrar um membro ou validar se a data de fim de um campeonato não é anterior à de início, será encapsulada em classes ou módulos de _Service_.

### 2.2. Repository (Repositório)

- **Objetivo:** Abstrair a lógica de acesso e manipulação do banco de dados (geralmente implementado junto a ORMs como SQLAlchemy).
- **Aplicação:** Os repositórios serão responsáveis por receber os dicionários ou objetos mapeados (como o `id_atletica`, `documentos_universidade`, etc.) e persistir ou buscar as informações de Atletas, Treinos e Campeonatos sem que a camada de Serviço precise saber se o banco é PostgreSQL, MySQL, etc.

### 2.3. Observer (Observador)

- **Objetivo:** Criar um mecanismo de notificação ou reação a eventos dentro do sistema de forma desacoplada (no Python, pode ser implementado via bibliotecas de sinais como `blinker` ou `Django Signals`).
- **Aplicação:** Será utilizado para atualizar o status do sistema de forma reativa. Por exemplo, quando um _Treino_ for atualizado (mudança de horário ou localidade), um evento será disparado para notificar a lista de `atletas_inscritos` ou gerentes sobre a alteração, sem acoplar a lógica de notificação diretamente na função de atualização do treino.

---

## 3. Diagrama de Classes: Arquitetura e Padrões de Projeto

Abaixo está a representação estrutural focada exclusivamente na arquitetura e nos padrões de projeto adotados (Service Layer, Repository e Observer).

![Diagrama de Classes da Sprint 2](./diagrama_design_patterns.png)

---

## 4. Padrões do Projeto

Para mantermos a consistência e a qualidade durante a Sprint 2 e as subsequentes, a equipe deve seguir as diretrizes abaixo, baseadas nas recomendações oficiais do Python (PEP 8):

### 4.1. Padrões de Commits (Conventional Commits)

Utilizaremos a padronização do _Conventional Commits_ para manter o histórico do Git legível e automatizável:

- `feat:` Para novas funcionalidades (ex: `feat: adiciona service de criacao de treinos`).
- `fix:` Para correção de bugs (ex: `fix: corrige validacao de data no campeonato`).
- `docs:` Para alterações na documentação (ex: `docs: atualiza readme da sprint 2`).
- `refactor:` Para refatoração de código que não adiciona _feature_ nem corrige _bug_.
- `test:` Para adição ou correção de testes (ex: utilizando `pytest`).
- `chore:` Para atualizações de dependências (ex: `requirements.txt` ou `pyproject.toml`).

### 4.2. Estratégia de Branches

Seguiremos um fluxo simplificado baseado no **GitHub Flow**:

- `main`: Código de produção, sempre estável.
- `develop`: Ramo principal de integração de desenvolvimento.
- `feature/nome-da-feature`: Para o desenvolvimento das histórias de usuário (ex: `feature/cadastro-atleta`).
- `bugfix/nome-do-bug`: Para correções fora do fluxo normal.

### 4.3. Padrões de Nomenclatura (PEP 8) e Idioma

- O código-fonte deverá ser escrito em **Português (PT-BR)**, alinhando-se aos _inputs_ e _outputs_ (JSON) já definidos na arquitetura.
- O Python favorece `snake_case`, o que já encaixa perfeitamente com os _payloads_ JSON da Sprint 1 (ex: `id_atletica`, `documentos_universidade`).
- **Classes e Exceções:** `PascalCase` (ex: `AtletaService`, `TreinoRepository`).
- **Métodos, Variáveis e Funções:** `snake_case` (ex: `criar_treino`, `id_atletica`).
- **Constantes:** `UPPER_SNAKE_CASE` (ex: `STATUS_CONFIRMADO`).

### 4.4. Tipagem, Comentários e Documentação

- **Type Hints (PEP 484):** Obrigatório o uso de tipagem nas assinaturas de métodos de _Service_ e _Repository_ (ex: `def criar_treino(dados: dict) -> str:`), facilitando a leitura e a integração com IDEs.
- **Docstrings (PEP 257):** Obrigatórias para classes e métodos públicos. Devem utilizar aspas triplas (`"""`) e descrever o que o método faz, seus parâmetros (`Args:`) e o retorno (`Returns:`).
- **Comentários em linha (`#`):** Evitar redundância. Utilizar apenas para explicar trechos de lógica complexa ou regras de negócio não triviais. O código deve ser descritivo o suficiente para não depender de comentários em linha. Utilizaremos ferramentas como `black` ou `ruff` para garantir a formatação uniforme.
