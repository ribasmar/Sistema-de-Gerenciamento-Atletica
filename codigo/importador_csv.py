"""Carrega as entidades do sistema a partir de arquivos CSV (respostas de formulario).

Cada CSV em uma pasta corresponde a uma entidade. As referencias entre entidades
sao resolvidas por chaves naturais: treinador por CPF e atleta por RA. A declaracao
de matricula em HTML e referenciada pela coluna 'comprovante_matricula' e lida de
forma contida: somente arquivos dentro da pasta de dados sao aceitos (sem caminho
absoluto e sem path traversal), e o CSV permanece como fonte autoritativa - o HTML
apenas preenche campos academicos deixados em branco.
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

from importador_html import importar_declaracao_html
from modelos import ResultadoOperacao

SEPARADOR_LISTA = ";"


def _ler_csv(caminho: Path) -> list[dict[str, str]]:
    """Le um CSV em lista de dicionarios; retorna vazio se o arquivo nao existir."""
    if not caminho.exists():
        return []
    with open(caminho, newline="", encoding="utf-8-sig") as arquivo:
        leitor = csv.DictReader(arquivo)
        return [
            {(chave or ""): (valor or "").strip() for chave, valor in linha.items()}
            for linha in leitor
        ]


def _lista(valor: str) -> list[str]:
    """Quebra uma celula multivalorada usando o separador de lista."""
    return [item.strip() for item in (valor or "").split(SEPARADOR_LISTA) if item.strip()]


def _documentos(caminho: str) -> list[dict[str, str]]:
    """Monta a lista de documentos a partir do caminho do comprovante de matricula."""
    caminho = (caminho or "").strip()
    if not caminho:
        return []
    return [{"tipo": "comprovante_matricula", "path": caminho}]


def _resolver_html_seguro(valor: str, base_html: Path) -> Path | None:
    """Resolve o caminho do HTML apenas se ele estiver contido na pasta de dados."""
    valor = (valor or "").strip()
    if not valor:
        return None

    candidato = Path(valor)
    if candidato.is_absolute():
        return None

    base = base_html.resolve()
    alvo = (base / candidato).resolve()
    try:
        alvo.relative_to(base)
    except ValueError:
        return None

    return alvo if alvo.is_file() else None


def _ler_html_seguro(valor: str, base_html: Path, alertas: list[str]) -> dict[str, str]:
    """Le e extrai dados da declaracao HTML com falha segura (degrada sem interromper)."""
    valor = (valor or "").strip()
    if not valor:
        return {}

    caminho = _resolver_html_seguro(valor, base_html)
    if caminho is None:
        alertas.append(
            f"Declaracao HTML ignorada (fora da pasta de dados ou inexistente): {valor}"
        )
        return {}

    try:
        return importar_declaracao_html(str(caminho))
    except (OSError, UnicodeError) as erro:
        alertas.append(f"Falha ao ler a declaracao HTML '{valor}': {erro}")
        return {}


def _preencher_vazios(dados: dict[str, Any], html: dict[str, str], campos: tuple[str, ...]) -> None:
    """Preenche apenas os campos vazios do CSV com valores extraidos do HTML."""
    for campo in campos:
        if not dados.get(campo) and html.get(campo):
            dados[campo] = html[campo]


def _periodo_valido(valor: str, html_periodo: str, padrao: str = "1") -> str:
    """Garante um numero de periodo, usando o HTML quando o CSV nao informa."""
    if valor:
        return valor
    encontrado = re.search(r"\d+", html_periodo or "")
    return encontrado.group(0) if encontrado else padrao


def _mapear_atletica(linha: dict[str, str]) -> dict[str, Any]:
    return {
        "nome": linha.get("nome", ""),
        "universidade": linha.get("universidade", ""),
        "campus": linha.get("campus", ""),
        "cnpj": linha.get("cnpj", ""),
    }


def _mapear_atleta(linha: dict[str, str], base_html: Path, alertas: list[str]) -> dict[str, Any]:
    comprovante = linha.get("comprovante_matricula", "")
    html = _ler_html_seguro(comprovante, base_html, alertas)
    dados = {
        "nome": linha.get("nome", ""),
        "ra": linha.get("ra", ""),
        "cpf": linha.get("cpf", ""),
        "curso": linha.get("curso", ""),
        "nascimento": linha.get("nascimento", ""),
        "egresso": linha.get("egresso", ""),
        "periodo": linha.get("periodo", ""),
        "conclusao": linha.get("conclusao", ""),
        "esportes": _lista(linha.get("esportes", "")),
        "documentos": _documentos(comprovante),
    }
    _preencher_vazios(dados, html, ("nome", "ra", "curso"))
    dados["periodo"] = _periodo_valido(dados["periodo"], html.get("periodo", ""))
    return dados


def _mapear_membro(
    linha: dict[str, str], id_atletica: str, base_html: Path, alertas: list[str]
) -> dict[str, Any]:
    comprovante = linha.get("comprovante_matricula", "")
    html = _ler_html_seguro(comprovante, base_html, alertas)
    dados = {
        "id_atletica": id_atletica,
        "nome": linha.get("nome", ""),
        "ra": linha.get("ra", ""),
        "cpf": linha.get("cpf", ""),
        "documento_pessoal": linha.get("documento_pessoal", ""),
        "curso": linha.get("curso", ""),
        "cargo": linha.get("cargo", ""),
        "tempo_atletica_inicio": linha.get("tempo_atletica_inicio", ""),
        "tempo_atletica_fim_esperado": linha.get("tempo_atletica_fim_esperado", ""),
        "data_nascimento": linha.get("data_nascimento", ""),
        "inicio_egresso": linha.get("inicio_egresso", ""),
        "periodo_atual": linha.get("periodo_atual", ""),
        "tempo_esperado_conclusao": linha.get("tempo_esperado_conclusao", ""),
        "documentos_universidade": _documentos(comprovante),
    }
    _preencher_vazios(dados, html, ("nome", "ra", "curso"))
    dados["periodo_atual"] = _periodo_valido(dados["periodo_atual"], html.get("periodo", ""))
    return dados


def _mapear_treinador(linha: dict[str, str], id_atletica: str) -> dict[str, Any]:
    return {
        "id_atletica": id_atletica,
        "nome": linha.get("nome", ""),
        "cpf": linha.get("cpf", ""),
        "modalidade": linha.get("modalidade", ""),
        "salario_por_treino": linha.get("salario_por_treino", "0"),
        "telefone": linha.get("telefone", ""),
    }


def _mapear_treino(
    linha: dict[str, str],
    id_atletica: str,
    treinador_por_cpf: dict[str, str],
    atleta_por_ra: dict[str, str],
) -> dict[str, Any]:
    cpf = linha.get("treinador_cpf", "")
    return {
        "id_atletica": id_atletica,
        "modalidade": linha.get("modalidade", ""),
        "id_treinador": treinador_por_cpf.get(cpf, cpf),
        "localidade": linha.get("localidade", ""),
        "dia_semana": linha.get("dia_semana", ""),
        "horario_inicio": linha.get("horario_inicio", ""),
        "horario_fim": linha.get("horario_fim", ""),
        "atletas_inscritos": [
            atleta_por_ra.get(ra, ra) for ra in _lista(linha.get("atletas_ra", ""))
        ],
        "status_treino": linha.get("status_treino") or "CONFIRMADO",
    }


def _mapear_campeonato(
    linha: dict[str, str],
    id_atletica: str,
    treinador_por_cpf: dict[str, str],
    atleta_por_ra: dict[str, str],
) -> dict[str, Any]:
    cpf = linha.get("treinador_cpf", "")
    return {
        "id_atletica": id_atletica,
        "nome_campeonato": linha.get("nome_campeonato", ""),
        "modalidades": _lista(linha.get("modalidades", "")),
        "id_treinador_responsavel": treinador_por_cpf.get(cpf, cpf),
        "atletas_convocados": [
            atleta_por_ra.get(ra, ra) for ra in _lista(linha.get("atletas_ra", ""))
        ],
        "transporte": {
            "tipo": linha.get("transporte_tipo", ""),
            "data_saida": linha.get("transporte_data_saida", ""),
            "data_retorno": linha.get("transporte_data_retorno", ""),
        },
        "datas": {
            "inicio": linha.get("data_inicio", ""),
            "fim": linha.get("data_fim", ""),
        },
        "locais": _lista(linha.get("locais", "")),
    }


def carregar_entidades(app: Any, diretorio: str) -> list[ResultadoOperacao]:
    """Le os CSVs do diretorio e os cadastra usando os servicos da aplicacao."""
    base = Path(diretorio)
    base_html = base.parent
    resultados: list[ResultadoOperacao] = []

    id_atletica = ""
    for linha in _ler_csv(base / "atletica.csv"):
        resultado = app.atleticas.inicializar(_mapear_atletica(linha))
        resultados.append(resultado)
        if resultado.exit_code == 0 and resultado.dados_gerados:
            id_atletica = resultado.dados_gerados["id_atletica"]

    alertas_atletas: list[str] = []
    atletas = [
        _mapear_atleta(linha, base_html, alertas_atletas)
        for linha in _ler_csv(base / "atleta.csv")
    ]
    if atletas:
        resultado_atletas = app.pessoas.cadastrar_atletas(
            {"id_atletica": id_atletica, "atletas": atletas}
        )
        resultado_atletas.alertas.extend(alertas_atletas)
        resultados.append(resultado_atletas)

    for linha in _ler_csv(base / "membro.csv"):
        alertas_membro: list[str] = []
        dados_membro = _mapear_membro(linha, id_atletica, base_html, alertas_membro)
        resultado_membro = app.pessoas.cadastrar_membro(dados_membro)
        resultado_membro.alertas.extend(alertas_membro)
        resultados.append(resultado_membro)

    for linha in _ler_csv(base / "treinador.csv"):
        resultados.append(
            app.pessoas.cadastrar_treinador(_mapear_treinador(linha, id_atletica))
        )

    treinador_por_cpf = {t.cpf: t.id_treinador for t in app.banco.treinadores.listar()}
    atleta_por_ra = {a.ra: a.id_atleta for a in app.banco.atletas.listar()}

    for linha in _ler_csv(base / "treino.csv"):
        resultados.append(
            app.treinos.criar(
                _mapear_treino(linha, id_atletica, treinador_por_cpf, atleta_por_ra)
            )
        )

    treino_por_modalidade = {t.modalidade: t.id_treino for t in app.banco.treinos.listar()}
    for linha in _ler_csv(base / "atualizacao_treino.csv"):
        id_treino = treino_por_modalidade.get(linha.get("modalidade", ""))
        if id_treino is None:
            continue
        campos: dict[str, Any] = {"id_treino": id_treino}
        for chave in ("localidade", "dia_semana", "horario_inicio", "horario_fim", "status_treino"):
            if linha.get(chave):
                campos[chave] = linha[chave]
        if linha.get("atletas_ra"):
            campos["atletas_inscritos"] = [
                atleta_por_ra.get(ra, ra) for ra in _lista(linha["atletas_ra"])
            ]
        resultados.append(app.treinos.atualizar(campos))

    for linha in _ler_csv(base / "campeonato.csv"):
        resultados.append(
            app.campeonatos.criar(
                _mapear_campeonato(linha, id_atletica, treinador_por_cpf, atleta_por_ra)
            )
        )

    return resultados
