"""Interface de terminal do Sistema de Gerenciamento de Atletica."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

from eventos import BarramentoEventos, CaixaNotificacoes
from importador_html import importar_declaracao_html, normalizar_caminho
from repositorios import BancoMemoria
from servicos import AtleticaService, CampeonatoService, PessoaService, TreinoService


class Aplicacao:
    """Compoe repositorios, servicos e observadores."""

    def __init__(self) -> None:
        self.banco = BancoMemoria()
        self.eventos = BarramentoEventos()
        self.notificacoes = CaixaNotificacoes()
        self.eventos.inscrever(
            "treino_atualizado", self.notificacoes.registrar_alteracao_treino
        )

        self.atleticas = AtleticaService(self.banco)
        self.pessoas = PessoaService(self.banco)
        self.treinos = TreinoService(self.banco, self.eventos)
        self.campeonatos = CampeonatoService(self.banco)


def imprimir(resultado: dict[str, Any]) -> None:
    """Imprime dados em JSON formatado."""
    print(json.dumps(resultado, ensure_ascii=False, indent=2, default=str))


LARGURA_TELA = 72


def linha(caractere: str = "-") -> str:
    """Monta uma linha visual para o menu."""
    return caractere * LARGURA_TELA


def painel_titulo(titulo: str, subtitulo: str = "") -> None:
    """Imprime um cabecalho centralizado."""
    print()
    print(linha("="))
    print(titulo.center(LARGURA_TELA))
    if subtitulo:
        print(subtitulo.center(LARGURA_TELA))
    print(linha("="))


def painel_secao(titulo: str) -> None:
    """Imprime uma divisoria de secao."""
    texto = f" {titulo} "
    tamanho = max(0, LARGURA_TELA - len(texto))
    print(f"\n{texto}{'-' * tamanho}")


def painel_opcao(numero: str, titulo: str, detalhe: str = "") -> None:
    """Imprime uma opcao alinhada do menu."""
    detalhe_formatado = f" {detalhe}" if detalhe else ""
    print(f"  {numero:>2}  {titulo:<38}{detalhe_formatado}")


def painel_status(tipo: str, mensagem: str) -> None:
    """Imprime uma mensagem curta de status."""
    print(f"\n[{tipo}] {mensagem}")


def imprimir_resultado_menu(resultado: dict[str, Any]) -> None:
    """Imprime o resultado de uma acao dentro do menu."""
    painel_secao("Resultado")
    imprimir(resultado)


def resumo_sessao(app: Aplicacao) -> str:
    """Resume a quantidade de cadastros feitos na sessao atual."""
    return (
        f"Atleticas: {len(app.banco.atleticas.listar())} | "
        f"Atletas: {len(app.banco.atletas.listar())} | "
        f"Membros: {len(app.banco.membros.listar())} | "
        f"Treinadores: {len(app.banco.treinadores.listar())}"
    )


def id_curto(valor: str) -> str:
    """Mostra apenas o inicio do identificador para leitura no menu."""
    return valor[:8]


def texto_lista(valores: list[str]) -> str:
    """Formata uma lista curta para exibicao no terminal."""
    return ", ".join(valores) if valores else "-"


def imprimir_vazio(rotulo: str) -> None:
    """Mostra uma mensagem de lista vazia."""
    print(f"  Nenhum {rotulo} cadastrado.")


def imprimir_linha(chave: str, valor: str) -> None:
    """Imprime um campo alinhado em uma tela de resumo."""
    print(f"  {chave:<18} {valor}")


def carregar_json(caminho: str) -> dict[str, Any]:
    """Carrega um arquivo JSON."""
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def caminho_comprovante_matricula(documentos: list[dict[str, Any]]) -> str:
    """Retorna o path do primeiro comprovante de matricula da lista."""
    for documento in documentos:
        if documento.get("tipo") == "comprovante_matricula" and documento.get("path"):
            return str(documento["path"])
    return ""


def preencher_pessoa_com_html(
    dados_pessoa: dict[str, Any],
    campo_documentos: str,
    campo_periodo: str,
    campo_ingresso: str,
) -> dict[str, Any]:
    """Preenche dados academicos usando o HTML do comprovante de matricula."""
    documentos = dados_pessoa.get(campo_documentos, [])
    caminho = caminho_comprovante_matricula(documentos)
    if not caminho:
        return dados_pessoa

    dados_html = importar_declaracao_html(caminho)
    dados_pessoa["nome"] = dados_html["nome"]
    dados_pessoa["ra"] = dados_html["ra"]
    dados_pessoa["curso"] = dados_html["curso"]
    dados_pessoa[campo_periodo] = int(numero_inicial(dados_html["periodo"], "1"))

    ingresso = ingresso_para_data(dados_html["ingresso"])
    if ingresso:
        dados_pessoa[campo_ingresso] = ingresso

    return dados_pessoa


def executar_fluxo(dados: dict[str, Any]) -> None:
    """Executa um fluxo completo a partir de dados estruturados."""
    app = Aplicacao()

    resultado_atletica = app.atleticas.inicializar(dados["atletica"])
    imprimir(resultado_atletica.para_dict())
    id_atletica = resultado_atletica.dados_gerados["id_atletica"]  # type: ignore[index]

    atletas = [
        preencher_pessoa_com_html(dict(atleta), "documentos", "periodo", "egresso")
        for atleta in dados["atletas"]
    ]
    dados_atletas = {"id_atletica": id_atletica, "atletas": atletas}
    resultado_atletas = app.pessoas.cadastrar_atletas(dados_atletas)
    imprimir(resultado_atletas.para_dict())

    atletas_por_ra = {
        item["ra"]: item["id_atleta_gerado"]
        for item in resultado_atletas.dados_gerados["importados"]  # type: ignore[index]
    }

    if "membro" in dados:
        membro = preencher_pessoa_com_html(
            dict(dados["membro"]),
            "documentos_universidade",
            "periodo_atual",
            "inicio_egresso",
        )
        membro = {"id_atletica": id_atletica, **membro}
        imprimir(app.pessoas.cadastrar_membro(membro).para_dict())

    treinador = {"id_atletica": id_atletica, **dados["treinador"]}
    resultado_treinador = app.pessoas.cadastrar_treinador(treinador)
    imprimir(resultado_treinador.para_dict())
    id_treinador = resultado_treinador.dados_gerados["id_treinador"]  # type: ignore[index]

    treino = {
        chave: valor
        for chave, valor in dados["treino"].items()
        if chave != "atletas_por_ra"
    }
    treino["id_atletica"] = id_atletica
    treino["id_treinador"] = id_treinador
    treino["atletas_inscritos"] = [
        atletas_por_ra[ra] for ra in dados["treino"]["atletas_por_ra"]
    ]
    resultado_treino = app.treinos.criar(treino)
    imprimir(resultado_treino.para_dict())
    id_treino = resultado_treino.dados_gerados["id_treino"]  # type: ignore[index]

    atualizacao = {
        chave: valor
        for chave, valor in dados["atualizacao_treino"].items()
        if chave != "atletas_por_ra"
    }
    atualizacao["id_treino"] = id_treino
    atualizacao["atletas_inscritos"] = [
        atletas_por_ra[ra] for ra in dados["atualizacao_treino"]["atletas_por_ra"]
    ]
    imprimir(app.treinos.atualizar(atualizacao).para_dict())

    campeonato = {
        chave: valor
        for chave, valor in dados["campeonato"].items()
        if chave != "atletas_por_ra"
    }
    campeonato["id_atletica"] = id_atletica
    campeonato["id_treinador_responsavel"] = id_treinador
    campeonato["atletas_convocados"] = [
        atletas_por_ra[ra] for ra in dados["campeonato"]["atletas_por_ra"]
    ]
    imprimir(app.campeonatos.criar(campeonato).para_dict())
    imprimir({"notificacoes": app.notificacoes.mensagens})


def executar_demo() -> None:
    """Executa uma demonstracao completa no terminal."""
    executar_fluxo(carregar_json(str(Path(__file__).with_name("dados_demo.json"))))


def perguntar(rotulo: str, padrao: str = "") -> str:
    """Pergunta um valor no terminal, aceitando valor padrao."""
    sufixo = f" [{padrao}]" if padrao else ""
    try:
        resposta = input(f"> {rotulo}{sufixo}: ").strip()
    except EOFError:
        painel_status("INFO", "Entrada encerrada.")
        raise SystemExit(0)
    return resposta or padrao


def perguntar_float(rotulo: str, padrao: str = "0") -> float:
    """Pergunta um numero decimal no terminal."""
    while True:
        valor = perguntar(rotulo, padrao).replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            painel_status("ERRO", "Valor invalido. Digite um numero, exemplo: 120.50")


def perguntar_inteiro(rotulo: str, padrao: str = "1", minimo: int = 1) -> int:
    """Pergunta um numero inteiro no terminal."""
    while True:
        valor = perguntar(rotulo, padrao)
        if valor.isdigit() and int(valor) >= minimo:
            return int(valor)
        painel_status(
            "ERRO",
            f"Valor invalido. Digite um numero inteiro maior ou igual a {minimo}.",
        )


def perguntar_data_iso(rotulo: str, padrao: str) -> str:
    """Pergunta uma data no formato AAAA-MM-DD."""
    while True:
        valor = perguntar(rotulo, padrao)
        try:
            date.fromisoformat(valor)
            return valor
        except ValueError:
            painel_status(
                "ERRO",
                "Data invalida. Use o formato AAAA-MM-DD, exemplo: 2004-07-07.",
            )


def perguntar_mes_ano(rotulo: str, padrao: str) -> str:
    """Pergunta uma competencia no formato AAAA-MM."""
    while True:
        valor = perguntar(rotulo, padrao)
        if re.fullmatch(r"\d{4}-\d{2}", valor):
            return valor
        painel_status("ERRO", "Valor invalido. Use o formato AAAA-MM, exemplo: 2027-01.")


def perguntar_datetime_iso(rotulo: str, padrao: str) -> str:
    """Pergunta uma data/hora no formato ISO."""
    while True:
        valor = perguntar(rotulo, padrao)
        try:
            datetime.fromisoformat(valor.replace("Z", "+00:00"))
            return valor
        except ValueError:
            painel_status(
                "ERRO",
                "Data/hora invalida. Use o formato AAAA-MM-DDTHH:MM:SSZ, "
                "exemplo: 2026-06-10T08:00:00Z.",
            )


def perguntar_lista(rotulo: str, padrao: str = "") -> list[str]:
    """Pergunta uma lista separada por virgulas."""
    valor = perguntar(rotulo, padrao)
    return [item.strip() for item in valor.split(",") if item.strip()]


def numero_inicial(valor: str, padrao: str = "1") -> str:
    """Extrai o primeiro numero de um texto, usado para periodo."""
    encontrado = re.search(r"\d+", valor or "")
    return encontrado.group(0) if encontrado else padrao


def ingresso_para_data(valor: str) -> str:
    """Converte o ingresso textual da declaracao para uma data aproximada."""
    ano = re.search(r"\b(20\d{2}|19\d{2})\b", valor or "")
    periodo = re.search(r"\d+", valor or "")
    if not ano:
        return ""

    mes = "01"
    if periodo and periodo.group(0) == "2":
        mes = "07"
    return f"{ano.group(1)}-{mes}-01"


def campo_extraido_ou_pergunta(
    rotulo: str, matricula: dict[str, str], chave: str, padrao: str = ""
) -> str:
    """Usa o valor extraido do HTML quando existir; caso contrario pergunta."""
    valor = matricula.get(chave, "")
    if valor:
        painel_status("OK", f"{rotulo}: {valor} (extraido do HTML)")
        return valor

    while True:
        valor = perguntar(rotulo, padrao)
        if valor:
            return valor
        painel_status("ERRO", f"{rotulo} e obrigatorio.")


def normalizar_cpf(cpf: str) -> str:
    """Mantem apenas os digitos do CPF."""
    return re.sub(r"\D", "", cpf)


def pessoa_com_ra(app: Aplicacao, ra: str) -> Any | None:
    """Busca atleta ou membro por RA."""
    for pessoa in [*app.banco.atletas.listar(), *app.banco.membros.listar()]:
        if pessoa.ra == ra:
            return pessoa
    return None


def pessoa_com_cpf(app: Aplicacao, cpf: str) -> Any | None:
    """Busca atleta ou membro por CPF."""
    cpf_normalizado = normalizar_cpf(cpf)
    for pessoa in [*app.banco.atletas.listar(), *app.banco.membros.listar()]:
        if normalizar_cpf(pessoa.cpf) == cpf_normalizado:
            return pessoa
    return None


def validar_ra_disponivel(app: Aplicacao, ra: str) -> bool:
    """Valida se o RA ja nao esta cadastrado na sessao."""
    existente = pessoa_com_ra(app, ra)
    if existente is None:
        return True

    painel_status(
        "AVISO",
        "RA ja cadastrado nesta sessao: "
        f"{existente.nome} ({existente.ra}). Cadastro cancelado.",
    )
    return False


def perguntar_cpf_disponivel(app: Aplicacao) -> str:
    """Pergunta CPF ate receber um valor ainda nao cadastrado."""
    while True:
        cpf = normalizar_cpf(perguntar("CPF"))
        if not cpf:
            painel_status("ERRO", "CPF e obrigatorio.")
            continue

        existente = pessoa_com_cpf(app, cpf)
        if existente is None:
            return cpf

        painel_status(
            "AVISO",
            "CPF ja cadastrado nesta sessao: "
            f"{existente.nome} ({existente.ra}). Digite outro CPF.",
        )


def periodo_extraido_ou_pergunta(matricula: dict[str, str]) -> int:
    """Usa periodo extraido do HTML ou pergunta um inteiro."""
    if matricula.get("periodo"):
        periodo = max(1, int(numero_inicial(matricula["periodo"], "1")))
        painel_status("OK", f"Periodo atual: {periodo} (extraido do HTML)")
        return periodo
    return perguntar_inteiro("Periodo atual", "1", minimo=1)


def egresso_extraido_ou_pergunta(matricula: dict[str, str]) -> str:
    """Usa ingresso extraido do HTML quando for possivel converter."""
    egresso = ingresso_para_data(matricula.get("ingresso", ""))
    if egresso:
        painel_status("OK", f"Data de ingresso: {egresso} (extraida do HTML)")
        return egresso
    return perguntar_data_iso("Data de ingresso (AAAA-MM-DD)", "2022-01-01")


def id_atletica_atual(app: Aplicacao) -> str | None:
    """Retorna a primeira atletica cadastrada na sessao."""
    atleticas = app.banco.atleticas.listar()
    if not atleticas:
        return None
    return atleticas[0].id_atletica


def garantir_atletica(app: Aplicacao) -> str:
    """Garante que exista uma atletica antes dos demais cadastros."""
    existente = id_atletica_atual(app)
    if existente:
        return existente

    painel_secao("Dados da atletica")
    painel_status("INFO", "Antes dos cadastros, informe os dados da atletica.")
    dados = {
        "nome": perguntar("Nome da atletica", "Atletica Engenharia"),
        "universidade": perguntar("Universidade", "UTFPR"),
        "campus": perguntar("Campus", "Apucarana"),
        "cnpj": perguntar("CNPJ", "00000000000100"),
    }
    resultado = app.atleticas.inicializar(dados)
    imprimir_resultado_menu(resultado.para_dict())
    return resultado.dados_gerados["id_atletica"]  # type: ignore[index]


def cadastrar_atletica_menu(app: Aplicacao) -> None:
    """Cadastra a atletica principal pela tela do menu."""
    painel_titulo("Cadastro da Atletica", "Primeiro passo para os demais cadastros")
    existente = id_atletica_atual(app)
    if existente:
        painel_status(
            "INFO",
            "Ja existe uma atletica cadastrada nesta sessao. Use os demais cadastros.",
        )
        return

    garantir_atletica(app)


def perguntar_matricula_html() -> dict[str, str]:
    """Pergunta se o usuario deseja preencher dados por HTML."""
    usar_html = perguntar("Enviar declaracao de matricula em HTML? (s/n)", "n").lower()
    if usar_html != "s":
        return {}

    while True:
        caminho = perguntar(
            "Caminho do arquivo HTML (vazio para preencher manualmente)"
        )
        if not caminho:
            painel_status("INFO", "Importacao HTML cancelada. Preenchimento manual ativado.")
            return {}

        try:
            dados = importar_declaracao_html(caminho)
            dados["arquivo_html"] = normalizar_caminho(caminho)
            painel_secao("Dados extraidos da declaracao")
            imprimir(
                {chave: valor for chave, valor in dados.items() if chave != "arquivo_html"}
            )
            return dados
        except OSError as erro:
            painel_status("ERRO", f"Nao foi possivel ler o HTML: {erro}")
            painel_status("INFO", "Confira o caminho e tente novamente.")


def cadastrar_atleta_menu(app: Aplicacao) -> None:
    """Cadastra um atleta pelo menu interativo."""
    painel_titulo("Cadastro de Atleta", "Dados pessoais podem vir da declaracao HTML")
    id_atletica = garantir_atletica(app)
    painel_secao("Declaracao de matricula")
    matricula = perguntar_matricula_html()
    painel_secao("Dados do atleta")
    nome = campo_extraido_ou_pergunta("Nome", matricula, "nome")
    ra = campo_extraido_ou_pergunta("RA", matricula, "ra")
    if not validar_ra_disponivel(app, ra):
        return
    cpf = perguntar_cpf_disponivel(app)
    curso = campo_extraido_ou_pergunta("Curso", matricula, "curso")
    documentos = (
        [{"tipo": "comprovante_matricula", "path": matricula["arquivo_html"]}]
        if matricula.get("arquivo_html")
        else []
    )

    dados = {
        "id_atletica": id_atletica,
        "atletas": [
            {
                "nome": nome,
                "ra": ra,
                "cpf": cpf,
                "curso": curso,
                "nascimento": perguntar_data_iso(
                    "Data de nascimento (AAAA-MM-DD)", "2000-01-01"
                ),
                "egresso": egresso_extraido_ou_pergunta(matricula),
                "periodo": periodo_extraido_ou_pergunta(matricula),
                "conclusao": perguntar_mes_ano("Conclusao esperada (AAAA-MM)", "2026-12"),
                "esportes": perguntar_lista("Esportes/modalidades", "Futsal Masculino"),
                "documentos": documentos,
            }
        ],
    }
    imprimir_resultado_menu(app.pessoas.cadastrar_atletas(dados).para_dict())


def cadastrar_membro_menu(app: Aplicacao) -> None:
    """Cadastra um membro da atletica pelo menu interativo."""
    painel_titulo(
        "Cadastro de Membro da Atletica",
        "Dados pessoais podem vir da declaracao HTML",
    )
    id_atletica = garantir_atletica(app)
    painel_secao("Declaracao de matricula")
    matricula = perguntar_matricula_html()
    painel_secao("Dados do membro")
    nome = campo_extraido_ou_pergunta("Nome", matricula, "nome")
    ra = campo_extraido_ou_pergunta("RA", matricula, "ra")
    if not validar_ra_disponivel(app, ra):
        return
    cpf = perguntar_cpf_disponivel(app)
    curso = campo_extraido_ou_pergunta("Curso", matricula, "curso")
    documentos_universidade = (
        [{"tipo": "comprovante_matricula", "path": matricula["arquivo_html"]}]
        if matricula.get("arquivo_html")
        else []
    )

    dados = {
        "id_atletica": id_atletica,
        "nome": nome,
        "ra": ra,
        "cpf": cpf,
        "documento_pessoal": perguntar("Documento pessoal (opcional)", ""),
        "curso": curso,
        "cargo": perguntar("Cargo", "Diretor de Esportes"),
        "tempo_atletica_inicio": perguntar_data_iso(
            "Inicio na atletica (AAAA-MM-DD)", "2024-01-01"
        ),
        "tempo_atletica_fim_esperado": perguntar_data_iso(
            "Fim esperado na atletica (AAAA-MM-DD)", "2026-12-31"
        ),
        "data_nascimento": perguntar_data_iso(
            "Data de nascimento (AAAA-MM-DD)", "2000-01-01"
        ),
        "inicio_egresso": egresso_extraido_ou_pergunta(matricula),
        "periodo_atual": periodo_extraido_ou_pergunta(matricula),
        "tempo_esperado_conclusao": perguntar_mes_ano(
            "Conclusao esperada (AAAA-MM)", "2026-12"
        ),
        "documentos_universidade": documentos_universidade,
    }
    imprimir_resultado_menu(app.pessoas.cadastrar_membro(dados).para_dict())


def cadastrar_treinador_menu(app: Aplicacao) -> None:
    """Cadastra um treinador pelo menu interativo."""
    painel_titulo("Cadastro de Treinador")
    id_atletica = garantir_atletica(app)
    painel_secao("Dados do treinador")
    dados = {
        "id_atletica": id_atletica,
        "nome": perguntar("Nome"),
        "cpf": perguntar("CPF"),
        "modalidade": perguntar("Modalidade", "Futsal Masculino"),
        "salario_por_treino": perguntar_float("Salario por treino", "120"),
        "telefone": perguntar("Telefone", ""),
    }
    imprimir_resultado_menu(app.pessoas.cadastrar_treinador(dados).para_dict())


def escolher_item(itens: list[Any], rotulo: str, campo_id: str) -> Any | None:
    """Mostra uma lista e retorna o item escolhido."""
    if not itens:
        painel_status("AVISO", f"Nenhum {rotulo} cadastrado.")
        return None

    painel_secao(f"Selecao de {rotulo}")
    for indice, item in enumerate(itens, start=1):
        nome = getattr(item, "nome", getattr(item, "modalidade", rotulo))
        identificador = getattr(item, campo_id)
        print(f"  {indice:>2}  {nome:<34} {identificador}")

    while True:
        escolha = perguntar(f"Escolha o numero do {rotulo}")
        if escolha.isdigit() and 1 <= int(escolha) <= len(itens):
            return itens[int(escolha) - 1]
        painel_status("ERRO", "Opcao invalida.")


def escolher_atletas(app: Aplicacao) -> list[str]:
    """Permite escolher varios atletas cadastrados."""
    atletas = app.banco.atletas.listar()
    if not atletas:
        painel_status("AVISO", "Nenhum atleta cadastrado.")
        return []

    painel_secao("Selecao de atletas")
    for indice, atleta in enumerate(atletas, start=1):
        print(f"  {indice:>2}  {atleta.nome:<34} RA {atleta.ra}")

    escolha = perguntar("Escolha os atletas por numero, separados por virgula")
    ids: list[str] = []
    for parte in escolha.split(","):
        parte = parte.strip()
        if parte.isdigit() and 1 <= int(parte) <= len(atletas):
            ids.append(atletas[int(parte) - 1].id_atleta)
    return ids


def cadastrar_treino_menu(app: Aplicacao) -> None:
    """Cadastra um treino pelo menu interativo."""
    painel_titulo("Cadastro de Treino")
    id_atletica = garantir_atletica(app)
    treinador = escolher_item(app.banco.treinadores.listar(), "treinador", "id_treinador")
    if treinador is None:
        return

    atletas = escolher_atletas(app)
    if not atletas:
        return

    painel_secao("Dados do treino")
    dados = {
        "id_atletica": id_atletica,
        "modalidade": perguntar("Modalidade", treinador.modalidade),
        "id_treinador": treinador.id_treinador,
        "localidade": perguntar("Localidade", "Ginasio Principal"),
        "dia_semana": perguntar("Dia da semana", "TERCA_FEIRA"),
        "horario_inicio": perguntar("Horario de inicio", "19:00"),
        "horario_fim": perguntar("Horario de fim", "21:00"),
        "atletas_inscritos": atletas,
    }
    imprimir_resultado_menu(app.treinos.criar(dados).para_dict())


def cadastrar_campeonato_menu(app: Aplicacao) -> None:
    """Cadastra um campeonato pelo menu interativo."""
    painel_titulo("Cadastro de Campeonato")
    id_atletica = garantir_atletica(app)
    treinador = escolher_item(app.banco.treinadores.listar(), "treinador", "id_treinador")
    if treinador is None:
        return

    atletas = escolher_atletas(app)
    if not atletas:
        return

    painel_secao("Dados do campeonato")
    dados = {
        "id_atletica": id_atletica,
        "nome_campeonato": perguntar("Nome do campeonato", "Jogos Universitarios"),
        "modalidades": perguntar_lista("Modalidades", treinador.modalidade),
        "id_treinador_responsavel": treinador.id_treinador,
        "atletas_convocados": atletas,
        "transporte": {
            "tipo": perguntar("Tipo de transporte", "Onibus Fretado"),
            "data_saida": perguntar_datetime_iso(
                "Data/hora de saida", "2026-06-10T08:00:00Z"
            ),
            "data_retorno": perguntar_datetime_iso(
                "Data/hora de retorno", "2026-06-15T22:00:00Z"
            ),
        },
        "datas": {
            "inicio": perguntar_data_iso("Data de inicio (AAAA-MM-DD)", "2026-06-10"),
            "fim": perguntar_data_iso("Data de fim (AAAA-MM-DD)", "2026-06-15"),
        },
        "locais": perguntar_lista("Locais", "Ginasio Municipal"),
    }
    imprimir_resultado_menu(app.campeonatos.criar(dados).para_dict())


def atualizar_treino_menu(app: Aplicacao) -> None:
    """Atualiza um treino ja cadastrado pelo menu interativo."""
    painel_titulo("Atualizacao de Treino")
    treino = escolher_item(app.banco.treinos.listar(), "treino", "id_treino")
    if treino is None:
        return

    painel_status("INFO", "Escolha novamente os atletas do treino.")
    atletas = escolher_atletas(app)
    if not atletas:
        atletas = treino.atletas_inscritos

    painel_secao("Novos dados do treino")
    dados = {
        "id_treino": treino.id_treino,
        "localidade": perguntar("Localidade", treino.localidade),
        "horario_inicio": perguntar("Horario de inicio", treino.horario_inicio),
        "horario_fim": perguntar("Horario de fim", treino.horario_fim),
        "atletas_inscritos": atletas,
        "status_treino": perguntar("Status do treino", treino.status_treino),
    }
    imprimir_resultado_menu(app.treinos.atualizar(dados).para_dict())


def importar_html_menu() -> None:
    """Executa a importacao de HTML pelo menu."""
    painel_titulo("Importar Declaracao HTML")
    caminho = perguntar("Caminho do arquivo HTML")
    if caminho:
        imprimir_resultado_menu(
            {
                "exit_code": 0,
                "status": "SUCESSO",
                "comando": "importar-declaracao-html",
                "dados_extraidos": importar_declaracao_html(caminho),
            }
        )


def listar_cadastros_menu(app: Aplicacao) -> None:
    """Mostra um resumo dos cadastros da sessao."""
    painel_titulo("Cadastros da Sessao", resumo_sessao(app))
    imprimir_resultado_menu(
        {
            "atleticas": app.banco.atleticas.como_dicts(),
            "atletas": app.banco.atletas.como_dicts(),
            "membros": app.banco.membros.como_dicts(),
            "treinadores": app.banco.treinadores.como_dicts(),
            "treinos": app.banco.treinos.como_dicts(),
            "campeonatos": app.banco.campeonatos.como_dicts(),
            "notificacoes": app.notificacoes.mensagens,
        }
    )


def executar_menu(app: Aplicacao) -> None:
    """Executa o menu interativo do terminal."""
    while True:
        painel_titulo("Sistema de Gerenciamento de Atletica", resumo_sessao(app))
        painel_secao("Cadastros")
        painel_opcao("1", "Cadastrar atletica", "entidade base")
        painel_opcao("2", "Cadastrar atleta", "com HTML opcional")
        painel_opcao("3", "Cadastrar membro da atletica", "com HTML opcional")
        painel_opcao("4", "Cadastrar treinador")
        painel_secao("Operacoes esportivas")
        painel_opcao("5", "Cadastrar treino")
        painel_opcao("6", "Cadastrar campeonato")
        painel_opcao("7", "Atualizar treino")
        painel_secao("Consulta e importacao")
        painel_opcao("8", "Importar declaracao de matricula HTML")
        painel_opcao("9", "Listar cadastros da sessao")
        painel_opcao("0", "Sair")

        opcao = perguntar("Escolha uma opcao")
        if opcao == "1":
            cadastrar_atletica_menu(app)
        elif opcao == "2":
            cadastrar_atleta_menu(app)
        elif opcao == "3":
            cadastrar_membro_menu(app)
        elif opcao == "4":
            cadastrar_treinador_menu(app)
        elif opcao == "5":
            cadastrar_treino_menu(app)
        elif opcao == "6":
            cadastrar_campeonato_menu(app)
        elif opcao == "7":
            atualizar_treino_menu(app)
        elif opcao == "8":
            importar_html_menu()
        elif opcao == "9":
            listar_cadastros_menu(app)
        elif opcao == "0":
            painel_status("INFO", "Encerrando menu.")
            break
        else:
            painel_status("ERRO", "Opcao invalida.")


def main() -> None:
    """Ponto de entrada da CLI."""
    parser = argparse.ArgumentParser(
        description="Sistema de Gerenciamento de Atletica - Sprint 3"
    )
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("demo", help="Executa uma demonstracao completa")
    sub.add_parser("menu", help="Abre o menu interativo no terminal")

    fluxo = sub.add_parser("executar-fluxo", help="Executa fluxo por JSON")
    fluxo.add_argument("--input", required=True, help="Arquivo JSON de entrada")

    html = sub.add_parser(
        "importar-declaracao-html", help="Extrai dados de aluno de um HTML"
    )
    html.add_argument("--input", required=True, help="Arquivo HTML de entrada")
    html.add_argument(
        "--encoding",
        default="auto",
        help="Encoding do arquivo HTML; use auto para detectar pelo charset",
    )

    cadastrar = sub.add_parser("inicializar-atletica")
    cadastrar.add_argument("--input", required=True, help="Arquivo JSON de entrada")

    args = parser.parse_args()
    app = Aplicacao()

    if args.comando == "demo":
        executar_demo()
    elif args.comando == "menu":
        executar_menu(app)
    elif args.comando == "executar-fluxo":
        executar_fluxo(carregar_json(args.input))
    elif args.comando == "importar-declaracao-html":
        imprimir(
            {
                "exit_code": 0,
                "status": "SUCESSO",
                "comando": "importar-declaracao-html",
                "dados_extraidos": importar_declaracao_html(args.input, args.encoding),
            }
        )
    elif args.comando == "inicializar-atletica":
        imprimir(app.atleticas.inicializar(carregar_json(args.input)).para_dict())


if __name__ == "__main__":
    main()
