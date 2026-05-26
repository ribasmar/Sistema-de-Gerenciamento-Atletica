
# Documentação do Sistema de Gestão de Atléticas

## 1. Roteiro e síntese da elicitação realizada (entrevistas, questionários ou análise de similares)

**Questionários:**
- Como é feito hoje o sistema de cadastro de estudante para campeonatos?
  -  É enviado a declaração de matrícula através do Whatsapp e formulário. 
- Como o atleta faz a inscrição para campeonatos hoje?
  - Compra o pacote dos jogos e envia a declaração de matrícula.
- Onde estão armazenadas as informações dos atletas?
  - Em drive de esportes. 
- Onde é feita a coleta de atletas disponíveis para os campeonatos?
  - Eles comparecem ao treino e o treinador os convoca via Whatsapp 
- Como é feita a gerência de treinadores e treinos hoje?
  - Tudo informalmente através do Whatsapp 

---

## 2. Histórias de usuário finalizadas com critérios de aceitação e priorização

* **[ALTA]** Eu, como membro da Atlética, preciso cadastrar atletas repetidamente.
* **[ALTA]** Eu, como membro da Atlética, preciso gerenciar treinos.
* **[ALTA]** Eu, como membro da Atlética, preciso gerenciar atletas para competições.
* **[ALTA]** Eu, como membro da Atlética, preciso gerenciar a escala de treinadores.
* **[MÉDIA]** Eu, como atleta, não quero ter que enviar documentos repetidamente.
* **[BAIXA]** Eu, como atleta, gostaria de um hub de informações sobre as atividades da atlética.

---

## 3. Registro da validação aplicada e Fluxo de Interações

**FLUXO DE INTERAÇÕES:**

`Cadastro da Atlética` ➔ `Cadastro do membro da Atlética` ➔ `Criar treinos` *(treinador, horário, localidade e atletas)* ➔ `Adicionar campeonatos` *(treinador, modalidades, atletas, transporte, datas e locais)*

**Campos levantados para o Cadastro do Atleta:**
* Nome
* RA
* CPF
* Curso
* Data de nascimento
* Início de egresso
* Período atual
* Tempo esperado de conclusão
* Documentos gerais comprobatórios da universidade

---

## 4. Contratos de API (Inputs e Outputs)

Estruturas em formato `.json` para os métodos principais.

### 4.1. Criar Atlética

**INPUT:**
```json
{
  "nome": "Atlética Engenharia",
  "universidade": "Universidade Exemplo",
  "campus": "Campus Central",
  "cnpj": "00000000000100",
  "created_at": "2026-05-22T19:52:25Z"
}

```

**OUTPUT:**

```json
// Status 201 (Created) ou 200 (OK):
{
  "mensagem": "Atlética criada com sucesso!",
  "id_atletica": "123e4567-e89b-12d3-a456-426614174000"
}

// Status 400 (Bad Request):
{
  "erro": "Dados inválidos. O campo 'nome' é obrigatório."
}

// Status 500 (Internal Server Error):
{
  "erro": "Erro interno ao criar a atlética!"
}

```

### 4.2. Cadastro de Atleta

**INPUT:**

```json
{
  "id_atletica": "123e4567-e89b-12d3-a456-426614174000",
  "nome": "Fulano",
  "ra": "a1234567",
  "cpf": "12345678901",
  "curso": "Engenharia Civil",
  "nascimento": "2004-07-07",
  "egresso": "2022-03-17",
  "periodo": 8,
  "conclusao": "2027-01",
  "documentos": [
    {
      "tipo": "comprovante_matricula",
      "url": "[https://storage.exemplo.com/docs/matricula_rafael.pdf](https://storage.exemplo.com/docs/matricula_rafael.pdf)"
    }
  ],
  "created_at": "2026-05-22T19:52:25Z"
}

```

**OUTPUT:**

```json
// Status 201 (Created) ou 200 (OK):
{
  "mensagem": "Atleta cadastrado com sucesso!",
  "id_atleta": "987fcdeb-51a2-43d7-9012-426614174000"
}

// Status 409 (Conflict):
{
  "erro": "Atleta com este CPF ou RA já cadastrado."
}

// Status 500 (Internal Server Error):
{
  "erro": "Erro no cadastro do atleta!"
}

```

### 4.3. Criar Treinos

**INPUT:**

```json
{
  "id_atletica": "123e4567-e89b-12d3-a456-426614174000",
  "modalidade": "Futsal Masculino",
  "id_treinador": "555a4567-e89b-12d3-a456-426614174333",
  "localidade": "Ginásio Principal",
  "dia_semana": "TERCA_FEIRA",
  "horario_inicio": "19:00",
  "horario_fim": "21:00",
  "atletas_inscritos": [
    "987fcdeb-51a2-43d7-9012-426614174000",
    "654abcef-51a2-43d7-9012-426614174111"
  ],
  "created_at": "2026-05-22T19:52:25Z"
}

```

**OUTPUT:**

```json
// Status 201 (Created) ou 200 (OK):
{
  "mensagem": "Treino criado com sucesso!",
  "id_treino": "333c4567-e89b-12d3-a456-426614174999"
}

// Status 404 (Not Found):
{
  "erro": "Treinador ou Atleta não encontrado."
}

// Status 500 (Internal Server Error):
{
  "erro": "Erro ao criar o treino!"
}

```

### 4.4. Criar Membro da Atlética

**INPUT:**

```json
{
  "id_atletica": "123e4567-e89b-12d3-a456-426614174000",
  "nome": "Ciclano",
  "ra": "a1234567",
  "cpf": "12345678901",
  "documento_pessoal": "[https://storage.exemplo.com/docs/rg_mariana.pdf](https://storage.exemplo.com/docs/rg_mariana.pdf)",
  "curso": "Engenharia de Software",
  "cargo": "Diretora de Esportes",
  "tempo_atletica_inicio": "2024-02-15",
  "tempo_atletica_fim_esperado": "2026-12-20",
  "data_nascimento": "2003-05-12",
  "inicio_egresso": "2022-02-10",
  "periodo_atual": 5,
  "tempo_esperado_conclusao": "2026-12",
  "documentos_universidade": [
    {
      "tipo": "comprovante_matricula",
      "url": "[https://storage.exemplo.com/docs/matricula_mariana.pdf](https://storage.exemplo.com/docs/matricula_mariana.pdf)"
    }
  ],
  "created_at": "2026-05-22T20:00:00Z"
}

```

**OUTPUT:**

```json
// Status 201 (Created) ou 200 (OK):
{
  "mensagem": "Membro da atlética cadastrado com sucesso!",
  "id_membro": "444d4567-e89b-12d3-a456-426614174555"
}

// Status 409 (Conflict):
{
  "erro": "Membro com este CPF ou RA já cadastrado."
}

// Status 500 (Internal Server Error):
{
  "erro": "Erro no cadastro do membro da atlética!"
}

```

### 4.5. Gerenciar Treinos (Atualização / Update)

**INPUT:**

```json
{
  "id_treino": "333c4567-e89b-12d3-a456-426614174999",
  "localidade": "Quadra Externa B",
  "horario_inicio": "19:30",
  "horario_fim": "21:30",
  "atletas_inscritos": [
    "987fcdeb-51a2-43d7-9012-426614174000",
    "654abcef-51a2-43d7-9012-426614174111",
    "111bcdef-51a2-43d7-9012-426614174222"
  ],
  "status_treino": "CONFIRMADO",
  "updated_at": "2026-05-22T20:15:00Z"
}

```

**OUTPUT:**

```json
// Status 200 (OK):
{
  "mensagem": "Treino atualizado com sucesso!",
  "id_treino": "333c4567-e89b-12d3-a456-426614174999"
}

// Status 404 (Not Found):
{
  "erro": "Treino não encontrado."
}

// Status 500 (Internal Server Error):
{
  "erro": "Erro ao atualizar os dados do treino!"
}

```

### 4.6. Adicionar Campeonatos

**INPUT:**

```json
{
  "id_atletica": "123e4567-e89b-12d3-a456-426614174000",
  "nome_campeonato": "Jogos Universitários 2026",
  "modalidades": ["Futsal Masculino", "Vôlei Feminino", "Handebol"],
  "id_treinador_responsavel": "555a4567-e89b-12d3-a456-426614174333",
  "atletas_convocados": [
    "987fcdeb-51a2-43d7-9012-426614174000",
    "654abcef-51a2-43d7-9012-426614174111"
  ],
  "transporte": {
    "tipo": "Ônibus Fretado",
    "data_saida": "2026-06-10T08:00:00Z",
    "data_retorno": "2026-06-15T22:00:00Z"
  },
  "datas": {
    "inicio": "2026-06-10",
    "fim": "2026-06-15"
  },
  "locais": [
    "Ginásio Municipal", 
    "Centro de Esportes Universitário"
  ],
  "created_at": "2026-05-22T20:30:00Z"
}

```

**OUTPUT:**

```json
// Status 201 (Created) ou 200 (OK):
{
  "mensagem": "Campeonato adicionado com sucesso!",
  "id_campeonato": "777e4567-e89b-12d3-a456-426614174888"
}

// Status 400 (Bad Request):
{
  "erro": "Dados incompletos. As datas de início e fim são obrigatórias."
}

// Status 500 (Internal Server Error):
{
  "erro": "Erro ao adicionar o campeonato!"
}

```
