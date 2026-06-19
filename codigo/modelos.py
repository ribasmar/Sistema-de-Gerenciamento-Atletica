"""Modelos de dominio do Sistema de Gerenciamento de Atletica."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any
from uuid import uuid4


def gerar_id() -> str:
    """Gera um identificador unico para as entidades do sistema."""
    return str(uuid4())


def agora_iso() -> str:
    """Retorna o timestamp atual no formato ISO."""
    return datetime.now().replace(microsecond=0).isoformat()


@dataclass
class Documento:
    """Documento associado a um aluno, atleta ou membro da atletica."""

    tipo: str
    path: str

    @classmethod
    def de_dict(cls, dados: dict[str, Any]) -> "Documento":
        """Cria um documento a partir de um dicionario."""
        return cls(tipo=dados["tipo"], path=dados["path"])


@dataclass
class Atletica:
    """Entidade principal que agrupa atletas, treinos e campeonatos."""

    nome: str
    universidade: str
    campus: str
    cnpj: str
    id_atletica: str = field(default_factory=gerar_id)


@dataclass
class Atleta:
    """Pessoa cadastrada para participar de modalidades e competicoes."""

    nome: str
    ra: str
    cpf: str
    curso: str
    nascimento: date
    egresso: date
    periodo: int
    conclusao: str
    documentos: list[Documento]
    esportes: list[str] = field(default_factory=list)
    id_atletica: str = ""
    id_atleta: str = field(default_factory=gerar_id)


@dataclass
class MembroAtletica:
    """Membro administrativo da atletica."""

    nome: str
    ra: str
    cpf: str
    documento_pessoal: str
    curso: str
    cargo: str
    tempo_atletica_inicio: date
    tempo_atletica_fim_esperado: date
    data_nascimento: date
    inicio_egresso: date
    periodo_atual: int
    tempo_esperado_conclusao: str
    documentos_universidade: list[Documento]
    id_atletica: str = ""
    id_membro: str = field(default_factory=gerar_id)


@dataclass
class Treinador:
    """Treinador disponivel para ser vinculado a treinos."""

    nome: str
    cpf: str
    modalidade: str
    salario_por_treino: float
    telefone: str
    id_atletica: str = ""
    id_treinador: str = field(default_factory=gerar_id)


@dataclass
class Treino:
    """Treino agendado para uma modalidade."""

    id_atletica: str
    modalidade: str
    id_treinador: str
    localidade: str
    dia_semana: str
    horario_inicio: str
    horario_fim: str
    atletas_inscritos: list[str]
    status_treino: str = "CONFIRMADO"
    id_treino: str = field(default_factory=gerar_id)


@dataclass
class Campeonato:
    """Campeonato ou evento esportivo gerenciado pela atletica."""

    id_atletica: str
    nome_campeonato: str
    modalidades: list[str]
    id_treinador_responsavel: str
    atletas_convocados: list[str]
    transporte: dict[str, Any]
    datas: dict[str, str]
    locais: list[str]
    id_campeonato: str = field(default_factory=gerar_id)


@dataclass
class ResultadoOperacao:
    """Saida padronizada para comandos e servicos."""

    exit_code: int
    status: str
    comando: str
    dados_gerados: dict[str, Any] | None = None
    erros: list[dict[str, Any]] | None = None
    alertas: list[str] = field(default_factory=list)
