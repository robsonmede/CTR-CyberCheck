import streamlit as st
from datetime import datetime

# ============================================================
# CTR DEFENSE - CYBERCHECK
# Assessment Gratuito de Maturidade em Cibersegurança
# Streamlit
# ============================================================

st.set_page_config(
    page_title="CTR CyberCheck | CTR DEFENSE",
    page_icon="🛡️",
    layout="wide",
)

# -----------------------------
# Configurações
# -----------------------------
OPTIONS = {
    "0 — Não existe / desconhecido": 0,
    "1 — Informal ou pontual": 1,
    "2 — Existe parcialmente": 2,
    "3 — Aplicado regularmente": 3,
    "4 — Aplicado, medido e/ou testado": 4,
}

LEVELS = [
    (0, 24, "Crítico", "Controles inexistentes ou muito frágeis. A exposição a riscos básicos é elevada."),
    (25, 49, "Inicial", "Existem algumas medidas, porém são informais, incompletas ou inconsistentes."),
    (50, 69, "Em Desenvolvimento", "Controles relevantes estão presentes, mas ainda existem lacunas importantes."),
    (70, 84, "Estruturado", "Boa base de segurança, com oportunidades de melhoria e maior formalização."),
    (85, 100, "Maduro", "Controles amplamente estabelecidos, acompanhados e testados. A evolução deve ser contínua."),
]

QUESTIONS = [
    {
        "id": 1,
        "dimension": "Governança e Gestão de Riscos",
        "nist": "Govern",
        "question": "A empresa possui uma política formal de segurança da informação aprovada pela direção?",
    },
    {
        "id": 2,
        "dimension": "Governança e Gestão de Riscos",
        "nist": "Govern",
        "question": "Os principais riscos cibernéticos da empresa são identificados e avaliados periodicamente?",
    },
    {
        "id": 3,
        "dimension": "Governança e Gestão de Riscos",
        "nist": "Govern",
        "question": "Existem responsáveis claramente definidos pelas atividades de segurança cibernética?",
    },
    {
        "id": 4,
        "dimension": "Governança e Gestão de Riscos",
        "nist": "Govern",
        "question": "A empresa possui requisitos de segurança para fornecedores e parceiros críticos?",
    },
    {
        "id": 5,
        "dimension": "Identificação e Inventário",
        "nist": "Identify",
        "question": "A empresa mantém inventário atualizado de computadores, servidores, dispositivos de rede, aplicações e serviços em nuvem?",
    },
    {
        "id": 6,
        "dimension": "Identificação e Inventário",
        "nist": "Identify",
        "question": "Os dados críticos são identificados e classificados de acordo com sua importância e sensibilidade?",
    },
    {
        "id": 7,
        "dimension": "Identificação e Inventário",
        "nist": "Identify",
        "question": "Existe uma avaliação periódica de vulnerabilidades e configurações de segurança?",
    },
    {
        "id": 8,
        "dimension": "Identificação e Inventário",
        "nist": "Identify",
        "question": "A empresa conhece quais sistemas e dados são mais críticos para a continuidade do negócio?",
    },
    {
        "id": 9,
        "dimension": "Proteção e Controle de Acesso",
        "nist": "Protect",
        "question": "O acesso aos sistemas é concedido de acordo com a função e o princípio do menor privilégio?",
    },
    {
        "id": 10,
        "dimension": "Proteção e Controle de Acesso",
        "nist": "Protect",
        "question": "A autenticação multifator (MFA) está habilitada para contas administrativas e sistemas críticos?",
    },
    {
        "id": 11,
        "dimension": "Proteção e Controle de Acesso",
        "nist": "Protect",
        "question": "Existem processos para criação, alteração e revogação de acessos quando funcionários entram, mudam de função ou saem da empresa?",
    },
    {
        "id": 12,
        "dimension": "Proteção e Controle de Acesso",
        "nist": "Protect",
        "question": "Computadores e servidores utilizam proteção contra malware/EDR e recebem atualizações de segurança?",
    },
    {
        "id": 13,
        "dimension": "Proteção e Controle de Acesso",
        "nist": "Protect",
        "question": "Os backups dos dados críticos são realizados regularmente e protegidos contra alteração ou exclusão indevida?",
    },
    {
        "id": 14,
        "dimension": "Detecção e Monitoramento",
        "nist": "Detect",
        "question": "A empresa monitora eventos relevantes de segurança em servidores, endpoints, rede ou serviços em nuvem?",
    },
    {
        "id": 15,
        "dimension": "Detecção e Monitoramento",
        "nist": "Detect",
        "question": "Existem alertas ou mecanismos para identificar atividades suspeitas, tentativas de invasão ou comportamento anômalo?",
    },
    {
        "id": 16,
        "dimension": "Detecção e Monitoramento",
        "nist": "Detect",
        "question": "Logs de sistemas críticos são mantidos por período definido e podem ser consultados quando ocorre um incidente?",
    },
    {
        "id": 17,
        "dimension": "Detecção e Monitoramento",
        "nist": "Detect",
        "question": "A empresa acompanha notícias, vulnerabilidades e ameaças relevantes para seu ambiente tecnológico?",
    },
    {
        "id": 18,
        "dimension": "Resposta e Recuperação",
        "nist": "Respond",
        "question": "Existe um plano documentado de resposta a incidentes de segurança?",
    },
    {
        "id": 19,
        "dimension": "Resposta e Recuperação",
        "nist": "Respond",
        "question": "A empresa sabe quem deve ser acionado em caso de ransomware, vazamento de dados ou indisponibilidade crítica?",
    },
    {
        "id": 20,
        "dimension": "Resposta e Recuperação",
        "nist": "Respond",
        "question": "São realizados testes ou simulações para validar a capacidade de resposta a incidentes?",
    },
    {
        "id": 21,
        "dimension": "Resposta e Recuperação",
        "nist": "Recover",
        "question": "Existe um plano de continuidade e/ou recuperação de desastres para serviços críticos?",
    },
    {
        "id": 22,
        "dimension": "Resposta e Recuperação",
        "nist": "Recover",
        "question": "Os backups são testados periodicamente para confirmar que a restauração realmente funciona?",
    },
    {
        "id": 23,
        "dimension": "Pessoas, Conscientização e Conformidade",
        "nist": "Protect",
        "question": "Os colaboradores recebem treinamento periódico sobre phishing, engenharia social, senhas e segurança digital?",
    },
    {
        "id": 24,
        "dimension": "Pessoas, Conscientização e Conformidade",
        "nist": "Govern",
        "question": "A empresa possui procedimentos para tratamento de incidentes envolvendo dados pessoais e requisitos aplicáveis da LGPD?",
    },
    {
        "id": 25,
        "dimension": "Pessoas, Conscientização e Conformidade",
        "nist": "Govern",
        "question": "A direção acompanha indicadores ou relatórios de segurança para tomar decisões e priorizar investimentos?",
    },
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


def get_level(score: float):
    for minimum, maximum, name, description in LEVELS:
        if minimum <= score <= maximum:
            return name, description
    return "Indefinido", ""


def calculate_score(answers: dict):
    total = sum(answers.values())
    maximum = len(QUESTIONS) * 4
    score = (total / maximum) * 100
    return round(score, 1)


def calculate_dimensions(answers: dict):
    data = {}
    for q in QUESTIONS:
        dimension = q["dimension"]
        data.setdefault(dimension, [])
        data[dimension].append(answers[q["id"]])

    result = {}
    for dimension, values in data.items():
        result[dimension] = round((sum(values) / (len(values) * 4)) * 100, 1)

    return result


def build_csv(answers, score, level, dimensions):
    lines = [
        "CTR DEFENSE - CTR CyberCheck",
        f"Data;{datetime.now().strftime('%d/%m/%Y %H:%M')}",
        f"Score;{score}",
        f"Nível;{level}",
        "",
        "Pergunta;Dimensão;NIST CSF;Nota",
    ]

    for q in QUESTIONS:
        lines.append(
            f'"{q["question"]}";"{q["dimension"]}";"{q["nist"]}";{answers[q["id"]]}'
        )

    lines += ["", "Dimensão;Score"]
    for dimension, value in dimensions.items():
        lines.append(f'"{dimension}";{value}')

    return "\n".join(lines).encode("utf-8-sig")


# -----------------------------
# Cabeçalho
# -----------------------------
st.title("🛡️ CTR CyberCheck")
st.subheader("Assessment Gratuito de Maturidade em Cibersegurança")

st.markdown(
    """
**Descubra o nível de maturidade em cibersegurança da sua empresa.**

Responda 25 perguntas objetivas e receba um **score de 0 a 100**, seu nível de
maturidade, análise por dimensão e recomendações prioritárias.

> **Importante:** esta ferramenta é uma avaliação inicial baseada nas respostas
> fornecidas. Não substitui pentest, auditoria, assessment técnico, certificação
> ou análise baseada em evidências.
"""
)

# -----------------------------
# Dados do lead
# -----------------------------
with st.expander("📋 Dados da organização — recomendado para geração de leads", expanded=True):
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
            ["Selecione", "1–10", "11–50", "51–100", "101–250", "251–500", "500+"],
        )

st.divider()

# -----------------------------
# Questionário
# -----------------------------
st.header("🔎 Questionário")

st.info(
    "Escala: 0 = não existe/desconhecido | 1 = informal | "
    "2 = parcial | 3 = aplicado regularmente | 4 = medido/testado."
)

answers = {}

for dimension in dict.fromkeys(q["dimension"] for q in QUESTIONS):
    st.markdown(f"### {dimension}")

    dimension_questions = [q for q in QUESTIONS if q["dimension"] == dimension]

    for q in dimension_questions:
        answers[q["id"]] = st.radio(
            f"{q['id']}. {q['question']}",
            options=list(OPTIONS.keys()),
            key=f"question_{q['id']}",
            horizontal=False,
        )

        # Converte imediatamente o texto selecionado em nota
        answers[q["id"]] = OPTIONS[answers[q["id"]]]

st.divider()

# -----------------------------
# Resultado
# -----------------------------
if st.button("🚀 CALCULAR MEU RESULTADO", type="primary", use_container_width=True):

    if not company or not contact or not email:
        st.warning(
            "Preencha pelo menos Empresa, Nome do responsável e E-mail corporativo "
            "antes de calcular o resultado."
        )
        st.stop()

    score = calculate_score(answers)
    level, description = get_level(score)
    dimensions = calculate_dimensions(answers)

    st.success("Assessment concluído!")

    # Score principal
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Score de Maturidade", f"{score}/100")

    with col2:
        st.metric("Nível", level)

    with col3:
        st.metric("Perguntas", f"{len(QUESTIONS)}/25")

    st.progress(min(score / 100, 1.0))

    st.markdown(f"### 🎯 Interpretação")
    st.write(description)

    # Resultado por dimensão
    st.markdown("### 📊 Resultado por dimensão")

    for dimension, value in dimensions.items():
        st.write(f"**{dimension}: {value}/100**")
        st.progress(min(value / 100, 1.0))

    # Pontos prioritários
    st.markdown("### ⚠️ Recomendações prioritárias")

    for recommendation in RECOMMENDATIONS[level]:
        st.markdown(f"- {recommendation}")

    # Próximos passos
    st.markdown("### 🚀 Próximos passos sugeridos pela CTR DEFENSE")

    if level in ("Crítico", "Inicial"):
        st.warning(
            "O resultado indica a necessidade de estruturar controles básicos e "
            "priorizar riscos que podem afetar dados, sistemas e continuidade do negócio."
        )
    elif level == "Em Desenvolvimento":
        st.info(
            "A empresa possui uma base de segurança, mas pode obter ganhos relevantes "
            "com um plano estruturado de evolução."
        )
    else:
        st.success(
            "A empresa apresenta uma base estruturada de segurança. O próximo passo "
            "é validar controles, medir resultados e evoluir continuamente."
        )

    st.markdown(
        """
**A CTR DEFENSE pode apoiar sua organização com:**

- Diagnóstico de Segurança
- Assessment de Cibersegurança
- Avaliação de Vulnerabilidades
- Análise de Riscos Cibernéticos
- Gestão de Identidade e Acessos
- Consultoria ISO 27001 / NIST
- Resposta a Incidentes
- Continuidade e Recuperação
- Segurança em Cloud
- Threat Intelligence
- Adequação a requisitos de clientes e fornecedores
"""
    )

    # Download CSV
    csv_data = build_csv(answers, score, level, dimensions)

    st.download_button(
        label="📥 Baixar resultado do Assessment (CSV)",
        data=csv_data,
        file_name="ctr_cybercheck_resultado.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # Resumo para CRM
    summary = f"""
CTR DEFENSE - CTR CyberCheck
Empresa: {company}
Responsável: {contact}
E-mail: {email}
Telefone: {phone}
Cargo: {role}
Colaboradores: {employees}
Score: {score}/100
Nível: {level}
"""

    st.download_button(
        label="📄 Baixar resumo comercial",
        data=summary.encode("utf-8"),
        file_name="ctr_cybercheck_resumo_comercial.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.divider()

st.caption(
    "CTR DEFENSE — Segurança Cibernética e Inteligência contra Ameaças | "
    "CTR CyberCheck | Assessment inicial de maturidade"
)
