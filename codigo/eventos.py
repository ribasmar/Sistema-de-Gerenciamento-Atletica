"""Implementacao simples do padrao Observer."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable

Observador = Callable[[dict[str, Any]], None]


class BarramentoEventos:
    """Dispara eventos de dominio para observadores inscritos."""

    def __init__(self) -> None:
        self._observadores: dict[str, list[Observador]] = defaultdict(list)

    def inscrever(self, evento: str, observador: Observador) -> None:
        """Inscreve uma funcao observadora em um evento."""
        self._observadores[evento].append(observador)

    def publicar(self, evento: str, payload: dict[str, Any]) -> None:
        """Publica o evento para todos os observadores inscritos."""
        for observador in self._observadores[evento]:
            observador(payload)


class CaixaNotificacoes:
    """Armazena notificacoes geradas durante a execucao."""

    def __init__(self) -> None:
        self.mensagens: list[str] = []

    def registrar_alteracao_treino(self, payload: dict[str, Any]) -> None:
        """Cria uma notificacao quando um treino e alterado."""
        mensagem = (
            "Treino atualizado: "
            f"{payload['id_treino']} alterou {', '.join(payload['campos_alterados'])}."
        )
        self.mensagens.append(mensagem)
