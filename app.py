import io
import re
import unicodedata
from datetime import datetime

import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import font_manager
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
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
    page_title="CTR CyberCheck | CTR DEFENSE",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CSS PERSONALIZADO
# ============================================================

st.markdown(
    """
    <style>
        /* Importação da fonte */
        @import url(
            'https://fonts.googleapis.com/css2?'
            'family=Inter:wght@400;500;600;700;800&display=swap'
        );

        /* Variáveis visuais */
        :root {
            --ctr-primary: #00d4ff;
            --ctr-primary-dark: #008fb3;
            --ctr-secondary: #16a085;
            --ctr-dark: #07141d;
            --ctr-dark-light: #102631;
            --ctr-card: #ffffff;
            --ctr-card-soft: #f5fafc;
            --ctr-border: #cfe2e9;
            --ctr-text: #15313d;
            --ctr-muted: #536d78;
        }

        /* Fonte geral */
        html,
        body,
        [class*="css"],
        [data-testid="stAppViewContainer"] {
            font-family: "Inter", sans-serif;
        }

        /* Fundo da aplicação */
        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(
                    circle at top right,
                    rgba(0, 212, 255, 0.10),
                    transparent 30%
                ),
                linear-gradient(
                    180deg,
                    #f8fcfd 0%,
                    #edf6f8 100%
                );
        }

        /* Área principal */
        .block-container {
            max-width: 1500px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        /* Oculta elementos desnecessários */
        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        /* Cabeçalho principal */
        .ctr-hero {
            position: relative;
            overflow: hidden;
            padding: 36px 38px;
            margin-bottom: 26px;
            color: #ffffff;
            border: 1px solid rgba(0, 212, 255, 0.26);
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
                );
            box-shadow:
                0 24px 55px rgba(6, 32, 43, 0.22);
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
            color: #05151d;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08rem;
            text-transform: uppercase;
            border-radius: 999px;
            background: linear-gradient(
                90deg,
                #59e1fb,
                #87f1d7
            );
        }

        .ctr-hero h1 {
            margin: 0 0 10px 0;
            color: #ffffff;
            font-size: clamp(2rem, 4vw, 3.3rem);
            font-weight: 800;
            letter-spacing: -0.06rem;
        }

        .ctr-hero h1 span {
            color: #64e5ff;
        }

        .ctr-hero p {
            max-width: 850px;
            margin: 0;
            color: #d7e8ed;
            font-size: 1.08rem;
            line-height: 1.75;
        }

        /* Barra explicativa */
        .ctr-scale {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            padding: 16px;
            margin: 18px 0 26px 0;
            border: 1px solid var(--ctr-border);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.88);
            box-shadow: 0 8px 25px rgba(15, 55, 70, 0.06);
        }

        .ctr-scale-item {
            flex: 1;
            min-width: 180px;
            padding: 11px 13px;
            color: var(--ctr-muted);
            font-size: 0.88rem;
            font-weight: 600;
            border-radius: 11px;
            background: #eef7f9;
        }

        .ctr-scale-item strong {
            display: inline-block;
            margin-right: 5px;
            color: #ffffff;
            padding: 2px 8px;
            border-radius: 7px;
            background: var(--ctr-primary-dark);
        }

        /* Expander dos dados */
        [data-testid="stExpander"] {
            overflow: hidden;
            border: 1px solid var(--ctr-border);
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.94);
            box-shadow: 0 10px 32px rgba(17, 57, 71, 0.07);
        }

        [data-testid="stExpander"] summary {
            padding: 6px 4px;
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--ctr-text);
        }

        /* Campos */
        [data-testid="stTextInput"] label,
        [data-testid="stSelectbox"] label {
            color: var(--ctr-text);
            font-size: 0.98rem;
            font-weight: 700;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stSelectbox"] > div > div {
            min-height: 48px;
            border-color: #bdd6df;
            border-radius: 11px;
            background: #fbfeff;
        }

        [data-testid="stTextInput"] input:focus {
            border-color: var(--ctr-primary-dark);
            box-shadow: 0 0 0 2px rgba(0, 143, 179, 0.12);
        }

        /* Títulos de dimensão */
        .dimension-header {
            display: flex;
            align-items: center;
            gap: 13px;
            padding: 18px 20px;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #ffffff;
            border-radius: 15px;
            background:
                linear-gradient(
                    100deg,
                    #0b2633 0%,
                    #145066 100%
                );
            box-shadow: 0 10px 25px rgba(9, 46, 60, 0.14);
        }

        .dimension-number {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            flex-shrink: 0;
            color: #06202b;
            font-weight: 800;
            border-radius: 10px;
            background: linear-gradient(
                135deg,
                #62e3fb,
                #76eecb
            );
        }

        .dimension-title {
            font-size: 1.22rem;
            font-weight: 800;
            letter-spacing: -0.01rem;
        }

        /* Cartões das perguntas */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            height: 100%;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            height: 100%;
            border-color: var(--ctr-border);
            border-radius: 17px;
            background:
                linear-gradient(
                    145deg,
                    #ffffff 0%,
                    #f5fafc 100%
                );
            box-shadow: 0 8px 24px rgba(17, 56, 70, 0.07);
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
            transform: translateY(-2px);
            border-color: #7bc6d8;
            box-shadow: 0 14px 30px rgba(14, 65, 83, 0.13);
        }

        /* Número e texto da pergunta */
        .question-heading {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            min-height: 105px;
            padding: 4px 2px 12px 2px;
        }

        .question-number {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            flex: 0 0 38px;
            color: #ffffff;
            font-size: 0.95rem;
            font-weight: 800;
            border-radius: 11px;
            background:
                linear-gradient(
                    135deg,
                    #047f9e,
                    #12a98f
                );
            box-shadow: 0 5px 12px rgba(4, 127, 158, 0.24);
        }

        .question-text {
            color: var(--ctr-text);
            font-size: 1.08rem;
            font-weight: 700;
            line-height: 1.55;
        }

        .nist-badge {
            display: inline-block;
            padding: 4px 8px;
            margin-top: 7px;
            color: #17677c;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.04rem;
            text-transform: uppercase;
            border-radius: 7px;
            background: #dff3f7;
        }

        /* Radio */
        div[data-testid="stRadio"] {
            padding-top: 5px;
        }

        div[data-testid="stRadio"] > label {
            display: none;
        }

        div[data-testid="stRadio"] [role="radiogroup"] {
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
        }

        div[data-testid="stRadio"] [role="radiogroup"] label {
            min-width: 45px;
            padding: 8px 11px;
            border: 1px solid #c6dbe2;
            border-radius: 10px;
            background: #ffffff;
            transition: all 0.16s ease;
        }

        div[data-testid="stRadio"] [role="radiogroup"] label:hover {
            border-color: #1591ad;
            background: #eaf8fb;
            transform: translateY(-1px);
        }

        div[data-testid="stRadio"] [role="radiogroup"] label p {
            color: #284c59;
            font-size: 0.88rem;
            font-weight: 700;
        }

        div[data-testid="stRadio"] input:checked + div {
            border-color: var(--ctr-primary-dark);
        }

        /* Botões */
        div[data-testid="stButton"] button,
        div[data-testid="stDownloadButton"] button {
            min-height: 56px;
            color: #ffffff;
            font-size: 1rem;
            font-weight: 800;
            letter-spacing: 0.02rem;
            border: 0;
            border-radius: 14px;
            background:
                linear-gradient(
                    100deg,
                    #047f9e,
                    #11a88f
                );
            box-shadow: 0 10px 25px rgba(4, 127, 158, 0.22);
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }

        div[data-testid="stButton"] button:hover,
        div[data-testid="stDownloadButton"] button:hover {
            color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 15px 30px rgba(4, 127, 158, 0.30);
        }

        /* Métricas */
        [data-testid="stMetric"] {
            min-height: 130px;
            padding: 20px;
            border: 1px solid var(--ctr-border);
            border-radius: 16px;
            background: #ffffff;
            box-shadow: 0 8px 25px rgba(17, 57, 71, 0.07);
        }

        [data-testid="stMetricLabel"] {
            font-weight: 700;
            color: var(--ctr-muted);
        }

        [data-testid="stMetricValue"] {
            color: #087f9d;
            font-weight: 800;
        }

        /* Alertas */
        [data-testid="stAlert"] {
            border-radius: 14px;
        }

        /* Separador */
        hr {
            border-color: rgba(91, 132, 146, 0.20);
        }

        /* Responsividade */
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

            .ctr-hero p {
                font-size: 1rem;
            }

            .question-heading {
                min-height: auto;
            }

            .question-text {
                font-size: 1rem;
            }

            div[data-testid="stRadio"] [role="radiogroup"] label {
                min-width: 42px;
                padding: 7px 8px;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ESTADO DA APLICAÇÃO
# ============================================================

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None

if "pdf_filename" not in st.session_state:
    st.session_state.pdf_filename = None

if "assessment_result" not in st.session_state:
    st.session_state.assessment_result = None


# ============================================================
# DADOS DO ASSESSMENT
# ============================================================

OPTIONS = {
    "0 — Inexistente": 0,
    "1 — Informal": 1,
    "2 — Parcial": 2,
    "3 — Aplicado": 3,
    "4 — Medido/Testado": 4,
}


QUESTIONS = [
    (
        1,
        "Governança e Gestão de Riscos",
        "Govern",
        "A empresa possui uma política formal de segurança da informação "
        "aprovada pela direção?",
    ),
    (
        2,
        "Governança e Gestão de Riscos",
        "Govern",
        "Os principais riscos cibernéticos da empresa são identificados e "
        "avaliados periodicamente?",
    ),
    (
        3,
        "Governança e Gestão de Riscos",
        "Govern",
        "Existem responsáveis claramente definidos pelas atividades de "
        "segurança cibernética?",
    ),
    (
        4,
        "Governança e Gestão de Riscos",
        "Govern",
        "A empresa possui requisitos de segurança para fornecedores e "
        "parceiros críticos?",
    ),
    (
        5,
        "Identificação e Inventário",
        "Identify",
        "A empresa mantém inventário atualizado de computadores, servidores, "
        "dispositivos de rede, aplicações e serviços em nuvem?",
    ),
    (
        6,
        "Identificação e Inventário",
        "Identify",
        "Os dados críticos são identificados e classificados de acordo com "
        "sua importância e sensibilidade?",
    ),
    (
        7,
        "Identificação e Inventário",
        "Identify",
        "Existe uma avaliação periódica de vulnerabilidades e configurações "
        "de segurança?",
    ),
    (
        8,
        "Identificação e Inventário",
        "Identify",
        "A empresa conhece quais sistemas e dados são mais críticos para a "
        "continuidade do negócio?",
    ),
    (
        9,
        "Proteção e Controle de Acesso",
        "Protect",
        "O acesso aos sistemas é concedido de acordo com a função e o "
        "princípio do menor privilégio?",
    ),
    (
        10,
        "Proteção e Controle de Acesso",
        "Protect",
        "A autenticação multifator (MFA) está habilitada para contas "
        "administrativas e sistemas críticos?",
    ),
    (
        11,
        "Proteção e Controle de Acesso",
        "Protect",
        "Existem processos para criação, alteração e revogação de acessos "
        "quando funcionários entram, mudam de função ou saem da empresa?",
    ),
    (
        12,
        "Proteção e Controle de Acesso",
        "Protect",
        "Computadores e servidores utilizam proteção contra malware/EDR e "
        "recebem atualizações de segurança?",
    ),
    (
        13,
        "Proteção e Controle de Acesso",
        "Protect",
        "Os backups dos dados críticos são realizados regularmente e "
        "protegidos contra alteração ou exclusão indevida?",
    ),
    (
        14,
        "Detecção e Monitoramento",
        "Detect",
        "A empresa monitora eventos relevantes de segurança em servidores, "
        "endpoints, rede ou serviços em nuvem?",
    ),
    (
        15,
        "Detecção e Monitoramento",
        "Detect",
        "Existem alertas ou mecanismos para identificar atividades "
        "suspeitas, tentativas de invasão ou comportamento anômalo?",
    ),
    (
        16,
        "Detecção e Monitoramento",
        "Detect",
        "Logs de sistemas críticos são mantidos por período definido e podem "
        "ser consultados quando ocorre um incidente?",
    ),
    (
        17,
        "Detecção e Monitoramento",
        "Detect",
        "A empresa acompanha notícias, vulnerabilidades e ameaças relevantes "
        "para seu ambiente tecnológico?",
    ),
    (
        18,
        "Resposta e Recuperação",
        "Respond",
        "Existe um plano documentado de resposta a incidentes de segurança?",
    ),
    (
        19,
        "Resposta e Recuperação",
        "Respond",
        "A empresa sabe quem deve ser acionado em caso de ransomware, "
        "vazamento de dados ou indisponibilidade crítica?",
    ),
    (
        20,
        "Resposta e Recuperação",
        "Respond",
        "São realizados testes ou simulações para validar a capacidade de "
        "resposta a incidentes?",
    ),
    (
        21,
        "Resposta e Recuperação",
        "Recover",
        "Existe um plano de continuidade e/ou recuperação de desastres para "
        "serviços críticos?",
    ),
    (
        22,
        "Resposta e Recuperação",
        "Recover",
        "Os backups são testados periodicamente para confirmar que a "
        "restauração realmente funciona?",
    ),
    (
        23,
        "Pessoas, Conscientização e Conformidade",
        "Protect",
        "Os colaboradores recebem treinamento periódico sobre phishing, "
        "engenharia social, senhas e segurança digital?",
    ),
    (
        24,
        "Pessoas, Conscientização e Conformidade",
        "Govern",
        "A empresa possui procedimentos para tratamento de incidentes "
        "envolvendo dados pessoais e requisitos aplicáveis da LGPD?",
    ),
    (
        25,
        "Pessoas, Conscientização e Conformidade",
        "Govern",
        "A direção acompanha indicadores ou relatórios de segurança para "
        "tomar decisões e priorizar investimentos?",
    ),
]


LEVELS = [
    (
        0,
        24,
        "Crítico",
        "Controles inexistentes ou muito frágeis. A exposição a riscos "
        "básicos é elevada.",
    ),
    (
        25,
        49,
        "Inicial",
        "Existem algumas medidas, porém são informais, incompletas ou "
        "inconsistentes.",
    ),
    (
        50,
        69,
        "Em Desenvolvimento",
        "Controles relevantes estão presentes, mas ainda existem lacunas "
        "importantes.",
    ),
    (
        70,
        84,
        "Estruturado",
        "Boa base de segurança, com oportunidades de melhoria e maior "
        "formalização.",
    ),
    (
        85,
        100,
        "Maduro",
        "Controles amplamente estabelecidos, acompanhados e testados. "
        "A evolução deve ser contínua.",
    ),
]


RECOMMENDATIONS = {
    "Crítico": [
        "Implantar MFA nas contas críticas e administrativas.",
        "Estruturar backups protegidos e testar a restauração.",
        "Atualizar sistemas e fortalecer a proteção dos endpoints.",
        "Revisar acessos e privilégios.",
        "Criar um plano básico de resposta a incidentes.",
    ],
    "Inicial": [
        "Formalizar políticas e responsabilidades de segurança.",
        "Criar inventário de ativos e dados críticos.",
        "Estruturar gestão de vulnerabilidades.",
        "Implantar treinamento periódico contra phishing.",
        "Formalizar processos de acesso, desligamento e recuperação.",
    ],
    "Em Desenvolvimento": [
        "Aprimorar monitoramento e centralização de logs.",
        "Formalizar a matriz de riscos cibernéticos.",
        "Executar testes de backup e recuperação.",
        "Realizar exercícios de resposta a incidentes.",
        "Avaliar requisitos de segurança de fornecedores.",
    ],
    "Estruturado": [
        "Definir e acompanhar KPIs/KRIs de segurança.",
        "Aprimorar gestão de terceiros e fornecedores.",
        "Expandir threat intelligence e monitoramento.",
        "Realizar testes recorrentes dos controles.",
        "Avaliar alinhamento com NIST CSF, ISO 27001 e requisitos setoriais.",
    ],
    "Maduro": [
        "Manter programa de melhoria contínua.",
        "Ampliar automação de controles e resposta.",
        "Executar exercícios avançados de incidentes.",
        "Realizar validações independentes periódicas.",
        "Aprimorar threat intelligence e gestão estratégica de riscos.",
    ],
}


# ============================================================
# CÁLCULOS
# ============================================================

def get_level(score):
    for minimum, maximum, name, description in LEVELS:
        if minimum <= score <= maximum:
            return name, description

    return "Indefinido", ""


def calculate_score(answers):
    total = sum(answers.values())
    maximum = len(QUESTIONS) * 4

    if maximum == 0:
        return 0.0

    return round((total / maximum) * 100, 1)


def calculate_dimensions(answers):
    grouped = {}

    for question_id, dimension, _, _ in QUESTIONS:
        grouped.setdefault(dimension, [])
        grouped[dimension].append(answers[question_id])

    result = {}

    for dimension, values in grouped.items():
        maximum = len(values) * 4

        result[dimension] = round(
            (sum(values) / maximum) * 100,
            1,
        )

    return result


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def safe_filename(text):
    normalized = unicodedata.normalize("NFKD", text)

    normalized = normalized.encode(
        "ascii",
        "ignore",
    ).decode("ascii")

    normalized = re.sub(
        r"[^A-Za-z0-9_-]+",
        "_",
        normalized.strip(),
    )

    return normalized.strip("_") or "empresa"


def register_pdf_fonts():
    font_definitions = {
        "DejaVuSans": font_manager.FontProperties(
            family="DejaVu Sans",
            style="normal",
            weight="normal",
        ),
        "DejaVuSans-Bold": font_manager.FontProperties(
            family="DejaVu Sans",
            style="normal",
            weight="bold",
        ),
        "DejaVuSans-Oblique": font_manager.FontProperties(
            family="DejaVu Sans",
            style="italic",
            weight="normal",
        ),
        "DejaVuSans-BoldOblique": font_manager.FontProperties(
            family="DejaVu Sans",
            style="italic",
            weight="bold",
        ),
    }

    registered_fonts = set(
        pdfmetrics.getRegisteredFontNames()
    )

    for font_name, properties in font_definitions.items():
        if font_name in registered_fonts:
            continue

        font_path = font_manager.findfont(
            properties,
            fallback_to_default=True,
        )

        pdfmetrics.registerFont(
            TTFont(font_name, font_path)
        )

    pdfmetrics.registerFontFamily(
        "DejaVuSans",
        normal="DejaVuSans",
        bold="DejaVuSans-Bold",
        italic="DejaVuSans-Oblique",
        boldItalic="DejaVuSans-BoldOblique",
    )

    return "DejaVuSans"


# ============================================================
# GRÁFICOS
# ============================================================

def create_pie_chart(dimensions):
    labels = list(dimensions.keys())
    values = [float(value) for value in dimensions.values()]

    filtered = [
        (label, value)
        for label, value in zip(labels, values)
        if value > 0
    ]

    if not filtered:
        filtered = [("Sem pontuação", 1.0)]

    chart_labels = [
        item[0]
        for item in filtered
    ]

    chart_values = [
        item[1]
        for item in filtered
    ]

    chart_colors = [
        "#163A4A",
        "#1F6F8B",
        "#2E8FA3",
        "#54B3C2",
        "#9FD8DF",
        "#D7EEF1",
    ]

    fig, ax = plt.subplots(
        figsize=(8, 5.2)
    )

    ax.pie(
        chart_values,
        labels=chart_labels,
        autopct="%1.1f%%",
        startangle=90,
        colors=chart_colors[:len(chart_values)],
        wedgeprops={
            "linewidth": 1,
            "edgecolor": "white",
        },
        textprops={
            "fontsize": 8,
        },
    )

    ax.set_title(
        "Composição dos Scores por Dimensão",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.axis("equal")

    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=180,
        bbox_inches="tight",
        facecolor="white",
    )

    plt.close(fig)
    buffer.seek(0)

    return buffer


def create_bar_chart(dimensions):
    labels = list(dimensions.keys())
    values = [
        float(value)
        for value in dimensions.values()
    ]

    fig, ax = plt.subplots(
        figsize=(8, 4.8)
    )

    bars = ax.barh(
        labels,
        values,
        color="#1F6F8B",
    )

    ax.set_xlim(0, 100)
    ax.set_xlabel("Maturidade (%)")

    ax.set_title(
        "Maturidade por Dimensão",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )

    ax.grid(
        axis="x",
        alpha=0.25,
    )

    ax.set_axisbelow(True)

    for bar, value in zip(bars, values):
        position = min(value + 1, 94)

        ax.text(
            position,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.1f}%",
            va="center",
            fontsize=8,
        )

    fig.tight_layout()

    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=180,
        bbox_inches="tight",
        facecolor="white",
    )

    plt.close(fig)
    buffer.seek(0)

    return buffer


# ============================================================
# PDF
# ============================================================

def build_pdf(
    company,
    contact,
    email,
    phone,
    role,
    employees,
    score,
    level,
    description,
    dimensions,
    answers,
):
    font_name = register_pdf_fonts()
    pdf_buffer = io.BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
        title="CTR CyberCheck - Relatório de Maturidade",
        author="CTR DEFENSE",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CTRTitle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=22,
        leading=27,
        alignment=TA_CENTER,
        spaceAfter=5 * mm,
        textColor=colors.HexColor("#163A4A"),
    )

    subtitle_style = ParagraphStyle(
        "CTRSubtitle",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=12,
        leading=16,
        alignment=TA_CENTER,
        spaceAfter=8 * mm,
    )

    heading_style = ParagraphStyle(
        "CTRHeading",
        parent=styles["Heading1"],
        fontName=font_name,
        fontSize=15,
        leading=19,
        spaceBefore=5 * mm,
        spaceAfter=3 * mm,
        textColor=colors.HexColor("#163A4A"),
    )

    body_style = ParagraphStyle(
        "CTRBody",
        parent=styles["BodyText"],
        fontName=font_name,
        fontSize=9.5,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=2.5 * mm,
    )

    small_style = ParagraphStyle(
        "CTRSmall",
        parent=body_style,
        fontName=font_name,
        fontSize=8,
        leading=11,
    )

    score_style = ParagraphStyle(
        "CTRScore",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=30,
        leading=34,
        alignment=TA_CENTER,
        spaceAfter=2 * mm,
        textColor=colors.HexColor("#1F6F8B"),
    )

    footer_style = ParagraphStyle(
        "CTRFooter",
        parent=small_style,
        alignment=TA_CENTER,
        fontSize=8,
    )

    story = []

    story.append(
        Paragraph(
            "CTR DEFENSE",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "CTR CYBERCHECK<br/>"
            "Assessment Gratuito de Maturidade em Cibersegurança",
            subtitle_style,
        )
    )

    story.append(Spacer(1, 4 * mm))

    info_data = [
        ["Empresa", company or "Não informado"],
        ["Responsável", contact or "Não informado"],
        ["E-mail", email or "Não informado"],
        ["WhatsApp / Telefone", phone or "Não informado"],
        ["Cargo", role or "Não informado"],
        ["Colaboradores", employees or "Não informado"],
        [
            "Data do assessment",
            datetime.now().strftime("%d/%m/%Y %H:%M"),
        ],
    ]

    info_table = Table(
        info_data,
        colWidths=[
            45 * mm,
            125 * mm,
        ],
    )

    info_table.setStyle(
        TableStyle(
            [
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    font_name,
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#EAF3F7"),
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#B7C9D0"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    story.append(info_table)
    story.append(Spacer(1, 8 * mm))

    story.append(
        Paragraph(
            "SCORE DE MATURIDADE",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            f"{score}/100",
            score_style,
        )
    )

    story.append(
        Paragraph(
            f"<b>Nível: {level}</b><br/>{description}",
            body_style,
        )
    )

    story.append(
        Paragraph(
            "Composição dos Scores",
            heading_style,
        )
    )

    pie_buffer = create_pie_chart(dimensions)

    story.append(
        Image(
            pie_buffer,
            width=165 * mm,
            height=108 * mm,
            kind="proportional",
        )
    )

    story.append(
        Paragraph(
            "O gráfico apresenta a composição dos pontos obtidos entre "
            "as dimensões avaliadas.",
            small_style,
        )
    )

    story.append(
        Paragraph(
            "Resultado por Dimensão",
            heading_style,
        )
    )

    dimension_rows = [
        [
            "Dimensão",
            "Score",
            "Classificação",
        ]
    ]

    for dimension, value in dimensions.items():
        dimension_level, _ = get_level(value)

        dimension_rows.append(
            [
                dimension,
                f"{value}/100",
                dimension_level,
            ]
        )

    dimension_table = Table(
        dimension_rows,
        colWidths=[
            95 * mm,
            30 * mm,
            45 * mm,
        ],
        repeatRows=1,
    )

    dimension_table.setStyle(
        TableStyle(
            [
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    font_name,
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    8.5,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#163A4A"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.HexColor("#B7C9D0"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    5,
                ),
            ]
        )
    )

    story.append(dimension_table)
    story.append(PageBreak())

    story.append(
        Paragraph(
            "Maturidade por Dimensão",
            heading_style,
        )
    )

    bar_buffer = create_bar_chart(dimensions)

    story.append(
        Image(
            bar_buffer,
            width=165 * mm,
            height=99 * mm,
            kind="proportional",
        )
    )

    story.append(
        Paragraph(
            "Recomendações Prioritárias",
            heading_style,
        )
    )

    for recommendation in RECOMMENDATIONS.get(level, []):
        story.append(
            Paragraph(
                f"• {recommendation}",
                body_style,
            )
        )

    story.append(
        Paragraph(
            "Resumo das Respostas",
            heading_style,
        )
    )

    answer_rows = [
        [
            "#",
            "Dimensão",
            "Nota",
        ]
    ]

    for question_id, dimension, _, _ in QUESTIONS:
        answer_rows.append(
            [
                str(question_id),
                dimension,
                str(answers[question_id]),
            ]
        )

    answer_table = Table(
        answer_rows,
        colWidths=[
            12 * mm,
            125 * mm,
            25 * mm,
        ],
        repeatRows=1,
    )

    answer_table.setStyle(
        TableStyle(
            [
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    font_name,
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    7.5,
                ),
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#163A4A"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.3,
                    colors.HexColor("#CBD5D9"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    4,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    3,
                ),
            ]
        )
    )

    story.append(answer_table)
    story.append(Spacer(1, 8 * mm))

    story.append(
        Paragraph(
            "Próximo Passo com a CTR DEFENSE",
            heading_style,
        )
    )

    story.append(
        Paragraph(
            "O CTR CyberCheck é uma avaliação inicial. Para validar os "
            "controles e transformar os resultados em um plano de ação, "
            "a CTR DEFENSE pode realizar Diagnóstico de Segurança, "
            "Assessment de Cibersegurança, Avaliação de Vulnerabilidades, "
            "Análise de Riscos, consultoria em NIST/ISO 27001, resposta a "
            "incidentes e continuidade de negócios.",
            body_style,
        )
    )

    story.append(Spacer(1, 4 * mm))

    story.append(
        Paragraph(
            "<b>Nota metodológica:</b> o resultado é baseado nas respostas "
            "autodeclaradas pelo participante. O assessment não constitui "
            "auditoria, pentest, certificação, garantia de segurança ou "
            "validação independente dos controles.",
            small_style,
        )
    )

    story.append(Spacer(1, 6 * mm))

    story.append(
        Paragraph(
            "CTR DEFENSE — Segurança Cibernética e Inteligência contra Ameaças",
            footer_style,
        )
    )

    document.build(story)

    pdf_buffer.seek(0)

    return pdf_buffer.getvalue()


# ============================================================
# CABEÇALHO DA INTERFACE
# ============================================================

st.markdown(
    """
    <div class="ctr-hero">
        <div class="ctr-badge">Assessment de Cibersegurança</div>
        <h1>🛡️ CTR <span>CyberCheck</span></h1>
        <p>
            Descubra o nível de maturidade em cibersegurança da sua
            organização. Responda às 25 perguntas e gere um relatório
            profissional com score, análise por dimensão e recomendações
            prioritárias.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DADOS DA ORGANIZAÇÃO
# ============================================================

with st.expander(
    "📋 Dados da organização",
    expanded=True,
):
    col1, col2 = st.columns(
        2,
        gap="large",
    )

    with col1:
        company = st.text_input(
            "Empresa *",
            placeholder="Nome da empresa",
        )

        contact = st.text_input(
            "Nome do responsável *",
            placeholder="Nome completo",
        )

        email = st.text_input(
            "E-mail corporativo *",
            placeholder="nome@empresa.com.br",
        )

    with col2:
        phone = st.text_input(
            "WhatsApp / Telefone",
            placeholder="(00) 00000-0000",
        )

        role = st.text_input(
            "Cargo / Função",
            placeholder="Ex.: Diretor, Gerente de TI",
        )

        employees = st.selectbox(
            "Quantidade aproximada de colaboradores *",
            [
                "Selecione",
                "1–10",
                "11–50",
                "51–100",
                "101–250",
                "251–500",
                "500+",
            ],
        )


# ============================================================
# QUESTIONÁRIO
# ============================================================

st.markdown("## 🔎 Questionário")

st.markdown(
    """
    <div class="ctr-scale">
        <div class="ctr-scale-item">
            <strong>0</strong> Inexistente ou desconhecido
        </div>
        <div class="ctr-scale-item">
            <strong>1</strong> Informal ou pontual
        </div>
        <div class="ctr-scale-item">
            <strong>2</strong> Existe parcialmente
        </div>
        <div class="ctr-scale-item">
            <strong>3</strong> Aplicado regularmente
        </div>
        <div class="ctr-scale-item">
            <strong>4</strong> Medido e/ou testado
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

answers = {}

dimensions_order = list(
    dict.fromkeys(
        question[1]
        for question in QUESTIONS
    )
)

for dimension_index, dimension in enumerate(
    dimensions_order,
    start=1,
):
    st.markdown(
        f"""
        <div class="dimension-header">
            <div class="dimension-number">{dimension_index}</div>
            <div class="dimension-title">{dimension}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dimension_questions = [
        question
        for question in QUESTIONS
        if question[1] == dimension
    ]

    # Organiza as perguntas em linhas com duas colunas.
    for row_start in range(
        0,
        len(dimension_questions),
        2,
    ):
        row_questions = dimension_questions[
            row_start:row_start + 2
        ]

        columns = st.columns(
            2,
            gap="large",
        )

        for column_index, question_data in enumerate(
            row_questions
        ):
            question_id = question_data[0]
            nist_function = question_data[2]
            question_text = question_data[3]

            with columns[column_index]:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div class="question-heading">
                            <div class="question-number">
                                {question_id}
                            </div>
                            <div>
                                <div class="question-text">
                                    {question_text}
                                </div>
                                <div class="nist-badge">
                                    NIST CSF · {nist_function}
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    selected = st.radio(
                        label=f"Resposta da pergunta {question_id}",
                        options=list(OPTIONS.keys()),
                        index=None,
                        key=f"question_{question_id}",
                        horizontal=True,
                        label_visibility="collapsed",
                    )

                    answers[question_id] = (
                        OPTIONS[selected]
                        if selected is not None
                        else None
                    )


# ============================================================
# PROCESSAMENTO
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

calculate_button = st.button(
    "🚀 CALCULAR RESULTADO E GERAR RELATÓRIO",
    type="primary",
    use_container_width=True,
)

if calculate_button:
    company_clean = company.strip()
    contact_clean = contact.strip()
    email_clean = email.strip()
    phone_clean = phone.strip()
    role_clean = role.strip()

    validation_errors = []

    if not company_clean:
        validation_errors.append(
            "Informe o nome da empresa."
        )

    if not contact_clean:
        validation_errors.append(
            "Informe o nome do responsável."
        )

    if not email_clean:
        validation_errors.append(
            "Informe o e-mail corporativo."
        )

    elif not re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        email_clean,
    ):
        validation_errors.append(
            "Informe um endereço de e-mail válido."
        )

    if employees == "Selecione":
        validation_errors.append(
            "Selecione a quantidade aproximada de colaboradores."
        )

    unanswered_questions = [
        question_id
        for question_id, answer in answers.items()
        if answer is None
    ]

    if unanswered_questions:
        pending_numbers = ", ".join(
            str(question_id)
            for question_id in unanswered_questions
        )

        validation_errors.append(
            "Responda todas as perguntas. "
            f"Perguntas pendentes: {pending_numbers}."
        )

    if validation_errors:
        st.error(
            "Não foi possível gerar o resultado. "
            "Verifique os itens abaixo:"
        )

        for validation_error in validation_errors:
            st.markdown(
                f"- {validation_error}"
            )

    else:
        try:
            valid_answers = {
                question_id: int(answer)
                for question_id, answer in answers.items()
            }

            score = calculate_score(valid_answers)

            level, description = get_level(
                score
            )

            dimensions = calculate_dimensions(
                valid_answers
            )

            with st.spinner(
                "Calculando o resultado e gerando o relatório PDF..."
            ):
                pdf_bytes = build_pdf(
                    company=company_clean,
                    contact=contact_clean,
                    email=email_clean,
                    phone=phone_clean,
                    role=role_clean,
                    employees=employees,
                    score=score,
                    level=level,
                    description=description,
                    dimensions=dimensions,
                    answers=valid_answers,
                )

            filename = (
                f"CTR_CyberCheck_"
                f"{safe_filename(company_clean)}_"
                f"{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            )

            st.session_state.pdf_bytes = pdf_bytes
            st.session_state.pdf_filename = filename

            st.session_state.assessment_result = {
                "score": score,
                "level": level,
                "description": description,
                "dimensions": dimensions,
                "recommendations": RECOMMENDATIONS.get(
                    level,
                    [],
                ),
            }

            st.success(
                "Assessment concluído e relatório gerado com sucesso!"
            )

        except Exception as error:
            st.session_state.pdf_bytes = None
            st.session_state.pdf_filename = None
            st.session_state.assessment_result = None

            st.error(
                "Ocorreu um erro durante a geração do relatório."
            )

            st.exception(error)


# ============================================================
# RESULTADOS
# ============================================================

result = st.session_state.assessment_result

if result is not None:
    score = result["score"]
    level = result["level"]
    description = result["description"]
    dimensions = result["dimensions"]
    recommendations = result["recommendations"]

    st.markdown("## 📊 Resultado do assessment")

    metric_col1, metric_col2, metric_col3 = st.columns(
        3,
        gap="large",
    )

    with metric_col1:
        st.metric(
            "Score geral",
            f"{score}/100",
        )

    with metric_col2:
        st.metric(
            "Nível de maturidade",
            level,
        )

    with metric_col3:
        st.metric(
            "Perguntas respondidas",
            f"{len(QUESTIONS)}/{len(QUESTIONS)}",
        )

    st.progress(
        min(
            max(float(score) / 100, 0.0),
            1.0,
        )
    )

    st.markdown("### 🎯 Interpretação")
    st.info(description)

    st.markdown("### Maturidade por dimensão")

    dimension_columns = st.columns(
        2,
        gap="large",
    )

    for index, (dimension, value) in enumerate(
        dimensions.items()
    ):
        target_column = dimension_columns[
            index % 2
        ]

        with target_column:
            with st.container(border=True):
                st.markdown(
                    f"**{dimension}**"
                )

                st.metric(
                    "Score",
                    f"{value}/100",
                )

                st.progress(
                    min(
                        max(float(value) / 100, 0.0),
                        1.0,
                    )
                )

    st.markdown("### ⚠️ Recomendações prioritárias")

    with st.container(border=True):
        for recommendation in recommendations:
            st.markdown(
                f"- {recommendation}"
            )


# ============================================================
# DOWNLOAD
# ============================================================

if (
    st.session_state.pdf_bytes is not None
    and st.session_state.pdf_filename is not None
):
    st.markdown("### 📄 Relatório profissional")

    st.download_button(
        label="📥 BAIXAR RELATÓRIO EM PDF",
        data=st.session_state.pdf_bytes,
        file_name=st.session_state.pdf_filename,
        mime="application/pdf",
        type="primary",
        use_container_width=True,
    )

    st.success(
        "O relatório contém os gráficos, a análise por dimensão, "
        "as recomendações prioritárias e o resumo das respostas."
    )


# ============================================================
# RODAPÉ
# ============================================================

st.divider()

st.caption(
    "CTR DEFENSE — Segurança Cibernética e Inteligência contra Ameaças | "
    "CTR CyberCheck"
)
