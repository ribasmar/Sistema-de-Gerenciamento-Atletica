#!/usr/bin/env python3
"""
parse_declaracao_matricula.py
Usa regex direcionadas para extrair apenas os campos solicitados
- nome
- Nº de registro
- curso
- duração
- Período/Ano de Ingresso
- Período do Aluno

Uso:
    python parse_declaracao_matricula.py "Declaração Matrícula.html" [--encoding cp1252] [--json out.json]

Dependências:
    pip install beautifulsoup4 lxml
"""

import argparse
import json
import re

from bs4 import BeautifulSoup

STOP_TOKENS = [
    "Nº de registro",
    "Nº",
    "Nº de matrícula",
    "Matrícula",
    "Registro",
    "Curso",
    "Carga Horária",
    "Carga Horária do Curso",
    "Carga Horaria",
    "Duração",
    "DURACAO",
    "Regime de Ensino",
    "Período/Ano de Ingresso",
    "Período do Aluno",
    "Período",
    "Turno",
    "Semestre Letivo",
    "Semestre",
    "Início do Semestre",
    "Término do Semestre",
    "Dias Letivos",
    "Estágio",
    "Reconhecimento/Autorização do Curso",
    "Reconhecimento",
    "Por ser verdade",
    "Este documento",
    "Código de validação",
    "Url para validação",
    "Url",
]

# Lookahead fragment (no word boundary to support multi-word tokens)
STOP_RE = r"(?=\s*(?:" + "|".join(re.escape(t) for t in STOP_TOKENS) + r"))"


def clean_text_from_html(html):
    """Extrai texto do HTML preservando quebras de bloco (usa \n) e normaliza espaços."""
    try:
        soup = BeautifulSoup(html, "lxml")
    except Exception:
        soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n", strip=True)
    # substituir NBSP
    text = text.replace("\xa0", " ")
    # normalizar quebras de linha múltiplas
    text = re.sub(r"\r", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)
    # colapsar espaços dentro de linhas
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in text.split("\n")]
    text = "\n".join([l for l in lines if l])
    return text


def extract_by_labels(text, label_variants):
    """Tenta extrair o valor que segue qualquer variante de label até o próximo STOP token.
    Retorna string vazia se não encontrar.
    """
    flags = re.IGNORECASE | re.DOTALL
    for label in label_variants:
        # captura até o próximo token conhecido (não guloso)
        pattern = r"(?i)" + re.escape(label) + r"\s*[:\-]?\s*(.*?)" + STOP_RE
        m = re.search(pattern, text, flags)
        if m:
            return clean_value(m.group(1))
    # fallback: captura até o fim da linha
    for label in label_variants:
        pattern = r"(?i)" + re.escape(label) + r"\s*[:\-]?\s*([^\n\r]+)"
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return clean_value(m.group(1))
    return ""


def clean_value(v):
    if not v:
        return ""
    s = v.replace("\n", " ").replace("\r", " ")
    s = re.sub(r"\s+", " ", s).strip(" \t\n\r:;-–—")
    return s


def extract_matricula(text):
    """Extrai número de registro/matrícula com heurísticas."""
    # 1) tentativas diretas com labels
    patterns = [
        r"(?i)(?:N[ºo°]|Nº|N[oº°]\s*de\s*registro|N[oº°]\s*de\s*matr[ií]cula|N[oº°] de registro)\s*[:\-]?\s*(\d{4,})",
        r"(?i)matr[ií]cula\s*[:\-]?\s*(\d{4,})",
        r"(?i)registro\s*[:\-]?\s*(\d{4,})",
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    # 2) procurar primeiro número que é plausível e próximo das palavras "Nome" ou "registro"
    m = re.search(r"(?i)(?:nome.*?)(\d{4,7})", text[:5000], re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1)
    # 3) fallback: procurar qualquer número de 5-8 dígitos no documento (menos ideal)
    m = re.search(r"\b(\d{5,8})\b", text)
    if m:
        return m.group(1)
    return ""


def extract_curso(text):
    # tentar label "Curso" até próximo token
    vals = extract_by_labels(text, ["Curso", "Curso:"])
    if vals:
        # remover possíveis palavras terminal como "Carga Horária do Curso" (caso lookahead falhou)
        vals = re.split(
            r"\bCarga Hor\w+|\bDura[cç][aã]o|\bRegime|\bPer[ií]odo|\bTurno",
            vals,
            flags=re.IGNORECASE,
        )[0]
        return clean_value(vals)


def extract_duracao(text):
    # procura "Duração" ou "Duração X períodos" etc
    v = extract_by_labels(text, ["Duração", "Duração:", "Duracao"])
    return v


def extract_ingresso(text):
    v = extract_by_labels(
        text,
        [
            "Período/Ano de Ingresso",
            "Período/Ano de Ingresso:",
            "Periodo/Ano de Ingresso",
        ],
    )
    return v


def extract_periodo_aluno(text):
    v = extract_by_labels(
        text, ["Período do Aluno", "Período do Aluno:", "Periodo do Aluno"]
    )
    return v


def parse_html_file(path, encoding="cp1252"):
    with open(path, "r", encoding=encoding, errors="ignore") as f:
        html = f.read()
    text = clean_text_from_html(html)

    result = {}
    result["nome"] = extract_by_labels(text, ["Nome", "Nome do Aluno", "Aluno"])
    # matrícula/registro
    matricula = extract_matricula(text)
    result["RA"] = matricula
    result["curso"] = extract_curso(text)
    result["duração"] = extract_duracao(text)
    result["ingresso"] = extract_ingresso(text)
    result["periodo"] = extract_periodo_aluno(text)

    return {"aluno": result}


def main():
    p = argparse.ArgumentParser(
        description="Extrai campos importantes de Declaração de Matrícula (HTML)"
    )
    p.add_argument("file", help="Caminho para o arquivo HTML")
    p.add_argument(
        "--encoding", default="cp1252", help="Encoding do HTML (default: cp1252)"
    )
    p.add_argument("--json", help="Grava saída JSON em arquivo")
    args = p.parse_args()

    out = parse_html_file(args.file, encoding=args.encoding)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as jf:
            json.dump(out, jf, ensure_ascii=False, indent=2)
        print("Gravado em", args.json)
    else:
        print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
