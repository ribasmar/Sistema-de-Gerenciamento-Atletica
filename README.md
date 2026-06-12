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

Fluxo completo por JSON:

```bash
python codigo/app.py executar-fluxo --input codigo/dados_demo.json
```

Menu interativo:

```bash
python codigo/app.py menu
```

Ao cadastrar atleta ou membro pelo menu, e possivel enviar uma declaracao de
matricula em HTML. Os dados extraidos do HTML nao sao pedidos novamente no
cadastro.

Importacao de declaracao de matricula em HTML:

```bash
python codigo/app.py importar-declaracao-html --input codigo/declaracao_exemplo.html
```

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
