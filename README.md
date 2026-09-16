# CTR CyberCheck — Assessment Gratuito de Maturidade em Cibersegurança

Aplicação web desenvolvida para a **CTR DEFENSE** com o objetivo de oferecer um assessment inicial e gratuito de maturidade em cibersegurança para empresas.

O sistema apresenta 25 perguntas, calcula um score de maturidade, classifica o nível de segurança da organização, apresenta resultados por dimensão e gera automaticamente um relatório profissional em PDF.

> **Importante:** o CTR CyberCheck é um assessment inicial de maturidade e não substitui uma auditoria, pentest, vulnerability assessment, análise forense, certificação ou avaliação formal de conformidade.

---

## 1. Objetivo

O CTR CyberCheck foi desenvolvido como uma ferramenta de **geração de leads e diagnóstico inicial** para a CTR DEFENSE.

A aplicação permite que potenciais clientes:

- avaliem gratuitamente sua maturidade em cibersegurança;
- identifiquem pontos de atenção;
- visualizem um score geral;
- analisem a maturidade por dimensão;
- recebam recomendações prioritárias;
- gerem um relatório PDF;
- conheçam os próximos passos para uma avaliação profissional.

A metodologia foi estruturada com referência às funções do **NIST Cybersecurity Framework (CSF) 2.0**:

- Govern
- Identify
- Protect
- Detect
- Respond
- Recover

---

## 2. Principais funcionalidades

### Assessment

A aplicação possui **25 perguntas** distribuídas em seis dimensões:

| Dimensão | Quantidade |
|---|---:|
| Governança e Gestão de Riscos | 4 |
| Identificação e Inventário | 4 |
| Proteção e Controle de Acesso | 5 |
| Detecção e Monitoramento | 4 |
| Resposta e Recuperação | 5 |
| Pessoas, Conscientização e Conformidade | 3 |
| **Total** | **25** |

### Sistema de pontuação

Cada pergunta possui cinco níveis de resposta:

| Pontuação | Resposta |
|---:|---|
| 0 | Não existe / desconhecido |
| 1 | Informal ou pontual |
| 2 | Existe parcialmente |
| 3 | Aplicado regularmente |
| 4 | Aplicado, medido e/ou testado |

O score final é convertido para uma escala de **0 a 100**.

### Classificação de maturidade

| Score | Nível |
|---:|---|
| 0–24 | Crítico |
| 25–49 | Inicial |
| 50–69 | Em Desenvolvimento |
| 70–84 | Estruturado |
| 85–100 | Maduro |

---

## 3. Relatório PDF

Após o preenchimento do assessment, a aplicação permite gerar um relatório PDF contendo:

- identificação da empresa;
- informações do responsável;
- score geral;
- nível de maturidade;
- análise por dimensão;
- gráfico de composição dos scores;
- gráfico de maturidade por dimensão;
- recomendações prioritárias;
- resumo das respostas;
- chamada para os serviços da CTR DEFENSE;
- aviso metodológico e limitações do assessment.

O arquivo é gerado localmente pelo Streamlit e pode ser baixado pelo usuário.

---


---

## 4. Fluxo de utilização

O fluxo básico é:

```text
Acesso ao CyberCheck
        ↓
Dados da empresa
        ↓
25 perguntas
        ↓
Cálculo do score
        ↓
Classificação da maturidade
        ↓
Resultado por dimensão
        ↓
Recomendações
        ↓
Geração do relatório PDF
        ↓
Download do relatório
        ↓
CTA para contato com a CTR DEFENSE
```

---




---

## 11. Possíveis evoluções

A versão atual pode ser evoluída para uma plataforma comercial completa.

### CRM

Integração com:

- CRM;
- e-mail;
- WhatsApp;
- automação de marketing;
- pipeline comercial.

### Banco de dados

Armazenamento de:

- empresa;
- contato;
- score;
- respostas;
- data do assessment;
- histórico de avaliações;

Interpretação:

> A organização possui controles relevantes, porém apresenta oportunidades de melhoria principalmente em detecção, resposta e recuperação. Recomenda-se priorizar monitoramento, gestão de incidentes, testes de recuperação e formalização dos processos.

---

## 15. Boas práticas para evolução do projeto

Para desenvolvimento contínuo:

1. manter o código versionado;
2. documentar alterações;
3. testar alterações antes da publicação;
4. manter dependências atualizadas;
5. utilizar ambiente de desenvolvimento separado da produção;
6. proteger secrets;
7. implementar testes automatizados;
8. revisar o questionário periodicamente;
9. revisar o modelo de scoring;
10. validar a metodologia com profissionais de segurança.

---



