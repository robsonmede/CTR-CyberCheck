import csv
import html
import io
import re
import unicodedata
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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
# CONFIGURAÇÃO DA PÁGINA
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
            --ctr-dark-light: #0b2633;
            --ctr-background: #dfe3e6;
            --ctr-background-secondary: #eef0f2;
            --ctr-border: #c4cbd0;
            --ctr-text: #102f3b;
            --ctr-text-secondary: #496570;
            --ctr-white: #ffffff;
        }

        html,
        body,
        [data-testid="stAppViewContainer"],
        [data-testid="stApp"],
        .stApp {
            color: var(--ctr-text) !important;
            background: var(--ctr-background) !important;
        }

        /*
        Não aplique uma fonte genérica a todos os elementos span e div.
        Os ícones do Streamlit utilizam uma fonte própria. Sobrescrevê-la
        pode fazer nomes internos como "_arr" aparecerem na interface.
        */
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

        .material-symbols-rounded,
        .material-symbols-outlined,
        [data-testid="stIconMaterial"] {
            font-family:
                "Material Symbols Rounded",
                "Material Symbols Outlined" !important;
            font-weight: normal !important;
            font-style: normal !important;
            line-height: 1 !important;
            letter-spacing: normal !important;
            text-transform: none !important;
            white-space: nowrap !important;
            word-wrap: normal !important;
            direction: ltr !important;
            -webkit-font-feature-settings: "liga" !important;
            -webkit-font-smoothing: antialiased !important;
            font-feature-settings: "liga" !important;
        }

        [data-testid="stHeader"] {
            background: rgba(223, 227, 230, 0.95) !important;
        }

        [data-testid="stToolbar"] {
            color: var(--ctr-text) !important;
        }

        [data-testid="stAppViewContainer"] p,
        [data-testid="stAppViewContainer"] li {
            color: var(--ctr-text);
        }

        .block-container {
            width: 100%;
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        #MainMenu,
        footer {
            visibility: hidden;
        }

        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4 {
            color: var(--ctr-text) !important;
        }

        /* Cabeçalho */
        .ctr-hero {
            position: relative;
            overflow: hidden;
            padding: 36px 38px;
            margin-bottom: 22px;
            color: #ffffff !important;
            border: 1px solid rgba(0, 212, 255, 0.30);
            border-radius: 24px;
            background:
                radial-gradient(
                    circle at 90% 15%,
                    rgba(0, 212, 255, 0.28),
                    transparent 34%
                ),
                linear-gradient(
                    135deg,
                    #06141d 0%,
                    #0b2633 52%,
                    #124253 100%
                ) !important;
            box-shadow: 0 24px 55px rgba(6, 32, 43, 0.22);
        }

        .ctr-hero::after {
            content: "";
            position: absolute;
            width: 220px;
            height: 220px;
            top: -110px;
            right: -60px;
            border: 1px solid rgba(255, 255, 255, 0.14);
            border-radius: 50%;
        }

        .ctr-badge {
            display: inline-block;
            padding: 7px 13px;
            margin-bottom: 15px;
            color: #06141d !important;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08rem;
            text-transform: uppercase;
            border-radius: 999px;
            background: linear-gradient(
                90deg,
                #59e1fb,
                #87f1d7
            ) !important;
        }

        .ctr-hero h1 {
            margin: 0 0 10px 0;
            color: #ffffff !important;
            font-size: clamp(2rem, 4vw, 3.3rem);
            font-weight: 800;
            letter-spacing: -0.06rem;
        }

        .ctr-hero h1 span {
            color: #64e5ff !important;
        }

        .ctr-hero p {
            max-width: 900px;
            margin: 0;
            color: #e4f2f5 !important;
            font-size: 1.08rem;
            line-height: 1.75;
        }

        /* Avisos */
        .ctr-session-notice {
            padding: 19px 21px;
            margin: 0 0 17px 0;
            color: #3f350d !important;
            border: 1px solid #dfbd4d;
            border-left: 6px solid #d9a514;
            border-radius: 15px;
            background: #fff8dc !important;
            box-shadow: 0 8px 22px rgba(81, 64, 6, 0.08);
        }

        .ctr-session-notice strong,
        .ctr-session-notice p,
        .ctr-session-notice div {
            color: #3f350d !important;
        }

        .ctr-privacy-notice {
            padding: 19px 21px;
            margin: 0 0 24px 0;
            color: #164d44 !important;
            border: 1px solid #91cfc2;
            border-left: 6px solid #11a88f;
            border-radius: 15px;
            background: #eaf9f5 !important;
            box-shadow: 0 8px 22px rgba(17, 100, 84, 0.07);
        }

        .ctr-privacy-notice strong,
        .ctr-privacy-notice p,
        .ctr-privacy-notice div,
        .ctr-privacy-notice li {
            color: #164d44 !important;
        }

        /* Painéis sem expander */
        .ctr-panel-header {
            padding: 3px 1px 14px 1px;
        }

        .ctr-panel-title {
            margin: 0 0 5px 0;
            color: var(--ctr-text) !important;
            font-size: 1.18rem;
            font-weight: 800;
        }

        .ctr-panel-description {
            margin: 0;
            color: var(--ctr-text-secondary) !important;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        /* Contêineres */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            height: 100%;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            height: 100%;
            color: var(--ctr-text) !important;
            border-color: var(--ctr-border) !important;
            border-radius: 17px !important;
            background: #ffffff !important;
            box-shadow: 0 8px 24px rgba(17, 56, 70, 0.10);
        }

        /* Labels */
        [data-testid="stTextInput"] label,
        [data-testid="stTextInput"] label p,
        [data-testid="stSelectbox"] label,
        [data-testid="stSelectbox"] label p,
        [data-testid="stTextArea"] label,
        [data-testid="stTextArea"] label p,
        [data-testid="stCheckbox"] label p,
        [data-testid="stToggle"] label p,
        [data-testid="stRadio"] > label,
        [data-testid="stRadio"] > label p {
            color: var(--ctr-text) !important;
            font-size: 0.98rem !important;
            font-weight: 700 !important;
        }

        /* Campos */
        [data-testid="stTextInput"] div[data-baseweb="input"] {
            overflow: hidden;
            min-height: 48px;
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border) !important;
            border-radius: 11px !important;
            background: #ffffff !important;
        }

        [data-testid="stTextInput"] input {
            min-height: 48px;
            color: var(--ctr-text) !important;
            caret-color: var(--ctr-primary) !important;
            background: #ffffff !important;
            -webkit-text-fill-color: var(--ctr-text) !important;
        }

        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
            color: #718a94 !important;
            opacity: 1 !important;
            -webkit-text-fill-color: #718a94 !important;
        }

        [data-testid="stTextInput"]
        div[data-baseweb="input"]:focus-within {
            border-color: var(--ctr-primary) !important;
            box-shadow: 0 0 0 3px rgba(4, 127, 158, 0.14) !important;
        }

        [data-testid="stTextArea"] textarea {
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border) !important;
            border-radius: 11px !important;
            background: #ffffff !important;
            caret-color: var(--ctr-primary) !important;
            -webkit-text-fill-color: var(--ctr-text) !important;
        }

        /* Selectbox */
        [data-testid="stSelectbox"]
        div[data-baseweb="select"] > div {
            min-height: 48px;
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border) !important;
            border-radius: 11px !important;
            background: #ffffff !important;
        }

        [data-testid="stSelectbox"]
        div[data-baseweb="select"] span {
            color: var(--ctr-text) !important;
            -webkit-text-fill-color: var(--ctr-text) !important;
        }

        [data-testid="stSelectbox"] svg {
            fill: var(--ctr-text) !important;
            color: var(--ctr-text) !important;
        }

        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="menu"],
        ul[role="listbox"] {
            color: var(--ctr-text) !important;
            border-color: var(--ctr-border) !important;
            background: #ffffff !important;
        }

        li[role="option"] {
            color: var(--ctr-text) !important;
            background: #ffffff !important;
        }

        li[role="option"] span,
        li[role="option"] div {
            color: var(--ctr-text) !important;
        }

        li[role="option"]:hover,
        li[role="option"][aria-selected="true"] {
            color: #063744 !important;
            background: #dff3f7 !important;
        }

        /* Escala */
        .ctr-scale {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            padding: 16px;
            margin: 18px 0 26px 0;
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border);
            border-radius: 16px;
            background: #ffffff !important;
            box-shadow: 0 8px 25px rgba(15, 55, 70, 0.09);
        }

        .ctr-scale-item {
            flex: 1;
            min-width: 165px;
            padding: 11px 13px;
            color: var(--ctr-text-secondary) !important;
            font-size: 0.88rem;
            font-weight: 600;
            border: 1px solid #d3dade;
            border-radius: 11px;
            background: #eef1f3 !important;
        }

        .ctr-scale-item strong {
            display: inline-block;
            margin-right: 5px;
            padding: 2px 8px;
            color: #ffffff !important;
            border-radius: 7px;
            background: var(--ctr-primary) !important;
        }

        /* Dimensões */
        .dimension-header {
            display: flex;
            align-items: center;
            gap: 13px;
            padding: 18px 20px;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #ffffff !important;
            border-radius: 15px;
            background: linear-gradient(
                100deg,
                #0b2633 0%,
                #145066 100%
            ) !important;
            box-shadow: 0 10px 25px rgba(9, 46, 60, 0.14);
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
            background: linear-gradient(
                135deg,
                #62e3fb,
                #76eecb
            ) !important;
        }

        .dimension-title {
            color: #ffffff !important;
            font-size: 1.22rem;
            font-weight: 800;
        }

        .dimension-description {
            margin-top: 2px;
            color: #d8edf2 !important;
            font-size: 0.87rem;
        }

        /* Perguntas */
        .question-heading {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            min-height: 125px;
            padding: 4px 2px 12px 2px;
            color: var(--ctr-text) !important;
        }

        .question-number {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            flex: 0 0 40px;
            color: #ffffff !important;
            font-size: 1rem;
            font-weight: 800;
            border-radius: 11px;
            background: linear-gradient(
                135deg,
                #047f9e,
                #11a88f
            ) !important;
        }

        .question-text {
            color: var(--ctr-text) !important;
            font-size: 1.04rem;
            font-weight: 750;
            line-height: 1.5;
        }

        .nist-badge {
            display: inline-block;
            padding: 4px 8px;
            margin-top: 7px;
            color: #075d73 !important;
            font-size: 0.70rem;
            font-weight: 800;
            text-transform: uppercase;
            border: 1px solid #b8dfe8;
            border-radius: 7px;
            background: #dff3f7 !important;
        }

        /* Radio */
        div[data-testid="stRadio"] > label {
            display: none;
        }

        div[data-testid="stRadio"] [role="radiogroup"] {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
        }

        div[data-testid="stRadio"]
        [role="radiogroup"] label {
            min-width: 45px;
            padding: 8px 11px;
            color: var(--ctr-text) !important;
            border: 1px solid #bcd5de !important;
            border-radius: 10px;
            background: #ffffff !important;
        }

        div[data-testid="stRadio"]
        [role="radiogroup"] label:hover {
            border-color: var(--ctr-primary) !important;
            background: #dff3f7 !important;
        }

        div[data-testid="stRadio"]
        [role="radiogroup"] label p,
        div[data-testid="stRadio"]
        [role="radiogroup"] label span {
            color: #173d4a !important;
            font-size: 0.88rem !important;
            font-weight: 700 !important;
            -webkit-text-fill-color: #173d4a !important;
        }

        div[data-testid="stRadio"] input {
            accent-color: var(--ctr-primary) !important;
        }

        /* Botões */
        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button {
            min-height: 54px;
            color: #ffffff !important;
            font-size: 1rem;
            font-weight: 800;
            border: 0 !important;
            border-radius: 14px;
            background: linear-gradient(
                100deg,
                #047f9e,
                #11a88f
            ) !important;
            box-shadow: 0 10px 25px rgba(4, 127, 158, 0.22);
        }

        div[data-testid="stButton"] button p,
        div[data-testid="stDownloadButton"] button p {
            color: #ffffff !important;
        }

        div[data-testid="stButton"] button:hover,
        div[data-testid="stDownloadButton"] button:hover {
            color: #ffffff !important;
            transform: translateY(-2px);
        }

        /* Métricas */
        [data-testid="stMetric"] {
            min-height: 130px;
            padding: 20px;
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border);
            border-radius: 16px;
            background: #ffffff !important;
            box-shadow: 0 8px 25px rgba(17, 57, 71, 0.09);
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricLabel"] p {
            color: var(--ctr-text-secondary) !important;
            font-weight: 700;
        }

        [data-testid="stMetricValue"],
        [data-testid="stMetricValue"] div {
            color: #047f9e !important;
            font-weight: 800;
        }

        /* Progresso */
        [data-testid="stProgress"] > div > div {
            background-color: #c5cdd1 !important;
        }

        [data-testid="stProgress"] > div > div > div {
            background: linear-gradient(
                90deg,
                #047f9e,
                #11a88f
            ) !important;
        }

        /* Alertas */
        [data-testid="stAlert"] {
            color: var(--ctr-text) !important;
            border-radius: 14px;
        }

        [data-testid="stAlert"] p,
        [data-testid="stAlert"] li,
        [data-testid="stAlert"] div {
            color: var(--ctr-text) !important;
        }

        /* Resultado */
        .result-card {
            padding: 28px;
            margin-top: 22px;
            color: #ffffff !important;
            border-radius: 20px;
            background: linear-gradient(
                135deg,
                #06141d,
                #124253
            ) !important;
            box-shadow: 0 20px 45px rgba(6, 32, 43, 0.22);
        }

        .result-card h2,
        .result-card h3,
        .result-card p,
        .result-card strong {
            color: #ffffff !important;
        }

        .result-score {
            color: #64e5ff !important;
            font-size: 3rem;
            font-weight: 900;
        }

        .recommendation-card {
            padding: 16px 18px;
            margin: 10px 0;
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border);
            border-left: 5px solid var(--ctr-primary);
            border-radius: 12px;
            background: #ffffff !important;
            box-shadow: 0 6px 18px rgba(17, 57, 71, 0.08);
        }

        [data-testid="stDataFrame"] {
            color: var(--ctr-text) !important;
            background: #ffffff !important;
        }

        [data-testid="stToggle"] label,
        [data-testid="stToggle"] label p {
            color: var(--ctr-text) !important;
            font-weight: 750 !important;
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            .ctr-hero {
                padding: 27px 23px;
                border-radius: 18px;
            }

            .ctr-hero h1 {
                font-size: 2rem;
            }

            .question-heading {
                min-height: auto;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DADOS DO CHECKLIST
# ============================================================

DIMENSOES = [
    {
        "codigo": "GV",
        "nome": "Governar",
        "nist": "NIST CSF 2.0 — Govern",
        "descricao": (
            "Estratégia, políticas, responsabilidades e gestão de riscos."
        ),
        "perguntas": [
            (
                "A organização possui uma política de segurança da "
                "informação formalmente aprovada?"
            ),
            (
                "As responsabilidades de segurança cibernética estão "
                "claramente definidas?"
            ),
            (
                "Os riscos cibernéticos são considerados nas decisões "
                "estratégicas da organização?"
            ),
            (
                "Fornecedores e terceiros são avaliados quanto aos riscos "
                "de segurança cibernética?"
            ),
        ],
    },
    {
        "codigo": "ID",
        "nome": "Identificar",
        "nist": "NIST CSF 2.0 — Identify",
        "descricao": (
            "Ativos, riscos, vulnerabilidades e dependências críticas."
        ),
        "perguntas": [
            (
                "A organização mantém um inventário atualizado de "
                "dispositivos, sistemas e softwares?"
            ),
            (
                "Os dados e ativos críticos para o negócio estão "
                "identificados e classificados?"
            ),
            (
                "São realizadas avaliações periódicas de riscos e "
                "vulnerabilidades?"
            ),
            (
                "A organização conhece suas dependências críticas de "
                "fornecedores e serviços externos?"
            ),
        ],
    },
    {
        "codigo": "PR",
        "nome": "Proteger",
        "nist": "NIST CSF 2.0 — Protect",
        "descricao": (
            "Controles preventivos, acessos, treinamento, dados e tecnologia."
        ),
        "perguntas": [
            (
                "A autenticação multifator é utilizada em contas e "
                "sistemas críticos?"
            ),
            (
                "Os acessos são concedidos conforme a função e revisados "
                "periodicamente?"
            ),
            (
                "Sistemas operacionais e aplicações recebem atualizações "
                "de segurança regularmente?"
            ),
            (
                "Os colaboradores recebem treinamento periódico de "
                "conscientização em segurança?"
            ),
            (
                "Os dados críticos são protegidos por criptografia e "
                "cópias de segurança?"
            ),
        ],
    },
    {
        "codigo": "DE",
        "nome": "Detectar",
        "nist": "NIST CSF 2.0 — Detect",
        "descricao": (
            "Monitoramento, alertas e identificação de atividades suspeitas."
        ),
        "perguntas": [
            (
                "A organização monitora eventos e atividades suspeitas "
                "em seus sistemas?"
            ),
            (
                "Existem alertas para tentativas de acesso indevido ou "
                "comportamentos anormais?"
            ),
            (
                "Os registros de auditoria e logs são armazenados e "
                "revisados periodicamente?"
            ),
            (
                "Há um processo para analisar e priorizar alertas "
                "de segurança?"
            ),
        ],
    },
    {
        "codigo": "RS",
        "nome": "Responder",
        "nist": "NIST CSF 2.0 — Respond",
        "descricao": (
            "Planos, comunicação, contenção e tratamento de incidentes."
        ),
        "perguntas": [
            (
                "Existe um plano documentado de resposta a incidentes "
                "cibernéticos?"
            ),
            (
                "Os responsáveis sabem como agir e quem comunicar durante "
                "um incidente?"
            ),
            (
                "O plano de resposta a incidentes é testado por meio de "
                "exercícios periódicos?"
            ),
            (
                "A organização possui procedimentos para conter e "
                "investigar incidentes?"
            ),
        ],
    },
    {
        "codigo": "RC",
        "nome": "Recuperar",
        "nist": "NIST CSF 2.0 — Recover",
        "descricao": (
            "Continuidade, restauração, backups e melhoria após incidentes."
        ),
        "perguntas": [
            (
                "Existem backups regulares dos dados e sistemas críticos?"
            ),
            (
                "As cópias de segurança são testadas periodicamente para "
                "confirmar sua restauração?"
            ),
            (
                "A organização possui um plano de continuidade e "
                "recuperação de desastres?"
            ),
            (
                "As lições aprendidas após incidentes são utilizadas para "
                "melhorar os controles?"
            ),
        ],
    },
]

OPCOES = {
    "Não avaliado": None,
    "0 — Inexistente": 0,
    "1 — Inicial": 1,
    "2 — Parcial": 2,
    "3 — Implementado": 3,
    "4 — Gerenciado": 4,
    "5 — Otimizado": 5,
}

TOTAL_PERGUNTAS = sum(
    len(dimensao["perguntas"])
    for dimensao in DIMENSOES
)


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def texto_seguro(valor):
    return html.escape(str(valor).strip())


def nome_arquivo_seguro(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^a-zA-Z0-9_-]+", "_", texto)
    texto = re.sub(r"_+", "_", texto)

    return texto.strip("_").lower() or "organizacao"


def obter_nivel(percentual):
    if percentual < 20:
        return (
            "Crítico",
            "Controles fundamentais inexistentes ou insuficientes.",
        )

    if percentual < 40:
        return (
            "Inicial",
            "Práticas pontuais, informais e predominantemente reativas.",
        )

    if percentual < 60:
        return (
            "Em desenvolvimento",
            "Controles parcialmente implementados e ainda inconsistentes.",
        )

    if percentual < 80:
        return (
            "Gerenciado",
            "Controles consistentes, documentados e acompanhados.",
        )

    return (
        "Otimizado",
        "Práticas maduras, mensuradas e continuamente aprimoradas.",
    )


def obter_prioridade(percentual, avaliadas):
    if avaliadas == 0:
        return "Não avaliada"

    if percentual < 40:
        return "Alta"

    if percentual < 70:
        return "Média"

    return "Baixa"


def recomendacao_dimensao(codigo):
    recomendacoes = {
        "GV": (
            "Formalize políticas, responsabilidades, indicadores e critérios "
            "de risco cibernético, incluindo fornecedores e terceiros."
        ),
        "ID": (
            "Atualize o inventário de ativos, classifique dados críticos e "
            "execute avaliações regulares de riscos e vulnerabilidades."
        ),
        "PR": (
            "Priorize autenticação multifator, gestão de acessos, correções "
            "de segurança, backups e capacitação dos colaboradores."
        ),
        "DE": (
            "Centralize logs, configure alertas e estabeleça uma rotina de "
            "monitoramento e análise de eventos suspeitos."
        ),
        "RS": (
            "Documente e teste o plano de resposta a incidentes, definindo "
            "papéis, comunicação, contenção e investigação."
        ),
        "RC": (
            "Teste a restauração dos backups e mantenha planos atualizados "
            "de continuidade e recuperação de desastres."
        ),
    }

    return recomendacoes.get(
        codigo,
        "Revisar os controles da dimensão.",
    )


def limpar_sessao():
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]

    st.rerun()


# ============================================================
# GRÁFICOS
# ============================================================

def criar_grafico_colunas(resultados):
    nomes = [
        resultado["dimensao"]
        for resultado in resultados
    ]

    percentuais = [
        resultado["percentual"]
        for resultado in resultados
    ]

    cores_barras = []

    for resultado in resultados:
        if resultado["avaliadas"] == 0:
            cores_barras.append("#A8B8BE")
        elif resultado["percentual"] < 40:
            cores_barras.append("#D9534F")
        elif resultado["percentual"] < 70:
            cores_barras.append("#E6A23C")
        else:
            cores_barras.append("#11A88F")

    figura, eixo = plt.subplots(figsize=(10, 5.5))
    figura.patch.set_facecolor("white")
    eixo.set_facecolor("white")

    barras = eixo.bar(
        nomes,
        percentuais,
        color=cores_barras,
        width=0.65,
    )

    eixo.set_title(
        "Maturidade por dimensão",
        fontsize=16,
        fontweight="bold",
        color="#102F3B",
        pad=18,
    )

    eixo.set_ylabel(
        "Maturidade (%)",
        color="#102F3B",
    )

    eixo.set_ylim(0, 110)
    eixo.grid(
        axis="y",
        linestyle="--",
        alpha=0.25,
    )

    eixo.set_axisbelow(True)
    eixo.spines["top"].set_visible(False)
    eixo.spines["right"].set_visible(False)

    for barra, resultado in zip(barras, resultados):
        texto = (
            f'{resultado["percentual"]:.1f}%'
            if resultado["avaliadas"] > 0
            else "N/A"
        )

        eixo.text(
            barra.get_x() + barra.get_width() / 2,
            barra.get_height() + 2,
            texto,
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#102F3B",
        )

    figura.tight_layout()

    return figura


def criar_grafico_pizza(resultados):
    resultados_avaliados = [
        resultado
        for resultado in resultados
        if resultado["avaliadas"] > 0
    ]

    if not resultados_avaliados:
        nomes = [
            resultado["dimensao"]
            for resultado in resultados
        ]

        valores = [1] * len(resultados)
        titulo = "Dimensões do checklist"
    else:
        nomes = [
            resultado["dimensao"]
            for resultado in resultados_avaliados
        ]

        valores = [
            resultado["pontos"]
            for resultado in resultados_avaliados
        ]

        if sum(valores) == 0:
            valores = [
                resultado["avaliadas"]
                for resultado in resultados_avaliados
            ]

            titulo = "Distribuição das perguntas avaliadas"
        else:
            titulo = "Distribuição dos pontos por dimensão"

    paleta = [
        "#047F9E",
        "#11A88F",
        "#35A7C8",
        "#64C7B5",
        "#E6A23C",
        "#6A7FDB",
    ]

    figura, eixo = plt.subplots(figsize=(8, 6.2))
    figura.patch.set_facecolor("white")
    eixo.set_facecolor("white")

    eixo.pie(
        valores,
        labels=nomes,
        colors=paleta[:len(valores)],
        autopct=lambda valor: f"{valor:.1f}%",
        startangle=90,
        pctdistance=0.76,
        wedgeprops={
            "edgecolor": "white",
            "linewidth": 2,
        },
        textprops={
            "fontsize": 9,
            "color": "#102F3B",
        },
    )

    circulo = plt.Circle(
        (0, 0),
        0.48,
        color="white",
    )

    eixo.add_artist(circulo)

    eixo.text(
        0,
        0.05,
        "CTR",
        ha="center",
        va="center",
        fontsize=19,
        fontweight="bold",
        color="#047F9E",
    )

    eixo.text(
        0,
        -0.11,
        "CyberCheck",
        ha="center",
        va="center",
        fontsize=10,
        color="#496570",
    )

    eixo.set_title(
        titulo,
        fontsize=15,
        fontweight="bold",
        color="#102F3B",
        pad=18,
    )

    figura.tight_layout()

    return figura


def figura_para_png(figura, dpi=180):
    imagem = io.BytesIO()

    figura.savefig(
        imagem,
        format="png",
        dpi=dpi,
        bbox_inches="tight",
        facecolor="white",
    )

    imagem.seek(0)

    return imagem


# ============================================================
# CSV
# ============================================================

def montar_csv_completo(
    empresa,
    resultados,
    respostas_detalhadas,
    percentual_geral,
    nivel,
    descricao_nivel,
    pontos_totais,
    maximo_total,
):
    arquivo = io.StringIO()

    escritor = csv.writer(
        arquivo,
        delimiter=";",
        quoting=csv.QUOTE_MINIMAL,
    )

    escritor.writerow(
        ["CTR CyberCheck - Relatório de Maturidade Cibernética"]
    )

    escritor.writerow(
        [
            "Data da avaliação",
            datetime.now().strftime("%d/%m/%Y %H:%M"),
        ]
    )

    escritor.writerow(
        [
            "Armazenamento",
            (
                "Não há armazenamento persistente; os dados foram "
                "processados somente durante a sessão."
            ),
        ]
    )

    escritor.writerow(
        [
            "Confidencialidade",
            (
                "Este relatório pode conter informações confidenciais "
                "e deve ser acessado somente por pessoas autorizadas."
            ),
        ]
    )

    escritor.writerow(["Organização", empresa["organizacao"]])
    escritor.writerow(["Responsável", empresa["responsavel"]])
    escritor.writerow(["E-mail", empresa["email"]])
    escritor.writerow(["Setor", empresa["setor"]])
    escritor.writerow(["Porte", empresa["porte"]])
    escritor.writerow(["Observações", empresa["observacoes"]])
    escritor.writerow(["Maturidade geral", f"{percentual_geral:.1f}%"])
    escritor.writerow(["Classificação", nivel])
    escritor.writerow(["Descrição", descricao_nivel])

    escritor.writerow(
        [
            "Pontuação geral",
            f"{pontos_totais}/{maximo_total}",
        ]
    )

    escritor.writerow([])
    escritor.writerow(["RESULTADO POR DIMENSÃO"])

    escritor.writerow(
        [
            "Código",
            "Dimensão",
            "Referência",
            "Perguntas avaliadas",
            "Pontos obtidos",
            "Pontos máximos",
            "Maturidade",
            "Prioridade",
            "Recomendação",
        ]
    )

    for resultado in resultados:
        escritor.writerow(
            [
                resultado["codigo"],
                resultado["dimensao"],
                resultado["nist"],
                resultado["avaliadas"],
                resultado["pontos"],
                resultado["maximo"],
                (
                    f'{resultado["percentual"]:.1f}%'
                    if resultado["avaliadas"] > 0
                    else "Não avaliada"
                ),
                resultado["prioridade"],
                recomendacao_dimensao(resultado["codigo"]),
            ]
        )

    escritor.writerow([])
    escritor.writerow(["CHECKLIST COMPLETO"])

    escritor.writerow(
        [
            "Número",
            "Código",
            "Dimensão",
            "Referência NIST CSF",
            "Pergunta",
            "Resposta",
            "Pontuação",
            "Status",
        ]
    )

    for resposta in respostas_detalhadas:
        pontuacao = resposta["pontuacao"]

        escritor.writerow(
            [
                resposta["numero"],
                resposta["codigo"],
                resposta["dimensao"],
                resposta["nist"],
                resposta["pergunta"],
                resposta["resposta"],
                pontuacao if pontuacao is not None else "",
                (
                    "Avaliado"
                    if pontuacao is not None
                    else "Não avaliado"
                ),
            ]
        )

    return arquivo.getvalue().encode("utf-8-sig")


# ============================================================
# PDF
# ============================================================

def adicionar_rodape_pdf(canvas, documento):
    canvas.saveState()

    largura, _ = landscape(A4)

    canvas.setStrokeColor(
        colors.HexColor("#BFD8E1")
    )

    canvas.line(
        1.2 * cm,
        1.05 * cm,
        largura - 1.2 * cm,
        1.05 * cm,
    )

    canvas.setFont(
        "Helvetica",
        8,
    )

    canvas.setFillColor(
        colors.HexColor("#496570")
    )

    canvas.drawString(
        1.2 * cm,
        0.65 * cm,
        "CTR CyberCheck - Relatório de maturidade cibernética",
    )

    canvas.drawRightString(
        largura - 1.2 * cm,
        0.65 * cm,
        f"Página {documento.page}",
    )

    canvas.restoreState()


def montar_pdf(
    empresa,
    resultados,
    respostas_detalhadas,
    percentual_geral,
    nivel,
    descricao_nivel,
    pontos_totais,
    maximo_total,
    respondidas,
    total_perguntas,
):
    arquivo_pdf = io.BytesIO()

    documento = SimpleDocTemplate(
        arquivo_pdf,
        pagesize=landscape(A4),
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.5 * cm,
        title="CTR CyberCheck - Relatório de Maturidade",
        author="CTR CyberCheck",
    )

    estilos = getSampleStyleSheet()

    estilo_titulo = ParagraphStyle(
        "TituloCTR",
        parent=estilos["Title"],
        fontName="Helvetica-Bold",
        fontSize=25,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#047F9E"),
        spaceAfter=8,
    )

    estilo_subtitulo = ParagraphStyle(
        "SubtituloCTR",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#496570"),
        spaceAfter=18,
    )

    estilo_secao = ParagraphStyle(
        "SecaoCTR",
        parent=estilos["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.HexColor("#102F3B"),
        spaceBefore=10,
        spaceAfter=10,
    )

    estilo_normal = ParagraphStyle(
        "NormalCTR",
        parent=estilos["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#102F3B"),
    )

    estilo_celula = ParagraphStyle(
        "CelulaCTR",
        parent=estilo_normal,
        fontSize=7.2,
        leading=9,
        alignment=TA_LEFT,
    )

    estilo_celula_central = ParagraphStyle(
        "CelulaCentralCTR",
        parent=estilo_celula,
        alignment=TA_CENTER,
    )

    estilo_resumo = ParagraphStyle(
        "ResumoCTR",
        parent=estilos["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=17,
        alignment=TA_CENTER,
        textColor=colors.white,
    )

    estilo_privacidade = ParagraphStyle(
        "PrivacidadeCTR",
        parent=estilo_normal,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#164D44"),
        borderColor=colors.HexColor("#91CFC2"),
        borderWidth=0.7,
        borderPadding=8,
        backColor=colors.HexColor("#EAF9F5"),
        spaceAfter=10,
    )

    elementos = [
        Paragraph(
            "CTR CyberCheck",
            estilo_titulo,
        ),
        Paragraph(
            (
                "Relatório de avaliação de maturidade cibernética "
                "baseado no NIST Cybersecurity Framework 2.0"
            ),
            estilo_subtitulo,
        ),
    ]

    dados_empresa = [
        [
            Paragraph("<b>Organização</b>", estilo_normal),
            Paragraph(
                html.escape(empresa["organizacao"] or "-"),
                estilo_normal,
            ),
            Paragraph("<b>Data</b>", estilo_normal),
            Paragraph(
                datetime.now().strftime("%d/%m/%Y %H:%M"),
                estilo_normal,
            ),
        ],
        [
            Paragraph("<b>Responsável</b>", estilo_normal),
            Paragraph(
                html.escape(empresa["responsavel"] or "-"),
                estilo_normal,
            ),
            Paragraph("<b>E-mail</b>", estilo_normal),
            Paragraph(
                html.escape(empresa["email"] or "-"),
                estilo_normal,
            ),
        ],
        [
            Paragraph("<b>Setor</b>", estilo_normal),
            Paragraph(
                html.escape(empresa["setor"] or "-"),
                estilo_normal,
            ),
            Paragraph("<b>Porte</b>", estilo_normal),
            Paragraph(
                html.escape(empresa["porte"] or "-"),
                estilo_normal,
            ),
        ],
        [
            Paragraph("<b>Observações</b>", estilo_normal),
            Paragraph(
                html.escape(empresa["observacoes"] or "-"),
                estilo_normal,
            ),
            "",
            "",
        ],
    ]

    tabela_empresa = Table(
        dados_empresa,
        colWidths=[
            3.2 * cm,
            8.8 * cm,
            2.5 * cm,
            10.2 * cm,
        ],
    )

    tabela_empresa.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#DFF3F7"),
                ),
                (
                    "BACKGROUND",
                    (2, 0),
                    (2, -1),
                    colors.HexColor("#DFF3F7"),
                ),
                ("SPAN", (1, 3), (3, 3)),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#BFD8E1"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elementos.append(tabela_empresa)
    elementos.append(Spacer(1, 0.4 * cm))

    elementos.append(
        Paragraph(
            (
                "<b>Privacidade e confidencialidade:</b> "
                "este relatório foi gerado em memória durante a sessão. "
                "O sistema não possui banco de dados nem armazenamento "
                "persistente das informações preenchidas. O documento "
                "pode conter informações confidenciais e deve ser "
                "armazenado e compartilhado somente com pessoas autorizadas."
            ),
            estilo_privacidade,
        )
    )

    elementos.append(Spacer(1, 0.2 * cm))

    resumo = [
        [
            Paragraph(
                (
                    "Maturidade geral<br/>"
                    f"<font size='22'>{percentual_geral:.1f}%</font>"
                ),
                estilo_resumo,
            ),
            Paragraph(
                (
                    "Classificação<br/>"
                    f"<font size='15'>{html.escape(nivel)}</font>"
                ),
                estilo_resumo,
            ),
            Paragraph(
                (
                    "Pontuação<br/>"
                    f"<font size='15'>{pontos_totais}/{maximo_total}</font>"
                ),
                estilo_resumo,
            ),
            Paragraph(
                (
                    "Perguntas avaliadas<br/>"
                    f"<font size='15'>{respondidas}/{total_perguntas}</font>"
                ),
                estilo_resumo,
            ),
        ]
    ]

    tabela_resumo = Table(
        resumo,
        colWidths=[6.2 * cm] * 4,
        rowHeights=[2.4 * cm],
    )

    tabela_resumo.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#0B2633"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.HexColor("#047F9E"),
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#547986"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    elementos.append(tabela_resumo)
    elementos.append(Spacer(1, 0.3 * cm))

    elementos.append(
        Paragraph(
            html.escape(descricao_nivel),
            estilo_normal,
        )
    )

    elementos.append(Spacer(1, 0.35 * cm))

    figura_colunas = criar_grafico_colunas(resultados)
    imagem_colunas = figura_para_png(figura_colunas)
    plt.close(figura_colunas)

    figura_pizza = criar_grafico_pizza(resultados)
    imagem_pizza = figura_para_png(figura_pizza)
    plt.close(figura_pizza)

    tabela_graficos = Table(
        [
            [
                Image(
                    imagem_colunas,
                    width=13.2 * cm,
                    height=7.2 * cm,
                ),
                Image(
                    imagem_pizza,
                    width=10.2 * cm,
                    height=7.8 * cm,
                ),
            ]
        ],
        colWidths=[
            14 * cm,
            11 * cm,
        ],
    )

    tabela_graficos.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ]
        )
    )

    elementos.append(tabela_graficos)
    elementos.append(PageBreak())

    elementos.append(
        Paragraph(
            "Resultado por dimensão",
            estilo_secao,
        )
    )

    dados_dimensoes = [
        [
            Paragraph("<b>Dimensão</b>", estilo_celula_central),
            Paragraph("<b>Referência</b>", estilo_celula_central),
            Paragraph("<b>Avaliadas</b>", estilo_celula_central),
            Paragraph("<b>Pontos</b>", estilo_celula_central),
            Paragraph("<b>Maturidade</b>", estilo_celula_central),
            Paragraph("<b>Prioridade</b>", estilo_celula_central),
            Paragraph("<b>Recomendação</b>", estilo_celula_central),
        ]
    ]

    for resultado in resultados:
        maturidade = (
            f'{resultado["percentual"]:.1f}%'
            if resultado["avaliadas"] > 0
            else "Não avaliada"
        )

        dados_dimensoes.append(
            [
                Paragraph(
                    html.escape(resultado["dimensao"]),
                    estilo_celula,
                ),
                Paragraph(
                    html.escape(resultado["nist"]),
                    estilo_celula,
                ),
                Paragraph(
                    str(resultado["avaliadas"]),
                    estilo_celula_central,
                ),
                Paragraph(
                    (
                        f'{resultado["pontos"]}/{resultado["maximo"]}'
                        if resultado["maximo"] > 0
                        else "-"
                    ),
                    estilo_celula_central,
                ),
                Paragraph(
                    maturidade,
                    estilo_celula_central,
                ),
                Paragraph(
                    html.escape(resultado["prioridade"]),
                    estilo_celula_central,
                ),
                Paragraph(
                    html.escape(
                        recomendacao_dimensao(resultado["codigo"])
                    ),
                    estilo_celula,
                ),
            ]
        )

    tabela_dimensoes = Table(
        dados_dimensoes,
        repeatRows=1,
        colWidths=[
            2.5 * cm,
            4.1 * cm,
            1.7 * cm,
            1.8 * cm,
            2 * cm,
            1.8 * cm,
            11.2 * cm,
        ],
    )

    tabela_dimensoes.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0B2633"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#EDF0F2"),
                    ],
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.45,
                    colors.HexColor("#BFD8E1"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elementos.append(tabela_dimensoes)
    elementos.append(PageBreak())

    elementos.append(
        Paragraph(
            "Checklist completo",
            estilo_secao,
        )
    )

    dados_checklist = [
        [
            Paragraph("<b>Nº</b>", estilo_celula_central),
            Paragraph("<b>Dimensão</b>", estilo_celula_central),
            Paragraph("<b>Referência</b>", estilo_celula_central),
            Paragraph("<b>Pergunta</b>", estilo_celula_central),
            Paragraph("<b>Resposta</b>", estilo_celula_central),
            Paragraph("<b>Pontos</b>", estilo_celula_central),
            Paragraph("<b>Status</b>", estilo_celula_central),
        ]
    ]

    for resposta in respostas_detalhadas:
        avaliada = resposta["pontuacao"] is not None

        dados_checklist.append(
            [
                Paragraph(
                    str(resposta["numero"]),
                    estilo_celula_central,
                ),
                Paragraph(
                    html.escape(resposta["dimensao"]),
                    estilo_celula,
                ),
                Paragraph(
                    html.escape(resposta["nist"]),
                    estilo_celula,
                ),
                Paragraph(
                    html.escape(resposta["pergunta"]),
                    estilo_celula,
                ),
                Paragraph(
                    html.escape(resposta["resposta"]),
                    estilo_celula,
                ),
                Paragraph(
                    (
                        str(resposta["pontuacao"])
                        if avaliada
                        else "-"
                    ),
                    estilo_celula_central,
                ),
                Paragraph(
                    (
                        "Avaliado"
                        if avaliada
                        else "Não avaliado"
                    ),
                    estilo_celula_central,
                ),
            ]
        )

    tabela_checklist_pdf = Table(
        dados_checklist,
        repeatRows=1,
        colWidths=[
            1 * cm,
            2.6 * cm,
            3.7 * cm,
            9.8 * cm,
            3.4 * cm,
            1.4 * cm,
            2.4 * cm,
        ],
    )

    tabela_checklist_pdf.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#0B2633"),
                ),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F0F2F3"),
                    ],
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#BFD8E1"),
                ),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    elementos.append(tabela_checklist_pdf)
    elementos.append(Spacer(1, 0.5 * cm))

    elementos.append(
        Paragraph(
            "Observação metodológica",
            estilo_secao,
        )
    )

    elementos.append(
        Paragraph(
            (
                "O resultado é orientativo e considera somente as perguntas "
                "efetivamente avaliadas. Ele não substitui auditoria técnica, "
                "análise de vulnerabilidades, teste de invasão, análise "
                "jurídica ou avaliação especializada de conformidade."
            ),
            estilo_normal,
        )
    )

    documento.build(
        elementos,
        onFirstPage=adicionar_rodape_pdf,
        onLaterPages=adicionar_rodape_pdf,
    )

    arquivo_pdf.seek(0)

    return arquivo_pdf.getvalue()


# ============================================================
# ESTADO
# ============================================================

if "resultado_calculado" not in st.session_state:
    st.session_state.resultado_calculado = False


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    """
    <section class="ctr-hero">
        <div class="ctr-badge">
            Avaliação de maturidade cibernética
        </div>

        <h1>CTR <span>CyberCheck</span></h1>

        <p>
            Avalie a maturidade de segurança cibernética da organização
            com base nas seis funções do NIST Cybersecurity Framework 2.0:
            Governar, Identificar, Proteger, Detectar, Responder e Recuperar.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# AVISOS DE PRIVACIDADE
# ============================================================

st.markdown(
    """
    <div class="ctr-session-notice">
        <strong>⚠️ Sistema sem armazenamento persistente</strong>
        <br><br>
        O CTR CyberCheck não possui banco de dados e não salva
        permanentemente as informações preenchidas. Os dados são
        processados somente na memória durante a sessão atual.
        <br><br>
        As informações poderão ser perdidas ao atualizar a página,
        fechar o navegador, encerrar a sessão ou reiniciar o servidor.
        Exporte os relatórios necessários antes de sair da aplicação.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="ctr-privacy-notice">
        <strong>🔒 LGPD e confidencialidade</strong>
        <br><br>
        Utilize somente as informações necessárias para a avaliação,
        observando os princípios de finalidade, adequação, necessidade,
        segurança, prevenção e responsabilização previstos na LGPD.
        <br><br>
        Não informe senhas, credenciais, chaves de acesso, CPF,
        dados pessoais sensíveis, segredos comerciais ou detalhes
        técnicos desnecessários. Os relatórios exportados podem conter
        informações confidenciais e devem ser armazenados e
        compartilhados apenas com pessoas autorizadas.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DADOS DA ORGANIZAÇÃO — SEM ST.EXPANDER
# ============================================================

with st.container(border=True):
    st.markdown(
        """
        <div class="ctr-panel-header">
            <div class="ctr-panel-title">
                🏢 Dados da organização
            </div>

            <p class="ctr-panel-description">
                Informe somente os dados institucionais necessários
                para identificar a avaliação. Evite dados pessoais,
                informações sensíveis e detalhes confidenciais
                desnecessários.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    coluna_1, coluna_2 = st.columns(2)

    with coluna_1:
        organizacao = st.text_input(
            "Nome da organização *",
            placeholder="Ex.: Empresa Exemplo Ltda.",
            key="organizacao",
        )

    with coluna_2:
        responsavel = st.text_input(
            "Responsável pela avaliação",
            placeholder="Nome ou função do responsável",
            key="responsavel",
        )

    coluna_3, coluna_4, coluna_5 = st.columns(3)

    with coluna_3:
        email = st.text_input(
            "E-mail corporativo opcional",
            placeholder="responsavel@empresa.com",
            key="email",
            help=(
                "O e-mail permanece somente durante a sessão. "
                "Informe-o apenas se for necessário ao relatório."
            ),
        )

    with coluna_4:
        setor = st.selectbox(
            "Setor",
            [
                "Selecione",
                "Agronegócio",
                "Comércio",
                "Educação",
                "Energia",
                "Financeiro",
                "Governo",
                "Indústria",
                "Saúde",
                "Serviços",
                "Tecnologia",
                "Outro",
            ],
            key="setor",
        )

    with coluna_5:
        porte = st.selectbox(
            "Porte da organização",
            [
                "Selecione",
                "Microempresa",
                "Pequena empresa",
                "Média empresa",
                "Grande empresa",
            ],
            key="porte",
        )

    observacoes = st.text_area(
        "Observações não sensíveis",
        placeholder=(
            "Registre somente informações necessárias e não "
            "confidenciais sobre o contexto da avaliação."
        ),
        height=90,
        key="observacoes",
    )

    ciencia_privacidade = st.checkbox(
        (
            "Estou ciente de que os dados são temporários e não "
            "inserirei credenciais, dados pessoais sensíveis ou "
            "informações confidenciais desnecessárias."
        ),
        key="ciencia_privacidade",
    )


# ============================================================
# ESCALA
# ============================================================

st.markdown("### Como responder")

st.write(
    "Escolha a opção que melhor representa a situação atual da organização. "
    "Quando não houver informação suficiente, mantenha **Não avaliado**."
)

st.markdown(
    """
    <div class="ctr-scale">
        <div class="ctr-scale-item">
            <strong>0</strong> Inexistente
        </div>

        <div class="ctr-scale-item">
            <strong>1</strong> Inicial e informal
        </div>

        <div class="ctr-scale-item">
            <strong>2</strong> Parcialmente aplicado
        </div>

        <div class="ctr-scale-item">
            <strong>3</strong> Implementado
        </div>

        <div class="ctr-scale-item">
            <strong>4</strong> Gerenciado
        </div>

        <div class="ctr-scale-item">
            <strong>5</strong> Otimizado
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# QUESTIONÁRIO
# ============================================================

numero_global = 1
chaves_respostas = []

for indice_dimensao, dimensao in enumerate(
    DIMENSOES,
    start=1,
):
    st.markdown(
        f"""
        <div class="dimension-header">
            <div class="dimension-number">
                {indice_dimensao}
            </div>

            <div>
                <div class="dimension-title">
                    {texto_seguro(dimensao["nome"])}
                </div>

                <div class="dimension-description">
                    {texto_seguro(dimensao["descricao"])}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    perguntas = dimensao["perguntas"]

    for inicio in range(0, len(perguntas), 2):
        colunas = st.columns(
            2,
            gap="large",
        )

        for deslocamento, coluna in enumerate(colunas):
            indice_pergunta = inicio + deslocamento

            if indice_pergunta >= len(perguntas):
                continue

            pergunta = perguntas[indice_pergunta]

            chave = (
                f'resposta_{dimensao["codigo"]}_'
                f'{indice_pergunta}'
            )

            chaves_respostas.append(chave)

            with coluna:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div class="question-heading">
                            <div class="question-number">
                                {numero_global}
                            </div>

                            <div>
                                <div class="question-text">
                                    {texto_seguro(pergunta)}
                                </div>

                                <div class="nist-badge">
                                    {texto_seguro(dimensao["nist"])}
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.radio(
                        "Selecione o nível",
                        options=list(OPCOES.keys()),
                        index=0,
                        key=chave,
                        label_visibility="collapsed",
                    )

            numero_global += 1


# ============================================================
# PROGRESSO
# ============================================================

respondidas = sum(
    1
    for chave in chaves_respostas
    if OPCOES.get(
        st.session_state.get(
            chave,
            "Não avaliado",
        )
    ) is not None
)

progresso = (
    respondidas / TOTAL_PERGUNTAS
    if TOTAL_PERGUNTAS > 0
    else 0
)

st.markdown("### Progresso da avaliação")

st.progress(progresso)

st.caption(
    f"{respondidas} de {TOTAL_PERGUNTAS} perguntas avaliadas "
    f"({progresso * 100:.0f}%)."
)


# ============================================================
# BOTÕES
# ============================================================

coluna_calcular, coluna_limpar = st.columns([3, 1])

with coluna_calcular:
    calcular = st.button(
        "Calcular resultado",
        type="primary",
        use_container_width=True,
    )

with coluna_limpar:
    limpar = st.button(
        "Limpar sessão",
        use_container_width=True,
        help=(
            "Apaga todos os dados mantidos temporariamente "
            "na sessão atual."
        ),
    )

if limpar:
    limpar_sessao()

if calcular:
    if not organizacao.strip():
        st.error(
            "Informe o nome da organização antes de calcular o resultado."
        )
    elif not st.session_state.get(
        "ciencia_privacidade",
        False,
    ):
        st.error(
            "Confirme a ciência sobre o processamento temporário, "
            "a LGPD e a confidencialidade das informações."
        )
    elif respondidas == 0:
        st.error(
            "Responda pelo menos uma pergunta antes de calcular o resultado."
        )
    else:
        st.session_state.resultado_calculado = True


# ============================================================
# RESULTADO
# ============================================================

if (
    st.session_state.resultado_calculado
    and organizacao.strip()
    and respondidas > 0
):
    resultados = []
    respostas_detalhadas = []

    pontos_totais = 0
    maximo_total = 0
    numero_resposta = 1

    for dimensao in DIMENSOES:
        pontos_dimensao = 0
        perguntas_avaliadas = 0

        for indice_pergunta, pergunta in enumerate(
            dimensao["perguntas"]
        ):
            chave = (
                f'resposta_{dimensao["codigo"]}_'
                f'{indice_pergunta}'
            )

            resposta_texto = st.session_state.get(
                chave,
                "Não avaliado",
            )

            pontuacao = OPCOES.get(resposta_texto)

            if pontuacao is not None:
                pontos_dimensao += pontuacao
                perguntas_avaliadas += 1

            respostas_detalhadas.append(
                {
                    "numero": numero_resposta,
                    "codigo": dimensao["codigo"],
                    "dimensao": dimensao["nome"],
                    "nist": dimensao["nist"],
                    "pergunta": pergunta,
                    "resposta": resposta_texto,
                    "pontuacao": pontuacao,
                }
            )

            numero_resposta += 1

        maximo_dimensao = perguntas_avaliadas * 5

        percentual_dimensao = (
            pontos_dimensao / maximo_dimensao * 100
            if maximo_dimensao > 0
            else 0
        )

        prioridade = obter_prioridade(
            percentual_dimensao,
            perguntas_avaliadas,
        )

        resultados.append(
            {
                "codigo": dimensao["codigo"],
                "dimensao": dimensao["nome"],
                "nist": dimensao["nist"],
                "pontos": pontos_dimensao,
                "maximo": maximo_dimensao,
                "avaliadas": perguntas_avaliadas,
                "percentual": percentual_dimensao,
                "prioridade": prioridade,
            }
        )

        pontos_totais += pontos_dimensao
        maximo_total += maximo_dimensao

    percentual_geral = (
        pontos_totais / maximo_total * 100
        if maximo_total > 0
        else 0
    )

    nivel, descricao_nivel = obter_nivel(
        percentual_geral
    )

    st.markdown(
        f"""
        <div class="result-card">
            <h2>Resultado da avaliação</h2>

            <div class="result-score">
                {percentual_geral:.1f}%
            </div>

            <h3>Nível: {texto_seguro(nivel)}</h3>

            <p>
                {texto_seguro(descricao_nivel)}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Visão geral")

    metrica_1, metrica_2, metrica_3, metrica_4 = st.columns(4)

    metrica_1.metric(
        "Maturidade geral",
        f"{percentual_geral:.1f}%",
    )

    metrica_2.metric(
        "Pontuação",
        f"{pontos_totais}/{maximo_total}",
    )

    metrica_3.metric(
        "Perguntas avaliadas",
        f"{respondidas}/{TOTAL_PERGUNTAS}",
    )

    metrica_4.metric(
        "Classificação",
        nivel,
    )

    # --------------------------------------------------------
    # GRÁFICOS
    # --------------------------------------------------------

    st.markdown("### Gráficos da avaliação")

    figura_colunas_tela = criar_grafico_colunas(
        resultados
    )

    figura_pizza_tela = criar_grafico_pizza(
        resultados
    )

    coluna_grafico_1, coluna_grafico_2 = st.columns(
        2,
        gap="large",
    )

    with coluna_grafico_1:
        st.markdown("#### Gráfico de colunas")

        st.pyplot(
            figura_colunas_tela,
            use_container_width=True,
        )

    with coluna_grafico_2:
        st.markdown("#### Gráfico de pizza")

        st.pyplot(
            figura_pizza_tela,
            use_container_width=True,
        )

    plt.close(figura_colunas_tela)
    plt.close(figura_pizza_tela)

    # --------------------------------------------------------
    # RESULTADO POR DIMENSÃO
    # --------------------------------------------------------

    st.markdown("### Resultado por dimensão")

    tabela_resultados = pd.DataFrame(
        [
            {
                "Dimensão": resultado["dimensao"],
                "NIST CSF": resultado["nist"],
                "Avaliadas": resultado["avaliadas"],
                "Pontuação": (
                    f'{resultado["pontos"]}/'
                    f'{resultado["maximo"]}'
                    if resultado["maximo"] > 0
                    else "Não avaliada"
                ),
                "Maturidade": (
                    f'{resultado["percentual"]:.1f}%'
                    if resultado["avaliadas"] > 0
                    else "Não avaliada"
                ),
                "Prioridade": resultado["prioridade"],
            }
            for resultado in resultados
        ]
    )

    st.dataframe(
        tabela_resultados,
        use_container_width=True,
        hide_index=True,
    )

    # --------------------------------------------------------
    # CHECKLIST COMPLETO — SEM ST.EXPANDER
    # --------------------------------------------------------

    st.markdown("### Checklist completo")

    mostrar_checklist = st.toggle(
        "📋 Exibir todos os dados do checklist",
        value=False,
        key="mostrar_checklist",
    )

    if mostrar_checklist:
        tabela_checklist_tela = pd.DataFrame(
            [
                {
                    "Nº": resposta["numero"],
                    "Código": resposta["codigo"],
                    "Dimensão": resposta["dimensao"],
                    "Referência": resposta["nist"],
                    "Pergunta": resposta["pergunta"],
                    "Resposta": resposta["resposta"],
                    "Pontuação": (
                        resposta["pontuacao"]
                        if resposta["pontuacao"] is not None
                        else ""
                    ),
                    "Status": (
                        "Avaliado"
                        if resposta["pontuacao"] is not None
                        else "Não avaliado"
                    ),
                }
                for resposta in respostas_detalhadas
            ]
        )

        with st.container(border=True):
            st.dataframe(
                tabela_checklist_tela,
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.caption(
            "Ative a opção acima para visualizar "
            "as respostas detalhadas."
        )

    # --------------------------------------------------------
    # RECOMENDAÇÕES
    # --------------------------------------------------------

    st.markdown("### Recomendações prioritárias")

    resultados_ordenados = sorted(
        resultados,
        key=lambda item: (
            item["avaliadas"] == 0,
            item["percentual"],
        ),
    )

    for resultado in resultados_ordenados:
        if resultado["avaliadas"] == 0:
            status = "Dimensão não avaliada"
        else:
            status = (
                f'Maturidade de {resultado["percentual"]:.1f}% — '
                f'prioridade {resultado["prioridade"].lower()}'
            )

        recomendacao = recomendacao_dimensao(
            resultado["codigo"]
        )

        st.markdown(
            f"""
            <div class="recommendation-card">
                <strong>
                    {texto_seguro(resultado["dimensao"])}
                </strong>

                <br>
                {texto_seguro(status)}.

                <br>
                {texto_seguro(recomendacao)}
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # RELATÓRIOS
    # --------------------------------------------------------

    empresa = {
        "organizacao": organizacao.strip(),
        "responsavel": responsavel.strip(),
        "email": email.strip(),
        "setor": setor,
        "porte": porte,
        "observacoes": observacoes.strip(),
    }

    relatorio_csv = montar_csv_completo(
        empresa=empresa,
        resultados=resultados,
        respostas_detalhadas=respostas_detalhadas,
        percentual_geral=percentual_geral,
        nivel=nivel,
        descricao_nivel=descricao_nivel,
        pontos_totais=pontos_totais,
        maximo_total=maximo_total,
    )

    try:
        relatorio_pdf = montar_pdf(
            empresa=empresa,
            resultados=resultados,
            respostas_detalhadas=respostas_detalhadas,
            percentual_geral=percentual_geral,
            nivel=nivel,
            descricao_nivel=descricao_nivel,
            pontos_totais=pontos_totais,
            maximo_total=maximo_total,
            respondidas=respondidas,
            total_perguntas=TOTAL_PERGUNTAS,
        )

        erro_pdf = None
    except Exception as erro:
        relatorio_pdf = None
        erro_pdf = str(erro)

    identificador = nome_arquivo_seguro(
        organizacao.strip()
    )

    data_arquivo = datetime.now().strftime(
        "%Y%m%d_%H%M"
    )

    st.markdown("### Baixar relatórios")

    st.info(
        "Os relatórios são gerados exclusivamente em memória. "
        "Depois do download, a responsabilidade pela proteção, "
        "armazenamento, compartilhamento e descarte dos arquivos "
        "é do usuário."
    )

    coluna_csv, coluna_pdf = st.columns(2)

    with coluna_csv:
        st.download_button(
            label="📊 Baixar relatório completo em CSV",
            data=relatorio_csv,
            file_name=(
                f"ctr_cybercheck_{identificador}_"
                f"{data_arquivo}.csv"
            ),
            mime="text/csv",
            use_container_width=True,
        )

    with coluna_pdf:
        if relatorio_pdf is not None:
            st.download_button(
                label="📄 Baixar relatório completo em PDF",
                data=relatorio_pdf,
                file_name=(
                    f"ctr_cybercheck_{identificador}_"
                    f"{data_arquivo}.pdf"
                ),
                mime="application/pdf",
                use_container_width=True,
            )
        else:
            st.error(
                "Não foi possível gerar o PDF. "
                f"Detalhes: {erro_pdf}"
            )

    if respondidas < TOTAL_PERGUNTAS:
        st.warning(
            "O resultado considera somente as perguntas avaliadas. "
            f"Ainda existem {TOTAL_PERGUNTAS - respondidas} perguntas "
            "marcadas como “Não avaliado”."
        )


# ============================================================
# RODAPÉ
# ============================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True,
)

st.caption(
    "CTR CyberCheck • Avaliação orientativa baseada no NIST "
    "Cybersecurity Framework 2.0 • Sistema sem armazenamento "
    "persistente: os dados são processados somente durante a sessão. "
    "Os relatórios exportados devem ser tratados de acordo com as "
    "políticas de confidencialidade e proteção de dados da organização. "
    "O resultado não substitui auditoria técnica, análise jurídica ou "
    "avaliação especializada."
)
