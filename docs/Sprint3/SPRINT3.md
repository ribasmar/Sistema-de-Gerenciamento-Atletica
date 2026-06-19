# Sprint 3: Desenvolvimento

## Objetivo da Sprint

A Sprint 3 transforma os requisitos e a arquitetura das sprints anteriores em um
prototipo funcional de terminal, sem interface grafica e inteiramente em Python,
como solicitado no enunciado do trabalho.

O fluxo final da aplicacao recebe arquivos CSV como entrada, aplica regras de
negocio e gera um relatorio Markdown estruturado.

## Historias cobertas

- Cadastro da atletica.
- Cadastro unico de atletas com documentos e esportes praticados.
- Cadastro de membro da atletica.
- Cadastro de treinador para posterior vinculo aos treinos.
- Criacao e atualizacao de treinos com treinador, local, horario e atletas.
- Criacao de campeonato com modalidades, treinador responsavel, atletas,
  transporte, datas e locais.

## Decisoes tecnicas

- A aplicacao segue o monolito modular definido na Sprint 2.
- A regra de negocio fica em `codigo/servicos.py`.
- O acesso a dados fica em `codigo/repositorios.py`, usando armazenamento em
  memoria para manter o prototipo simples e testavel.
- O padrao Observer aparece em `codigo/eventos.py`, disparando notificacoes
  quando um treino e atualizado.
- A entrada principal e composta por CSVs em `codigo/data/forms/`.
- A saida final e um relatorio Markdown gerado por `codigo/relatorio_md.py`.

## Como demonstrar no terminal

Execute, a partir da raiz do repositorio:

```bash
python codigo/app.py
```

Saida padrao:

```text
codigo/data/relatorio_atletica.md
```

Para demonstrar com os dados mockados:

```bash
python codigo/app.py --dir codigo/data/mocks --output codigo/data/mocks/relatorio_mock.md
```

## O que o comando executa

1. Le os CSVs da pasta informada.
2. Inicializa a atletica.
3. Cadastra atletas, membros e treinadores.
4. Cria treinos e campeonatos.
5. Aplica validacoes de integridade e datas.
6. Registra notificacoes quando treinos sao atualizados.
7. Gera um relatorio Markdown com resumo, tabelas e log de processamento.

## Pontos para explicar na review

- `ResultadoOperacao` padroniza as respostas de sucesso e erro.
- `PessoaService` concentra a validacao de duplicidade de CPF/RA.
- `TreinoService` valida referencias antes de criar treinos.
- `CampeonatoService` valida regra temporal antes de cadastrar campeonato.
- `BarramentoEventos` desacopla a atualizacao do treino da notificacao.
- `relatorio_md.py` agrega os dados processados em uma saida Markdown.
