# Sistema de Gerenciamento de Atlética

## Descrição do Projeto

O Sistema de Gerenciamento de Atlética tem como objetivo centralizar e automatizar os processos administrativos e esportivos de uma atlética universitária. Atualmente, diversas atividades são realizadas de forma manual, descentralizada ou repetitiva, causando retrabalho e dificuldade no gerenciamento de informações.

O sistema permitirá o cadastro e gerenciamento de atletas, treinadores, treinos, competições e documentos acadêmicos, além de oferecer um hub central de informações para os membros da atlética.

---

## Problema que o Sistema Resolve

As atléticas universitárias frequentemente enfrentam problemas como:

- Cadastro repetitivo de atletas para diferentes eventos e competições;
- Falta de centralização de documentos dos atletas;
- Dificuldade em organizar treinos e escala de treinadores;
- Controle manual de participação em competições;
- Comunicação descentralizada entre membros da atlética;
- Ausência de um portal único para acesso às informações importantes.

O sistema busca resolver esses problemas por meio de uma plataforma integrada, segura e organizada.

---

## Público-Alvo

O sistema será utilizado principalmente por:

- Membros administrativos da atlética;
- Atletas universitários;
- Treinadores;
- Coordenadores esportivos;
- Diretoria da atlética.

---

## Funcionalidades Principais

### Gerenciamento de Atletas
- Cadastro de atletas;
- Armazenamento de documentos;
- Histórico esportivo;
- Participação em competições.

### Gerenciamento de Treinos
- Criação e organização de treinos;
- Controle de presença;
- Associação de treinadores.

### Gerenciamento de Competições
- Cadastro de competições;
- Convocação de atletas;
- Controle de inscrições.

### Escala de Treinadores
- Organização de horários;
- Distribuição de responsáveis por treino.

### Hub de Informações
- Divulgação de atividades;
- Avisos e comunicados;
- Calendário esportivo.

---

## Modelagem Inicial de Usuários

### Aluno
- Nome
- RA
- CPF
- Curso
- Data de nascimento
- Início de egresso
- Período atual
- Tempo esperado de conclusão
- Documentos gerais comprobatórios da universidade

### Membro da Atlética
- Nome
- RA
- Documento pessoal
- Curso
- Cargo
- Tempo na atlética (início e fim esperado)
- CPF
- Data de nascimento
- Início de egresso
- Período atual
- Tempo esperado de conclusão
- Documentos gerais comprobatórios da universidade

---

## Histórias de Usuário

- Eu, como membro da Atlética, preciso cadastrar atletas repetidamente.
- Eu, como responsável esportivo, preciso gerenciar treinos.
- Eu, como responsável esportivo, preciso gerenciar atletas para competições.
- Eu, como coordenador, preciso gerenciar escala de treinadores.
- Eu, como atleta, não quero ter que enviar documentos repetidamente.
- Eu, como atleta, gostaria de um hub de informações sobre as atividades da atlética.

---

## Equipe do Projeto

#### Lucas
#### Tiene
#### Ribas

---

## Como Executar

Os dados das entidades sao recebidos por arquivos CSV (um por entidade) na pasta
`codigo/data/forms/`, como respostas de formulario. O processamento le esses CSVs
e gera um relatorio Markdown com os dados gerenciados da atletica:

```bash
python codigo/app.py
```

Saida padrao: `codigo/data/relatorio_atletica.md`. As colunas e convencoes de cada
CSV estao documentadas em `codigo/data/forms/README.md`.

A declaracao de matricula em HTML e enviada a parte: o CSV referencia o arquivo
pela coluna `comprovante_matricula`, e o sistema le apenas arquivos contidos na
pasta `codigo/data/` (sem caminho absoluto e sem path traversal). O CSV e a fonte
autoritativa; o HTML apenas preenche campos academicos deixados em branco.

Para escolher outra pasta de CSVs ou outro arquivo de saida:

```bash
python codigo/app.py --dir codigo/data/mocks --output codigo/data/mocks/relatorio_mock.md
```

---

## Decisões de Projeto

- **Entrada por CSV (uma planilha por entidade)** e **saída em relatório Markdown**:
  um único fluxo de processamento, sem interface gráfica, em Python puro.
- **Referências por chave natural** entre entidades (treinador por CPF, atleta por
  RA), evitando expor identificadores internos nos CSVs.
- **Declaração de matrícula (HTML) enviada à parte**, referenciada pelo CSV e lida
  de forma contida (sem caminho absoluto e sem path traversal); o CSV é a fonte
  autoritativa e o HTML só preenche campos vazios.
- **Armazenamento em memória** isolado pela camada Repository, mantendo o protótipo
  simples e os testes determinísticos.
- **Padrões de projeto:** Service Layer (`servicos.py`), Repository
  (`repositorios.py`) e Observer (`eventos.py`).

## Documentação

- [`docs/requisitos.md`](docs/requisitos.md) — elicitação, histórias de usuário e validação.
- [`docs/arquitetura.md`](docs/arquitetura.md) — arquitetura, componentes, padrões e trade-offs.
- [`docs/testes.md`](docs/testes.md) — estratégia de testes, cobertura e lacunas.

<!-- 
---

## Tecnologias Previstas

- Frontend: React / Vue.js
- Backend: Node.js / Java Spring Boot
- Banco de Dados: PostgreSQL
- Controle de Versão: Git e GitHub

---

## Objetivo Final

Desenvolver uma plataforma completa para facilitar a gestão esportiva e administrativa da atlética universitária, reduzindo retrabalho, melhorando a organização interna e proporcionando uma melhor experiência para atletas e gestores. -->
