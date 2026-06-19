# Requisitos — Sistema de Gerenciamento de Atlética

Síntese da engenharia de requisitos (elicitação, histórias de usuário, validação)
e o contrato de entrada/saída do sistema. Consolida o material da Sprint 1,
alinhado ao fluxo atual de entrada por CSV e saída em relatório Markdown.

## 1. Problema, público-alvo e relevância

Atléticas universitárias gerenciam atletas, treinadores, treinos e campeonatos de
forma manual e descentralizada (WhatsApp, planilhas, drives, papel). Isso gera
retrabalho no recadastro de atletas a cada competição, perda de documentos e
dificuldade para organizar treinos e convocações.

**Público-alvo:** membros da diretoria da atlética (presidência, esportes, eventos,
marketing, gestão de pessoas), treinadores e atletas universitários.

**Relevância:** o sistema centraliza o cadastro único de atletas e seus documentos,
a escala de treinadores/treinos e a montagem de campeonatos, reduzindo retrabalho
e erros de integridade (CPF/RA duplicado, referências inexistentes, datas inválidas).

## 2. Síntese da elicitação

Foram realizadas três entrevistas com gestores de atléticas (fontes reais):

- **Ex-presidente — Atlética XII de Março (UTFPR, Apucarana):** cadastro por
  declaração de matrícula enviada via WhatsApp/formulário; dados em drive de
  esportes; convocação informal por WhatsApp.
- **Ex-presidente — VII de Abril (UNIFIL, Londrina):** lista de atletas (nome,
  curso, matrícula) conferida por declaração de matrícula/diploma; diretoria de
  esportes dividida por modalidade; treino em formato de "racha" com custo do
  treinador rateado entre os presentes.
- **Ex-vice-presidente — Exatas (UEL, Londrina):** lista da universidade +
  comprovante individual de matrícula; arquivos físicos descartados após uso; um
  assessor de esportes por modalidade, custos rateados.

**Convergências:** a declaração de matrícula é o documento-chave; o recadastro é
repetitivo; a gestão de treinos/treinadores é informal; os dados ficam dispersos.

## 3. Histórias de usuário (com critérios de aceitação e priorização)

### HU-01 [ALTA] — Cadastro único de atletas
Como membro da atlética, quero cadastrar atletas uma única vez (dados pessoais,
documentos de matrícula e esportes), para não repetir o processo a cada competição.

Critérios de aceitação:

- O sistema registra atleta com nome, RA, CPF, curso, datas, período, conclusão,
  esportes e documento de matrícula.
- RA ou CPF já existentes são rejeitados como conflito de integridade, sem
  interromper o processamento dos demais registros.
- Cada atleta cadastrado recebe um identificador único.

### HU-02 [ALTA] — Gerenciamento de treinos
Como membro da atlética, quero criar e atualizar treinos vinculando treinador,
local, horário e atletas, para organizar a agenda por modalidade.

Critérios de aceitação:

- Só é possível criar treino com treinador e atletas previamente cadastrados.
- Treinador ou atleta inexistente gera conflito de integridade.
- Atualizar um treino registra os campos alterados e notifica a mudança.

### HU-03 [ALTA] — Escala de treinadores
Como membro da atlética, quero manter um catálogo de treinadores (dados, modalidade,
salário por treino) para vinculá-los aos treinos quando acionados.

Critérios de aceitação:

- O sistema registra treinador com nome, CPF, modalidade, salário e telefone.
- O treinador fica disponível para vínculo em treinos e campeonatos.

### HU-04 [MÉDIA] — Menos repetição de documentos para o atleta
Como atleta, não quero reenviar documentos repetidamente; quero enviar apenas a
declaração de matrícula.

Critérios de aceitação:

- A declaração de matrícula (HTML) é referenciada pelo cadastro e lida com
  segurança (ver seção 5).
- Dados acadêmicos ausentes (nome, RA, curso, período) podem ser preenchidos a
  partir da declaração.

### HU-05 [ALTA] — Gestão de campeonatos
Como membro da atlética, quero montar campeonatos com modalidades, treinador
responsável, atletas convocados, transporte, datas e locais.

Critérios de aceitação:

- A data de fim não pode ser anterior à de início (validação temporal).
- Treinador responsável e atletas convocados devem existir.

### HU-06 [BAIXA] — Hub de informações
Como atleta, gostaria de um hub de informações da atlética. *Fora do escopo desta
entrega (registrada como evolução futura).*

## 4. Validação aplicada

- **Ambiguidade resolvida:** "gerenciar atletas para competições" era redundante
  com HU-01 e HU-05; foi descartada como história isolada.
- **Conflito identificado:** modelos de gestão variam por atlética (racha,
  rateio, listas físicas). O sistema padroniza o cadastro/estrutura sem impor o
  modelo financeiro de cada atlética.
- **Questões em aberto:** controle financeiro do rateio de treinos e o hub de
  informações (HU-06) ficaram fora do escopo desta entrega.

## 5. Contrato de entrada e saída

**Entrada — arquivos CSV (respostas de formulário).** Uma pasta contém um CSV por
entidade: `atletica`, `atleta`, `membro`, `treinador`, `treino`,
`atualizacao_treino` e `campeonato`. Convenções: vírgula como delimitador, `;`
para listas dentro de uma célula, datas em `AAAA-MM-DD`, decimais com ponto, UTF-8.
As referências entre entidades usam chaves naturais (treinador por CPF, atleta por
RA). O formato detalhado está em `codigo/data/forms/README.md`.

**Declaração de matrícula (HTML) — enviada à parte.** O CSV referencia o arquivo
pela coluna `comprovante_matricula`. A leitura é contida: somente arquivos dentro
da pasta de dados são aceitos (sem caminho absoluto e sem *path traversal*); em
caso de falha, o cadastro segue com os dados do CSV e registra um alerta. O CSV é
a fonte autoritativa; o HTML apenas preenche campos vazios.

**Saída — relatório Markdown.** O sistema processa os CSVs e gera um `.md` com os
dados gerenciados da atlética: resumo, tabelas de atletas, membros, treinadores,
treinos e campeonatos, notificações e um log de processamento.

**Resultado das operações.** Cada operação produz internamente um
`ResultadoOperacao` com código de saída padronizado, refletido no log do relatório:

- `0 — SUCESSO`
- `1 — ERRO_VALIDACAO` / `ERRO_VALIDACAO_LOGICA` (campos obrigatórios, datas)
- `2 — CONFLITO_INTEGRIDADE` / `REGISTRO_NAO_ENCONTRADO` (duplicidade, referência inexistente)

Execução, a partir de `codigo/`:

```bash
python app.py processar-csv --dir data/forms --output data/relatorio_atletica.md
```
