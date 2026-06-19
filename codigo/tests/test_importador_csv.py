"""Testes do carregador CSV e do gerador de relatorio Markdown."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tests import contexto  # noqa: F401  (ajuste de sys.path)

from app import Aplicacao
from importador_csv import _lista, carregar_entidades
from relatorio_md import gerar_markdown

ATLETICA = "nome,universidade,campus,cnpj\nAtletica X,UTFPR,Campus,000\n"
ATLETA = (
    "nome,ra,cpf,curso,nascimento,egresso,periodo,conclusao,esportes,comprovante_matricula\n"
    "Joao,2461650,111,ES,2004-01-01,2022-01-01,6,2027-01,Futsal;Volei,\n"
)
TREINADOR = "nome,cpf,modalidade,salario_por_treino,telefone\nCarlos,11122233344,Futsal,120.00,(43) 9\n"
TREINO = (
    "modalidade,treinador_cpf,localidade,dia_semana,horario_inicio,horario_fim,atletas_ra,status_treino\n"
    "Futsal,{cpf},Ginasio,TER,19:00,21:00,2461650,CONFIRMADO\n"
)


def _criar(diretorio: Path, nome: str, conteudo: str) -> None:
    (diretorio / nome).write_text(conteudo, encoding="utf-8")


class TestLista(unittest.TestCase):
    """Cobre importador_csv._lista."""

    def test_sucesso_multiplos_valores(self) -> None:
        self.assertEqual(_lista("Futsal;Volei"), ["Futsal", "Volei"])

    def test_falha_string_vazia_retorna_lista_vazia(self) -> None:
        self.assertEqual(_lista(""), [])

    def test_borda_ignora_espacos_e_separadores_soltos(self) -> None:
        self.assertEqual(_lista(" Futsal ; ; Volei ;"), ["Futsal", "Volei"])


class TestCarregarEntidades(unittest.TestCase):
    """Cobre importador_csv.carregar_entidades."""

    def test_sucesso_carrega_conjunto_completo(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            _criar(base, "atletica.csv", ATLETICA)
            _criar(base, "atleta.csv", ATLETA)
            _criar(base, "treinador.csv", TREINADOR)
            _criar(base, "treino.csv", TREINO.format(cpf="11122233344"))

            app = Aplicacao()
            resultados = carregar_entidades(app, str(base))

            self.assertEqual(len(app.banco.atletas.listar()), 1)
            self.assertEqual(len(app.banco.treinadores.listar()), 1)
            self.assertEqual(len(app.banco.treinos.listar()), 1)
            self.assertTrue(all(r.exit_code == 0 for r in resultados))

    def test_falha_treino_com_treinador_inexistente(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            _criar(base, "atletica.csv", ATLETICA)
            _criar(base, "atleta.csv", ATLETA)
            _criar(base, "treino.csv", TREINO.format(cpf="00000000000"))

            app = Aplicacao()
            resultados = carregar_entidades(app, str(base))

            self.assertEqual(len(app.banco.treinos.listar()), 0)
            self.assertTrue(any(r.status == "CONFLITO_INTEGRIDADE" for r in resultados))

    def test_borda_diretorio_sem_arquivos_opcionais(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            _criar(base, "atletica.csv", ATLETICA)

            app = Aplicacao()
            resultados = carregar_entidades(app, str(base))

            self.assertEqual(len(app.banco.atleticas.listar()), 1)
            self.assertEqual(len(app.banco.atletas.listar()), 0)
            self.assertEqual(len(resultados), 1)


class TestGerarMarkdown(unittest.TestCase):
    """Cobre relatorio_md.gerar_markdown."""

    def test_sucesso_inclui_dados_da_atletica(self) -> None:
        with tempfile.TemporaryDirectory() as pasta:
            base = Path(pasta)
            _criar(base, "atletica.csv", ATLETICA)
            _criar(base, "atleta.csv", ATLETA)
            app = Aplicacao()
            resultados = carregar_entidades(app, str(base))

            markdown = gerar_markdown(app, resultados)
            self.assertIn("# Relatório de Dados da Atlética", markdown)
            self.assertIn("Atletica X", markdown)
            self.assertIn("Joao", markdown)

    def test_borda_sem_dados_indica_ausencia(self) -> None:
        app = Aplicacao()
        markdown = gerar_markdown(app, [])
        self.assertIn("_Nenhuma atlética cadastrada._", markdown)


if __name__ == "__main__":
    unittest.main()
