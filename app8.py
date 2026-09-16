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
    --primary: #047f9e;
    --secondary: #11a88f;
    --dark: #06141d;
    --text: #102f3b;
    --muted: #536b75;
    --border: #cbd4d8;
    --background: #e8edef;
}

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"],
.stApp {
    background: var(--background) !important;
    color: var(--text) !important;
}

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

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

#MainMenu,
footer {
    visibility: hidden;
}

/* Cabeçalho */

.ctr-hero {
    padding: 38px 42px;
    margin-bottom: 22px;
    color: white !important;
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

.ctr-notice {
    padding: 19px 21px;
    margin-bottom: 17px;
    line-height: 1.6;
    border-radius: 15px;
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

/* Painéis */

div[data-testid="stVerticalBlockBorderWrapper"] > div {
    color: var(--text) !important;
    border-color: var(--border) !important;
    border-radius: 17px !important;
    background: white !important;
    box-shadow: 0 8px 24px rgba(17, 56, 70, 0.1);
}

/* Campos */

[data-testid="stTextInput"] label,
[data-testid="stTextInput"] label p,
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p,
[data-testid="stCheckbox"] label p,
[data-testid="stRadio"] > label,
[data-testid="stRadio"] > label p {
    color: var(--text) !important;
    font-weight: 700 !important;
}

[data-testid="stTextInput"] input {
    color: var(--text) !important;
    background: white !important;
    border-color: var(--border) !important;
    -webkit-text-fill-color: var(--text) !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    color: var(--text) !important;
    background: white !important;
    border-color: var(--border) !important;
}

[data-testid="stSelectbox"] span {
    color: var(--text) !important;
}

/* Escala */

.ctr-scale {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 8px;
    margin: 14px 0 25px 0;
}

.ctr-scale-item {
    padding: 10px 7px;
    color: #163d49 !important;
    font-size: 0.78rem;
    text-align: center;
    border: 1px solid #bed6dd;
    border-radius: 10px;
    background: #f9fcfd;
}

.ctr-scale-item strong {
    display: block;
    color: var(--primary) !important;
    font-size: 1.25rem;
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
    padding: 18px;
    margin-bottom: 14px;
    border: 1px solid var(--border);
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
    color: var(--text) !important;
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
    color: var(--text) !important;
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
    min-height: 50px;
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
.result-card p,
.result-card strong {
    color: white !important;
}

.result-score {
    color: #64e5ff !important;
    font-size: 3rem;
    font-weight: 900;
}

/* Visão executiva */

.exec-card {
    padding: 26px 28px;
    margin-top: 22px;
    color: var(--text) !important;
    border: 1px solid var(--border);
    border-top: 6px solid #b42318;
    border-radius: 18px;
    background: white !important;
    box-shadow: 0 12px 30px rgba(17, 57, 71, 0.1);
}

.exec-card h3 {
    margin: 0 0 7px 0;
    color: var(--text) !important;
    font-size: 1.3rem;
}

.exec-subtitle {
    color: var(--muted) !important;
    font-size: 0.92rem;
}

.exec-summary {
    padding: 16px 18px;
    margin: 14px 0;
    color: var(--text) !important;
    font-size: 1.02rem;
    line-height: 1.7;
    border-left: 5px solid var(--primary);
    border-radius: 10px;
    background: #f3f7f9 !important;
}

.exec-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 12px;
    margin: 16px 0;
}

.exec-kpi {
    padding: 16px;
    border: 1px solid var(--border);
    border-radius: 13px;
    background: #fafbfc !important;
}

.exec-kpi-label {
    display: block;
    margin-bottom: 6px;
    color: var(--muted) !important;
    font-size: 0.76rem;
    font-weight: 800;
    text-transform: uppercase;
}

.exec-kpi-value {
    display: block;
    color: #063744 !important;
    font-size: 1.35rem;
    font-weight: 900;
}

.exec-kpi-note {
    display: block;
    margin-top: 4px;
    color: var(--muted) !important;
    font-size: 0.8rem;
}

.exec-row {
    display: grid;
    grid-template-columns: 150px 115px 1fr;
    gap: 14px;
    align-items: start;
    padding: 13px 14px;
    margin: 8px 0;
    border: 1px solid var(--border);
    border-radius: 12px;
    background: white !important;
}

.exec-row-dim {
    color: var(--text) !important;
    font-weight: 800;
}

.exec-row-dim small {
    display: block;
    color: var(--muted) !important;
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
    color: var(--muted) !important;
    font-size: 0.9rem;
    line-height: 1.5;
}

.exec-disclaimer {
    margin-top: 14px;
    color: var(--muted) !important;
    font-size: 0.8rem;
    line-height: 1.5;
}

@media (max-width: 700px) {
    .ctr-hero h1 {
        font-size: 2.2rem;
    }

    .ctr-scale {
        grid-template-columns: repeat(3, 1fr);
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
# DADOS
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

IMPACTOS = {
    "Governar": (
        "Responsabilidade legal e regulatória",
        "Políticas frágeis podem elevar a exposição a sanções, disputas e responsabilização executiva.",
        "Exposição regulatória",
    ),
    "Identificar": (
        "Ativos e fragilidades desconhecidos",
        "O que não é inventariado não pode ser adequadamente protegido, priorizado ou orçado.",
        "Eficiência do investimento",
    ),
    "Proteger": (
        "Ransomware e paralisação operacional",
        "Controles preventivos insuficientes podem gerar indisponibilidade, perda de receita e recuperação dispendiosa.",
        "Continuidade da receita",
    ),
    "Detectar": (
        "Tempo prolongado de permanência do atacante",
        "A descoberta tardia pode ampliar o volume de dados comprometidos e o custo de resposta.",
        "Custo por incidente",
    ),
    "Responder": (
        "Gestão de crise improvisada",
        "A ausência de papéis e procedimentos pode atrasar decisões, comunicação e contenção.",
        "Dano reputacional",
    ),
    "Recuperar": (
        "Perda de dados e operações",
        "Backups não testados podem prolongar a indisponibilidade e consumir caixa operacional.",
        "Tempo de retomada",
    ),
}


# ============================================================
# FUNÇÕES
# ============================================================

def renderizar_html(conteudo):
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
        return (
            f"R$ {valor / 1_000_000:,.1f} milhões"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    if valor >= 1_000:
        return f"R$ {valor / 1_000:,.0f} mil".replace(",", ".")

    return f"R$ {valor:,.0f}".replace(",", ".")


def nome_arquivo_seguro(nome):
    nome = re.sub(r"[^a-zA-Z0-9_-]+", "_", nome)
    return nome.strip("_") or "relatorio_ctr_cybercheck"


def obter_cor_exposicao(percentual):
    if percentual < 40:
        return "Crítica", "#b42318"
    if percentual < 60:
        return "Alta", "#d9a514"
    if percentual < 80:
        return "Moderada", "#047f9e"
    return "Controlada", "#11a88f"


def calcular_risco(
    maturidade_geral,
    resultados_dimensoes,
    faixa_faturamento,
):
    nivel = obter_nivel(maturidade_geral)

    probabilidade = PROBABILIDADE_POR_NIVEL[nivel]
    faturamento = FAIXAS_FATURAMENTO[faixa_faturamento]

    if faturamento:
        custo_incidente = max(
            faturamento * EXPOSICAO_FATURAMENTO_POR_NIVEL[nivel],
            6_500_000 * 0.3,
        )
        custo_incidente = min(custo_incidente, 6_500_000 * 3)
        multa_lgpd = min(faturamento * 0.02, 50_000_000)
    else:
        custo_incidente = 6_500_000
        multa_lgpd = None

    perda_esperada = probabilidade * custo_incidente

    niveis = list(PROBABILIDADE_POR_NIVEL.keys())
    indice = niveis.index(nivel)
    proximo_nivel = niveis[min(indice + 1, len(niveis) - 1)]

    perda_proximo_nivel = (
        PROBABILIDADE_POR_NIVEL[proximo_nivel]
        * custo_incidente
    )

    economia = max(perda_esperada - perda_proximo_nivel, 0)

    dimensoes = []

    for item in resultados_dimensoes:
        exposicao, cor = obter_cor_exposicao(item["percentual"])
        risco, consequencia, indicador = IMPACTOS[item["nome"]]

        dimensoes.append(
            {
                "dimensao": item["nome"],
                "percentual": item["percentual"],
                "exposicao": exposicao,
                "cor": cor,
                "risco": risco,
                "consequencia": consequencia,
                "indicador": indicador,
            }
        )

    dimensoes.sort(key=lambda item: item["percentual"])

    exposicao_geral, cor_geral = obter_cor_exposicao(maturidade_geral)

    return {
        "nivel_geral": nivel,
        "exposicao_geral": exposicao_geral,
        "cor_geral": cor_geral,
        "probabilidade": probabilidade,
        "custo_incidente": custo_incidente,
        "perda_esperada": perda_esperada,
        "multa_lgpd": multa_lgpd,
        "proximo_nivel": proximo_nivel,
        "economia": economia,
        "dimensoes": dimensoes,
    }


def mensagem_executiva(risco):
    texto = (
        f"A organização apresenta exposição cibernética "
        f"<strong>{risco['exposicao_geral'].lower()}</strong>. "
        f"A probabilidade orientativa de um incidente relevante nos próximos "
        f"12 meses é de aproximadamente "
        f"<strong>{risco['probabilidade'] * 100:.0f}%</strong>. "
        f"O custo potencial por evento é estimado em "
        f"<strong>{formatar_moeda(risco['custo_incidente'])}</strong>. "
        f"A perda esperada anual é de aproximadamente "
        f"<strong>{formatar_moeda(risco['perda_esperada'])}</strong>. "
        f"A evolução para o nível "
        f"<strong>{risco['proximo_nivel']}</strong> "
        f"poderia reduzir a perda esperada em aproximadamente "
        f"<strong>{formatar_moeda(risco['economia'])}</strong>."
    )

    if risco["multa_lgpd"]:
        texto += (
            " A referência regulatória deve ser validada pela assessoria "
            "jurídica e não representa cálculo definitivo de penalidade."
        )

    return texto


def limpar_sessao():
    st.session_state.clear()


def criar_grafico(resultados):
    fig, ax = plt.subplots(figsize=(10, 5))

    nomes = [item["nome"] for item in resultados]
    valores = [item["percentual"] for item in resultados]

    cores = [
        "#b42318"
        if valor < 40
        else "#d9a514"
        if valor < 60
        else "#047f9e"
        if valor < 80
        else "#11a88f"
        for valor in valores
    ]

    ax.bar(nomes, valores, color=cores)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Maturidade (%)")
    ax.set_title("Maturidade por dimensão NIST CSF")
    ax.grid(axis="y", alpha=0.25)

    for i, valor in enumerate(valores):
        ax.text(
            i,
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
# CSV
# ============================================================

def montar_csv(
    organizacao,
    responsavel,
    faixa_faturamento,
    objetivo,
    maturidade,
    resultados,
    respostas,
    risco,
):
    buffer = io.StringIO()
    escritor = csv.writer(buffer)

    escritor.writerow(["CTR CyberCheck"])
    escritor.writerow(
        [
            "Relatório executivo",
            datetime.now().strftime("%d/%m/%Y %H:%M"),
        ]
    )
    escritor.writerow([])

    escritor.writerow(["DADOS DA ORGANIZAÇÃO"])
    escritor.writerow(["Organização", organizacao])
    escritor.writerow(["Responsável", responsavel])
    escritor.writerow(["Faixa de faturamento", faixa_faturamento])
    escritor.writerow(["Objetivo", objetivo])
    escritor.writerow([])

    escritor.writerow(["RESUMO EXECUTIVO"])
    escritor.writerow(["Maturidade geral", f"{maturidade:.1f}%"])
    escritor.writerow(["Nível geral", risco["nivel_geral"]])
    escritor.writerow(["Exposição geral", risco["exposicao_geral"]])
    escritor.writerow(
        [
            "Probabilidade em 12 meses",
            f"{risco['probabilidade'] * 100:.0f}%",
        ]
    )
    escritor.writerow(
        [
            "Custo por incidente",
            formatar_moeda(risco["custo_incidente"]),
        ]
    )
    escritor.writerow(
        [
            "Perda esperada anual",
            formatar_moeda(risco["perda_esperada"]),
        ]
    )
    escritor.writerow(
        [
            "Referência LGPD",
            formatar_moeda(risco["multa_lgpd"]),
        ]
    )
    escritor.writerow(
        [
            "Economia potencial",
            formatar_moeda(risco["economia"]),
        ]
    )
    escritor.writerow([])

    escritor.writerow(["DIMENSÕES"])
    escritor.writerow(
        [
            "Dimensão",
            "Maturidade",
            "Exposição",
            "Risco de negócio",
            "Indicador",
            "Consequência",
        ]
    )

    for item in risco["dimensoes"]:
        escritor.writerow(
            [
                item["dimensao"],
                f"{item['percentual']:.1f}%",
                item["exposicao"],
                item["risco"],
                item["indicador"],
                item["consequencia"],
            ]
        )

    escritor.writerow([])
    escritor.writerow(["RESPOSTAS"])
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
# PDF
# ============================================================

def montar_pdf(
    organizacao,
    responsavel,
    faixa_faturamento,
    objetivo,
    maturidade,
    resultados,
    risco,
    grafico_png,
):
    buffer = io.BytesIO()

    documento = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
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
        alignment=TA_CENTER,
        textColor=colors.HexColor("#102f3b"),
        spaceAfter=12,
    )

    estilo_secao = ParagraphStyle(
        "SecaoCTR",
        parent=estilos["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=17,
        textColor=colors.HexColor("#047f9e"),
        spaceBefore=8,
        spaceAfter=8,
    )

    estilo_normal = ParagraphStyle(
        "NormalCTR",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=11.5,
        textColor=colors.HexColor("#102f3b"),
    )

    estilo_celula = ParagraphStyle(
        "CelulaCTR",
        parent=estilo_normal,
        fontSize=7.8,
        leading=9.5,
    )

    estilo_celula_negrito = ParagraphStyle(
        "CelulaNegritoCTR",
        parent=estilo_celula,
        fontName="Helvetica-Bold",
    )

    estilo_pequeno = ParagraphStyle(
        "PequenoCTR",
        parent=estilos["Normal"],
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#536b75"),
    )

    def celula(valor, negrito=False):
        """
        Converte todas as células em Paragraph.
        Isso corrige a quebra automática de linhas nas tabelas.
        """
        valor = "" if valor is None else str(valor)
        valor = html.escape(valor).replace("\n", "<br/>")

        estilo = (
            estilo_celula_negrito
            if negrito
            else estilo_celula
        )

        return Paragraph(valor, estilo)

    elementos = []

    elementos.append(
        Paragraph(
            "CTR CyberCheck",
            estilo_titulo,
        )
    )

    elementos.append(
        Paragraph(
            "Relatório Executivo de Maturidade e Risco",
            estilo_secao,
        )
    )

    dados_org = [
        [celula("Organização", True), celula(organizacao)],
        [celula("Responsável", True), celula(responsavel)],
        [celula("Objetivo", True), celula(objetivo)],
        [celula("Faixa de faturamento", True), celula(faixa_faturamento)],
        [celula("Maturidade geral", True), celula(f"{maturidade:.1f}%")],
        [celula("Nível geral", True), celula(risco["nivel_geral"])],
        [
            celula("Data da avaliação", True),
            celula(datetime.now().strftime("%d/%m/%Y %H:%M")),
        ],
    ]

    tabela_org = Table(
        dados_org,
        colWidths=[5.2 * cm, 9.8 * cm],
    )

    tabela_org.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#eaf3f5"),
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

    elementos.append(tabela_org)
    elementos.append(Spacer(1, 0.35 * cm))

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

    elementos.append(Spacer(1, 0.2 * cm))

    dados_kpi = [
        [
            celula("Indicador", True),
            celula("Valor", True),
            celula("Leitura executiva", True),
        ],
        [
            celula("Exposição atual"),
            celula(risco["exposicao_geral"]),
            celula(f"Maturidade {risco['nivel_geral']}"),
        ],
        [
            celula("Probabilidade em 12 meses"),
            celula(f"{risco['probabilidade'] * 100:.0f}%"),
            celula("Probabilidade orientativa de incidente relevante"),
        ],
        [
            celula("Custo por incidente"),
            celula(formatar_moeda(risco["custo_incidente"])),
            celula("Parada, resposta, recuperação e reputação"),
        ],
        [
            celula("Perda esperada anual"),
            celula(formatar_moeda(risco["perda_esperada"])),
            celula("Referência para priorização de investimentos"),
        ],
        [
            celula("Economia potencial"),
            celula(formatar_moeda(risco["economia"])),
            celula(f"Meta: nível {risco['proximo_nivel']}"),
        ],
    ]

    tabela_kpi = Table(
        dados_kpi,
        colWidths=[6 * cm, 5 * cm, 13 * cm],
        repeatRows=1,
    )

    tabela_kpi.setStyle(
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
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.HexColor("#f7fafb"),
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

    elementos.append(tabela_kpi)
    elementos.append(Spacer(1, 0.25 * cm))

    elementos.append(
        Paragraph(
            "Os valores financeiros são estimativas orientativas. "
            "Não constituem previsão financeira, avaliação atuarial, "
            "cotação de seguro ou parecer jurídico.",
            estilo_pequeno,
        )
    )

    elementos.append(PageBreak())

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

    elementos.append(
        Paragraph(
            "Tradução dos riscos técnicos para o negócio",
            estilo_secao,
        )
    )

    tabela_dimensoes_dados = [
        [
            celula("Dimensão", True),
            celula("Maturidade", True),
            celula("Exposição", True),
            celula("Risco de negócio", True),
            celula("Impacto executivo", True),
        ]
    ]

    for item in risco["dimensoes"]:
        tabela_dimensoes_dados.append(
            [
                celula(item["dimensao"], True),
                celula(f"{item['percentual']:.0f}%"),
                celula(item["exposicao"]),
                celula(item["risco"]),
                celula(item["consequencia"]),
            ]
        )

    tabela_dimensoes = Table(
        tabela_dimensoes_dados,
        colWidths=[
            3.1 * cm,
            2.5 * cm,
            2.8 * cm,
            5.0 * cm,
            11.0 * cm,
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
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#cbd4d8"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(tabela_dimensoes)
    elementos.append(Spacer(1, 0.3 * cm))

    elementos.append(
        Paragraph(
            "Confidencialidade: este relatório contém informações sobre "
            "a postura de segurança da organização e deve ser compartilhado "
            "somente com pessoas autorizadas.",
            estilo_pequeno,
        )
    )

    documento.build(elementos)

    buffer.seek(0)
    return buffer.getvalue()


# ============================================================
# INTERFACE PRINCIPAL
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
<div class="ctr-notice ctr-session-notice">
<strong>⚠️ Sistema sem armazenamento persistente</strong><br>
As informações inseridas são processadas somente na memória da sessão atual. Este aplicativo não utiliza banco de dados nem grava os dados permanentemente no servidor.
</div>
"""
)

renderizar_html(
    """
<div class="ctr-notice ctr-privacy-notice">
<strong>🔒 LGPD e confidencialidade</strong><br>
Informe somente os dados necessários para a avaliação. Evite inserir dados pessoais sensíveis, credenciais, segredos comerciais ou informações operacionais desnecessárias. Os relatórios devem ser tratados como informação confidencial e compartilhados apenas com pessoas autorizadas.
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
    )

    objetivo = coluna4.selectbox(
        "Objetivo principal",
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
        "Estou ciente de que os dados são processados somente durante esta sessão e devem ser tratados com confidencialidade.",
        key="ciencia_privacidade",
    )


st.markdown("### 📊 Escala de maturidade")

renderizar_html(
    """
<div class="ctr-scale">
<div class="ctr-scale-item"><strong>0</strong>Não implementado</div>
<div class="ctr-scale-item"><strong>1</strong>Inicial</div>
<div class="ctr-scale-item"><strong>2</strong>Parcial</div>
<div class="ctr-scale-item"><strong>3</strong>Definido</div>
<div class="ctr-scale-item"><strong>4</strong>Gerenciado</div>
<div class="ctr-scale-item"><strong>5</strong>Otimizado</div>
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

    soma = 0

    for indice_pergunta, pergunta in enumerate(dimensao["perguntas"]):
        chave = f"resposta_{indice_dimensao}_{indice_pergunta}"

        with st.container(border=True):
            renderizar_html(
                f"""
<div class="question-card">
<span class="question-number">{numero_pergunta}</span>
<span class="question-text">{html.escape(pergunta)}</span><br>
<span class="nist-badge">NIST CSF 2.0 · {dimensao['codigo']}</span>
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

        soma += valor

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

    percentual = soma / (len(dimensao["perguntas"]) * 5) * 100

    resultados_dimensoes.append(
        {
            "nome": dimensao["nome"],
            "codigo": dimensao["codigo"],
            "percentual": percentual,
            "nivel": obter_nivel(percentual),
            "prioridade": obter_prioridade(percentual),
        }
    )


total_pontos = sum(item["pontuacao"] for item in respostas)
total_maximo = len(respostas) * 5
maturidade_geral = total_pontos / total_maximo * 100

risco = calcular_risco(
    maturidade_geral,
    resultados_dimensoes,
    faixa_faturamento,
)


st.markdown("### ⚙️ Ações")

acao1, acao2 = st.columns(2)

with acao1:
    calcular = st.button(
        "📊 Calcular avaliação",
        use_container_width=True,
    )

with acao2:
    limpar = st.button(
        "🧹 Limpar sessão",
        use_container_width=True,
    )


if limpar:
    limpar_sessao()
    st.rerun()


if calcular:
    if not organizacao.strip():
        st.error("Informe o nome da organização.")
    elif not ciencia_privacidade:
        st.error(
            "Confirme a ciência sobre o processamento temporário "
            "e a confidencialidade."
        )
    else:
        st.session_state.resultado_calculado = True
        st.success("Avaliação calculada com sucesso.")


# ============================================================
# RESULTADOS
# ============================================================

if st.session_state.get("resultado_calculado"):
    st.markdown("## 📌 Resultado executivo")

    renderizar_html(
        f"""
<div class="result-card">
<h2>Resultado da avaliação</h2>
<p>Organização: <strong>{html.escape(organizacao)}</strong></p>
<p>Objetivo: <strong>{html.escape(objetivo)}</strong></p>
<div class="result-score">{maturidade_geral:.1f}%</div>
<p>Nível geral de maturidade: <strong>{risco['nivel_geral']}</strong></p>
</div>
"""
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Maturidade geral", f"{maturidade_geral:.1f}%")
    col2.metric("Nível", risco["nivel_geral"])
    col3.metric("Dimensões avaliadas", len(resultados_dimensoes))
    col4.metric(
        "Prioridade alta",
        sum(
            item["prioridade"] == "Alta"
            for item in resultados_dimensoes
        ),
    )

    kpis = f"""
<div class="exec-grid">
<div class="exec-kpi">
<span class="exec-kpi-label">Exposição atual</span>
<span class="exec-kpi-value" style="color:{risco['cor_geral']} !important;">{risco['exposicao_geral']}</span>
<span class="exec-kpi-note">Maturidade: {risco['nivel_geral']}</span>
</div>

<div class="exec-kpi">
<span class="exec-kpi-label">Probabilidade de incidente</span>
<span class="exec-kpi-value">{risco['probabilidade'] * 100:.0f}%</span>
<span class="exec-kpi-note">Horizonte de 12 meses</span>
</div>

<div class="exec-kpi">
<span class="exec-kpi-label">Custo por incidente</span>
<span class="exec-kpi-value">{formatar_moeda(risco['custo_incidente'])}</span>
<span class="exec-kpi-note">Impacto potencial por evento</span>
</div>

<div class="exec-kpi">
<span class="exec-kpi-label">Perda esperada anual</span>
<span class="exec-kpi-value">{formatar_moeda(risco['perda_esperada'])}</span>
<span class="exec-kpi-note">Probabilidade × impacto</span>
</div>

<div class="exec-kpi">
<span class="exec-kpi-label">Economia potencial</span>
<span class="exec-kpi-value" style="color:#11a88f !important;">{formatar_moeda(risco['economia'])}</span>
<span class="exec-kpi-note">Ao evoluir para {risco['proximo_nivel']}</span>
</div>
</div>
"""

    linhas = ""

    for item in risco["dimensoes"]:
        linhas += f"""
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
Tradução dos resultados técnicos para impacto no negócio.
</p>
<div class="exec-summary">{mensagem_executiva(risco)}</div>
{kpis}
<h3 style="font-size:1.05rem; margin-top:18px;">
Onde está o dinheiro em risco
</h3>
{linhas}
<p class="exec-disclaimer">
As estimativas são orientativas e não substituem análise atuarial,
avaliação jurídica, cotação de seguro ou validação financeira.
</p>
</div>
"""
    )

    st.markdown("### 📈 Maturidade por dimensão")

    tabela = pd.DataFrame(
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
        tabela,
        use_container_width=True,
        hide_index=True,
    )

    grafico = criar_grafico(resultados_dimensoes)
    st.pyplot(grafico, use_container_width=True)

    st.markdown("### 📥 Exportação")

    csv_bytes = montar_csv(
        organizacao,
        responsavel,
        faixa_faturamento,
        objetivo,
        maturidade_geral,
        resultados_dimensoes,
        respostas,
        risco,
    )

    grafico_pdf = criar_grafico(resultados_dimensoes)
    grafico_png = figura_para_png(grafico_pdf)

    pdf_bytes = montar_pdf(
        organizacao,
        responsavel,
        faixa_faturamento,
        objetivo,
        maturidade_geral,
        resultados_dimensoes,
        risco,
        grafico_png,
    )

    nome_base = nome_arquivo_seguro(
        f"CTR_CyberCheck_{organizacao}"
    )

    export1, export2 = st.columns(2)

    with export1:
        st.download_button(
            "⬇️ Baixar relatório CSV",
            data=csv_bytes,
            file_name=f"{nome_base}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with export2:
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
