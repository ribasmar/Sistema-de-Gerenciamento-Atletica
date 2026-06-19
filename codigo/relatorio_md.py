"""Gera um relatorio em Markdown com os dados gerenciados da atletica."""

from __future__ import annotations

from typing import Any, Sequence

from modelos import ResultadoOperacao, agora_iso


def _tabela(cabecalho: Sequence[str], linhas: Sequence[Sequence[Any]]) -> str:
    """Monta uma tabela Markdown; informa quando nao ha registros."""
    if not linhas:
        return "_Nenhum registro._\n"
    partes = [
        "| " + " | ".join(cabecalho) + " |",
        "| " + " | ".join("---" for _ in cabecalho) + " |",
    ]
    partes.extend(
        "| " + " | ".join(str(celula) for celula in linha) + " |" for linha in linhas
    )
    return "\n".join(partes) + "\n"


def gerar_markdown(app: Any, resultados: list[ResultadoOperacao]) -> str:
    """Constroi o relatorio Markdown a partir do estado da aplicacao."""
    banco = app.banco
    atleticas = banco.atleticas.listar()
    atletica = atleticas[0] if atleticas else None
    nome_treinador = {t.id_treinador: t.nome for t in banco.treinadores.listar()}

    blocos: list[str] = ["# Relatório de Dados da Atlética\n"]
    blocos.append(
        "*Documento gerado automaticamente a partir dos formulários CSV em `/data`. "
        f"Emitido em {agora_iso()}.*\n"
    )

    if atletica:
        blocos.append("## Atlética\n")
        blocos.append(
            f"- **Nome:** {atletica.nome}\n"
            f"- **Universidade:** {atletica.universidade}\n"
            f"- **Campus:** {atletica.campus}\n"
            f"- **CNPJ:** {atletica.cnpj}\n"
        )
    else:
        blocos.append("## Atlética\n\n_Nenhuma atlética cadastrada._\n")

    blocos.append("## Resumo Geral\n")
    blocos.append(
        _tabela(
            ["Entidade", "Quantidade"],
            [
                ["Atletas", len(banco.atletas.listar())],
                ["Membros", len(banco.membros.listar())],
                ["Treinadores", len(banco.treinadores.listar())],
                ["Treinos", len(banco.treinos.listar())],
                ["Campeonatos", len(banco.campeonatos.listar())],
            ],
        )
    )

    blocos.append("## Atletas\n")
    blocos.append(
        _tabela(
            ["Nome", "RA", "Curso", "Período", "Esportes"],
            [
                [a.nome, a.ra, a.curso, a.periodo, ", ".join(a.esportes) or "-"]
                for a in banco.atletas.listar()
            ],
        )
    )

    blocos.append("## Membros da Gestão\n")
    blocos.append(
        _tabela(
            ["Nome", "RA", "Cargo", "Curso", "Período"],
            [
                [m.nome, m.ra, m.cargo, m.curso, m.periodo_atual]
                for m in banco.membros.listar()
            ],
        )
    )

    blocos.append("## Treinadores\n")
    blocos.append(
        _tabela(
            ["Nome", "Modalidade", "Salário/treino", "Telefone"],
            [
                [t.nome, t.modalidade, f"R$ {t.salario_por_treino:.2f}", t.telefone]
                for t in banco.treinadores.listar()
            ],
        )
    )

    blocos.append("## Treinos\n")
    blocos.append(
        _tabela(
            ["Modalidade", "Treinador", "Local", "Dia", "Horário", "Atletas", "Status"],
            [
                [
                    tr.modalidade,
                    nome_treinador.get(tr.id_treinador, "-"),
                    tr.localidade,
                    tr.dia_semana,
                    f"{tr.horario_inicio}-{tr.horario_fim}",
                    len(tr.atletas_inscritos),
                    tr.status_treino,
                ]
                for tr in banco.treinos.listar()
            ],
        )
    )

    blocos.append("## Campeonatos\n")
    blocos.append(
        _tabela(
            ["Nome", "Modalidades", "Responsável", "Período", "Locais", "Convocados", "Transporte"],
            [
                [
                    c.nome_campeonato,
                    ", ".join(c.modalidades),
                    nome_treinador.get(c.id_treinador_responsavel, "-"),
                    f"{c.datas.get('inicio', '?')} a {c.datas.get('fim', '?')}",
                    ", ".join(c.locais),
                    len(c.atletas_convocados),
                    c.transporte.get("tipo", "-"),
                ]
                for c in banco.campeonatos.listar()
            ],
        )
    )

    blocos.append("## Notificações\n")
    mensagens = app.notificacoes.mensagens
    if mensagens:
        blocos.append("\n".join(f"- {mensagem}" for mensagem in mensagens) + "\n")
    else:
        blocos.append("_Nenhuma notificação registrada._\n")

    blocos.append("## Log de Processamento\n")
    blocos.append(
        _tabela(
            ["Comando", "Status", "Exit code"],
            [[r.comando, r.status, r.exit_code] for r in resultados],
        )
    )

    ocorrencias: list[str] = []
    for resultado in resultados:
        for erro in resultado.erros or []:
            ocorrencias.append(f"- **{resultado.comando}** (erro): {erro}")
        dados = resultado.dados_gerados or {}
        for rejeitado in dados.get("rejeitados", []):
            ocorrencias.append(f"- **{resultado.comando}** (rejeição): {rejeitado}")
        for alerta in resultado.alertas:
            ocorrencias.append(f"- **{resultado.comando}** (alerta): {alerta}")

    if ocorrencias:
        blocos.append("### Erros, rejeições e alertas\n")
        blocos.append("\n".join(ocorrencias) + "\n")

    return "\n".join(blocos) + "\n"
