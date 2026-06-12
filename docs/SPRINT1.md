
# Documentação do Sistema de Gestão de Atléticas

## 1. Roteiro e síntese da elicitação realizada (entrevistas, questionários ou análise de similares)

**Questionários:**
#### Entrevistado: Ex-Presidente da Atletica XII de Março, da UTFPR - Campus Apucarana
- Como é feito hoje o sistema de cadastro de estudante para campeonatos?

    R: É enviado a declaração de matrícula através do Whatsapp e formulário. 
- Como o atleta faz a inscrição para campeonatos hoje?

    R:  Compra o pacote dos jogos e envia a declaração de matrícula.
- Onde estão armazenadas as informações dos atletas?

    R:  Em drive de esportes. 
- Onde é feita a coleta de atletas disponíveis para os campeonatos?

    R:  Eles comparecem ao treino e o treinador os convoca via Whatsapp 
- Como é feita a gerência de treinadores e treinos hoje?

    R: Tudo informalmente através do Whatsapp


#### Entrevistado:  Ex-Presidente da VII de Abril, UNIFIL - Campus Londrina 
- Como é feito hoje o sistema de cadastro de estudante para campeonatos?

   R: Hoje, a VII de Abril participa apenas de jogos universitários, mas ja chegou a participar de jogos abertos, como o de Cambé, é feita uma lista com nome, curso e numero de matricula dos atletas, se é formado ou estuda a distância, dependendo da necessidade, constamos na lista, as informações são conferidas por declaração de matricula emitida pelo proprio aluno, ou diploma.

- Como o atleta faz a inscrição para campeonatos hoje?

   R: Os diretores responsáveis pela área esportiva junto dos presidentes fazem a coleta de dados e preenchem a lista pra ser mandada para o responsável pelo campeonato.

- Onde estão armazenadas as informações dos atletas?

   R: Nas próprias declarações de matricula ou diploma.

- Onde é feita a coleta de atletas disponíveis para os campeonatos?

   R: Na própria faculdade, ou em treinos que disponibilizamos para os interessados, conforme a quantidade, é feita uma seletiva, e o técnico escolhe os jogadores titulares e reservas.

- Como é feita a gerência de treinadores e treinos hoje?

   R: A diretoria de esportes é dividida em modalidades, e cada diretor organiza os treinos pré planejados no inicio do ano, conforme a divisão de dias de posse de quadras, entre nós e a outra atletica pertencente a faculdade. Os treinos funcionam em forma de “racha”, é dividido o valor do tecnico por treino, entre os atletas presentes naquele dia, através de listas passadas em grupos segmentados no WhatsApp, o pagamento é feito  pelo financeiro todo dia 10 de cada mês, ou conforme a necessidade e solicitação do tecnico.

#### Entrevistado: Ex-Vice Presidente da Exatas UEL - Campus Londrina
- Como é feito hoje o sistema de cadastro de estudante para campeonatos?

   R: Lista de alunos do centro representado pela atlética emitida pela universidade e comprovante de matrícula (pedimos individual pra cada atleta)
- Como o atleta faz a inscrição para campeonatos hoje?
  
   R: Só vai com o RG em mãos e fazemos o resto

- Onde estão armazenadas as informações dos atletas?

   R: Arquivos físicos que são queimados depois de usados (no caso os do jia do ano passado estao cmg e não queimei ainda kkkkkk)

- Onde é feita a coleta de atletas disponíveis para os campeonatos?

   R: ⁠Passamos nas salas de primeiro ano pessoalmente  
- Como é feita a gerência de treinadores e treinos hoje?

   R: 1 assessor de esportes responsável por cada modalidade, o diretor acompanha e auxilia as modalidades que precisam, os custos de treinador e quadra são rachados entre os atletas da modalidade
---

## 2. Histórias de usuário finalizadas com critérios de aceitação e priorização

* **[ALTA]** Eu, como membro da Atlética, preciso cadastrar atletas repetidamente. Preciso de seus dados pessoais, documentos de matrícula 
             e esportes práticados recorrentemente. Por isso, preciso de um meio para automatizar esse processo ou torna-lo mais ágil.
####            **Como:**
  
                --- Um sistema de cadastro único, onde eu cadastro o atleta (com os dados citados acima) e apenas atualizo seu status em campeonatos (participa/Não participa), 
                --- modalidades (selecionada modalidades atuais e apenas vincula os dados do atleta).
                
* **[ALTA]** Eu, como membro da Atlética, preciso gerenciar treinos. Preciso verificar número de alunos por modalidade, 
             escalar treinadores para respectivos treinos e gerenciar espaços para os treinos. Por isso, preciso de um gerenciador de treinos, 
             para permitir que esse processo seja mais prático, e ágil.
####            **Como:**

                --- Um programa onde eu possa gerenciar uma modalidade e nela vincular o treinador a partir de um cadastro anterior, junto aos atletas que selecionaram a modalidade no momento de cadastro.
                --- A partir do vinculo completo, poder colocar no cronogramar o horário do treino e selecionar o local pré-cadastrado para treino.
                
* **[ALTA]** Eu, como membro da Atlética, preciso gerenciar atletas para competições.

              --- AMBÍGUA - A primeira já resolve esse problema.
  
* **[ALTA]** Eu, como membro da Atlética, preciso gerenciar a escala de treinadores. Preciso recorrentemente contatar treinadores para algumas modalidades. 
             Por isso, preciso de um catálogo de treinadores cadastrados por mim, onde a partir do momento que forem acionados eu possa vincula-los aos treinos.
####            **Como:**

                --- Cadastrar um treinador com informações pessoais, modalidade, salário.
                
* **[MÉDIA]** Eu, como atleta, não quero ter que enviar documentos repetidamente. Preciso recorrentemente enviar meus documentos pessoais ao participar de competições. Por isso, preciso
              de um meio mais prático de menos repetivo e cansativo.
####              **Como:**

                --- Enviar apenas meus dados de mátricula. Ao ínves de forms longos.
              
* **[BAIXA]** Eu, como atleta, gostaria de um hub de informações sobre as atividades da atlética.

  Possível implementação a ser feita, sem descrição.

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

## 4. Inputs e Outputs esperados.

Estruturas em formato `.json` para os métodos principais.


### 4.1. Criar Atlética

**INPUT:**
```json
{
  "nome": "Atlética Engenharia",
  "universidade": "Universidade Exemplo",
  "campus": "Campus Central",
  "cnpj": "00000000000100",
  "timestamp_ingestao": "2026-05-22T19:52:25Z"
}

```

**OUTPUT:**

```json
// Cenário 1: Sucesso Total (Exit Code: 0)
{
  "exit_code": 0,
  "status": "SUCESSO",
  "timestamp_execucao": "2026-05-26T17:10:00Z",
  "comando": "inicializar-atletica",
  "dados_gerados": {
    "mensagem": "Entidade Atlética inicializada com sucesso no pipeline.",
    "id_atletica": "123e4567-e89b-12d3-a456-426614174000"
  },
  "alertas": []
}

// Cenário 2: Erro de Validação de Campos (Exit Code: 1)
{
  "exit_code": 1,
  "status": "ERRO_VALIDACAO",
  "timestamp_execucao": "2026-05-26T17:10:05Z",
  "comando": "inicializar-atletica",
  "erros": [
    {
      "campo": "nome",
      "motivo": "O campo 'nome' é obrigatório e não foi fornecido no ficheiro de entrada."
    }
  ]
}

```

### 4.2. Cadastro de Atleta

**INPUT:**

```json
{
  "id_atletica": "123e4567-e89b-12d3-a456-426614174000",
  "atletas": [
    {
      "nome": "Fulano de Tal",
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
          "path": "codigo/data/Declaração Matrícula.html"
        }
      ]
    }
  ]
}

```

**OUTPUT:**

```json
// Cenário 1: Processamento Concluído (Mesmo com falhas parciais, o pipeline corre até ao fim. Exit Code: 0 se tudo passar, 2 se houver rejeições de negócio)
{
  "exit_code": 2,
  "status": "PROCESSADO_COM_REJEICOES",
  "timestamp_execucao": "2026-05-26T17:12:00Z",
  "metricas": {
    "total_registros_lidos": 2,
    "total_sucesso": 1,
    "total_falhas": 1
  },
  "importados": [
    {
      "ra": "a1234567",
      "id_atleta_gerado": "987fcdeb-51a2-43d7-9012-426614174000",
      "status": "REGISTADO"
    }
  ],
  "rejeitados": [
    {
      "ra": "a7654321",
      "motivo_rejeicao": "CONFLITO_INTEGRIDADE",
      "detalhe": "Atleta com o RA ou CPF informado já se encontra registado no sistema local."
    }
  ]
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
  ]
}

```

**OUTPUT:**

```json
// Cenário 1: Sucesso (Exit Code: 0)
{
  "exit_code": 0,
  "status": "SUCESSO",
  "timestamp_execucao": "2026-05-26T17:15:00Z",
  "dados_gerados": {
    "mensagem": "Agenda de treino estruturada e vinculada com sucesso.",
    "id_treino": "333c4567-e89b-12d3-a456-426614174999"
  }
}

// Cenário 2: Quebra de Chave Estrangeira / ID Não Encontrado (Exit Code: 2)
{
  "exit_code": 2,
  "status": "CONFLITO_INTEGRIDADE",
  "timestamp_execucao": "2026-05-26T17:15:30Z",
  "erros": [
    {
      "entidade": "Treinador",
      "id_referenciado": "555a4567-e89b-12d3-a456-426614174333",
      "motivo": "O identificador do treinador não foi localizado na base de dados local. Operação abortada."
    }
  ]
}
```

### 4.4. Criar Membro da Atlética

**INPUT:**

```json
{
  "id_atletica": "123e4567-e89b-12d3-a456-426614174000",
  "nome": "Ciclano de Oliveira",
  "ra": "a8765432",
  "cpf": "98765432100",
  "documento_pessoal": "codigo/data/documento_pessoal_exemplo.txt",
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
      "path": "codigo/data/Declaração Matrícula-Pedro.html"
    }
  ]
}

```

**OUTPUT:**

```json
// Cenário 1: Sucesso (Exit Code: 0)
{
  "exit_code": 0,
  "status": "SUCESSO",
  "timestamp_execucao": "2026-05-26T17:18:00Z",
  "dados_gerados": {
    "mensagem": "Membro da gestão da Atlética registado com sucesso.",
    "id_membro": "444d4567-e89b-12d3-a456-426614174555"
  }
}

// Cenário 2: Duplicidade detetada (Exit Code: 2)
{
  "exit_code": 2,
  "status": "CONFLITO_INTEGRIDADE",
  "timestamp_execucao": "2026-05-26T17:18:45Z",
  "erros": [
    {
      "chave": "CPF_RA_DUPLICADO",
      "detalhe": "Já existe um membro ou atleta registado com o CPF 98765432100 ou RA a8765432."
    }
  ]
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
  "status_treino": "CONFIRMADO"
}

```

**OUTPUT:**

```json
// Cenário 1: Modificação bem-sucedida (Exit Code: 0)
{
  "exit_code": 0,
  "status": "SUCESSO",
  "timestamp_execucao": "2026-05-26T17:22:00Z",
  "modificacoes_aplicadas": {
    "id_treino": "333c4567-e89b-12d3-a456-426614174999",
    "campos_alterados": ["localidade", "horario_inicio", "horario_fim", "atletas_inscritos"]
  }
}

// Cenário 2: Treino Inexistente no dataset (Exit Code: 2)
{
  "exit_code": 2,
  "status": "REGISTO_NAO_ENCONTRADO",
  "timestamp_execucao": "2026-05-26T17:22:15Z",
  "erros": [
    {
      "identificador": "id_treino",
      "valor_procurado": "333c4567-e89b-12d3-a456-426614174999",
      "motivo": "O identificador do treino fornecido não corresponde a nenhum registo ativo para modificação."
    }
  ]
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
  ]
}

```

**OUTPUT:**

```json
// Cenário 1: Sucesso na Consolidação (Exit Code: 0)
{
  "exit_code": 0,
  "status": "SUCESSO",
  "timestamp_execucao": "2026-05-26T17:25:00Z",
  "dados_gerados": {
    "mensagem": "Campeonato processado e atletas vinculados à escala de transporte com sucesso.",
    "id_campeonato": "777e4567-e89b-12d3-a456-426614174888"
  }
}

// Cenário 2: Erro de Validação de Regra de Negócio Temporal (Exit Code: 1)
{
  "exit_code": 1,
  "status": "ERRO_VALIDACAO_LOGICA",
  "timestamp_execucao": "2026-05-26T17:25:30Z",
  "erros": [
    {
      "contexto": "datas",
      "motivo": "A data de fim do campeonato não pode ser anterior à data de início."
    }
  ]
}
```
