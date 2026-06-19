"""Interface de linha de comando do Sistema de Gerenciamento de Atletica.

Estabelece um unico fluxo: le os CSVs das entidades (respostas de formulario) e
gera um relatorio Markdown com os dados gerenciados da atletica.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from eventos import BarramentoEventos, CaixaNotificacoes
from importador_csv import carregar_entidades
from relatorio_md import gerar_markdown
from repositorios import BancoMemoria
from servicos import AtleticaService, CampeonatoService, PessoaService, TreinoService


class Aplicacao:
    """Compoe repositorios, servicos e observadores."""

    def __init__(self) -> None:
        self.banco = BancoMemoria()
        self.eventos = BarramentoEventos()
        self.notificacoes = CaixaNotificacoes()
        self.eventos.inscrever(
            "treino_atualizado", self.notificacoes.registrar_alteracao_treino
        )

        self.atleticas = AtleticaService(self.banco)
        self.pessoas = PessoaService(self.banco)
        self.treinos = TreinoService(self.banco, self.eventos)
        self.campeonatos = CampeonatoService(self.banco)


def processar_csv(diretorio: str, saida: str) -> None:
    """Le os CSVs do diretorio informado e grava o relatorio Markdown."""
    app = Aplicacao()
    resultados = carregar_entidades(app, diretorio)
    Path(saida).write_text(gerar_markdown(app, resultados), encoding="utf-8")
    print(f"[OK] Relatorio Markdown gerado em: {saida}")


def main() -> None:
    """Ponto de entrada da CLI: unico fluxo CSV -> Markdown."""
    pasta_dados = Path(__file__).with_name("data")
    parser = argparse.ArgumentParser(
        description="Sistema de Gerenciamento de Atletica - entrada CSV, saida Markdown"
    )
    parser.add_argument(
        "--dir",
        default=str(pasta_dados / "forms"),
        help="Pasta com os CSVs das entidades",
    )
    parser.add_argument(
        "--output",
        default=str(pasta_dados / "relatorio_atletica.md"),
        help="Arquivo Markdown de saida",
    )

    args = parser.parse_args()
    processar_csv(args.dir, args.output)


if __name__ == "__main__":
    main()
