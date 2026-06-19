"""Testes da camada de servico cobrindo sucesso, falha e borda das regras de negocio."""

from __future__ import annotations

import unittest

from tests import contexto  # noqa: F401  (ajuste de sys.path)

from eventos import BarramentoEventos
from repositorios import BancoMemoria
from servicos import AtleticaService, CampeonatoService, PessoaService, TreinoService


def _atleta_valido(ra: str = "a1234567", cpf: str = "111.111.111-11") -> dict:
    return {
        "nome": "Atleta Teste",
        "ra": ra,
        "cpf": cpf,
        "curso": "Engenharia",
        "nascimento": "2000-01-01",
        "egresso": "2019-03-01",
        "periodo": 4,
        "conclusao": "2024-12-01",
        "documentos": [],
        "esportes": ["volei"],
    }


class TestAtleticaServiceInicializar(unittest.TestCase):
    """Cobre AtleticaService.inicializar."""

    def setUp(self) -> None:
        self.service = AtleticaService(BancoMemoria())

    def test_sucesso_cadastra_atletica(self) -> None:
        resultado = self.service.inicializar(
            {
                "nome": "Atletica X",
                "universidade": "UTFPR",
                "campus": "Campo Mourao",
                "cnpj": "00.000.000/0001-00",
            }
        )
        self.assertEqual(resultado.exit_code, 0)
        self.assertEqual(resultado.status, "SUCESSO")
        self.assertIn("id_atletica", resultado.dados_gerados)

    def test_falha_campo_obrigatorio_ausente(self) -> None:
        resultado = self.service.inicializar(
            {"nome": "Atletica X", "universidade": "UTFPR", "campus": "Campo Mourao"}
        )
        self.assertEqual(resultado.exit_code, 1)
        self.assertEqual(resultado.status, "ERRO_VALIDACAO")
        self.assertEqual(resultado.erros[0]["campo"], "cnpj")

    def test_borda_campo_vazio_e_invalido(self) -> None:
        resultado = self.service.inicializar(
            {
                "nome": "Atletica X",
                "universidade": "UTFPR",
                "campus": "Campo Mourao",
                "cnpj": "",
            }
        )
        self.assertEqual(resultado.status, "ERRO_VALIDACAO")
        self.assertEqual(resultado.erros[0]["campo"], "cnpj")


class TestPessoaServiceCadastrarAtletas(unittest.TestCase):
    """Cobre PessoaService.cadastrar_atletas."""

    def setUp(self) -> None:
        self.banco = BancoMemoria()
        self.service = PessoaService(self.banco)

    def test_sucesso_cadastra_novo_atleta(self) -> None:
        resultado = self.service.cadastrar_atletas(
            {"id_atletica": "atl-1", "atletas": [_atleta_valido()]}
        )
        self.assertEqual(resultado.exit_code, 0)
        self.assertEqual(resultado.status, "SUCESSO")
        self.assertEqual(resultado.dados_gerados["metricas"]["total_sucesso"], 1)
        self.assertEqual(len(self.banco.atletas.listar()), 1)

    def test_falha_rejeita_cpf_ou_ra_duplicado(self) -> None:
        self.service.cadastrar_atletas(
            {"id_atletica": "atl-1", "atletas": [_atleta_valido()]}
        )
        resultado = self.service.cadastrar_atletas(
            {"id_atletica": "atl-1", "atletas": [_atleta_valido()]}
        )
        self.assertEqual(resultado.exit_code, 2)
        self.assertEqual(resultado.status, "PROCESSADO_COM_REJEICOES")
        self.assertEqual(resultado.dados_gerados["metricas"]["total_falhas"], 1)

    def test_borda_lista_vazia(self) -> None:
        resultado = self.service.cadastrar_atletas(
            {"id_atletica": "atl-1", "atletas": []}
        )
        self.assertEqual(resultado.exit_code, 0)
        self.assertEqual(resultado.dados_gerados["metricas"]["total_registros_lidos"], 0)
        self.assertEqual(resultado.dados_gerados["metricas"]["total_sucesso"], 0)


class TestCampeonatoServiceCriar(unittest.TestCase):
    """Cobre CampeonatoService.criar."""

    def setUp(self) -> None:
        self.banco = BancoMemoria()
        self.service = CampeonatoService(self.banco)
        pessoa = PessoaService(self.banco)
        criado = pessoa.cadastrar_atletas(
            {"id_atletica": "atl-1", "atletas": [_atleta_valido()]}
        )
        self.id_atleta = criado.dados_gerados["importados"][0]["id_atleta_gerado"]
        treinador = pessoa.cadastrar_treinador(
            {
                "id_atletica": "atl-1",
                "nome": "Treinador Teste",
                "cpf": "222.222.222-22",
                "modalidade": "volei",
                "salario_por_treino": 100.0,
                "telefone": "44999999999",
            }
        )
        self.id_treinador = treinador.dados_gerados["id_treinador"]

    def _payload(self, inicio: str, fim: str, id_treinador: str | None = None) -> dict:
        return {
            "id_atletica": "atl-1",
            "nome_campeonato": "Copa Teste",
            "modalidades": ["volei"],
            "id_treinador_responsavel": id_treinador or self.id_treinador,
            "atletas_convocados": [self.id_atleta],
            "transporte": {},
            "datas": {"inicio": inicio, "fim": fim},
            "locais": ["Ginasio"],
        }

    def test_sucesso_cria_campeonato(self) -> None:
        resultado = self.service.criar(self._payload("2026-08-01", "2026-08-05"))
        self.assertEqual(resultado.exit_code, 0)
        self.assertEqual(resultado.status, "SUCESSO")
        self.assertEqual(len(self.banco.campeonatos.listar()), 1)

    def test_falha_treinador_inexistente(self) -> None:
        resultado = self.service.criar(
            self._payload("2026-08-01", "2026-08-05", id_treinador="inexistente")
        )
        self.assertEqual(resultado.exit_code, 2)
        self.assertEqual(resultado.status, "CONFLITO_INTEGRIDADE")

    def test_borda_data_fim_igual_inicio(self) -> None:
        resultado = self.service.criar(self._payload("2026-08-01", "2026-08-01"))
        self.assertEqual(resultado.exit_code, 0)
        self.assertEqual(resultado.status, "SUCESSO")


class TestTreinoServiceAtualizar(unittest.TestCase):
    """Cobre TreinoService.atualizar e a publicacao de evento (Observer)."""

    def setUp(self) -> None:
        self.banco = BancoMemoria()
        self.eventos = BarramentoEventos()
        self.recebidos: list[dict] = []
        self.eventos.inscrever("treino_atualizado", self.recebidos.append)
        self.service = TreinoService(self.banco, self.eventos)

        pessoa = PessoaService(self.banco)
        criado = pessoa.cadastrar_atletas(
            {"id_atletica": "atl-1", "atletas": [_atleta_valido()]}
        )
        id_atleta = criado.dados_gerados["importados"][0]["id_atleta_gerado"]
        treinador = pessoa.cadastrar_treinador(
            {
                "id_atletica": "atl-1",
                "nome": "Treinador Teste",
                "cpf": "222.222.222-22",
                "modalidade": "volei",
                "salario_por_treino": 100.0,
                "telefone": "44999999999",
            }
        )
        treino = self.service.criar(
            {
                "id_atletica": "atl-1",
                "modalidade": "volei",
                "id_treinador": treinador.dados_gerados["id_treinador"],
                "localidade": "Ginasio",
                "dia_semana": "SEG",
                "horario_inicio": "18:00",
                "horario_fim": "20:00",
                "atletas_inscritos": [id_atleta],
            }
        )
        self.id_treino = treino.dados_gerados["id_treino"]

    def test_sucesso_altera_campo_e_publica_evento(self) -> None:
        resultado = self.service.atualizar(
            {"id_treino": self.id_treino, "localidade": "Quadra Nova"}
        )
        self.assertEqual(resultado.exit_code, 0)
        self.assertIn("localidade", resultado.dados_gerados["campos_alterados"])
        self.assertEqual(len(self.recebidos), 1)

    def test_falha_treino_inexistente(self) -> None:
        resultado = self.service.atualizar(
            {"id_treino": "nao-existe", "localidade": "Quadra Nova"}
        )
        self.assertEqual(resultado.exit_code, 2)
        self.assertEqual(resultado.status, "REGISTRO_NAO_ENCONTRADO")

    def test_borda_sem_alteracao_real_nao_publica_evento(self) -> None:
        resultado = self.service.atualizar(
            {"id_treino": self.id_treino, "localidade": "Ginasio"}
        )
        self.assertEqual(resultado.exit_code, 0)
        self.assertEqual(resultado.dados_gerados["campos_alterados"], [])
        self.assertEqual(len(self.recebidos), 0)


if __name__ == "__main__":
    unittest.main()
