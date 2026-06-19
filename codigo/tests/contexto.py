"""Ajusta o sys.path para permitir importar os modulos da pasta codigo nos testes."""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ_CODIGO = Path(__file__).resolve().parent.parent

if str(RAIZ_CODIGO) not in sys.path:
    sys.path.insert(0, str(RAIZ_CODIGO))
