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

## 5. Público-alvo

A ferramenta foi pensada principalmente para:

- pequenas empresas;
- médias empresas;
- gestores;
- diretores;
- responsáveis por TI;
- responsáveis por segurança da informação;
- responsáveis por compliance;
- empresas que estão iniciando sua jornada de segurança cibernética.

---

## 6. Uso comercial pela CTR DEFENSE

O CyberCheck pode funcionar como um **lead magnet** no site da CTR DEFENSE.

### Oferta gratuita

O usuário recebe:

- assessment;
- score;
- nível de maturidade;
- principais pontos de atenção;
- recomendações iniciais;
- relatório PDF.

### Serviços profissionais

Após o assessment, a CTR DEFENSE pode oferecer serviços como:

- Assessment completo de Cibersegurança;
- análise de riscos;
- diagnóstico de segurança;
- vulnerability assessment;
- pentest;
- análise de exposição externa;
- adequação à LGPD;
- implementação de ISO/IEC 27001;
- implantação de controles de segurança;
- elaboração de políticas;
- gestão de vulnerabilidades;
- Threat Intelligence;
- monitoramento e resposta a incidentes;
- Security Awareness;
- preparação para auditorias e due diligence.

---

## 7. Recomendações comerciais

O resultado gratuito deve ser apresentado como uma **avaliação inicial**, evitando transformar o score em uma promessa de segurança absoluta.

Exemplo de CTA:

> **Sua empresa descobriu o nível de maturidade. E agora?**
>
> A CTR DEFENSE pode transformar os pontos identificados neste assessment em um plano prático de evolução da segurança cibernética da sua organização.
>
> **Solicite uma avaliação profissional.**

Botões sugeridos:

```text
SOLICITAR AVALIAÇÃO PROFISSIONAL
FALAR COM A CTR DEFENSE
AGENDAR DIAGNÓSTICO
```

---

## 8. Privacidade e proteção de dados

Caso a aplicação seja publicada na internet, recomenda-se implementar controles adicionais para tratamento dos dados informados pelos participantes.

Entre eles:

- HTTPS obrigatório;
- política de privacidade;
- aviso de tratamento de dados;
- consentimento quando aplicável;
- minimização de dados;
- controle de acesso;
- proteção dos relatórios;
- retenção definida;
- exclusão periódica de dados;
- proteção contra spam e abuso;
- logs de segurança;
- rate limiting;
- proteção de infraestrutura.

Se os dados forem armazenados ou enviados para terceiros, a arquitetura deve ser revisada para atender aos requisitos aplicáveis da **LGPD**.

---

## 9. Segurança da aplicação

Antes de colocar a ferramenta em produção, recomenda-se:

- não armazenar senhas no código;
- não armazenar chaves/API tokens diretamente no arquivo Python;
- utilizar variáveis de ambiente ou secrets;
- habilitar HTTPS;
- restringir acesso administrativo;
- validar entradas do usuário;
- evitar exposição de informações internas;
- manter Python e bibliotecas atualizados;
- utilizar dependências fixadas em ambiente de produção;
- realizar backup quando houver armazenamento de dados;
- implementar monitoramento;
- revisar os logs periodicamente.

---

## 10. Implantação em produção

A aplicação pode ser hospedada em diferentes ambientes, por exemplo:

- servidor Linux com Streamlit;
- Docker;
- cloud pública;
- VM;
- plataforma de hospedagem compatível com Streamlit.

Para produção, recomenda-se colocar um **reverse proxy** na frente da aplicação e utilizar HTTPS.

Arquitetura simplificada:

```text
Internet
   │
   ▼
HTTPS / Reverse Proxy
   │
   ▼
Streamlit
   │
   ├── Assessment
   ├── Cálculo
   ├── Gráficos
   └── PDF
```

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
- relatórios.

### Dashboard administrativo

Possíveis indicadores:

- número de assessments;
- leads por período;
- score médio;
- maturidade média;
- principais riscos;
- empresas por nível de maturidade;
- conversão em oportunidades comerciais.

### Relatórios avançados

Possibilidades:

- relatório executivo;
- relatório técnico;
- plano de ação;
- matriz de riscos;
- roadmap de 30/60/90 dias;
- comparação entre assessments;
- benchmarking.

### Integração com frameworks

Futuras versões podem mapear resultados para:

- NIST CSF 2.0;
- ISO/IEC 27001;
- ISO/IEC 27002;
- CIS Controls;
- LGPD;
- requisitos setoriais;
- requisitos de clientes e fornecedores.

---

## 12. Limitações

O CyberCheck não realiza automaticamente:

- varredura de portas;
- exploração de vulnerabilidades;
- pentest;
- análise de código;
- análise de malware;
- investigação forense;
- validação técnica dos controles;
- auditoria formal;
- certificação;
- emissão de relatório de conformidade.

As respostas dependem das informações fornecidas pelo participante.

Por isso, o resultado deve ser interpretado como **indicativo de maturidade**, e não como garantia de que a organização esteja segura.

---

## 13. Metodologia

A estrutura do assessment utiliza conceitos alinhados ao **NIST Cybersecurity Framework 2.0**, especialmente suas seis funções:

```text
GOVERN
   ↓
IDENTIFY
   ↓
PROTECT
   ↓
DETECT
   ↓
RESPOND
   ↓
RECOVER
```

O questionário foi adaptado para uma avaliação inicial de empresas e não constitui uma implementação completa do NIST CSF.

---

## 14. Exemplo de resultado

Um resultado hipotético:

```text
Empresa: Empresa Exemplo Ltda.

Score geral: 67/100

Maturidade:
EM DESENVOLVIMENTO
```

Distribuição:

```text
Governança e Gestão de Riscos       70%
Identificação e Inventário          65%
Proteção e Controle de Acesso       75%
Detecção e Monitoramento             50%
Resposta e Recuperação               55%
Pessoas e Conformidade               60%
```

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

## 16. Licença e propriedade

Este projeto foi desenvolvido para utilização da **CTR DEFENSE**.

O conteúdo, metodologia adaptada, identidade visual, textos comerciais e materiais relacionados devem ser tratados conforme os direitos e condições definidos pela CTR DEFENSE.


