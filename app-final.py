import csv
import html
import io
import re
import unicodedata
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
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


def renderizar_html(conteudo):
    """Remove linhas vazias e indentação para o Markdown não tratar o HTML como código."""
    linhas = [l.strip() for l in conteudo.strip().splitlines() if l.strip()]
    st.markdown("".join(linhas), unsafe_allow_html=True)


# ============================================================
# CSS
# ============================================================
st.markdown(
    """
<style>
:root{--ctr-primary:#047f9e;--ctr-secondary:#11a88f;--ctr-background:#dfe3e6;--ctr-border:#c4cbd0;--ctr-text:#102f3b;--ctr-text-secondary:#496570;}
html,body,[data-testid="stAppViewContainer"],.stApp{color:var(--ctr-text)!important;background:var(--ctr-background)!important;}
.stApp p,.stApp label,.stApp li,.stApp button,.stApp input,.stApp textarea{font-family:Inter,Arial,Helvetica,sans-serif;}
.material-symbols-rounded,.material-symbols-outlined,[data-testid="stIconMaterial"]{font-family:"Material Symbols Rounded","Material Symbols Outlined"!important;font-weight:normal!important;line-height:1!important;letter-spacing:normal!important;text-transform:none!important;white-space:nowrap!important;-webkit-font-feature-settings:"liga"!important;font-feature-settings:"liga"!important;}
[data-testid="stHeader"]{background:rgba(223,227,230,.95)!important;}
.block-container{max-width:1500px;padding-top:2rem;padding-bottom:4rem;}
#MainMenu,footer{visibility:hidden;}
[data-testid="stAppViewContainer"] h1,[data-testid="stAppViewContainer"] h2,[data-testid="stAppViewContainer"] h3,[data-testid="stAppViewContainer"] h4,[data-testid="stAppViewContainer"] p,[data-testid="stAppViewContainer"] li{color:var(--ctr-text)!important;}
.ctr-hero{position:relative;overflow:hidden;padding:36px 38px;margin-bottom:22px;border:1px solid rgba(0,212,255,.3);border-radius:24px;background:radial-gradient(circle at 90% 15%,rgba(0,212,255,.28),transparent 34%),linear-gradient(135deg,#06141d 0%,#0b2633 52%,#124253 100%)!important;box-shadow:0 24px 55px rgba(6,32,43,.22);}
.ctr-hero::after{content:"";position:absolute;width:220px;height:220px;top:-110px;right:-60px;border:1px solid rgba(255,255,255,.14);border-radius:50%;}
.ctr-badge{display:inline-block;padding:7px 13px;margin-bottom:15px;color:#06141d!important;font-size:.78rem;font-weight:800;letter-spacing:.08rem;text-transform:uppercase;border-radius:999px;background:linear-gradient(90deg,#59e1fb,#87f1d7)!important;}
.ctr-hero h1{margin:0 0 10px 0;color:#fff!important;font-size:clamp(2rem,4vw,3.3rem);font-weight:800;letter-spacing:-.06rem;}
.ctr-hero h1 span{color:#64e5ff!important;}
.ctr-hero p{max-width:900px;margin:0;color:#e4f2f5!important;font-size:1.08rem;line-height:1.75;}
.ctr-session-notice{padding:19px 21px;margin:0 0 17px 0;border:1px solid #dfbd4d;border-left:6px solid #d9a514;border-radius:15px;background:#fff8dc!important;line-height:1.6;}
.ctr-session-notice *{color:#3f350d!important;}
.ctr-privacy-notice{padding:19px 21px;margin:0 0 24px 0;border:1px solid #91cfc2;border-left:6px solid #11a88f;border-radius:15px;background:#eaf9f5!important;line-height:1.6;}
.ctr-privacy-notice *{color:#164d44!important;}
.ctr-privacy-notice ul{margin:6px 0 0 18px;padding:0;}
.ctr-notice-title{display:block;margin-bottom:8px;font-size:1.02rem;font-weight:800;}
.ctr-notice-text{margin:0 0 6px 0;}
div[data-testid="stVerticalBlockBorderWrapper"]>div{border-color:var(--ctr-border)!important;border-radius:17px!important;background:#fff!important;box-shadow:0 8px 24px rgba(17,56,70,.1);}
[data-testid="stTextInput"] label p,[data-testid="stSelectbox"] label p,[data-testid="stTextArea"] label p,[data-testid="stCheckbox"] label p{color:var(--ctr-text)!important;font-size:.98rem!important;font-weight:700!important;}
[data-testid="stTextInput"] div[data-baseweb="input"]{min-height:48px;border:1px solid var(--ctr-border)!important;border-radius:11px!important;background:#fff!important;}
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea{color:var(--ctr-text)!important;background:#fff!important;-webkit-text-fill-color:var(--ctr-text)!important;caret-color:var(--ctr-primary)!important;}
[data-testid="stTextInput"] input::placeholder,[data-testid="stTextArea"] textarea::placeholder{color:#718a94!important;-webkit-text-fill-color:#718a94!important;opacity:1!important;}
[data-testid="stTextArea"] textarea{border:1px solid var(--ctr-border)!important;border-radius:11px!important;}
[data-testid="stSelectbox"] div[data-baseweb="select"]>div{min-height:48px;border:1px solid var(--ctr-border)!important;border-radius:11px!important;background:#fff!important;}
[data-testid="stSelectbox"] div[data-baseweb="select"] span{color:var(--ctr-text)!important;-webkit-text-fill-color:var(--ctr-text)!important;}
[data-testid="stSelectbox"] svg{fill:var(--ctr-text)!important;}
div[data-baseweb="popover"],div[data-baseweb="popover"]>div,div[data-baseweb="menu"],ul[role="listbox"],li[role="option"]{color:var(--ctr-text)!important;background:#fff!important;}
li[role="option"] *{color:var(--ctr-text)!important;}
li[role="option"]:hover,li[role="option"][aria-selected="true"]{background:#dff3f7!important;}
.ctr-scale{display:flex;flex-wrap:wrap;gap:10px;padding:16px;margin:18px 0 26px 0;border:1px solid var(--ctr-border);border-radius:16px;background:#fff!important;box-shadow:0 8px 25px rgba(15,55,70,.09);}
.ctr-scale-item{flex:1;min-width:165px;padding:11px 13px;color:var(--ctr-text-secondary)!important;font-size:.88rem;font-weight:600;border:1px solid #d3dade;border-radius:11px;background:#eef1f3!important;}
.ctr-scale-item strong{display:inline-block;margin-right:5px;padding:2px 8px;color:#fff!important;border-radius:7px;background:var(--ctr-primary)!important;}
.dimension-header{display:flex;align-items:center;gap:13px;padding:18px 20px;margin:30px 0 15px 0;border-radius:15px;background:linear-gradient(100deg,#0b2633 0%,#145066 100%)!important;box-shadow:0 10px 25px rgba(9,46,60,.14);}
.dimension-number{display:flex;align-items:center;justify-content:center;width:42px;height:42px;flex-shrink:0;color:#06202b!important;font-weight:800;border-radius:10px;background:linear-gradient(135deg,#62e3fb,#76eecb)!important;}
.dimension-title{color:#fff!important;font-size:1.22rem;font-weight:800;}
.dimension-description{margin-top:2px;color:#d8edf2!important;font-size:.87rem;}
.question-heading{display:flex;align-items:flex-start;gap:12px;padding:4px 2px 8px 2px;}
.question-number{display:flex;align-items:center;justify-content:center;width:40px;height:40px;flex:0 0 40px;color:#fff!important;font-weight:800;border-radius:11px;background:linear-gradient(135deg,#047f9e,#11a88f)!important;}
.question-text{color:var(--ctr-text)!important;font-size:1.04rem;font-weight:750;line-height:1.5;}
.nist-badge{display:inline-block;padding:4px 8px;margin-top:7px;color:#075d73!important;font-size:.7rem;font-weight:800;text-transform:uppercase;border:1px solid #b8dfe8;border-radius:7px;background:#dff3f7!important;}
div[data-testid="stRadio"]>label{display:none;}
div[data-testid="stRadio"] [role="radiogroup"]{display:flex;flex-wrap:wrap;gap:7px;}
div[data-testid="stRadio"] [role="radiogroup"] label{padding:8px 11px;border:1px solid #bcd5de!important;border-radius:10px;background:#fff!important;}
div[data-testid="stRadio"] [role="radiogroup"] label:hover{border-color:var(--ctr-primary)!important;background:#dff3f7!important;}
div[data-testid="stRadio"] [role="radiogroup"] label p,div[data-testid="stRadio"] [role="radiogroup"] label span{color:#173d4a!important;font-size:.88rem!important;font-weight:700!important;-webkit-text-fill-color:#173d4a!important;}
div[data-testid="stButton"] button,div[data-testid="stDownloadButton"] button{min-height:54px;color:#fff!important;font-weight:800;border:0!important;border-radius:14px;background:linear-gradient(100deg,#047f9e,#11a88f)!important;box-shadow:0 10px 25px rgba(4,127,158,.22);}
div[data-testid="stButton"] button p,div[data-testid="stDownloadButton"] button p{color:#fff!important;}
div[data-testid="stButton"] button:hover,div[data-testid="stDownloadButton"] button:hover{transform:translateY(-2px);}
[data-testid="stMetric"]{min-height:130px;padding:20px;border:1px solid var(--ctr-border);border-radius:16px;background:#fff!important;box-shadow:0 8px 25px rgba(17,57,71,.09);}
[data-testid="stMetricLabel"] p{color:var(--ctr-text-secondary)!important;font-weight:700;}
[data-testid="stMetricValue"] div{color:#047f9e!important;font-weight:800;}
[data-testid="stProgress"]>div>div{background-color:#c5cdd1!important;}
[data-testid="stProgress"]>div>div>div{background:linear-gradient(90deg,#047f9e,#11a88f)!important;}
[data-testid="stAlert"]{border-radius:14px;}
[data-testid="stAlert"] *{color:var(--ctr-text)!important;}
.result-card{padding:28px;margin-top:22px;border-radius:20px;background:linear-gradient(135deg,#06141d,#124253)!important;box-shadow:0 20px 45px rgba(6,32,43,.22);}
.result-card *{color:#fff!important;}
.result-card h2{margin:0 0 6px 0;font-size:1.5rem;}
.result-score{color:#64e5ff!important;font-size:3rem;font-weight:900;}
.recommendation-card{padding:16px 18px;margin:10px 0;border:1px solid var(--ctr-border);border-left:5px solid var(--ctr-primary);border-radius:12px;background:#fff!important;box-shadow:0 6px 18px rgba(17,57,71,.08);line-height:1.6;}
.recommendation-card *{color:var(--ctr-text)!important;}
.recommendation-card strong{color:#063744!important;}
.exec-card{padding:26px 28px;margin-top:22px;border:1px solid var(--ctr-border);border-top:6px solid #b42318;border-radius:18px;background:#fff!important;box-shadow:0 12px 30px rgba(17,57,71,.1);}
.exec-card h3{margin:0 0 6px 0;color:var(--ctr-text)!important;font-size:1.3rem;font-weight:800;}
.exec-subtitle{margin:0 0 16px 0;color:var(--ctr-text-secondary)!important;font-size:.92rem;}
.exec-summary{padding:16px 18px;margin:14px 0;font-size:1.02rem;line-height:1.7;border-left:5px solid #047f9e;border-radius:10px;background:#f3f7f9!important;}
.exec-summary *{color:var(--ctr-text)!important;}
.exec-summary strong{color:#063744!important;}
.exec-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:16px 0;}
.exec-kpi{padding:16px;border:1px solid var(--ctr-border);border-radius:13px;background:#fafbfc!important;}
.exec-kpi-label{display:block;margin-bottom:6px;color:var(--ctr-text-secondary)!important;font-size:.78rem;font-weight:800;text-transform:uppercase;letter-spacing:.05rem;}
.exec-kpi-value{display:block;color:#063744!important;font-size:1.45rem;font-weight:900;line-height:1.2;}
.exec-kpi-note{display:block;margin-top:4px;color:var(--ctr-text-secondary)!important;font-size:.8rem;}
.exec-row{display:grid;grid-template-columns:150px 120px 1fr;gap:14px;align-items:start;padding:13px 14px;margin:8px 0;border:1px solid var(--ctr-border);border-radius:12px;background:#fff!important;}
.exec-row-dim{color:var(--ctr-text)!important;font-weight:800;}
.exec-row-dim small{display:block;color:var(--ctr-text-secondary)!important;font-weight:600;}
.exec-pill{display:inline-block;padding:5px 10px;color:#fff!important;font-size:.78rem;font-weight:800;text-transform:uppercase;border-radius:8px;}
.exec-row-text strong{display:block;margin-bottom:3px;color:#063744!important;}
.exec-row-text span{color:var(--ctr-text-secondary)!important;font-size:.9rem;line-height:1.5;}
.exec-disclaimer{margin-top:14px;color:var(--ctr-text-secondary)!important;font-size:.8rem;line-height:1.5;}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# DADOS DO CHECKLIST (NIST CSF 2.0)
# ============================================================
DIMENSOES = [
    {
        "nome": "Governar",
        "codigo": "GV",
        "descricao": "Estratégia, políticas, papéis e supervisão da segurança.",
        "perguntas": [
            ("Existe uma política de segurança da informação formal, aprovada pela direção e comunicada a todos?", "GV.PO"),
            ("Os papéis e responsabilidades de segurança (inclusive DPO/encarregado LGPD) estão definidos?", "GV.RR"),
            ("Riscos de fornecedores e terceiros são avaliados antes da contratação e periodicamente?", "GV.SC"),
            ("A direção acompanha indicadores de segurança e risco cibernético em reuniões periódicas?", "GV.OV"),
        ],
    },
    {
        "nome": "Identificar",
        "codigo": "ID",
        "descricao": "Conhecimento dos ativos, dados e vulnerabilidades da organização.",
        "perguntas": [
            ("Existe inventário atualizado de equipamentos, sistemas, softwares e dados críticos?", "ID.AM"),
            ("Os dados pessoais tratados estão mapeados (fluxo, finalidade e base legal)?", "ID.AM"),
            ("São realizadas análises de vulnerabilidade ou testes de segurança periodicamente?", "ID.RA"),
            ("Os riscos identificados são registrados, priorizados e acompanhados até o tratamento?", "ID.IM"),
        ],
    },
    {
        "nome": "Proteger",
        "codigo": "PR",
        "descricao": "Controles que reduzem a probabilidade e o impacto de incidentes.",
        "perguntas": [
            ("A autenticação multifator (MFA) está ativa em e-mails, VPN, nuvem e sistemas críticos?", "PR.AA"),
            ("Os colaboradores recebem treinamentos periódicos de conscientização (phishing, senhas, engenharia social)?", "PR.AT"),
            ("Dados sensíveis são criptografados em repouso e em trânsito, com controle de acesso por necessidade?", "PR.DS"),
            ("Sistemas e dispositivos recebem atualizações de segurança de forma controlada e tempestiva?", "PR.PS"),
        ],
    },
    {
        "nome": "Detectar",
        "codigo": "DE",
        "descricao": "Capacidade de perceber eventos e ataques em andamento.",
        "perguntas": [
            ("Logs de sistemas críticos, rede e autenticação são centralizados e retidos?", "DE.CM"),
            ("Existe solução de proteção de endpoints (EDR/antivírus gerenciado) com monitoramento?", "DE.CM"),
            ("Há alertas configurados para atividades suspeitas (acessos anômalos, exfiltração, malware)?", "DE.AE"),
            ("Alguém é responsável por analisar alertas em horário definido (interno ou SOC terceirizado)?", "DE.AE"),
        ],
    },
    {
        "nome": "Responder",
        "codigo": "RS",
        "descricao": "Ações organizadas quando um incidente ocorre.",
        "perguntas": [
            ("Existe um plano de resposta a incidentes documentado, com papéis e contatos definidos?", "RS.MA"),
            ("O plano de resposta é testado ou simulado ao menos uma vez por ano?", "RS.MA"),
            ("
