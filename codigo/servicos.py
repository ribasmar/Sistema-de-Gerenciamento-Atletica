"""Camada de servico com as regras de negocio da aplicacao."""

from __future__ import annotations

from datetime import date
from typing import Any

from eventos import BarramentoEventos
from modelos import (
    Atletica,
    Atleta,
    Campeonato,
    Documento,
    MembroAtletica,
    ResultadoOperacao,
    Treinador,
    Treino,
)
from repositorios import BancoMemoria


def _data(valor: str) -> date:
    return date.fromisoformat(valor)


def _documentos(lista: list[dict[str, Any]]) -> list[Documento]:
    return [Documento.de_dict(item) for item in lista]


class AtleticaService:
    """Servicos para cadastro da atletica."""

    def __init__(self, banco: BancoMemoria) -> None:
        self.banco = banco

    def inicializar(self, dados: dict[str, Any]) -> ResultadoOperacao:
        """Cadastra a atletica principal."""
        obrigatorios = ["nome", "universidade", "campus", "cnpj"]
        faltantes = [campo for campo in obrigatorios if not dados.get(campo)]
        if faltantes:
            return ResultadoOperacao(
                1,
                "ERRO_VALIDACAO",
                "inicializar-atletica",
                erros=[
                    {
                        "campo": campo,
                        "motivo": f"O campo '{campo}' e obrigatorio.",
                    }
                    for campo in faltantes
                ],
            )

        atletica = Atletica(
            nome=dados["nome"],
            universidade=dados["universidade"],
            campus=dados["campus"],
            cnpj=dados["cnpj"],
        )
        self.banco.atleticas.adicionar(atletica)
        return ResultadoOperacao(
            0,
            "SUCESSO",
            "inicializar-atletica",
            dados_gerados={
                "mensagem": "Entidade Atletica inicializada com sucesso.",
                "id_atletica": atletica.id_atletica,
            },
        )


class PessoaService:
    """Servicos para atletas, membros e treinadores."""

    def __init__(self, banco: BancoMemoria) -> None:
        self.banco = banco

    def cadastrar_atletas(self, dados: dict[str, Any]) -> ResultadoOperacao:
        """Cadastra atletas e registra rejeicoes por duplicidade."""
        importados: list[dict[str, str]] = []
        rejeitados: list[dict[str, str]] = []

        for item in dados.get("atletas", []):
            if self.banco.cpf_ou_ra_existe(item["cpf"], item["ra"]):
                rejeitados.append(
                    {
                        "ra": item["ra"],
                        "motivo_rejeicao": "CONFLITO_INTEGRIDADE",
                        "detalhe": "Atleta com RA ou CPF ja cadastrado.",
                    }
                )
                continue

            atleta = Atleta(
                id_atletica=dados["id_atletica"],
                nome=item["nome"],
                ra=item["ra"],
                cpf=item["cpf"],
                curso=item["curso"],
                nascimento=_data(item["nascimento"]),
                egresso=_data(item["egresso"]),
                periodo=int(item["periodo"]),
                conclusao=item["conclusao"],
                documentos=_documentos(item.get("documentos", [])),
                esportes=item.get("esportes", []),
            )
            self.banco.atletas.adicionar(atleta)
            importados.append(
                {
                    "ra": atleta.ra,
                    "id_atleta_gerado": atleta.id_atleta,
                    "status": "REGISTRADO",
                }
            )

        status = "SUCESSO" if not rejeitados else "PROCESSADO_COM_REJEICOES"
        return ResultadoOperacao(
            0 if not rejeitados else 2,
            status,
            "cadastrar-atletas",
            dados_gerados={
                "metricas": {
                    "total_registros_lidos": len(dados.get("atletas", [])),
                    "total_sucesso": len(importados),
                    "total_falhas": len(rejeitados),
                },
                "importados": importados,
                "rejeitados": rejeitados,
            },
        )

    def cadastrar_membro(self, dados: dict[str, Any]) -> ResultadoOperacao:
        """Cadastra um membro administrativo da atletica."""
        if self.banco.cpf_ou_ra_existe(dados["cpf"], dados["ra"]):
            return ResultadoOperacao(
                2,
                "CONFLITO_INTEGRIDADE",
                "cadastrar-membro",
                erros=[
                    {
                        "chave": "CPF_RA_DUPLICADO",
                        "detalhe": "Ja existe membro ou atleta com o CPF ou RA informado.",
                    }
                ],
            )

        membro = MembroAtletica(
            id_atletica=dados["id_atletica"],
            nome=dados["nome"],
            ra=dados["ra"],
            cpf=dados["cpf"],
            documento_pessoal=dados["documento_pessoal"],
            curso=dados["curso"],
            cargo=dados["cargo"],
            tempo_atletica_inicio=_data(dados["tempo_atletica_inicio"]),
            tempo_atletica_fim_esperado=_data(dados["tempo_atletica_fim_esperado"]),
            data_nascimento=_data(dados["data_nascimento"]),
            inicio_egresso=_data(dados["inicio_egresso"]),
            periodo_atual=int(dados["periodo_atual"]),
            tempo_esperado_conclusao=dados["tempo_esperado_conclusao"],
            documentos_universidade=_documentos(dados.get("documentos_universidade", [])),
        )
        self.banco.membros.adicionar(membro)
        return ResultadoOperacao(
            0,
            "SUCESSO",
            "cadastrar-membro",
            dados_gerados={
                "mensagem": "Membro da gestao da Atletica registrado com sucesso.",
                "id_membro": membro.id_membro,
            },
        )

    def cadastrar_treinador(self, dados: dict[str, Any]) -> ResultadoOperacao:
        """Cadastra um treinador para posterior vinculo aos treinos."""
        treinador = Treinador(
            id_atletica=dados["id_atletica"],
            nome=dados["nome"],
            cpf=dados["cpf"],
            modalidade=dados["modalidade"],
            salario_por_treino=float(dados["salario_por_treino"]),
            telefone=dados["telefone"],
        )
        self.banco.treinadores.adicionar(treinador)
        return ResultadoOperacao(
            0,
            "SUCESSO",
            "cadastrar-treinador",
            dados_gerados={
                "mensagem": "Treinador cadastrado com sucesso.",
                "id_treinador": treinador.id_treinador,
            },
        )


class TreinoService:
    """Servicos para criacao e atualizacao de treinos."""

    def __init__(self, banco: BancoMemoria, eventos: BarramentoEventos) -> None:
        self.banco = banco
        self.eventos = eventos

    def criar(self, dados: dict[str, Any]) -> ResultadoOperacao:
        """Cria um treino validando treinador e atletas."""
        if not self.banco.treinadores.existe(dados["id_treinador"]):
            return ResultadoOperacao(
                2,
                "CONFLITO_INTEGRIDADE",
                "criar-treino",
                erros=[
                    {
                        "entidade": "Treinador",
                        "id_referenciado": dados["id_treinador"],
                        "motivo": "O treinador informado nao foi localizado.",
                    }
                ],
            )

        atletas_invalidos = [
            atleta
            for atleta in dados.get("atletas_inscritos", [])
            if not self.banco.atletas.existe(atleta)
        ]
        if atletas_invalidos:
            return ResultadoOperacao(
                2,
                "CONFLITO_INTEGRIDADE",
                "criar-treino",
                erros=[
                    {
                        "entidade": "Atleta",
                        "ids_referenciados": atletas_invalidos,
                        "motivo": "Ha atletas nao cadastrados na lista do treino.",
                    }
                ],
            )

        treino = Treino(**dados)
        self.banco.treinos.adicionar(treino)
        return ResultadoOperacao(
            0,
            "SUCESSO",
            "criar-treino",
            dados_gerados={
                "mensagem": "Agenda de treino estruturada e vinculada com sucesso.",
                "id_treino": treino.id_treino,
            },
        )

    def atualizar(self, dados: dict[str, Any]) -> ResultadoOperacao:
        """Atualiza um treino existente e dispara evento de notificacao."""
        id_treino = dados["id_treino"]
        treino = self.banco.treinos.obter(id_treino)
        if treino is None:
            return ResultadoOperacao(
                2,
                "REGISTRO_NAO_ENCONTRADO",
                "atualizar-treino",
                erros=[
                    {
                        "identificador": "id_treino",
                        "valor_procurado": id_treino,
                        "motivo": "O treino informado nao existe.",
                    }
                ],
            )

        campos = {chave: valor for chave, valor in dados.items() if chave != "id_treino"}
        campos_alterados = [
            chave for chave, valor in campos.items() if getattr(treino, chave, None) != valor
        ]
        self.banco.treinos.atualizar(id_treino, campos)
        if campos_alterados:
            self.eventos.publicar(
                "treino_atualizado",
                {"id_treino": id_treino, "campos_alterados": campos_alterados},
            )

        return ResultadoOperacao(
            0,
            "SUCESSO",
            "atualizar-treino",
            dados_gerados={
                "id_treino": id_treino,
                "campos_alterados": campos_alterados,
            },
        )


class CampeonatoService:
    """Servicos para gerenciamento de campeonatos."""

    def __init__(self, banco: BancoMemoria) -> None:
        self.banco = banco

    def criar(self, dados: dict[str, Any]) -> ResultadoOperacao:
        """Cria um campeonato validando datas e referencias."""
        if date.fromisoformat(dados["datas"]["fim"]) < date.fromisoformat(
            dados["datas"]["inicio"]
        ):
            return ResultadoOperacao(
                1,
                "ERRO_VALIDACAO_LOGICA",
                "criar-campeonato",
                erros=[
                    {
                        "contexto": "datas",
                        "motivo": "A data de fim nao pode ser anterior a data de inicio.",
                    }
                ],
            )

        if not self.banco.treinadores.existe(dados["id_treinador_responsavel"]):
            return ResultadoOperacao(
                2,
                "CONFLITO_INTEGRIDADE",
                "criar-campeonato",
                erros=[
                    {
                        "entidade": "Treinador",
                        "id_referenciado": dados["id_treinador_responsavel"],
                        "motivo": "O treinador responsavel nao foi localizado.",
                    }
                ],
            )

        atletas_invalidos = [
            atleta
            for atleta in dados.get("atletas_convocados", [])
            if not self.banco.atletas.existe(atleta)
        ]
        if atletas_invalidos:
            return ResultadoOperacao(
                2,
                "CONFLITO_INTEGRIDADE",
                "criar-campeonato",
                erros=[
                    {
                        "entidade": "Atleta",
                        "ids_referenciados": atletas_invalidos,
                        "motivo": "Ha atletas convocados que nao estao cadastrados.",
                    }
                ],
            )

        campeonato = Campeonato(**dados)
        self.banco.campeonatos.adicionar(campeonato)
        return ResultadoOperacao(
            0,
            "SUCESSO",
            "criar-campeonato",
            dados_gerados={
                "mensagem": "Campeonato processado e atletas vinculados com sucesso.",
                "id_campeonato": campeonato.id_campeonato,
            },
        )
