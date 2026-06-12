# Roteiro de Review da Sprint 3

## Comando principal

```bash
python codigo/app.py executar-fluxo --input codigo/dados_demo.json
```

## Comando para importar HTML

```bash
python codigo/app.py importar-declaracao-html --input codigo/declaracao_exemplo.html
```

Esse comando simula o envio de uma declaracao de matricula em HTML e extrai
nome, RA, curso, duracao, ingresso e periodo do aluno.

## O que a demonstracao mostra

1. A aplicacao recebe dados estruturados em JSON.
2. A camada de servico processa os dados e aplica regras de negocio.
3. Os repositorios em memoria simulam persistencia das entidades.
4. A saida tambem e estruturada em JSON, com `exit_code`, `status`,
   `comando` e dados gerados.
5. Ao atualizar um treino, o Observer registra uma notificacao sem acoplar essa
   regra diretamente ao cadastro de treino.

## Sequencia esperada no terminal

- `inicializar-atletica`: cria a entidade da atletica.
- `cadastrar-atletas`: cadastra os atletas e mostra metricas de sucesso/falha.
- `cadastrar-membro`: cadastra um membro administrativo.
- `cadastrar-treinador`: cria o treinador usado no treino e campeonato.
- `criar-treino`: vincula modalidade, treinador, local, horario e atletas.
- `atualizar-treino`: altera local e horario do treino.
- `criar-campeonato`: cria campeonato com atletas convocados e transporte.
- `notificacoes`: mostra a mensagem gerada pelo Observer.

## Como explicar cada arquivo

- `codigo/app.py`: ponto de entrada da CLI e orquestracao da demo.
- `codigo/modelos.py`: entidades do dominio, como Atleta, Treino e Campeonato.
- `codigo/servicos.py`: regras de negocio, validacoes e respostas padronizadas.
- `codigo/repositorios.py`: armazenamento em memoria, seguindo o padrao
  Repository.
- `codigo/eventos.py`: Observer usado para reagir a atualizacao de treino.
- `codigo/dados_demo.json`: entrada estruturada usada na demonstracao.
- `codigo/importador_html.py`: extrai dados de declaracao de matricula em HTML.

## Perguntas provaveis do professor

**Por que usar repositorio em memoria?**

Porque a Sprint 3 exige demonstracao funcional no terminal. O repositorio em
memoria permite validar as regras e o fluxo sem adicionar banco de dados antes
da etapa de testes/refatoracao.

**Onde estao os padroes de projeto?**

Service Layer em `servicos.py`, Repository em `repositorios.py` e Observer em
`eventos.py`.

**Qual regra de negocio esta implementada?**

Validacao de duplicidade de CPF/RA, validacao de referencias de treinador e
atletas, e validacao temporal de campeonato para impedir data final anterior a
data inicial.

**O que falta para a Sprint 4?**

Criar testes automatizados com `unittest`, cobrindo sucesso, falha e caso de
borda para pelo menos dois metodos relevantes.
