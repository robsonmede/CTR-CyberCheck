import io
import re
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
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)

# ============================================================
# CTR DEFENSE - CTR CYBERCHECK
# Streamlit + PDF + Gráfico de Pizza
# ============================================================

st.set_page_config(
    page_title="CTR CyberCheck | CTR DEFENSE",
    page_icon="🛡️",
    layout="wide",
)

# ------------------------------------------------------------
# Dados do assessment
# ------------------------------------------------------------

OPTIONS = {
    "0 — Não existe / desconhecido": 0,
    "1 — Informal ou pontual": 1,
    "2 — Existe parcialmente": 2,
    "3 — Aplicado regularmente": 3,
    "4 — Aplicado, medido e/ou testado": 4,
}

QUESTIONS = [
    (1, "Governança e Gestão de Riscos", "Govern",
     "A empresa possui uma política formal de segurança da informação aprovada pela direção?"),
    (2, "Governança e Gestão de Riscos", "Govern",
     "Os principais riscos cibernéticos da empresa são identificados e avaliados periodicamente?"),
    (3, "Governança e Gestão de Riscos", "Govern",
     "Existem responsáveis claramente definidos pelas atividades de segurança cibernética?"),
    (4, "Governança e Gestão de Riscos", "Govern",
     "A empresa possui requisitos de segurança para fornecedores e parceiros críticos?"),

    (5, "Identificação e Inventário", "Identify",
     "A empresa mantém inventário atualizado de computadores, servidores, dispositivos de rede, aplicações e serviços em nuvem?"),
    (6, "Identificação e Inventário", "Identify",
     "Os dados críticos são identificados e classificados de acordo com sua importância e sensibilidade?"),
    (7, "Identificação e Inventário", "Identify",
     "Existe uma avaliação periódica de vulnerabilidades e configurações de segurança?"),
    (8, "Identificação e Inventário", "Identify",
     "A empresa conhece quais sistemas e dados são mais críticos para a continuidade do negócio?"),

    (9, "Proteção e Controle de Acesso", "Protect",
     "O acesso aos sistemas é concedido de acordo com a função e o princípio do menor privilégio?"),
    (10, "Proteção e Controle de Acesso", "Protect",
     "A autenticação multifator (MFA) está habilitada para contas administrativas e sistemas críticos?"),
    (11, "Proteção e Controle de Acesso", "Protect",
     "Existem processos para criação, alteração e revogação de acessos quando funcionários entram, mudam de função ou saem da empresa?"),
    (12, "Proteção e Controle de Acesso", "Protect",
     "Computadores e servidores utilizam proteção contra malware/EDR e recebem atualizações de segurança?"),
    (13, "Proteção e Controle de Acesso", "Protect",
     "Os backups dos dados críticos são realizados regularmente e protegidos contra alteração ou exclusão indevida?"),

    (14, "Detecção e Monitoramento", "Detect",
     "A empresa monitora eventos relevantes de segurança em servidores, endpoints, rede ou serviços em nuvem?"),
    (15, "Detecção e Monitoramento", "Detect",
     "Existem alertas ou mecanismos para identificar atividades suspeitas, tentativas de invasão ou comportamento anômalo?"),
    (16, "Detecção e Monitoramento", "Detect",
     "Logs de sistemas críticos são mantidos por período definido e podem ser consultados quando ocorre um incidente?"),
    (17, "Detecção e Monitoramento", "Detect",
     "A empresa acompanha notícias, vulnerabilidades e ameaças relevantes para seu ambiente tecnológico?"),

    (18, "Resposta e Recuperação", "Respond",
     "Existe um plano documentado de resposta a incidentes de segurança?"),
    (19, "Resposta e Recuperação", "Respond",
     "A empresa sabe quem deve ser acionado em caso de ransomware, vazamento de dados ou indisponibilidade crítica?"),
    (20, "Resposta e Recuperação", "Respond",
     "São realizados testes ou simulações para validar a capacidade de resposta a incidentes?"),
    (21, "Resposta e Recuperação", "Recover",
     "Existe um plano de continuidade e/ou recuperação de desastres para serviços críticos?"),
    (22, "Resposta e Recuperação", "Recover",
     "Os backups são testados periodicamente para confirmar que a restauração realmente funciona?"),

    (23, "Pessoas, Conscientização e Conformidade", "Protect",
     "Os colaboradores recebem treinamento periódico sobre phishing, engenharia social, senhas e segurança digital?"),
    (24, "Pessoas, Conscientização e Conformidade", "Govern",
     "A empresa possui procedimentos para tratamento de incidentes envolvendo dados pessoais e requisitos aplicáveis da LGPD?"),
    (25, "Pessoas, Conscientização e Conformidade", "Govern",
     "A direção acompanha indicadores ou relatórios de segurança para tomar decisões e priorizar investimentos?"),
]

LEVELS = [
    (0, 24, "Crítico",
     "Controles inexistentes ou muito frágeis. A exposição a riscos básicos é elevada."),
    (25, 49, "Inicial",
     "Existem algumas medidas, porém são informais, incompletas ou inconsistentes."),
    (50, 69, "Em Desenvolvimento",
     "Controles relevantes estão presentes, mas ainda existem lacunas importantes."),
    (70, 84, "Estruturado",
     "Boa base de segurança, com oportunidades de melhoria e maior formalização."),
    (85, 100, "Maduro",
     "Controles amplamente estabelecidos, acompanhados e testados. A evolução deve ser contínua."),
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


# ------------------------------------------------------------
# Cálculos
# ------------------------------------------------------------

def get_level(score):
    for minimum, maximum, name, description in LEVELS:
        if minimum <= score <= maximum:
            return name, description
    return "Indefinido", ""


def calculate_score(answers):
    total = sum(answers.values())
    maximum = len(QUESTIONS) * 4
    return round((total / maximum) * 100, 1)


def calculate_dimensions(answers):
    grouped = {}

    for q_id, dimension, _, _ in QUESTIONS:
        grouped.setdefault(dimension, [])
        grouped[dimension].append(answers[q_id])

    result = {}

    for dimension, values in grouped.items():
        # Percentual de maturidade da dimensão: pontos obtidos / pontos máximos.
        result[dimension] = round(
            (sum(values) / (len(values) * 4)) * 100, 1
        )

    return result


# ------------------------------------------------------------
# PDF
# ------------------------------------------------------------

def register_pdf_font():
    """Registra DejaVu Sans para suportar acentos do português."""
    font_path = font_manager.findfont("DejaVu Sans")
    pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))
    return "DejaVuSans"


def safe_filename(text):
    text = re.sub(r"[^A-Za-z0-9_-]+", "_", text.strip())
    return text.strip("_") or "empresa"


def create_pie_chart(dimensions):
    """
    Cria gráfico de pizza com os pontos obtidos em cada dimensão.

    Observação:
    As fatias representam a composição dos pontos efetivamente obtidos.
    Para comparar maturidade entre dimensões, o PDF também apresenta
    uma tabela com o percentual de cada dimensão.
    """
    labels = list(dimensions.keys())
    values = [float(v) for v in dimensions.values()]

    # Remove dimensões sem pontos para evitar fatias zero.
    filtered = [
        (label, value)
        for label, value in zip(labels, values)
        if value > 0
    ]

    if not filtered:
        filtered = [("Sem pontuação", 1)]

    labels = [item[0] for item in filtered]
    values = [item[1] for item in filtered]

    fig, ax = plt.subplots(figsize=(8, 5.2))
    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
        textprops={"fontsize": 8},
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
    )
    plt.close(fig)
    buffer.seek(0)

    return buffer


def create_bar_chart(dimensions):
    """Cria gráfico adicional para facilitar a comparação da maturidade."""
    labels = list(dimensions.keys())
    values = list(dimensions.values())

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(labels, values)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Maturidade (%)")
    ax.set_title(
        "Maturidade por Dimensão",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()

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


def build_pdf(company, contact, email, phone, role, employees,
               score, level, description, dimensions, answers):
    font_name = register_pdf_font()

    pdf_buffer = io.BytesIO()

    doc = SimpleDocTemplate(
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

    h1_style = ParagraphStyle(
        "CTRHeading1",
        parent=styles["Heading1"],
        fontName=font_name,
        fontSize=15,
        leading=19,
        spaceBefore=5 * mm,
        spaceAfter=3 * mm,
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
    )

    story = []

    # Capa / cabeçalho
    story.append(Paragraph("CTR DEFENSE", title_style))
    story.append(
        Paragraph(
            "CTR CYBERCHECK<br/>Assessment Gratuito de Maturidade em Cibersegurança",
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
        ["Data do assessment", datetime.now().strftime("%d/%m/%Y %H:%M")],
    ]

    info_table = Table(info_data, colWidths=[45 * mm, 125 * mm])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("FONTNAME", (0, 0), (0, -1), font_name),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF3F7")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B7C9D0")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(info_table)
    story.append(Spacer(1, 8 * mm))

    # Score
    story.append(Paragraph("SCORE DE MATURIDADE", h1_style))
    story.append(Paragraph(f"{score}/100", score_style))
    story.append(
        Paragraph(
            f"<b>Nível: {level}</b><br/>{description}",
            body_style,
        )
    )

    # Pizza
    story.append(Paragraph("Composição dos Scores", h1_style))
    pie = create_pie_chart(dimensions)
    story.append(Image(pie, width=165 * mm, height=108 * mm))
    story.append(
        Paragraph(
            "O gráfico de pizza apresenta a composição dos pontos obtidos "
            "entre as dimensões avaliadas. A comparação de maturidade é "
            "detalhada na tabela abaixo.",
            small_style,
        )
    )

    # Tabela de dimensões
    story.append(Paragraph("Resultado por Dimensão", h1_style))

    dimension_rows = [["Dimensão", "Score", "Classificação"]]

    for dimension, value in dimensions.items():
        dim_level, _ = get_level(value)
        dimension_rows.append(
            [dimension, f"{value}/100", dim_level]
        )

    dimension_table = Table(
        dimension_rows,
        colWidths=[95 * mm, 30 * mm, 45 * mm],
        repeatRows=1,
    )

    dimension_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#163A4A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B7C9D0")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(dimension_table)

    # Gráfico de barras
    story.append(PageBreak())
    story.append(Paragraph("Maturidade por Dimensão", h1_style))
    bar = create_bar_chart(dimensions)
    story.append(Image(bar, width=165 * mm, height=93 * mm))

    # Recomendações
    story.append(Paragraph("Recomendações Prioritárias", h1_style))
    for recommendation in RECOMMENDATIONS[level]:
        story.append(
            Paragraph(f"• {recommendation}", body_style)
        )

    # Respostas
    story.append(Paragraph("Resumo das Respostas", h1_style))

    answer_rows = [["#", "Dimensão", "Nota"]]
    for q_id, dimension, _, _ in QUESTIONS:
        answer_rows.append(
            [str(q_id), dimension, str(answers[q_id])]
        )

    answer_table = Table(
        answer_rows,
        colWidths=[12 * mm, 125 * mm, 25 * mm],
        repeatRows=1,
    )

    answer_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#163A4A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CBD5D9")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(answer_table)

    # CTA comercial
    story.append(Spacer(1, 8 * mm))
    story.append(Paragraph("Próximo Passo com a CTR DEFENSE", h1_style))
    story.append(
        Paragraph(
            "O CTR CyberCheck é uma avaliação inicial. Para validar os controles "
            "e transformar os resultados em um plano de ação, a CTR DEFENSE pode "
            "realizar Diagnóstico de Segurança, Assessment de Cibersegurança, "
            "Avaliação de Vulnerabilidades, Análise de Riscos, consultoria em "
            "NIST/ISO 27001, resposta a incidentes e continuidade de negócios.",
            body_style,
        )
    )

    # Aviso
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
            ParagraphStyle(
                "Footer",
                parent=small_style,
                alignment=TA_CENTER,
                fontSize=8,
            ),
        )
    )

    doc.build(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()


# ------------------------------------------------------------
# Interface Streamlit
# ------------------------------------------------------------

st.title("🛡️ CTR CyberCheck")
st.subheader("Assessment Gratuito de Maturidade em Cibersegurança")

st.markdown(
    """
**Descubra o nível de maturidade em cibersegurança da sua empresa.**

Responda às 25 perguntas e receba um **relatório profissional em PDF**, contendo:
**score geral, nível de maturidade, gráfico de pizza, maturidade por dimensão,
recomendações prioritárias e resumo das respostas.**
"""
)

with st.expander("📋 Dados da organização", expanded=True):
    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("Empresa")
        contact = st.text_input("Nome do responsável")
        email = st.text_input("E-mail corporativo")

    with col2:
        phone = st.text_input("WhatsApp / Telefone")
        role = st.text_input("Cargo / Função")
        employees = st.selectbox(
            "Quantidade aproximada de colaboradores",
            ["Selecione", "1–10", "11–50", "51–100",
             "101–250", "251–500", "500+"],
        )

st.divider()
st.header("🔎 Questionário")

st.info(
    "0 = não existe/desconhecido | 1 = informal | 2 = parcial | "
    "3 = aplicado regularmente | 4 = medido/testado"
)

answers = {}

for dimension in dict.fromkeys(q[1] for q in QUESTIONS):
    st.markdown(f"### {dimension}")

    for q_id, q_dimension, nist, question in QUESTIONS:
        if q_dimension != dimension:
            continue

        selected = st.radio(
            f"{q_id}. {question}",
            options=list(OPTIONS.keys()),
            key=f"question_{q_id}",
        )
        answers[q_id] = OPTIONS[selected]

st.divider()

if st.button(
    "🚀 CALCULAR RESULTADO E GERAR RELATÓRIO",
    type="primary",
    use_container_width=True,
):
    if not company or not contact or not email:
        st.warning(
            "Preencha Empresa, Nome do responsável e E-mail corporativo."
        )
        st.stop()

    score = calculate_score(answers)
    level, description = get_level(score)
    dimensions = calculate_dimensions(answers)

    st.success("Assessment concluído!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Score", f"{score}/100")

    with col2:
        st.metric("Nível", level)

    with col3:
        st.metric("Perguntas", "25/25")

    st.progress(score / 100)

    st.markdown("### 🎯 Interpretação")
    st.write(description)

    st.markdown("### 📊 Score por dimensão")

    for dimension, value in dimensions.items():
        st.write(f"**{dimension}: {value}/100**")
        st.progress(value / 100)

    st.markdown("### ⚠️ Recomendações prioritárias")

    for recommendation in RECOMMENDATIONS[level]:
        st.markdown(f"- {recommendation}")

    # Gera PDF somente após cálculo
    with st.spinner("Gerando relatório PDF..."):
        pdf_bytes = build_pdf(
            company=company,
            contact=contact,
            email=email,
            phone=phone,
            role=role,
            employees=employees,
            score=score,
            level=level,
            description=description,
            dimensions=dimensions,
            answers=answers,
        )

    filename = (
        f"CTR_CyberCheck_{safe_filename(company)}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    )

    st.markdown("### 📄 Relatório profissional")

    st.download_button(
        label="📥 BAIXAR RELATÓRIO EM PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        type="primary",
        use_container_width=True,
    )

    st.success(
        "Relatório pronto. O PDF contém o gráfico de pizza, análise por "
        "dimensão, recomendações e respostas do assessment."
    )

st.divider()

st.caption(
    "CTR DEFENSE — Segurança Cibernética e Inteligência contra Ameaças | "
    "CTR CyberCheck"
)
