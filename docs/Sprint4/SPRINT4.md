# Sprint 4: Testes e Refatoração

## Objetivo da Sprint

Escrever testes automatizados, refatorar e finalizar o repositório, atendendo aos
requisitos mínimos de entrega do trabalho.

## Refatorações realizadas

- **Fluxo único CSV → Markdown.** A entrada passou a ser exclusivamente por
  arquivos CSV (um por entidade) e a saída um relatório Markdown. Foram removidos
  a ingestão por JSON, o menu interativo e toda a saída em JSON do `app.py`.
- **Leitura segura da declaração HTML.** O HTML é referenciado pelo CSV e lido de
  forma contida (sem caminho absoluto e sem *path traversal*), com falha segura e
  registro de alerta no relatório. O CSV é a fonte autoritativa.
- **Novos módulos:** `importador_csv.py` (carregamento e resolução de referências
  por chave natural) e `relatorio_md.py` (geração do relatório).
- **Notificações via Observer:** atualização de treino (`atualizacao_treino.csv`)
  dispara o evento `treino_atualizado`, refletido na seção de notificações.

## Testes automatizados

Suíte com `unittest` em `codigo/tests/`, com 29 casos cobrindo sucesso, falha e
borda (mínimo exigido: 2 métodos com 3 casos). Detalhes, tabela de cobertura e
lacunas em [`docs/testes.md`](../testes.md).

Execução, a partir de `codigo/`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Como demonstrar

A partir de `codigo/`:

```bash
python app.py                                                  # usa data/forms
python app.py --dir data/mocks --output data/mocks/relatorio_mock.md
```

## Estrutura final da entrega

```
README.md
docs/requisitos.md      docs/arquitetura.md      docs/testes.md
codigo/*.py             codigo/tests/*.py
codigo/data/forms/      codigo/data/mocks/
```
