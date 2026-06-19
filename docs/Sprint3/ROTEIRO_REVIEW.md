# Roteiro de Review da Sprint 3

## Comando principal

```bash
python codigo/app.py
```

Esse comando processa os CSVs de `codigo/data/forms/` e gera:

```text
codigo/data/relatorio_atletica.md
```

Para demonstrar com a massa maior de dados mockados:

```bash
python codigo/app.py --dir codigo/data/mocks --output codigo/data/mocks/relatorio_mock.md
```

## O que a demonstracao mostra

1. A aplicacao recebe dados estruturados em CSV.
2. O parser CSV converte as linhas em dicionarios.
3. O parser HTML complementa dados academicos quando o CSV referencia uma
   declaracao valida.
4. A camada de servico processa os dados e aplica regras de negocio.
5. Os repositorios em memoria guardam as entidades durante a execucao.
6. Ao atualizar um treino, o Observer registra uma notificacao sem acoplar essa
   regra diretamente ao cadastro de treino.
7. O sistema agrega os dados em um relatorio Markdown.

## Sequencia esperada no processamento

- `inicializar-atletica`: cria a entidade da atletica.
- `cadastrar-atletas`: cadastra os atletas e mostra metricas de sucesso/falha.
- `cadastrar-membro`: cadastra um membro administrativo.
- `cadastrar-treinador`: cria os treinadores usados nos treinos e campeonatos.
- `criar-treino`: vincula modalidade, treinador, local, horario e atletas.
- `atualizar-treino`: altera campos do treino quando houver CSV de atualizacao.
- `criar-campeonato`: cria campeonato com atletas convocados e transporte.
- `relatorio_md`: gera tabelas, notificacoes e log de processamento.

## Como explicar cada arquivo

- `codigo/app.py`: ponto de entrada da CLI e composicao da aplicacao.
- `codigo/modelos.py`: entidades do dominio, como Atleta, Treino e Campeonato.
- `codigo/servicos.py`: regras de negocio, validacoes e respostas padronizadas.
- `codigo/repositorios.py`: armazenamento em memoria, seguindo o padrao
  Repository.
- `codigo/eventos.py`: Observer usado para reagir a atualizacao de treino.
- `codigo/importador_csv.py`: le CSVs e resolve referencias entre entidades.
- `codigo/importador_html.py`: extrai dados de declaracao de matricula em HTML.
- `codigo/relatorio_md.py`: agrega os dados processados em um arquivo Markdown.

## Perguntas provaveis do professor

**Por que usar repositorio em memoria?**

Porque a entrega prioriza um prototipo simples, testavel e sem dependencia de
infraestrutura externa. O padrao Repository deixa aberta a troca futura por um
banco real.

**Onde estao os padroes de projeto?**

Service Layer em `servicos.py`, Repository em `repositorios.py` e Observer em
`eventos.py`.

**Qual regra de negocio esta implementada?**

Validacao de duplicidade de CPF/RA, validacao de referencias de treinador e
atletas, e validacao temporal de campeonato para impedir data final anterior a
data inicial.

**Qual e a saida final?**

Um relatorio Markdown com resumo das entidades, tabelas de dados, notificacoes e
log de processamento.
