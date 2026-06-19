# Formulários CSV de entrada

Cada arquivo `.csv` desta pasta representa as respostas de um formulário para uma
entidade do sistema. O comando `processar-csv` lê todos eles e gera um relatório
Markdown com os dados gerenciados da atlética.

## Convenções

- **Delimitador de campo:** vírgula (`,`).
- **Listas dentro de uma célula:** separadas por ponto e vírgula (`;`).
  Ex.: `Futsal Masculino;Volei`.
- **Datas:** formato `AAAA-MM-DD`. Datas/horas: ISO `AAAA-MM-DDTHH:MM:SSZ`.
- **Decimais:** use ponto (`.`), não vírgula. Ex.: `120.00`.
- **Codificação:** UTF-8.
- Arquivos opcionais ausentes são simplesmente ignorados.

## Declaração de matrícula em HTML

O HTML é enviado **à parte** (arquivo separado), e o CSV apenas o referencia pela
coluna `comprovante_matricula`. Embutir o conteúdo HTML dentro de uma célula CSV
**não** é suportado, por ser inseguro (quebra de parsing, células enormes e risco
de injeção de fórmula/CSV).

Regras de segurança ao ler o HTML:

- O arquivo deve estar **dentro da pasta `codigo/data/`** (pasta-pai de `forms/`).
- Caminhos **absolutos** e com `..` (path traversal) são rejeitados.
- Se o arquivo não existir ou não puder ser lido, o cadastro continua usando os
  dados do próprio CSV e um alerta é registrado no relatório.
- O CSV é a fonte autoritativa: o HTML só preenche `nome`, `ra`, `curso` e o
  período **quando esses campos estão em branco** no CSV.

Exemplo de valor válido: `Declaração Matrícula.html` (relativo a `codigo/data/`).

## Referências entre entidades

Como os identificadores internos são gerados em tempo de execução, os CSVs se
referenciam por chaves naturais:

- `treino.csv` e `campeonato.csv` apontam para o treinador pela coluna
  `treinador_cpf`.
- `treino.csv` e `campeonato.csv` apontam para atletas pela coluna `atletas_ra`
  (lista de RAs separada por `;`).

## Colunas por arquivo

- **atletica.csv:** `nome, universidade, campus, cnpj`
- **atleta.csv:** `nome, ra, cpf, curso, nascimento, egresso, periodo, conclusao, esportes, comprovante_matricula`
- **membro.csv:** `nome, ra, cpf, documento_pessoal, curso, cargo, tempo_atletica_inicio, tempo_atletica_fim_esperado, data_nascimento, inicio_egresso, periodo_atual, tempo_esperado_conclusao, comprovante_matricula`
- **treinador.csv:** `nome, cpf, modalidade, salario_por_treino, telefone`
- **treino.csv:** `modalidade, treinador_cpf, localidade, dia_semana, horario_inicio, horario_fim, atletas_ra, status_treino`
- **campeonato.csv:** `nome_campeonato, modalidades, treinador_cpf, atletas_ra, transporte_tipo, transporte_data_saida, transporte_data_retorno, data_inicio, data_fim, locais`

## Execução

A partir da pasta `codigo/`:

```bash
python app.py processar-csv
```

Saída padrão: `codigo/data/relatorio_atletica.md`. Use `--dir` e `--output` para
personalizar a pasta de entrada e o arquivo de saída.
