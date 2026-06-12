"""Repositorios em memoria usados pelo prototipo da Sprint 3."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class RepositorioMemoria(Generic[T]):
    """Repositorio generico baseado em dicionario."""

    def __init__(self, campo_id: str) -> None:
        self._campo_id = campo_id
        self._itens: dict[str, T] = {}

    def adicionar(self, entidade: T) -> T:
        """Adiciona uma entidade ao repositorio."""
        identificador = str(getattr(entidade, self._campo_id))
        self._itens[identificador] = entidade
        return entidade

    def obter(self, identificador: str) -> T | None:
        """Busca uma entidade pelo identificador."""
        return self._itens.get(identificador)

    def listar(self) -> list[T]:
        """Retorna todas as entidades cadastradas."""
        return list(self._itens.values())

    def atualizar(self, identificador: str, campos: dict[str, Any]) -> T | None:
        """Atualiza campos simples de uma entidade existente."""
        entidade = self.obter(identificador)
        if entidade is None:
            return None
        for campo, valor in campos.items():
            if hasattr(entidade, campo):
                setattr(entidade, campo, valor)
        return entidade

    def existe(self, identificador: str) -> bool:
        """Indica se uma entidade existe."""
        return identificador in self._itens

    def como_dicts(self) -> list[dict[str, Any]]:
        """Retorna entidades como dicionarios."""
        return [asdict(item) for item in self._itens.values()]


class BancoMemoria:
    """Agrupa os repositorios do sistema."""

    def __init__(self) -> None:
        from modelos import Atletica, Atleta, Campeonato, MembroAtletica, Treinador, Treino

        self.atleticas: RepositorioMemoria[Atletica] = RepositorioMemoria("id_atletica")
        self.atletas: RepositorioMemoria[Atleta] = RepositorioMemoria("id_atleta")
        self.membros: RepositorioMemoria[MembroAtletica] = RepositorioMemoria("id_membro")
        self.treinadores: RepositorioMemoria[Treinador] = RepositorioMemoria(
            "id_treinador"
        )
        self.treinos: RepositorioMemoria[Treino] = RepositorioMemoria("id_treino")
        self.campeonatos: RepositorioMemoria[Campeonato] = RepositorioMemoria(
            "id_campeonato"
        )

    def cpf_ou_ra_existe(self, cpf: str, ra: str) -> bool:
        """Verifica duplicidade de CPF ou RA entre atletas e membros."""
        pessoas = [*self.atletas.listar(), *self.membros.listar()]
        return any(pessoa.cpf == cpf or pessoa.ra == ra for pessoa in pessoas)
