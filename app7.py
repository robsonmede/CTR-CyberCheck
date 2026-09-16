import csv
import html
import io
import re
from datetime import datetime

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="CTR CyberCheck",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
:root {
    --ctr-primary: #047f9e;
    --ctr-secondary: #11a88f;
    --ctr-dark: #06141d;
    --ctr-text: #102f3b;
    --ctr-muted: #536b75;
    --ctr-border: #cbd4d8;
    --ctr-bg: #e5e9eb;
}

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.stApp {
    background: var(--ctr-bg) !important;
    color: var(--ctr-text) !important;
}

html,
body,
.stApp,
.stApp p,
.stApp label,
.stApp li,
.stApp button,
.stApp input,
.stApp textarea,
.stApp select {
    font-family: Inter, Arial, Helvetica, sans-serif;
}

[data-testid="stAppViewContainer"] h1,
[data-testid="stAppViewContainer"] h2,
[data-testid="stAppViewContainer"] h3,
[data-testid="stAppViewContainer"] h4 {
    color: var(--ctr-text) !important;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu,
footer {
    visibility: hidden;
}

/* Ícones nativos do Streamlit */
.material-symbols-rounded,
.material-symbols-outlined,
[data-testid="stIconMaterial"] {
    font-family:
        "Material Symbols Rounded",
        "Material Symbols Outlined" !important;
    font-weight: normal !important;
    line-height: 1 !important;
    letter-spacing: normal !important;
    text-transform: none !important;
    white-space: nowrap !important;
    direction: ltr !important;
    font-feature-settings: "liga" !important;
}

/* Cabeçalho */
.ctr-hero {
    padding: 36px 40px;
    margin-bottom: 22px;
    color: white !important;
    border: 1px solid rgba(0, 212, 255, 0.3);
    border-radius: 24px;
    background:
        radial-gradient(
            circle at 90% 15%,
            rgba(0, 212, 255, 0.28),
            transparent 34%
        ),
        linear-gradient(135deg, #06141d, #0b2633 55%, #124253);
    box-shadow: 0 24px 55px rgba(6, 32, 43, 0.22);
}

.ctr-hero h1 {
    margin: 0 0 10px 0;
    color: white !important;
    font-size: 3rem;
    font-weight: 800;
}

.ctr-hero h1 span {
    color: #64e5ff !important;
}

.ctr-hero p {
    margin: 0;
    color: #e4f2f5 !important;
    font-size: 1.08rem;
    line-height: 1.7;
}

/* Avisos */
.ctr-session-notice,
.ctr-privacy-notice {
    padding: 19px 21px;
    margin-bottom: 17px;
    border-radius: 15px;
    line-height: 1.6;
}

.ctr-session-notice {
    color: #3f350d !important;
    border: 1px solid #dfbd4d;
    border-left: 6px solid #d9a514;
    background: #fff8dc !important;
}

.ctr-privacy-notice {
    color: #164d44 !important;
    border: 1px solid #91cfc2;
    border-left: 6px solid #11a88f;
    background: #eaf9f5 !important;
}

.ctr-session-notice strong,
.ctr-session-notice p,
.ctr-privacy-notice strong,
.ctr-privacy-notice p {
    color: inherit !important;
}

/* Painéis */
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    color: var(--ctr-text) !important;
    border-color: var(--ctr-border) !important;
    border-radius: 17px !important;
    background: white !important;
    box-shadow: 0 8px 24px rgba(17, 56, 70, 0.1);
}

/* Campos */
[data-testid="stTextInput"] label,
[data-testid="stTextInput"] label p,
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p,
[data-testid="stTextArea"] label,
[data-testid="stTextArea"] label p,
[data-testid="stCheckbox"] label p,
[data-testid="stRadio"] > label,
[data-testid="stRadio"] > label p {
    color: var(--ctr-text) !important;
    font-weight: 700 !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
    color: var(--ctr-text) !important;
    background: white !important;
    border-color: var(--ctr-border) !important;
    -webkit-text-fill-color: var(--ctr-text) !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    color: var(--ctr-text) !important;
    background: white !important;
    border-color: var(--ctr-border) !important;
}

[data-testid="stSelectbox"] span {
    color: var(--ctr-text) !important;
}

/* Dimensões */
.dimension-header {
    display: flex;
    align-items: center;
    gap: 13px;
    padding: 18px 20px;
    margin-top: 30px;
    margin-bottom: 15px;
    color: white !important;
    border-radius: 15px;
    background: linear-gradient(100deg, #0b2633, #145066);
}

.dimension-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    flex-shrink: 0;
    color: #06202b !important;
    font-weight: 800;
    border-radius: 10px;
    background: linear-gradient(135deg, #62e3fb, #76eecb);
}

.dimension-title {
    color: white !important;
    font-size: 1.2rem;
    font-weight: 800;
}

.dimension-description {
    margin-top: 3px;
    color: #d8edf2 !important;
    font-size: 0.87rem;
}

/* Perguntas */
.question-card {
    min-height: 175px;
    padding: 18px;
    margin-bottom: 16px;
    border: 1px solid var(--ctr-border);
    border-radius: 15px;
    background: white;
    box-shadow: 0 6px 18px rgba(17, 57, 71, 0.08);
}

.question-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 38px;
    height: 38px;
    margin-right: 9px;
    color: white !important;
    font-weight: 800;
    border-radius: 10px;
    background: linear-gradient(135deg, #047f9e, #11a88f);
}

.question-text {
    color: var(--ctr-text) !important;
    font-size: 1rem;
    font-weight: 750;
    line-height: 1.45;
}

.nist-badge {
    display: inline-block;
    padding: 4px 8px;
    margin-top: 8px;
    color: #075d73 !important;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    border: 1px solid #b8dfe8;
    border-radius: 7px;
    background: #dff3f7;
}

/* Radio */
div[data-testid="stRadio"] [role="radiogroup"] {
    display: flex;
    flex-wrap: wrap;
    gap: 7px;
}

div[data-testid="stRadio"] [role="radiogroup"] label {
    min-width: 45px;
    padding: 8px 11px;
    color: var(--ctr-text) !important;
    border: 1px solid #bcd5de !important;
    border-radius: 10px;
    background: white !important;
}

div[data-testid="stRadio"] [role="radiogroup"] label p,
div[data-testid="stRadio"] [role="radiogroup"] label span {
    color: #173d4a !important;
    font-weight: 700 !important;
}

/* Botões */
div[data-testid="stButton"] button,
div[data-testid="stDownloadButton"] button {
    min-height: 52px;
    color: white !important;
    font-weight: 800;
    border: 0 !important;
    border-radius: 13px;
    background: linear-gradient(100deg, #047f9e, #11a88f) !important;
}

div[data-testid="stButton"] button p,
div[data-testid="stDownloadButton"] button p {
    color: white !important;
}

/* Resultado */
.result-card {
    padding: 28px;
    margin-top: 22px;
    color: white !important;
    border-radius: 20px;
    background: linear-gradient(135deg, #06141d, #124253);
    box-shadow: 0 20px 45px rgba(6, 32, 43, 0.22);
}

.result-card h2,
.result-card h3,
.result-card p,
.result-card strong {
    color: white !important;
}

.result-score {
    color: #64e5ff !important;
    font-size: 3rem;
    font-weight: 900;
}

/* Visão C-Level */
.exec-card {
    padding: 26px 28px;
    margin-top: 22px;
    color: var(--ctr-text) !important;
    border: 1px solid var(--ctr-border);
    border-top: 6px solid #b42318;
    border-radius: 18px;
    background: white !important;
    box-shadow: 0 12px 30px rgba(17, 57, 71, 0.1);
}

.exec-card h3 {
    margin: 0 0 6px 0;
    color: var(--ctr-text) !important;
    font-size: 1.3rem;
    font-weight: 800;
}

.exec-subtitle {
    margin: 0 0 16px 0;
    color: var(--ctr-muted) !important;
    font-size: 0.92rem;
}

.exec-summary {
    padding: 16px 18px;
    margin: 14px 0;
    color: var(--ctr-text) !important;
    font-size: 1.02rem;
    line-height: 1.7;
    border-left: 5px solid #047f9e;
    border-radius: 10px;
    background: #f3f7f9 !important;
}

.exec-summary strong {
    color: #063744 !important;
}

.exec-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(205px, 1fr));
    gap: 12px;
    margin: 16px 0;
}

.exec-kpi {
    padding: 16px;
    border: 1px solid var(--ctr-border);
    border-radius: 13px;
    background: #fafbfc !important;
}

.exec-kpi-label {
    display: block;
    margin-bottom: 6px;
    color: var(--ctr-muted) !important;
    font-size: 0.76rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.04rem;
}

.exec-kpi-value {
    display: block;
    color: #063744 !important;
    font-size: 1.38rem;
    font-weight: 900;
    line-height: 1.2;
}

.exec-kpi-note {
    display: block;
    margin-top: 4px;
    color: var(--ctr-muted) !important;
    font-size: 0.8rem;
}

.exec-row {
    display: grid;
    grid-template-columns: 150px 120px 1fr;
    gap: 14px;
    align-items: start;
    padding: 13px 14px;
    margin: 8px 0;
    border: 1px solid var(--ctr-border);
    border-radius: 12px;
    background: white !important;
}

.exec-row-dim {
    color: var(--ctr-text) !important;
    font-weight: 800;
}

.exec-row-dim small {
    display: block;
    color: var(--ctr-muted) !important;
    font-weight: 600;
}

.exec-pill {
    display: inline-block;
    padding: 5px 10px;
    color: white !important;
    font-size: 0.76rem;
    font-weight: 800;
    text-transform: uppercase;
    border-radius: 8px;
}

.exec-row-text strong {
    display: block;
    margin-bottom: 3px;
    color: #063744 !important;
}

.exec-row-text span {
    color: var(--ctr-muted) !important;
    font-size: 0.9rem;
    line-height: 1.5;
}

.exec-disclaimer {
    margin-top: 14px;
    color: var(--ctr-muted) !important;
    font-size: 0.8rem;
    line-height: 1.5;
}

@media (max-width: 700px) {
    .ctr-hero h1 {
        font-size: 2.2rem;
    }

    .exec-row {
        grid-template-columns: 1fr;
        gap: 7px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DADOS DO ASSESSMENT
# ============================================================

DIMENSOES = [
    {
        "nome": "Governar",
        "codigo": "GV",
        "descricao": "Estratégia, políticas, responsabilidades, riscos e supervisão executiva.",
        "perguntas": [
            "A organização possui uma estratégia formal de segurança da informação?",
            "As responsabilidades de segurança estão definidas para as áreas críticas?",
            "Os riscos cibernéticos são apresentados periodicamente à alta administração?",
            "Existem políticas formais aprovadas e revisadas?",
        ],
    },
    {
        "nome": "Identificar",
        "codigo": "ID",
        "descricao": "Inventário, contexto de negócio, riscos, ativos e dependências.",
        "perguntas": [
            "Existe inventário atualizado de ativos tecnológicos e dados?",
            "Os processos críticos e suas dependências estão documentados?",
            "Os riscos cibernéticos são avaliados de forma estruturada?",
            "A organização conhece seus fornecedores críticos e terceiros?",
        ],
    },
    {
        "nome": "Proteger",
        "codigo": "PR",
        "descricao": "Controles preventivos, identidade, proteção de dados e treinamento.",
        "perguntas": [
            "A autenticação multifator está implementada para acessos críticos?",
            "Existem controles de privilégio mínimo e revisão de acessos?",
            "Os dados sensíveis possuem controles de proteção adequados?",
            "Os colaboradores recebem treinamento periódico de segurança?",
        ],
    },
    {
        "nome": "Detectar",
        "codigo": "DE",
        "descricao": "Monitoramento, eventos, detecção e análise de anomalias.",
        "perguntas": [
            "Os eventos de segurança são coletados e monitorados?",
            "Existem alertas para comportamentos anômalos?",
            "Os logs críticos são protegidos contra alteração?",
            "A organização mede o tempo de detecção de incidentes?",
        ],
    },
    {
        "nome": "Responder",
        "codigo": "RS",
        "descricao": "Gestão de incidentes, comunicação, contenção e análise.",
        "perguntas": [
            "Existe um plano formal de resposta a incidentes?",
            "O plano de resposta é testado periodicamente?",
            "Estão definidos responsáveis e canais de comunicação de crise?",
            "Há procedimentos para comunicação com clientes e autoridades?",
        ],
    },
    {
        "nome": "Recuperar",
        "codigo": "RC",
        "descricao": "Continuidade, recuperação, restauração e melhoria pós-incidente.",
        "perguntas": [
            "Existem backups protegidos e testados regularmente?",
            "A organização possui objetivos de RTO e RPO definidos?",
            "Os processos de recuperação foram simulados?",
            "As lições aprendidas são incorporadas aos controles?",
        ],
    },
]

OPCOES = {
    0: "Não implementado",
    1: "Inicial",
    2: "Parcial",
    3: "Definido",
    4: "Gerenciado",
    5: "Otimizado",
}

FAIXAS_FATURAMENTO = {
    "Não informar": None,
    "Até R$ 4,8 milhões": 4_800_000,
    "R$ 4,8 mi a R$ 30 milhões": 17_000_000,
    "R$ 30 mi a R$ 100 milhões": 65_000_000,
    "R$ 100 mi a R$ 500 milhões": 300_000_000,
    "Acima de R$ 500 milhões": 750_000_000,
}


# ============================================================
# MODELO DE RISCO FINANCEIRO
# ============================================================

CUSTO_MEDIO_INCIDENTE_REFERENCIA = 6_500_000

PROBABILIDADE_POR_NIVEL = {
    "Crítico": 0.65,
    "Baixo": 0.45,
    "Intermediário": 0.28,
    "Avançado": 0.15,
    "Otimizado": 0.08,
}

EXPOSICAO_FATURAMENTO_POR_NIVEL = {
    "Crítico": 0.08,
    "Baixo": 0.05,
    "Intermediário": 0.03,
    "Avançado": 0.015,
    "Otimizado": 0.007,
}

IMPACTO_NEGOCIO_DIMENSAO = {
    "Governar": {
        "risco": "Responsabilidade legal e regulatória",
        "consequencia": (
            "Políticas frágeis e baixa supervisão podem aumentar a exposição "
            "a sanções, disputas contratuais e responsabilização executiva."
        ),
        "indicador": "Exposição regulatória",
    },
    "Identificar": {
        "risco": "Ativos e fragilidades desconhecidos",
        "consequencia": (
            "O que não é inventariado não pode ser adequadamente protegido, "
            "priorizado, segurado ou incluído no orçamento."
        ),
        "indicador": "Eficiência do investimento",
    },
    "Proteger": {
        "risco": "Ransomware e paralisação operacional",
        "consequencia": (
            "Controles preventivos insuficientes podem provocar indisponibilidade, "
            "perda de receita e custos de reconstrução."
        ),
        "indicador": "Continuidade da receita",
    },
    "Detectar": {
        "risco": "Tempo prolongado de permanência do atacante",
        "consequencia": (
            "A descoberta tardia pode ampliar o volume de dados comprometidos, "
            "o custo de resposta e o dano reputacional."
        ),
        "indicador": "Custo por incidente",
    },
    "Responder": {
        "risco": "Gestão de crise improvisada",
        "consequencia": (
            "A ausência de papéis e procedimentos pode atrasar decisões, "
            "comunicações e contenção do incidente."
        ),
        "indicador": "Dano reputacional",
    },
    "Recuperar": {
        "risco": "Perda de dados e operações",
        "consequencia": (
            "Backups não testados e planos não exercitados podem prolongar "
            "a indisponibilidade e consumir caixa operacional."
        ),
        "indicador": "Tempo de retomada",
    },
}


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def renderizar_html(conteudo):
    """
    Remove linhas vazias e indentação para evitar que o Markdown
    do Streamlit interprete o HTML como bloco de código.
    """
    linhas = [
        linha.strip()
        for linha in conteudo.strip().splitlines()
        if linha.strip()
    ]
    st.markdown("".join(linhas), unsafe_allow_html=True)


def obter_nivel(percentual):
    if percentual < 20:
        return "Crítico"
    if percentual < 40:
        return "Baixo"
    if percentual < 60:
        return "Intermediário"
    if percentual < 80:
        return "Avançado"
    return "Otimizado"


def obter_prioridade(percentual):
    if percentual < 40:
        return "Alta"
    if percentual < 60:
        return "Média"
    return "Baixa"


def formatar_moeda(valor):
    if valor is None:
        return "Não estimado"

    if valor >= 1_000_000:
        texto = f"R$ {valor / 1_000_000:,.1f} milhões"
        return texto.replace(",", "X").replace(".", ",").replace("X", ".")

    if valor >= 1_000:
        texto = f"R$ {valor / 1_000:,.0f} mil"
        return texto.replace(",", ".")

    return f"R$ {valor:,.0f}".replace(",", ".")


def classificar_exposicao(percentual):
    if percentual < 40:
        return "Crítica", "#b42318"
    if percentual < 60:
        return "Alta", "#d9a514"
    if percentual < 80:
        return "Moderada", "#047f9e"
    return "Controlada", "#11a88f"


def calcular_risco_financeiro(
    maturidade_geral,
    resultados_dimensoes,
    faixa_faturamento,
):
    nivel_geral = obter_nivel(maturidade_geral)

    probabilidade = PROBABILIDADE_POR_NIVEL.get(
        nivel_geral,
        0.30,
    )

    faturamento = FAIXAS_FATURAMENTO.get(faixa_faturamento)

    if faturamento:
        exposicao_pct = EXPOSICAO_FATURAMENTO_POR_NIVEL.get(
            nivel_geral,
            0.03,
        )

        custo_incidente = max(
            faturamento * exposicao_pct,
            CUSTO_MEDIO_INCIDENTE_REFERENCIA * 0.3,
        )

        custo_incidente = min(
            custo_incidente,
            CUSTO_MEDIO_INCIDENTE_REFERENCIA * 3,
        )
    else:
        custo_incidente = CUSTO_MEDIO_INCIDENTE_REFERENCIA

    perda_esperada_anual = probabilidade * custo_incidente

    # Referência indicativa. A aplicação não substitui análise jurídica.
    multa_lgpd = (
        min(faturamento * 0.02, 50_000_000)
        if faturamento
        else None
    )

    niveis = list(PROBABILIDADE_POR_NIVEL.keys())

    indice = (
        niveis.index(nivel_geral)
        if nivel_geral in niveis
        else 1
    )

    proximo_nivel = niveis[
        min(indice + 1, len(niveis) - 1)
    ]

    perda_proximo_nivel = (
        PROBABILIDADE_POR_NIVEL[proximo_nivel]
        * custo_incidente
    )

    economia_potencial = max(
        perda_esperada_anual - perda_proximo_nivel,
        0,
    )

    dimensoes_financeiras = []

    for item in resultados_dimensoes:
        exposicao, cor = classificar_exposicao(
            item["percentual"]
        )

        info = IMPACTO_NEGOCIO_DIMENSAO.get(
            item["nome"],
            {},
        )

        dimensoes_financeiras.append(
            {
                "dimensao": item["nome"],
                "percentual": item["percentual"],
                "exposicao": exposicao,
                "cor": cor,
                "risco": info.get("risco", ""),
                "consequencia": info.get("consequencia", ""),
                "indicador": info.get("indicador", ""),
            }
        )

    dimensoes_financeiras.sort(
        key=lambda item: item["percentual"]
    )

    exposicao_geral, cor_geral = classificar_exposicao(
        maturidade_geral
    )

    return {
        "nivel_geral": nivel_geral,
        "exposicao_geral": exposicao_geral,
        "cor_geral": cor_geral,
        "probabilidade_12m": probabilidade,
        "custo_incidente": custo_incidente,
        "perda_esperada_anual": perda_esperada_anual,
        "multa_lgpd": multa_lgpd,
        "proximo_nivel": proximo_nivel,
        "economia_potencial": economia_potencial,
        "faturamento_informado": faturamento is not None,
        "dimensoes": dimensoes_financeiras,
    }


def mensagem_executiva(risco):
    probabilidade = int(
        risco["probabilidade_12m"] * 100
    )

    texto = (
        "A organização apresenta exposição cibernética "
        f"<strong>{risco['exposicao_geral'].lower()}</strong>. "
        f"Com base na maturidade observada, estima-se uma probabilidade "
        f"orientativa de aproximadamente <strong>{probabilidade}%</strong> "
        "de ocorrência de um incidente relevante nos próximos 12 meses. "
        f"O custo potencial por evento é estimado em "
        f"<strong>{formatar_moeda(risco['custo_incidente'])}</strong>, "
        "considerando indisponibilidade, resposta, recuperação, impacto "
        "regulatório e reputacional. "
        f"A perda esperada anual é de aproximadamente "
        f"<strong>{formatar_moeda(risco['perda_esperada_anual'])}</strong>. "
        f"A evolução para o nível <strong>{risco['proximo_nivel']}</strong> "
        f"poderia reduzir a perda esperada em aproximadamente "
        f"<strong>{formatar_moeda(risco['economia_potencial'])}</strong> "
        "por ano, segundo os parâmetros utilizados."
    )

    if risco["multa_lgpd"]:
        texto += (
            " A exposição regulatória foi apresentada como referência "
            "indicativa e deve ser validada pela assessoria jurídica."
        )

    return texto


def texto_seguro(texto):
    return html.escape(str(texto))


def nome_arquivo_seguro(nome):
    nome = re.sub(r"[^a-zA-Z0-9_-]+", "_", nome)
    return nome.strip("_") or "relatorio_ctr_cybercheck"


def limpar_sessao():
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]


def criar_grafico_dimensoes(resultados):
    fig, ax = plt.subplots(figsize=(10, 5))

    nomes = [item["nome"] for item in resultados]
    valores = [item["percentual"] for item in resultados]

    cores = [
        "#b42318" if valor < 40
        else "#d9a514" if valor < 60
        else "#047f9e" if valor < 80
        else "#11a88f"
        for valor in valores
    ]

    ax.bar(nomes, valores, color=cores)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Maturidade (%)")
    ax.set_title("Maturidade por dimensão NIST CSF")
    ax.grid(axis="y", alpha=0.25)

    for indice, valor in enumerate(valores):
        ax.text(
            indice,
            valor + 2,
            f"{valor:.0f}%",
            ha="center",
            fontweight="bold",
        )

    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()

    return fig


def figura_para_png(fig):
    buffer = io.BytesIO()
    fig.savefig(
        buffer,
        format="png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(fig)
    buffer.seek(0)
    return buffer


# ============================================================
# EXPORTAÇÃO CSV
# ============================================================

def montar_csv_completo(
    organizacao,
    responsavel,
    faixa_faturamento,
    maturidade_geral,
    resultados_dimensoes,
    respostas,
    risco,
):
    buffer = io.StringIO()
    escritor = csv.writer(buffer)

    escritor.writerow(["CTR CyberCheck"])
    escritor.writerow(
        [
            "Relatório de Assessment de Cibersegurança",
            datetime.now().strftime("%d/%m/%Y %H:%M"),
        ]
    )
    escritor.writerow([])

    escritor.writerow(["DADOS DA ORGANIZAÇÃO"])
    escritor.writerow(["Organização", organizacao])
    escritor.writerow(["Responsável", responsavel])
    escritor.writerow(["Faixa de faturamento", faixa_faturamento])
    escritor.writerow([])

    escritor.writerow(["RESUMO DE MATURIDADE"])
    escritor.writerow(
        [
            "Maturidade geral",
            f"{maturidade_geral:.1f}%",
        ]
    )
    escritor.writerow(
        [
            "Nível geral",
            risco["nivel_geral"],
        ]
    )
    escritor.writerow([])

    escritor.writerow(["VISÃO EXECUTIVA - RISCO FINANCEIRO"])
    escritor.writerow(["Indicador", "Valor"])
    escritor.writerow(
        [
            "Exposição geral",
            risco["exposicao_geral"],
        ]
    )
    escritor.writerow(
        [
            "Probabilidade de incidente em 12 meses",
            f"{risco['probabilidade_12m'] * 100:.0f}%",
        ]
    )
    escritor.writerow(
        [
            "Custo estimado por incidente grave",
            formatar_moeda(risco["custo_incidente"]),
        ]
    )
    escritor.writerow(
        [
            "Perda esperada anual",
            formatar_moeda(risco["perda_esperada_anual"]),
        ]
    )
    escritor.writerow(
        [
            "Referência regulatória LGPD",
            formatar_moeda(risco["multa_lgpd"]),
        ]
    )
    escritor.writerow(
        [
            "Economia potencial ao evoluir um nível",
            formatar_moeda(risco["economia_potencial"]),
        ]
    )
    escritor.writerow([])

    escritor.writerow(
        [
            "DIMENSÕES E IMPACTO DE NEGÓCIO"
        ]
    )
    escritor.writerow(
        [
            "Dimensão",
            "Maturidade (%)",
            "Exposição",
            "Risco de negócio",
            "Indicador executivo",
            "Consequência",
        ]
    )

    for item in risco["dimensoes"]:
        escritor.writerow(
            [
                item["dimensao"],
                f"{item['percentual']:.1f}",
                item["exposicao"],
                item["risco"],
                item["indicador"],
                item["consequencia"],
            ]
        )

    escritor.writerow([])
    escritor.writerow(["DETALHAMENTO DAS RESPOSTAS"])
    escritor.writerow(
        [
            "Dimensão",
            "Código",
            "Pergunta",
            "Resposta",
            "Pontuação",
        ]
    )

    for resposta in respostas:
        escritor.writerow(
            [
                resposta["dimensao"],
                resposta["codigo"],
                resposta["pergunta"],
                resposta["resposta"],
                resposta["pontuacao"],
            ]
        )

    return buffer.getvalue().encode("utf-8-sig")


# ============================================================
# EXPORTAÇÃO PDF
# ============================================================

def montar_pdf(
    organizacao,
    responsavel,
    faixa_faturamento,
    maturidade_geral,
    resultados_dimensoes,
    risco,
    grafico_png,
):
    buffer = io.BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.3 * cm,
        leftMargin=1.3 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloCTR",
        parent=estilos["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#102f3b"),
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    estilo_secao = ParagraphStyle(
        "SecaoCTR",
        parent=estilos["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#047f9e"),
        spaceBefore=10,
        spaceAfter=8,
    )

    estilo_normal = ParagraphStyle(
        "NormalCTR",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#102f3b"),
    )

    estilo_pequeno = ParagraphStyle(
        "PequenoCTR",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#536b75"),
    )

    elementos = []

    elementos.append(
        Paragraph(
            "CTR CyberCheck",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Relatório Executivo de Maturidade e Risco Financeiro",
            estilo_secao,
        )
    )

    dados_organizacao = [
        ["Organização", organizacao or "Não informada"],
        ["Responsável", responsavel or "Não informado"],
        ["Data", datetime.now().strftime("%d/%m/%Y %H:%M")],
        ["Faixa de faturamento", faixa_faturamento],
        ["Maturidade geral", f"{maturidade_geral:.1f}%"],
        ["Nível geral", risco["nivel_geral"]],
    ]

    tabela_dados = Table(
        dados_organizacao,
        colWidths=[5 * cm, 9 * cm],
    )

    tabela_dados.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#eaf3f5"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#102f3b"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#cbd4d8"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elementos.append(tabela_dados)
    elementos.append(Spacer(1, 0.35 * cm))

    # Sumário C-Level
    elementos.append(
        Paragraph(
            "Sumário Executivo — Risco Financeiro",
            estilo_secao,
        )
    )

    texto_exec = re.sub(
        r"</?strong>",
        "",
        mensagem_executiva(risco),
    )

    elementos.append(
        Paragraph(
            texto_exec,
            estilo_normal,
        )
    )

    elementos.append(Spacer(1, 0.25 * cm))

    tabela_kpis = [
        [
            "Indicador",
            "Valor",
            "Leitura para a diretoria",
        ],
        [
            "Exposição atual",
            risco["exposicao_geral"],
            f"Maturidade {risco['nivel_geral']}",
        ],
        [
            "Probabilidade em 12 meses",
            f"{risco['probabilidade_12m'] * 100:.0f}%",
            "Chance orientativa de evento relevante",
        ],
        [
            "Custo por incidente grave",
            formatar_moeda(risco["custo_incidente"]),
            "Resposta, parada, recuperação e reputação",
        ],
        [
            "Perda esperada anual",
            formatar_moeda(risco["perda_esperada_anual"]),
            "Referência para orçamento de segurança",
        ],
        [
            "Economia ao evoluir um nível",
            formatar_moeda(risco["economia_potencial"]),
            f"Meta: nível {risco['proximo_nivel']}",
        ],
    ]

    tabela_kpis_pdf = Table(
        tabela_kpis,
        colWidths=[6 * cm, 5 * cm, 13 * cm],
    )

    tabela_kpis_pdf.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0b2633"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#cbd4d8"),
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#f7fafb"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#102f3b"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elementos.append(tabela_kpis_pdf)
    elementos.append(Spacer(1, 0.25 * cm))

    elementos.append(
        Paragraph(
            "Observação: os valores são estimativas orientativas baseadas "
            "na maturidade informada e em parâmetros de referência. "
            "Não constituem previsão financeira, avaliação atuarial, "
            "cotação de seguro ou parecer jurídico.",
            estilo_pequeno,
        )
    )

    elementos.append(PageBreak())

    # Gráfico
    elementos.append(
        Paragraph(
            "Maturidade por dimensão NIST CSF",
            estilo_secao,
        )
    )

    elementos.append(
        Image(
            grafico_png,
            width=23 * cm,
            height=10.5 * cm,
        )
    )

    elementos.append(PageBreak())

    # Impacto por dimensão
    elementos.append(
        Paragraph(
            "Tradução dos riscos técnicos para o negócio",
            estilo_secao,
        )
    )

    dados_dimensoes = [
        [
            "Dimensão",
            "Maturidade",
            "Exposição",
            "Risco de negócio",
            "Impacto executivo",
        ]
    ]

    for item in risco["dimensoes"]:
        dados_dimensoes.append(
            [
                item["dimensao"],
                f"{item['percentual']:.0f}%",
                item["exposicao"],
                item["risco"],
                item["consequencia"],
            ]
        )

    tabela_dimensoes = Table(
        dados_dimensoes,
        colWidths=[
            3.1 * cm,
            2.5 * cm,
            2.8 * cm,
            5 * cm,
            11 * cm,
        ],
        repeatRows=1,
    )

    tabela_dimensoes.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0b2633"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#cbd4d8"),
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.white,
                ),
                (
                    "TEXTCOLOR",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#102f3b"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("LEADING", (0, 0), (-1, -1), 9),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(tabela_dimensoes)
    elementos.append(Spacer(1, 0.4 * cm))

    elementos.append(
        Paragraph(
            "Confidencialidade: este relatório contém informações relacionadas "
            "à postura de segurança da organização e deve ser compartilhado "
            "somente com pessoas autorizadas.",
            estilo_pequeno,
        )
    )

    documento.build(elementos)

    buffer.seek(0)
    return buffer.getvalue()


# ============================================================
# INTERFACE
# ============================================================

renderizar_html(
    """
<section class="ctr-hero">
<h1>CTR <span>CyberCheck</span></h1>
<p>Avaliação executiva de maturidade cibernética baseada no NIST CSF 2.0, com tradução dos riscos técnicos para impacto financeiro e empresarial.</p>
</section>
"""
)

renderizar_html(
    """
<div class="ctr-session-notice">
<strong>⚠️ Sistema sem armazenamento persistente</strong><br>
As informações inseridas são processadas somente na memória da sessão atual. O sistema não utiliza banco de dados nem grava os dados permanentemente no servidor.
</div>
"""
)

renderizar_html(
    """
<div class="ctr-privacy-notice">
<strong>🔒 LGPD e confidencialidade</strong><br>
Utilize somente as informações necessárias para a avaliação. Evite inserir dados pessoais sensíveis, credenciais, segredos comerciais ou detalhes operacionais que não sejam indispensáveis. O relatório deve ser tratado como informação confidencial e compartilhado apenas com pessoas autorizadas.
</div>
"""
)


if "resultado_calculado" not in st.session_state:
    st.session_state.resultado_calculado = False


with st.container(border=True):
    st.markdown("### 🏢 Dados da organização")

    coluna1, coluna2 = st.columns(2)

    organizacao = coluna1.text_input(
        "Nome da organização",
        key="organizacao",
    )

    responsavel = coluna2.text_input(
        "Responsável pela avaliação",
        key="responsavel",
    )

    coluna3, coluna4 = st.columns(2)

    faixa_faturamento = coluna3.selectbox(
        "Faixa de faturamento anual — opcional",
        list(FAIXAS_FATURAMENTO.keys()),
        key="faixa_faturamento",
        help=(
            "Utilizada somente para calibrar a estimativa financeira. "
            "Não é armazenada permanentemente."
        ),
    )

    objetivo = coluna4.selectbox(
        "Objetivo principal da avaliação",
        [
            "Diagnóstico executivo",
            "Planejamento de investimentos",
            "Adequação regulatória",
            "Preparação para auditoria",
            "Revisão de riscos",
        ],
        key="objetivo",
    )

    ciencia_privacidade = st.checkbox(
        "Estou ciente de que os dados são processados somente durante esta sessão e devem ser inseridos de forma minimizada e confidencial.",
        key="ciencia_privacidade",
    )


st.markdown("### 📊 Escala de maturidade")

renderizar_html(
    """
<div class="ctr-scale">
<div class="ctr-scale-item"><strong>0</strong> Não implementado</div>
<div class="ctr-scale-item"><strong>1</strong> Inicial</div>
<div class="ctr-scale-item"><strong>2</strong> Parcial</div>
<div class="ctr-scale-item"><strong>3</strong> Definido</div>
<div class="ctr-scale-item"><strong>4</strong> Gerenciado</div>
<div class="ctr-scale-item"><strong>5</strong> Otimizado</div>
</div>
"""
)


respostas = []
resultados_dimensoes = []

numero_pergunta = 1

for indice_dimensao, dimensao in enumerate(DIMENSOES, start=1):
    renderizar_html(
        f"""
<div class="dimension-header">
<div class="dimension-number">{indice_dimensao}</div>
<div>
<div class="dimension-title">{html.escape(dimensao['nome'])} — {dimensao['codigo']}</div>
<div class="dimension-description">{html.escape(dimensao['descricao'])}</div>
</div>
</div>
"""
    )

    soma_dimensao = 0

    perguntas = dimensao["perguntas"]

    for indice_pergunta, pergunta in enumerate(perguntas):
        chave = f"resposta_{indice_dimensao}_{indice_pergunta}"

        with st.container(border=True):
            renderizar_html(
                f"""
<div class="question-card">
<div>
<span class="question-number">{numero_pergunta}</span>
<span class="question-text">{html.escape(pergunta)}</span>
</div>
<div class="nist-badge">NIST CSF 2.0 · {dimensao['codigo']}</div>
</div>
"""
            )

            valor = st.radio(
                "Nível de implementação",
                options=list(OPCOES.keys()),
                format_func=lambda item: (
                    f"{item} — {OPCOES[item]}"
                ),
                horizontal=True,
                key=chave,
                label_visibility="collapsed",
            )

        soma_dimensao += valor

        respostas.append(
            {
                "dimensao": dimensao["nome"],
                "codigo": dimensao["codigo"],
                "pergunta": pergunta,
                "resposta": OPCOES[valor],
                "pontuacao": valor,
            }
        )

        numero_pergunta += 1

    percentual_dimensao = (
        soma_dimensao
        / (len(perguntas) * 5)
        * 100
    )

    resultados_dimensoes.append(
        {
            "nome": dimensao["nome"],
            "codigo": dimensao["codigo"],
            "percentual": percentual_dimensao,
            "nivel": obter_nivel(percentual_dimensao),
            "prioridade": obter_prioridade(percentual_dimensao),
        }
    )


total_pontos = sum(
    resposta["pontuacao"]
    for resposta in respostas
)

total_pontos_maximos = len(respostas) * 5

maturidade_geral = (
    total_pontos / total_pontos_maximos * 100
    if total_pontos_maximos
    else 0
)


risco = calcular_risco_financeiro(
    maturidade_geral,
    resultados_dimensoes,
    faixa_faturamento,
)


st.markdown("### ⚙️ Ações")

coluna_acao1, coluna_acao2 = st.columns(2)

with coluna_acao1:
    calcular = st.button(
        "📊 Calcular avaliação",
        use_container_width=True,
    )

with coluna_acao2:
    limpar = st.button(
        "🧹 Limpar sessão",
        use_container_width=True,
    )


if limpar:
    limpar_sessao()
    st.rerun()


if calcular:
    if not organizacao.strip():
        st.error(
            "Informe o nome da organização antes de calcular."
        )
    elif not ciencia_privacidade:
        st.error(
            "Confirme a ciência sobre o processamento temporário "
            "e a confidencialidade das informações."
        )
    else:
        st.session_state.resultado_calculado = True
        st.success(
            "Avaliação calculada com sucesso."
        )


if st.session_state.get("resultado_calculado"):
    st.markdown("## 📌 Resultado executivo")

    nivel_geral = obter_nivel(maturidade_geral)

    renderizar_html(
        f"""
<div class="result-card">
<h2>Resultado da avaliação</h2>
<p>Organização: <strong>{html.escape(organizacao)}</strong></p>
<p>Objetivo: <strong>{html.escape(objetivo)}</strong></p>
<div class="result-score">{maturidade_geral:.1f}%</div>
<p>Nível geral de maturidade: <strong>{nivel_geral}</strong></p>
</div>
"""
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Maturidade geral",
        f"{maturidade_geral:.1f}%",
    )

    col2.metric(
        "Nível",
        nivel_geral,
    )

    col3.metric(
        "Dimensões avaliadas",
        len(resultados_dimensoes),
    )

    col4.metric(
        "Prioridade alta",
        sum(
            item["prioridade"] == "Alta"
            for item in resultados_dimensoes
        ),
    )

    # Visão C-Level
    kpis_html = f"""
<div class="exec-grid">
<div class="exec-kpi">
<span class="exec-kpi-label">Exposição atual</span>
<span class="exec-kpi-value" style="color:{risco['cor_geral']} !important;">{risco['exposicao_geral']}</span>
<span class="exec-kpi-note">Maturidade: {risco['nivel_geral']}</span>
</div>
<div class="exec-kpi">
<span class="exec-kpi-label">Probabilidade de incidente</span>
<span class="exec-kpi-value">{risco['probabilidade_12m'] * 100:.0f}%</span>
<span class="exec-kpi-note">Horizonte de 12 meses</span>
</div>
<div class="exec-kpi">
<span class="exec-kpi-label">Custo por incidente grave</span>
<span class="exec-kpi-value">{formatar_moeda(risco['custo_incidente'])}</span>
<span class="exec-kpi-note">Impacto potencial por evento</span>
</div>
<div class="exec-kpi">
<span class="exec-kpi-label">Perda esperada anual</span>
<span class="exec-kpi-value">{formatar_moeda(risco['perda_esperada_anual'])}</span>
<span class="exec-kpi-note">Probabilidade × impacto</span>
</div>
<div class="exec-kpi">
<span class="exec-kpi-label">Economia potencial</span>
<span class="exec-kpi-value" style="color:#11a88f !important;">{formatar_moeda(risco['economia_potencial'])}</span>
<span class="exec-kpi-note">Ao evoluir para {risco['proximo_nivel']}</span>
</div>
</div>
"""

    linhas_html = ""

    for item in risco["dimensoes"]:
        linhas_html += f"""
<div class="exec-row">
<div class="exec-row-dim">
{html.escape(item['dimensao'])}
<small>{item['percentual']:.0f}% de maturidade</small>
</div>
<div>
<span class="exec-pill" style="background:{item['cor']} !important;">
{item['exposicao']}
</span>
</div>
<div class="exec-row-text">
<strong>{html.escape(item['risco'])}</strong>
<span>{html.escape(item['consequencia'])}</span>
</div>
</div>
"""

    renderizar_html(
        f"""
<div class="exec-card">
<h3>💼 Visão Executiva — Risco Financeiro</h3>
<p class="exec-subtitle">
Tradução dos resultados técnicos para impacto no negócio, orientada à diretoria, ao comitê executivo e ao conselho.
</p>
<div class="exec-summary">{mensagem_executiva(risco)}</div>
{kpis_html}
<h3 style="font-size:1.05rem; margin-top:18px;">Onde está o dinheiro em risco</h3>
{linhas_html}
<p class="exec-disclaimer">
As estimativas são orientativas e baseadas na maturidade informada e em parâmetros de referência. Não substituem análise atuarial, avaliação jurídica, cotação de seguro cibernético ou validação da área financeira.
</p>
</div>
"""
    )

    st.markdown("### 📈 Maturidade por dimensão")

    tabela_resultados = pd.DataFrame(
        [
            {
                "Dimensão": item["nome"],
                "Código": item["codigo"],
                "Maturidade": f"{item['percentual']:.1f}%",
                "Nível": item["nivel"],
                "Prioridade": item["prioridade"],
            }
            for item in resultados_dimensoes
        ]
    )

    st.dataframe(
        tabela_resultados,
        use_container_width=True,
        hide_index=True,
    )

    grafico = criar_grafico_dimensoes(
        resultados_dimensoes
    )

    st.pyplot(
        grafico,
        use_container_width=True,
    )

    st.markdown("### 📥 Exportação")

    csv_bytes = montar_csv_completo(
        organizacao=organizacao,
        responsavel=responsavel,
        faixa_faturamento=faixa_faturamento,
        maturidade_geral=maturidade_geral,
        resultados_dimensoes=resultados_dimensoes,
        respostas=respostas,
        risco=risco,
    )

    grafico_pdf = criar_grafico_dimensoes(
        resultados_dimensoes
    )

    grafico_png = figura_para_png(
        grafico_pdf
    )

    pdf_bytes = montar_pdf(
        organizacao=organizacao,
        responsavel=responsavel,
        faixa_faturamento=faixa_faturamento,
        maturidade_geral=maturidade_geral,
        resultados_dimensoes=resultados_dimensoes,
        risco=risco,
        grafico_png=grafico_png,
    )

    nome_base = nome_arquivo_seguro(
        f"CTR_CyberCheck_{organizacao}"
    )

    export_col1, export_col2 = st.columns(2)

    with export_col1:
        st.download_button(
            "⬇️ Baixar relatório CSV",
            data=csv_bytes,
            file_name=f"{nome_base}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with export_col2:
        st.download_button(
            "⬇️ Baixar relatório PDF",
            data=pdf_bytes,
            file_name=f"{nome_base}.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


st.caption(
    "CTR CyberCheck • Avaliação orientativa baseada no NIST CSF 2.0. "
    "As informações devem ser tratadas com confidencialidade."
)
