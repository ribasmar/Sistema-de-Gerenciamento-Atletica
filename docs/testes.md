# Estratégia de Testes

## Como executar

A partir da pasta `codigo/`:

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

## Estratégia adotada

Adotamos **testes de unidade automatizados com `unittest`**, focados nas camadas
que concentram as regras de negócio e o processamento de dados: a **camada de
serviço** (`servicos.py`), o **importador de declarações HTML** (`importador_html.py`)
e o **carregador CSV + gerador de relatório** (`importador_csv.py`, `relatorio_md.py`).

Cada método/função coberto exercita a tríade **sucesso, falha e borda**. Os
serviços e o carregador são testados contra o repositório em memória real
(`BancoMemoria`), sem mocks, pois ele é determinístico e isolado por teste
(`setUp`/`TemporaryDirectory` a cada caso), o que mantém os testes rápidos e fiéis
ao comportamento de produção. As funções do importador HTML são puras e testadas
por entrada/saída.

São **29 casos** distribuídos em três arquivos (`tests/test_servicos.py`,
`tests/test_importador_html.py`, `tests/test_importador_csv.py`), acima do mínimo
de 2 métodos com 3 casos:

| Alvo | Sucesso | Falha | Borda |
|------|---------|-------|-------|
| `AtleticaService.inicializar` | cadastro válido | campo obrigatório ausente | campo presente porém vazio |
| `PessoaService.cadastrar_atletas` | novo atleta | CPF/RA duplicado | lista vazia |
| `CampeonatoService.criar` | campeonato criado | treinador inexistente | data fim igual à data início |
| `TreinoService.atualizar` | altera campo e publica evento | treino inexistente | alteração sem mudança real não publica evento |
| `extrair_ra` | RA com rótulo | texto sem número | número solto de 5 dígitos |
| `extrair_texto_html` | texto visível | ignora `<script>` | HTML vazio |
| `limpar_valor` | normaliza espaços | remove pontuação de borda | só espaços |
| `importador_csv._lista` | múltiplos valores | string vazia | espaços/separadores soltos |
| `importador_csv.carregar_entidades` | conjunto completo carregado | treino com treinador inexistente | diretório sem CSVs opcionais |
| `relatorio_md.gerar_markdown` | inclui dados da atlética | — | sem dados indica ausência |

## Adequação

Os testes cobrem as validações críticas de integridade (duplicidade de CPF/RA,
referências a treinador/atleta inexistentes), a validação lógica de datas, o
padrão Observer (publicação de `treino_atualizado` só quando há alteração real) e
o pipeline de ponta a ponta CSV → relatório. A leitura segura do HTML
(`_resolver_html_seguro`) é exercitada de forma direta na verificação manual,
rejeitando caminho absoluto, *path traversal* e arquivos inexistentes.

## Lacunas não cobertas

- `cadastrar_membro` é exercitado pelo carregador, mas não tem caso unitário
  dedicado.
- A leitura de arquivo do importador HTML (`ler_html`, `normalizar_caminho`,
  detecção de encoding) depende de I/O e não é coberta por teste automatizado.
- `app.py` (CLI) e o timestamp não determinístico de `ResultadoOperacao`
  não têm testes.
- Não há medição formal de cobertura (ex.: `coverage.py`); a verificação é por
  exercício direto dos métodos.
