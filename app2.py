import csv
import html
import io
from datetime import datetime

import pandas as pd
import streamlit as st


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
# CSS PERSONALIZADO — CONTRASTE E RESPONSIVIDADE
# ============================================================

st.markdown(
    """
    <style>
        :root {
            --ctr-primary: #047f9e;
            --ctr-secondary: #11a88f;
            --ctr-dark: #06141d;
            --ctr-dark-light: #0b2633;
            --ctr-background: #edf6f8;
            --ctr-border: #bfd8e1;
            --ctr-text: #102f3b;
            --ctr-text-secondary: #496570;
            --ctr-white: #ffffff;
        }

        html,
        body,
        [data-testid="stAppViewContainer"],
        [data-testid="stApp"] {
            color: var(--ctr-text) !important;
            background:
                radial-gradient(
                    circle at top right,
                    rgba(0, 180, 215, 0.12),
                    transparent 32%
                ),
                linear-gradient(
                    180deg,
                    #f8fcfd 0%,
                    var(--ctr-background) 100%
                ) !important;
        }

        html,
        body,
        p,
        span,
        label,
        li,
        div,
        button,
        input,
        textarea,
        select,
        [class*="st-"] {
            font-family: Inter, Arial, Helvetica, sans-serif;
        }

        [data-testid="stHeader"] {
            background: rgba(248, 252, 253, 0.88) !important;
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

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4 {
            color: var(--ctr-text) !important;
        }

        /* Cabeçalho principal */
        .ctr-hero {
            position: relative;
            overflow: hidden;
            padding: 36px 38px;
            margin-bottom: 26px;
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
            background: linear-gradient(90deg, #59e1fb, #87f1d7) !important;
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

        /* Expander */
        [data-testid="stExpander"] {
            overflow: hidden;
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border) !important;
            border-radius: 18px !important;
            background: #ffffff !important;
            box-shadow: 0 10px 32px rgba(17, 57, 71, 0.08);
        }

        [data-testid="stExpander"] details,
        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary span,
        [data-testid="stExpander"] summary p {
            color: var(--ctr-text) !important;
            background: #ffffff !important;
        }

        [data-testid="stExpander"] summary {
            padding: 8px 5px;
            font-size: 1.05rem;
            font-weight: 800;
        }

        [data-testid="stExpanderDetails"] {
            color: var(--ctr-text) !important;
            background: #ffffff !important;
        }

        /* Labels */
        [data-testid="stTextInput"] label,
        [data-testid="stTextInput"] label p,
        [data-testid="stSelectbox"] label,
        [data-testid="stSelectbox"] label p,
        [data-testid="stTextArea"] label,
        [data-testid="stTextArea"] label p,
        [data-testid="stRadio"] > label,
        [data-testid="stRadio"] > label p {
            color: var(--ctr-text) !important;
            font-size: 0.98rem !important;
            font-weight: 700 !important;
        }

        /* Inputs */
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

        [data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
            border-color: var(--ctr-primary) !important;
            box-shadow: 0 0 0 3px rgba(4, 127, 158, 0.14) !important;
        }

        /* Área de texto */
        [data-testid="stTextArea"] textarea {
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border) !important;
            border-radius: 11px !important;
            background: #ffffff !important;
            caret-color: var(--ctr-primary) !important;
            -webkit-text-fill-color: var(--ctr-text) !important;
        }

        /* Selectbox */
        [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
            min-height: 48px;
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border) !important;
            border-radius: 11px !important;
            background: #ffffff !important;
        }

        [data-testid="stSelectbox"] div[data-baseweb="select"] span {
            color: var(--ctr-text) !important;
            -webkit-text-fill-color: var(--ctr-text) !important;
        }

        [data-testid="stSelectbox"] svg {
            fill: var(--ctr-text) !important;
            color: var(--ctr-text) !important;
        }

        /* Menu do selectbox */
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
            box-shadow: 0 8px 25px rgba(15, 55, 70, 0.07);
        }

        .ctr-scale-item {
            flex: 1;
            min-width: 170px;
            padding: 11px 13px;
            color: var(--ctr-text-secondary) !important;
            font-size: 0.88rem;
            font-weight: 600;
            border: 1px solid #d9e9ee;
            border-radius: 11px;
            background: #eef7f9 !important;
        }

        .ctr-scale-item strong {
            display: inline-block;
            margin-right: 5px;
            padding: 2px 8px;
            color: #ffffff !important;
            border-radius: 7px;
            background: var(--ctr-primary) !important;
        }

        /* Cabeçalhos das dimensões */
        .dimension-header {
            display: flex;
            align-items: center;
            gap: 13px;
            padding: 18px 20px;
            margin-top: 30px;
            margin-bottom: 15px;
            color: #ffffff !important;
            border-radius: 15px;
            background: linear-gradient(100deg, #0b2633 0%, #145066 100%) !important;
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
            background: linear-gradient(135deg, #62e3fb, #76eecb) !important;
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

        /* Cartões */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            height: 100%;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            height: 100%;
            color: var(--ctr-text) !important;
            border-color: var(--ctr-border) !important;
            border-radius: 17px !important;
            background: linear-gradient(145deg, #ffffff 0%, #f1f8fa 100%) !important;
            box-shadow: 0 8px 24px rgba(17, 56, 70, 0.08);
            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease,
                border-color 0.2s ease;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div:hover {
            transform: translateY(-2px);
            border-color: #72bfd1 !important;
            box-shadow: 0 14px 30px rgba(14, 65, 83, 0.14);
        }

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
            background: linear-gradient(135deg, #047f9e, #11a88f) !important;
            box-shadow: 0 5px 12px rgba(4, 127, 158, 0.24);
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
            letter-spacing: 0.03rem;
            text-transform: uppercase;
            border: 1px solid #b8dfe8;
            border-radius: 7px;
            background: #dff3f7 !important;
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
            color: var(--ctr-text) !important;
            border: 1px solid #bcd5de !important;
            border-radius: 10px;
            background: #ffffff !important;
            transition: all 0.16s ease;
        }

        div[data-testid="stRadio"] [role="radiogroup"] label:hover {
            border-color: var(--ctr-primary) !important;
            background: #dff3f7 !important;
            transform: translateY(-1px);
        }

        div[data-testid="stRadio"] [role="radiogroup"] label p,
        div[data-testid="stRadio"] [role="radiogroup"] label span {
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
            background: linear-gradient(100deg, #047f9e, #11a88f) !important;
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
            box-shadow: 0 15px 30px rgba(4, 127, 158, 0.30);
        }

        /* Métricas */
        [data-testid="stMetric"] {
            min-height: 130px;
            padding: 20px;
            color: var(--ctr-text) !important;
            border: 1px solid var(--ctr-border);
            border-radius: 16px;
            background: #ffffff !important;
            box-shadow: 0 8px 25px rgba(17, 57, 71, 0.07);
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
            background-color: #d6e8ed !important;
        }

        [data-testid="stProgress"] > div > div > div {
            background: linear-gradient(90deg, #047f9e, #11a88f) !important;
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

        [data-testid="stCaptionContainer"],
        [data-testid="stCaptionContainer"] p {
            color: var(--ctr-text-secondary) !important;
        }

        /* Resultado */
        .result-card {
            padding: 28px;
            margin-top: 22px;
            color: #ffffff !important;
            border-radius: 20px;
            background: linear-gradient(135deg, #06141d, #124253) !important;
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
        }

        hr {
            border-color: rgba(91, 132, 146, 0.25) !important;
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
# DADOS DO QUESTIONÁRIO
# ============================================================

DIMENSOES = [
    {
        "codigo": "GV",
        "nome": "Governar",
        "nist": "NIST CSF 2.0 — Govern",
        "descricao": "Estratégia, políticas, responsabilidades e gestão de riscos.",
        "perguntas": [
            "A organização possui uma política de segurança da informação formalmente aprovada?",
            "As responsabilidades de segurança cibernética estão claramente definidas?",
            "Os riscos cibernéticos são considerados nas decisões estratégicas da organização?",
            "Fornecedores e terceiros são avaliados quanto aos riscos de segurança cibernética?",
        ],
    },
    {
        "codigo": "ID",
        "nome": "Identificar",
        "nist": "NIST CSF 2.0 — Identify",
        "descricao": "Ativos, riscos, vulnerabilidades e dependências críticas.",
        "perguntas": [
            "A organização mantém um inventário atualizado de dispositivos, sistemas e softwares?",
            "Os dados e ativos críticos para o negócio estão identificados e classificados?",
            "São realizadas avaliações periódicas de riscos e vulnerabilidades?",
            "A organização conhece suas dependências críticas de fornecedores e serviços externos?",
        ],
    },
    {
        "codigo": "PR",
        "nome": "Proteger",
        "nist": "NIST CSF 2.0 — Protect",
        "descricao": "Controles preventivos, acessos, treinamento, dados e tecnologia.",
        "perguntas": [
            "A autenticação multifator é utilizada em contas e sistemas críticos?",
            "Os acessos são concedidos conforme a função e revisados periodicamente?",
            "Sistemas operacionais e aplicações recebem atualizações de segurança regularmente?",
            "Os colaboradores recebem treinamento periódico de conscientização em segurança?",
            "Os dados críticos são protegidos por criptografia e cópias de segurança?",
        ],
    },
    {
        "codigo": "DE",
        "nome": "Detectar",
        "nist": "NIST CSF 2.0 — Detect",
        "descricao": "Monitoramento, alertas e identificação de atividades suspeitas.",
        "perguntas": [
            "A organização monitora eventos e atividades suspeitas em seus sistemas?",
            "Existem alertas para tentativas de acesso indevido ou comportamentos anormais?",
            "Os registros de auditoria e logs são armazenados e revisados periodicamente?",
            "Há um processo para analisar e priorizar alertas de segurança?",
        ],
    },
    {
        "codigo": "RS",
        "nome": "Responder",
        "nist": "NIST CSF 2.0 — Respond",
        "descricao": "Planos, comunicação, contenção e tratamento de incidentes.",
        "perguntas": [
            "Existe um plano documentado de resposta a incidentes cibernéticos?",
            "Os responsáveis sabem como agir e quem comunicar durante um incidente?",
            "O plano de resposta a incidentes é testado por meio de exercícios periódicos?",
            "A organização possui procedimentos para conter e investigar incidentes?",
        ],
    },
    {
        "codigo": "RC",
        "nome": "Recuperar",
        "nist": "NIST CSF 2.0 — Recover",
        "descricao": "Continuidade, restauração, backups e melhoria após incidentes.",
        "perguntas": [
            "Existem backups regulares dos dados e sistemas críticos?",
            "As cópias de segurança são testadas periodicamente para confirmar sua restauração?",
            "A organização possui um plano de continuidade e recuperação de desastres?",
            "As lições aprendidas após incidentes são utilizadas para melhorar os controles?",
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
    """Escapa valores exibidos dentro de HTML."""
    return html.escape(str(valor).strip())


def obter_nivel(percentual):
    """Retorna a classificação geral de maturidade."""
    if percentual < 20:
        return "Crítico", "Controles fundamentais inexistentes ou insuficientes."
    if percentual < 40:
        return "Inicial", "Práticas pontuais, informais e predominantemente reativas."
    if percentual < 60:
        return "Em desenvolvimento", "Controles parcialmente implementados."
    if percentual < 80:
        return "Gerenciado", "Controles consistentes, documentados e acompanhados."
    return "Otimizado", "Práticas maduras, mensuradas e continuamente aprimoradas."


def obter_prioridade(percentual):
    """Retorna a prioridade de tratamento de uma dimensão."""
    if percentual < 40:
        return "Alta"
    if percentual < 70:
        return "Média"
    return "Baixa"


def recomendacao_dimensao(codigo):
    recomendacoes = {
        "GV": (
            "Formalize políticas, responsabilidades, indicadores e critérios "
            "de risco cibernético, incluindo fornecedores."
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
    return recomendacoes[codigo]


def montar_csv(empresa, resultados, respostas_detalhadas):
    """Gera o conteúdo CSV do relatório."""
    arquivo = io.StringIO()
    escritor = csv.writer(arquivo, delimiter=";")

    escritor.writerow(["CTR CyberCheck — Relatório de Maturidade"])
    escritor.writerow(["Data", datetime.now().strftime("%d/%m/%Y %H:%M")])
    escritor.writerow(["Organização", empresa["organizacao"]])
    escritor.writerow(["Responsável", empresa["responsavel"]])
    escritor.writerow(["E-mail", empresa["email"]])
    escritor.writerow(["Setor", empresa["setor"]])
    escritor.writerow(["Porte", empresa["porte"]])
    escritor.writerow([])

    escritor.writerow(
        [
            "Dimensão",
            "NIST CSF",
            "Pontuação obtida",
            "Pontuação máxima",
            "Percentual",
            "Prioridade",
        ]
    )

    for resultado in resultados:
        escritor.writerow(
            [
                resultado["dimensao"],
                resultado["nist"],
                resultado["pontos"],
                resultado["maximo"],
                f'{resultado["percentual"]:.1f}%',
                resultado["prioridade"],
            ]
        )

    escritor.writerow([])
    escritor.writerow(
        [
            "Número",
            "Dimensão",
            "Pergunta",
            "Resposta",
            "Pontuação",
        ]
    )

    for resposta in respostas_detalhadas:
        escritor.writerow(
            [
                resposta["numero"],
                resposta["dimensao"],
                resposta["pergunta"],
                resposta["resposta"],
                (
                    resposta["pontuacao"]
                    if resposta["pontuacao"] is not None
                    else "Não avaliado"
                ),
            ]
        )

    return arquivo.getvalue().encode("utf-8-sig")


# ============================================================
# ESTADO DA APLICAÇÃO
# ============================================================

if "resultado_calculado" not in st.session_state:
    st.session_state.resultado_calculado = False


# ============================================================
# CABEÇALHO
# ============================================================

st.markdown(
    """
    <section class="ctr-hero">
        <div class="ctr-badge">Avaliação de maturidade cibernética</div>
        <h1>CTR <span>CyberCheck</span></h1>
        <p>
            Avalie a maturidade de segurança cibernética da sua organização
            com base nas seis funções do NIST Cybersecurity Framework 2.0:
            Governar, Identificar, Proteger, Detectar, Responder e Recuperar.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DADOS DA ORGANIZAÇÃO
# ============================================================

with st.expander("🏢 Dados da organização", expanded=True):
    linha_1_col_1, linha_1_col_2 = st.columns(2)

    with linha_1_col_1:
        organizacao = st.text_input(
            "Nome da organização *",
            placeholder="Ex.: Empresa Exemplo Ltda.",
        )

    with linha_1_col_2:
        responsavel = st.text_input(
            "Responsável pela avaliação",
            placeholder="Nome do responsável",
        )

    linha_2_col_1, linha_2_col_2, linha_2_col_3 = st.columns(3)

    with linha_2_col_1:
        email = st.text_input(
            "E-mail",
            placeholder="responsavel@empresa.com",
        )

    with linha_2_col_2:
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
        )

    with linha_2_col_3:
        porte = st.selectbox(
            "Porte da organização",
            [
                "Selecione",
                "Microempresa",
                "Pequena empresa",
                "Média empresa",
                "Grande empresa",
            ],
        )

    observacoes = st.text_area(
        "Observações",
        placeholder="Informações adicionais sobre o contexto da avaliação.",
        height=90,
    )


# ============================================================
# ORIENTAÇÕES E ESCALA
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

for indice_dimensao, dimensao in enumerate(DIMENSOES, start=1):
    nome = texto_seguro(dimensao["nome"])
    descricao = texto_seguro(dimensao["descricao"])
    nist = texto_seguro(dimensao["nist"])

    st.markdown(
        f"""
        <div class="dimension-header">
            <div class="dimension-number">{indice_dimensao}</div>
            <div>
                <div class="dimension-title">{nome}</div>
                <div class="dimension-description">{descricao}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    perguntas = dimensao["perguntas"]

    for inicio in range(0, len(perguntas), 2):
        colunas = st.columns(2, gap="large")

        for deslocamento, coluna in enumerate(colunas):
            indice_pergunta = inicio + deslocamento

            if indice_pergunta >= len(perguntas):
                continue

            pergunta = perguntas[indice_pergunta]
            chave = f'resposta_{dimensao["codigo"]}_{indice_pergunta}'
            chaves_respostas.append(chave)

            with coluna:
                with st.container(border=True):
                    st.markdown(
                        f"""
                        <div class="question-heading">
                            <div class="question-number">{numero_global}</div>
                            <div>
                                <div class="question-text">
                                    {texto_seguro(pergunta)}
                                </div>
                                <div class="nist-badge">{nist}</div>
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
    if OPCOES.get(st.session_state.get(chave)) is not None
)

progresso = respondidas / TOTAL_PERGUNTAS

st.markdown("### Progresso da avaliação")
st.progress(progresso)
st.caption(
    f"{respondidas} de {TOTAL_PERGUNTAS} perguntas avaliadas "
    f"({progresso * 100:.0f}%)."
)


# ============================================================
# AÇÕES
# ============================================================

col_botao_1, col_botao_2 = st.columns([3, 1])

with col_botao_1:
    calcular = st.button(
        "Calcular resultado",
        type="primary",
        use_container_width=True,
    )

with col_botao_2:
    limpar = st.button(
        "Limpar respostas",
        use_container_width=True,
    )

if limpar:
    for chave in chaves_respostas:
        if chave in st.session_state:
            del st.session_state[chave]

    st.session_state.resultado_calculado = False
    st.rerun()


# ============================================================
# CÁLCULO DO RESULTADO
# ============================================================

if calcular:
    if not organizacao.strip():
        st.error("Informe o nome da organização antes de calcular o resultado.")
    elif respondidas == 0:
        st.error("Responda pelo menos uma pergunta antes de calcular o resultado.")
    else:
        st.session_state.resultado_calculado = True


if st.session_state.resultado_calculado and organizacao.strip():
    resultados = []
    respostas_detalhadas = []

    pontos_totais = 0
    maximo_total_avaliado = 0
    numero_resposta = 1

    for dimensao in DIMENSOES:
        pontos_dimensao = 0
        perguntas_avaliadas = 0

        for indice_pergunta, pergunta in enumerate(dimensao["perguntas"]):
            chave = f'resposta_{dimensao["codigo"]}_{indice_pergunta}'
            resposta_texto = st.session_state.get(chave, "Não avaliado")
            pontuacao = OPCOES.get(resposta_texto)

            if pontuacao is not None:
                pontos_dimensao += pontuacao
                perguntas_avaliadas += 1

            respostas_detalhadas.append(
                {
                    "numero": numero_resposta,
                    "dimensao": dimensao["nome"],
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

        resultados.append(
            {
                "codigo": dimensao["codigo"],
                "dimensao": dimensao["nome"],
                "nist": dimensao["nist"],
                "pontos": pontos_dimensao,
                "maximo": maximo_dimensao,
                "avaliadas": perguntas_avaliadas,
                "percentual": percentual_dimensao,
                "prioridade": obter_prioridade(percentual_dimensao),
            }
        )

        pontos_totais += pontos_dimensao
        maximo_total_avaliado += maximo_dimensao

    percentual_geral = (
        pontos_totais / maximo_total_avaliado * 100
        if maximo_total_avaliado > 0
        else 0
    )

    nivel, descricao_nivel = obter_nivel(percentual_geral)

    st.markdown(
        f"""
        <div class="result-card">
            <h2>Resultado da avaliação</h2>
            <div class="result-score">{percentual_geral:.1f}%</div>
            <h3>Nível: {texto_seguro(nivel)}</h3>
            <p>{texto_seguro(descricao_nivel)}</p>
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
        f"{pontos_totais}/{maximo_total_avaliado}",
    )

    metrica_3.metric(
        "Perguntas avaliadas",
        f"{respondidas}/{TOTAL_PERGUNTAS}",
    )

    metrica_4.metric(
        "Classificação",
        nivel,
    )

    st.markdown("### Resultado por dimensão")

    dados_grafico = pd.DataFrame(
        {
            "Dimensão": [
                resultado["dimensao"]
                for resultado in resultados
            ],
            "Maturidade (%)": [
                round(resultado["percentual"], 1)
                for resultado in resultados
            ],
        }
    ).set_index("Dimensão")

    st.bar_chart(
        dados_grafico,
        color="#047F9E",
        horizontal=True,
    )

    tabela_resultados = pd.DataFrame(
        [
            {
                "Dimensão": resultado["dimensao"],
                "NIST CSF": resultado["nist"],
                "Avaliadas": resultado["avaliadas"],
                "Pontuação": (
                    f'{resultado["pontos"]}/{resultado["maximo"]}'
                    if resultado["maximo"] > 0
                    else "Não avaliado"
                ),
                "Maturidade": f'{resultado["percentual"]:.1f}%',
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

    st.markdown("### Recomendações prioritárias")

    resultados_ordenados = sorted(
        resultados,
        key=lambda item: item["percentual"],
    )

    for resultado in resultados_ordenados:
        if resultado["avaliadas"] == 0:
            status = "Dimensão não avaliada"
        else:
            status = (
                f'Maturidade de {resultado["percentual"]:.1f}% — '
                f'prioridade {resultado["prioridade"].lower()}'
            )

        st.markdown(
            f"""
            <div class="recommendation-card">
                <strong>{texto_seguro(resultado["dimensao"])}</strong><br>
                {texto_seguro(status)}.<br>
                {texto_seguro(recomendacao_dimensao(resultado["codigo"]))}
            </div>
            """,
            unsafe_allow_html=True,
        )

    empresa = {
        "organizacao": organizacao.strip(),
        "responsavel": responsavel.strip(),
        "email": email.strip(),
        "setor": setor,
        "porte": porte,
        "observacoes": observacoes.strip(),
    }

    relatorio_csv = montar_csv(
        empresa,
        resultados,
        respostas_detalhadas,
    )

    nome_arquivo = (
        "ctr_cybercheck_"
        + "".join(
            caractere.lower() if caractere.isalnum() else "_"
            for caractere in organizacao.strip()
        ).strip("_")
        + ".csv"
    )

    st.download_button(
        label="Baixar relatório em CSV",
        data=relatorio_csv,
        file_name=nome_arquivo,
        mime="text/csv",
        use_container_width=True,
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

st.markdown("<br>", unsafe_allow_html=True)
st.caption(
    "CTR CyberCheck • Avaliação orientativa baseada nas funções do "
    "NIST Cybersecurity Framework 2.0. O resultado não substitui uma "
    "auditoria técnica especializada."
)
