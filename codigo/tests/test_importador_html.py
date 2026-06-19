"""Testes das funcoes puras de extracao do importador de declaracoes HTML."""

from __future__ import annotations

import unittest

from tests import contexto  # noqa: F401  (ajuste de sys.path)

from importador_html import extrair_ra, extrair_texto_html, limpar_valor


class TestExtrairRa(unittest.TestCase):
    """Cobre importador_html.extrair_ra."""

    def test_sucesso_extrai_ra_com_rotulo(self) -> None:
        self.assertEqual(extrair_ra("RA: a1234567 do aluno"), "a1234567")

    def test_falha_sem_numero_retorna_vazio(self) -> None:
        self.assertEqual(extrair_ra("Declaracao sem identificador numerico"), "")

    def test_borda_numero_solto_de_cinco_digitos(self) -> None:
        self.assertEqual(extrair_ra("Matricula 12345 confirmada"), "12345")


class TestExtrairTextoHtml(unittest.TestCase):
    """Cobre importador_html.extrair_texto_html."""

    def test_sucesso_extrai_texto_visivel(self) -> None:
        html = "<html><body><p>Nome do Aluno: Maria</p></body></html>"
        self.assertEqual(extrair_texto_html(html), "Nome do Aluno: Maria")

    def test_falha_ignora_conteudo_de_script(self) -> None:
        html = "<body><script>var x = 1;</script><p>Curso: ES</p></body>"
        self.assertEqual(extrair_texto_html(html), "Curso: ES")

    def test_borda_html_vazio(self) -> None:
        self.assertEqual(extrair_texto_html(""), "")


class TestLimparValor(unittest.TestCase):
    """Cobre importador_html.limpar_valor."""

    def test_sucesso_normaliza_espacos(self) -> None:
        self.assertEqual(limpar_valor("  Engenharia   de   Software  "), "Engenharia de Software")

    def test_falha_remove_pontuacao_de_borda(self) -> None:
        self.assertEqual(limpar_valor(": Curso ;"), "Curso")

    def test_borda_string_so_com_espacos(self) -> None:
        self.assertEqual(limpar_valor("   \n\t "), "")


if __name__ == "__main__":
    unittest.main()
