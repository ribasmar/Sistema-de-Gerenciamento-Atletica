# Sprint 3: Desenvolvimento

## Objetivo da Sprint

A Sprint 3 transforma os requisitos e a arquitetura das sprints anteriores em um
prototipo funcional de terminal, sem interface grafica e inteiramente em Python,
como solicitado no enunciado do trabalho.

## Historias cobertas

- Cadastro da atletica.
- Cadastro unico de atletas com documentos e esportes praticados.
- Cadastro de treinador para posterior vinculo aos treinos.
- Criacao e atualizacao de treinos com treinador, local, horario e atletas.
- Criacao de campeonato com modalidades, treinador responsavel, atletas,
  transporte, datas e locais.

## Decisoes tecnicas

- A aplicacao segue o monolito modular definido na Sprint 2.
- A regra de negocio fica em `codigo/servicos.py`.
- O acesso a dados fica em `codigo/repositorios.py`, usando armazenamento em
  memoria para manter o prototipo simples e demonstravel.
- O padrao Observer aparece em `codigo/eventos.py`, disparando notificacoes
  quando um treino e atualizado.
- As saidas seguem o formato JSON estruturado definido na Sprint 1.

## Como demonstrar no terminal

Execute, a partir da raiz do repositorio:

```bash
python codigo/app.py demo
```

Ou usando um arquivo JSON de entrada:

```bash
python codigo/app.py executar-fluxo --input codigo/dados_demo.json
```

Para extrair dados de uma declaracao de matricula em HTML:

```bash
python codigo/app.py importar-declaracao-html --input codigo/declaracao_exemplo.html
```

O comando executa um fluxo completo:

1. inicializa uma atletica;
2. cadastra dois atletas;
3. cadastra um treinador;
4. cria um treino;
5. atualiza o treino e registra notificacao via Observer;
6. cria um campeonato.

## Pontos para explicar na review

- `ResultadoOperacao` padroniza as respostas de sucesso e erro.
- `PessoaService` concentra a validacao de duplicidade de CPF/RA.
- `TreinoService` valida referencias antes de criar treinos.
- `CampeonatoService` valida regra temporal antes de cadastrar campeonato.
- `BarramentoEventos` desacopla a atualizacao do treino da notificacao.
