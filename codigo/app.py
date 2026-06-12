"""Interface de terminal do Sistema de Gerenciamento de Atletica."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from eventos import BarramentoEventos, CaixaNotificacoes
from importador_html import importar_declaracao_html
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


def imprimir(resultado: dict[str, Any]) -> None:
    """Imprime dados em JSON formatado."""
    print(json.dumps(resultado, ensure_ascii=False, indent=2, default=str))


def carregar_json(caminho: str) -> dict[str, Any]:
    """Carrega um arquivo JSON."""
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def executar_fluxo(dados: dict[str, Any]) -> None:
    """Executa um fluxo completo a partir de dados estruturados."""
    app = Aplicacao()

    resultado_atletica = app.atleticas.inicializar(dados["atletica"])
    imprimir(resultado_atletica.para_dict())
    id_atletica = resultado_atletica.dados_gerados["id_atletica"]  # type: ignore[index]

    dados_atletas = {"id_atletica": id_atletica, "atletas": dados["atletas"]}
    resultado_atletas = app.pessoas.cadastrar_atletas(dados_atletas)
    imprimir(resultado_atletas.para_dict())

    atletas_por_ra = {
        item["ra"]: item["id_atleta_gerado"]
        for item in resultado_atletas.dados_gerados["importados"]  # type: ignore[index]
    }

    if "membro" in dados:
        membro = {"id_atletica": id_atletica, **dados["membro"]}
        imprimir(app.pessoas.cadastrar_membro(membro).para_dict())

    treinador = {"id_atletica": id_atletica, **dados["treinador"]}
    resultado_treinador = app.pessoas.cadastrar_treinador(treinador)
    imprimir(resultado_treinador.para_dict())
    id_treinador = resultado_treinador.dados_gerados["id_treinador"]  # type: ignore[index]

    treino = {
        chave: valor
        for chave, valor in dados["treino"].items()
        if chave != "atletas_por_ra"
    }
    treino["id_atletica"] = id_atletica
    treino["id_treinador"] = id_treinador
    treino["atletas_inscritos"] = [
        atletas_por_ra[ra] for ra in dados["treino"]["atletas_por_ra"]
    ]
    resultado_treino = app.treinos.criar(treino)
    imprimir(resultado_treino.para_dict())
    id_treino = resultado_treino.dados_gerados["id_treino"]  # type: ignore[index]

    atualizacao = {
        chave: valor
        for chave, valor in dados["atualizacao_treino"].items()
        if chave != "atletas_por_ra"
    }
    atualizacao["id_treino"] = id_treino
    atualizacao["atletas_inscritos"] = [
        atletas_por_ra[ra] for ra in dados["atualizacao_treino"]["atletas_por_ra"]
    ]
    imprimir(app.treinos.atualizar(atualizacao).para_dict())

    campeonato = {
        chave: valor
        for chave, valor in dados["campeonato"].items()
        if chave != "atletas_por_ra"
    }
    campeonato["id_atletica"] = id_atletica
    campeonato["id_treinador_responsavel"] = id_treinador
    campeonato["atletas_convocados"] = [
        atletas_por_ra[ra] for ra in dados["campeonato"]["atletas_por_ra"]
    ]
    imprimir(app.campeonatos.criar(campeonato).para_dict())
    imprimir({"notificacoes": app.notificacoes.mensagens})


def executar_demo() -> None:
    """Executa uma demonstracao completa no terminal."""
    executar_fluxo(
        {
            "atletica": {
                "nome": "Atletica Engenharia",
                "universidade": "Universidade Exemplo",
                "campus": "Campus Central",
                "cnpj": "00000000000100",
            },
            "atletas": [
                {
                    "nome": "Fulano de Tal",
                    "ra": "a1234567",
                    "cpf": "12345678901",
                    "curso": "Engenharia Civil",
                    "nascimento": "2004-07-07",
                    "egresso": "2022-03-17",
                    "periodo": 8,
                    "conclusao": "2027-01",
                    "esportes": ["Futsal Masculino"],
                    "documentos": [
                        {
                            "tipo": "comprovante_matricula",
                            "url": "https://storage.exemplo.com/docs/matricula.pdf",
                        }
                    ],
                },
                {
                    "nome": "Beltrana Souza",
                    "ra": "a7654321",
                    "cpf": "98765432109",
                    "curso": "Engenharia de Software",
                    "nascimento": "2003-10-02",
                    "egresso": "2021-03-10",
                    "periodo": 9,
                    "conclusao": "2026-12",
                    "esportes": ["Futsal Masculino"],
                    "documentos": [
                        {
                            "tipo": "comprovante_matricula",
                            "url": "https://storage.exemplo.com/docs/matricula2.pdf",
                        }
                    ],
                },
            ],
            "membro": {
                "nome": "Ciclano de Oliveira",
                "ra": "a8765432",
                "cpf": "98765432100",
                "documento_pessoal": "https://storage.exemplo.com/docs/rg.pdf",
                "curso": "Engenharia de Software",
                "cargo": "Diretor de Esportes",
                "tempo_atletica_inicio": "2024-02-15",
                "tempo_atletica_fim_esperado": "2026-12-20",
                "data_nascimento": "2003-05-12",
                "inicio_egresso": "2022-02-10",
                "periodo_atual": 5,
                "tempo_esperado_conclusao": "2026-12",
                "documentos_universidade": [
                    {
                        "tipo": "comprovante_matricula",
                        "url": "https://storage.exemplo.com/docs/matricula_membro.pdf",
                    }
                ],
            },
            "treinador": {
                "nome": "Carlos Oliveira",
                "cpf": "11122233344",
                "modalidade": "Futsal Masculino",
                "salario_por_treino": 120.0,
                "telefone": "(43) 99999-0000",
            },
            "treino": {
                "modalidade": "Futsal Masculino",
                "localidade": "Ginasio Principal",
                "dia_semana": "TERCA_FEIRA",
                "horario_inicio": "19:00",
                "horario_fim": "21:00",
                "atletas_por_ra": ["a1234567", "a7654321"],
            },
            "atualizacao_treino": {
                "localidade": "Quadra Externa B",
                "horario_inicio": "19:30",
                "horario_fim": "21:30",
                "status_treino": "CONFIRMADO",
                "atletas_por_ra": ["a1234567", "a7654321"],
            },
            "campeonato": {
                "nome_campeonato": "Jogos Universitarios 2026",
                "modalidades": ["Futsal Masculino"],
                "atletas_por_ra": ["a1234567", "a7654321"],
                "transporte": {
                    "tipo": "Onibus Fretado",
                    "data_saida": "2026-06-10T08:00:00Z",
                    "data_retorno": "2026-06-15T22:00:00Z",
                },
                "datas": {"inicio": "2026-06-10", "fim": "2026-06-15"},
                "locais": ["Ginasio Municipal"],
            },
        }
    )


def main() -> None:
    """Ponto de entrada da CLI."""
    parser = argparse.ArgumentParser(
        description="Sistema de Gerenciamento de Atletica - Sprint 3"
    )
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("demo", help="Executa uma demonstracao completa")

    fluxo = sub.add_parser("executar-fluxo", help="Executa fluxo por JSON")
    fluxo.add_argument("--input", required=True, help="Arquivo JSON de entrada")

    html = sub.add_parser(
        "importar-declaracao-html", help="Extrai dados de aluno de um HTML"
    )
    html.add_argument("--input", required=True, help="Arquivo HTML de entrada")
    html.add_argument(
        "--encoding",
        default="auto",
        help="Encoding do arquivo HTML; use auto para detectar pelo charset",
    )

    cadastrar = sub.add_parser("inicializar-atletica")
    cadastrar.add_argument("--input", required=True, help="Arquivo JSON de entrada")

    args = parser.parse_args()
    app = Aplicacao()

    if args.comando == "demo":
        executar_demo()
    elif args.comando == "executar-fluxo":
        executar_fluxo(carregar_json(args.input))
    elif args.comando == "importar-declaracao-html":
        imprimir(
            {
                "exit_code": 0,
                "status": "SUCESSO",
                "comando": "importar-declaracao-html",
                "dados_extraidos": importar_declaracao_html(args.input, args.encoding),
            }
        )
    elif args.comando == "inicializar-atletica":
        imprimir(app.atleticas.inicializar(carregar_json(args.input)).para_dict())


if __name__ == "__main__":
    main()
