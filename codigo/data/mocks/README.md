# Dados mockados

Conjunto de dados fictício para demonstrar o sistema, no mesmo formato dos
formulários em `../forms/` (veja `../forms/README.md` para as convenções de CSV).

Conteúdo:

- **atletica.csv** — 1 atlética (Atlética Engenharia, UTFPR).
- **atleta.csv** — 27 atletas: 15 do futsal masculino (RA `23xxxxx`) e 12 do
  vôlei feminino (RA `24xxxxx`).
- **treinador.csv** — 2: Carlos Eduardo Oliveira (Futsal Masculino) e Patrícia
  Mendes Rocha (Vôlei Feminino).
- **membro.csv** — 5 membros da diretoria: Presidência, Eventos, Esportes,
  Marketing e Gestão de Pessoas.
- **treino.csv** — 2 treinos, um por time, vinculando treinador(a) e atletas.
- **atualizacao_treino.csv** — atualizações dos treinos (referenciadas pela
  `modalidade`). Cada alteração efetiva dispara o padrão Observer e gera uma
  **notificação** na seção "Notificações" do relatório.
- **campeonato.csv** — 3 campeonatos: 2 de futsal masculino (Copa Universitária e
  Liga Interatléticas) e 1 de vôlei feminino (Copa Universitária).
- **declaracoes/** — 32 declarações de matrícula mockadas em HTML (uma por atleta
  e por membro), referenciadas pela coluna `comprovante_matricula` como
  `mocks/declaracoes/<RA>.html` (caminho relativo a `codigo/data/`).

## Como executar

A partir da pasta `codigo/`:

```bash
python app.py --dir data/mocks --output data/mocks/relatorio_mock.md
```
