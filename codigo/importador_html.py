"""Importacao de dados de aluno a partir de declaracao de matricula em HTML."""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path


class ExtratorTextoHTML(HTMLParser):
    """Extrai texto de um documento HTML usando apenas a biblioteca padrao."""

    def __init__(self) -> None:
        super().__init__()
        self._partes: list[str] = []
        self._ignorar_conteudo = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        """Ignora blocos que nao fazem parte dos dados visiveis da declaracao."""
        if tag.lower() in {"script", "style"}:
            self._ignorar_conteudo = True

    def handle_endtag(self, tag: str) -> None:
        """Volta a coletar texto ao sair de blocos ignorados."""
        if tag.lower() in {"script", "style"}:
            self._ignorar_conteudo = False

    def handle_data(self, data: str) -> None:
        """Recebe cada trecho textual encontrado pelo parser."""
        if not self._ignorar_conteudo and data.strip():
            self._partes.append(data.strip())

    def texto(self) -> str:
        """Retorna o texto normalizado do HTML."""
        texto = "\n".join(self._partes).replace("\xa0", " ")
        linhas = [re.sub(r"\s+", " ", linha).strip() for linha in texto.splitlines()]
        return "\n".join(linha for linha in linhas if linha)


ROTULOS_PARADA = [
    "Nº de registro",
    "Nº de matricula",
    "Nº de matrícula",
    "Matricula",
    "Matrícula",
    "Registro",
    "Curso",
    "Carga Horaria",
    "Carga Horária",
    "Duracao",
    "Duração",
    "Regime de Ensino",
    "Periodo/Ano de Ingresso",
    "Período/Ano de Ingresso",
    "Periodo do Aluno",
    "Período do Aluno",
    "Turno",
    "Semestre",
    "Por ser verdade",
    "Codigo de validacao",
    "Código de validação",
    "Url",
]


def limpar_valor(valor: str) -> str:
    """Remove quebras e pontuacao solta das bordas."""
    valor = valor.replace("\n", " ").replace("\r", " ")
    return re.sub(r"\s+", " ", valor).strip(" \t\n\r:;-")


def extrair_texto_html(conteudo_html: str) -> str:
    """Extrai texto limpo de uma string HTML."""
    parser = ExtratorTextoHTML()
    parser.feed(conteudo_html)
    return parser.texto()


def extrair_por_rotulo(texto: str, rotulos: list[str]) -> str:
    """Extrai o valor apos um dos rotulos informados."""
    parada = "|".join(re.escape(rotulo) for rotulo in ROTULOS_PARADA)
    for rotulo in rotulos:
        padrao = re.escape(rotulo) + r"\s*[:\-]?\s*(.*?)(?=\s*(?:" + parada + r")|$)"
        encontrado = re.search(padrao, texto, re.IGNORECASE | re.DOTALL)
        if encontrado:
            return limpar_valor(encontrado.group(1))

    for rotulo in rotulos:
        padrao = re.escape(rotulo) + r"\s*[:\-]?\s*([^\n\r]+)"
        encontrado = re.search(padrao, texto, re.IGNORECASE)
        if encontrado:
            return limpar_valor(encontrado.group(1))

    return ""


def extrair_ra(texto: str) -> str:
    """Extrai RA, matricula ou numero de registro."""
    padroes = [
        r"(?:RA|Registro|Matr[ií]cula|N[ºo°]\s*de\s*registro)\s*[:\-]?\s*([A-Za-z]?\d{4,})",
        r"\b([A-Za-z]\d{6,})\b",
        r"\b(\d{5,8})\b",
    ]
    for padrao in padroes:
        encontrado = re.search(padrao, texto, re.IGNORECASE)
        if encontrado:
            return encontrado.group(1).strip()
    return ""


def normalizar_caminho(caminho: str) -> str:
    """Normaliza caminhos digitados no terminal, inclusive com aspas ou mojibake."""
    caminho = caminho.strip().strip("'\"")
    if Path(caminho).exists():
        return caminho

    try:
        reparado = caminho.encode("latin-1").decode("utf-8")
    except UnicodeError:
        return caminho

    return reparado if Path(reparado).exists() else caminho


def ler_html(caminho: str, encoding: str = "auto") -> str:
    """Le o HTML detectando encoding quando necessario."""
    caminho = normalizar_caminho(caminho)
    with open(caminho, "rb") as arquivo:
        conteudo = arquivo.read()

    if encoding != "auto":
        return conteudo.decode(encoding, errors="ignore")

    inicio = conteudo[:1000].decode("ascii", errors="ignore")
    encontrado = re.search(r"charset=([\w-]+)", inicio, re.IGNORECASE)
    codificacoes = [encontrado.group(1)] if encontrado else []
    codificacoes.extend(["utf-8", "cp1252", "latin-1"])

    for codificacao in codificacoes:
        try:
            return conteudo.decode(codificacao)
        except UnicodeDecodeError:
            continue
    return conteudo.decode("utf-8", errors="ignore")


def importar_declaracao_html(caminho: str, encoding: str = "auto") -> dict[str, str]:
    """Le um HTML de declaracao de matricula e retorna os dados encontrados."""
    texto = extrair_texto_html(ler_html(caminho, encoding))

    return {
        "nome": extrair_por_rotulo(texto, ["Nome do Aluno", "Nome", "Aluno"]),
        "ra": extrair_ra(texto),
        "curso": extrair_por_rotulo(texto, ["Curso"]),
        "duracao": extrair_por_rotulo(texto, ["Duração", "Duracao"]),
        "ingresso": extrair_por_rotulo(
            texto, ["Período/Ano de Ingresso", "Periodo/Ano de Ingresso"]
        ),
        "periodo": extrair_por_rotulo(
            texto, ["Período do Aluno", "Periodo do Aluno", "Período", "Periodo"]
        ),
    }
