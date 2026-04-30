# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../../../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%">
  </a>
</p>









# Sompo RiskRadar - Sistema Preditivo de Risco para Equipamentos Agrícolas

> **Challenge FIAP x Sompo Seguros** | Sprint 1

---

## 👨‍🎓 Integrantes:
- <a href="https://www.linkedin.com/in/beatriz-barreto-pinto-btrz">Beatriz Moreira Barreto Pinto</a>
- <a href="https://www.linkedin.com/in/gustoliver-caldas-7a9a33350">Gustavo de Oliveira Caldas</a>
- <a href="https://www.linkedin.com/in/jfnalves">João Felipe das Neves Alves</a>
- <a href="https://www.linkedin.com/in/paulocbarreto">Paulo Oliveira</a>
- <a href="https://www.linkedin.com/in/tamiresvferreiras/">Tamires Ferreira</a>

## 👩‍🏫 Professores:
### Tutor(a)
- <a href="https://www.linkedin.com/in/nicollycrsouza">Nicolly Candida Rodrigues de Souza</a>

### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato">André Godoi Chiovato</a>

## 📋 Sumário

1. [Descrição do Problema](#1-descrição-do-problema)
2. [Solução Proposta](#2-solução-proposta)
3. [Personas e Necessidades](#3-personas-e-necessidades)
4. [User Stories](#4-user-stories)
5. [Estrutura dos Dados](#5-estrutura-dos-dados)
6. [Arquitetura da Solução](#6-arquitetura-da-solução)
7. [Proposta do Modelo Preditivo](#7-proposta-do-modelo-preditivo)
8. [Stack Tecnológica](#8-stack-tecnológica)
9. [Segurança](#9-segurança)
10. [Planejamento das Próximas Sprints](#10-planejamento-das-próximas-sprints)
11. [Equipe](#11-equipe)
12. [Apresentação em Vídeo](#12-apresentação-em-vídeo)

---

## 1. Descrição do Problema

### Contexto

O agronegócio brasileiro depende fortemente de maquinários de alto valor, colheitadeiras, tratores, plantadeiras, que operam em condições ambientais adversas e variáveis. A Sompo Seguros, parceira deste desafio, identifica um problema central em sua carteira: **a alta sinistralidade de equipamentos agrícolas causada por eventos que poderiam ser previstos e evitados**.

Atualmente, a tomada de decisão dos gestores de frota é majoritariamente **reativa**: o dano ocorre, o operador reporta, a seguradora aciona o processo de sinistro. Não há um sistema que antecipe o risco, oriente o gestor antes da operação e o ajude a tomar decisões preventivas baseadas em dados ambientais e operacionais.

### Impactos do Problema

- Custos elevados com sinistros evitáveis (atolamento, danos por chuva, colisões em transporte)
- Perda de produtividade por paralisação de equipamentos em campo
- Dificuldade do gestor em monitorar múltiplos operadores e máquinas simultaneamente
- Falta de visibilidade sobre o histórico de risco por equipamento ou região
- Ausência de incentivo financeiro claro para a manutenção preventiva

### Por que focar no Gestor?

O gestor de operações é o elo entre a seguradora e os operadores em campo. Ele é quem:

- Autoriza o início de operações
- Define rotas de transporte de equipamentos
- Acompanha o uso da frota
- Responde pelos sinistros perante a seguradora

Uma solução direcionada ao gestor tem **maior alavancagem**: uma única decisão sua pode proteger múltiplos equipamentos e operadores ao mesmo tempo.

---

## 2. Solução Proposta

### O que é a Sompo RiskRadar?

A **Sompo RiskRadar** é uma plataforma de gestão de risco preditivo para frotas de equipamentos agrícolas, com foco no gestor de operações. A solução integra dados climáticos, ambientais e operacionais para gerar:

1. **Alertas antecipados de risco climático** — com base na previsão dos próximos dias, o sistema informa ao gestor quais equipamentos e regiões estão em situação de risco elevado antes que a operação comece.

2. **Recomendações de ação pós-evento cotidiano** — após chuvas, variações bruscas de temperatura ou outros eventos climáticos do dia a dia, o sistema sugere ações de manutenção e preservação específicas para cada equipamento afetado.

3. **Painel de economia e risco acumulado** — o gestor visualiza, em perspectiva financeira, o quanto foi economizado em sinistros ao seguir as recomendações e o risco acumulado de equipamentos com manutenção negligenciada.

### Valor Entregue

| Para quem           | Valor                                              |
| ------------------- | -------------------------------------------------- |
| Gestor de operações | Decisões baseadas em dados, não em intuição        |
| Operadores          | Alertas claros antes de iniciar operações de risco |
| Sompo Seguros       | Redução na incidência de sinistros evitáveis       |

### KPI Principal

> **Redução na incidência de sinistros** — medido comparando o histórico de acionamentos antes e depois da adoção da plataforma, com recorte específico para sinistros após eventos climáticos de médio e grande porte.

---

## 3. Personas e Necessidades

### Persona 1 — Gestor de Operações (Persona Principal)

**Perfil:** Responsável pela gestão de uma frota de 5 a 30 equipamentos agrícolas. Acompanha o trabalho de múltiplos operadores em campo, muitas vezes em diferentes propriedades ou regiões.

**Dores:**

- Não tem visibilidade consolidada do risco da frota em tempo real
- Toma decisões de "liberar" ou "segurar" operações com base em experiência pessoal, sem dados climáticos integrados
- Não consegue rastrear quais equipamentos passaram por condições adversas recentemente
- Dificuldade em justificar para a diretoria o investimento em manutenção preventiva

**Necessidades na solução:**

- Dashboard centralizado com status de risco de cada equipamento
- Alertas consolidados por região e janela de tempo (próximas 24h, 48h)
- Histórico de recomendações cumpridas e descumpridas
- Relatório de impacto financeiro das ações preventivas

**Como a Sompo RiskRadar ajuda:** O gestor acessa o painel pela manhã, verifica o mapa de risco da semana, recebe alertas automáticos por e-mail/SMS para eventos climáticos significativos e acompanha o histórico de manutenções realizadas.

---

###  Persona 2 — Operador de Campo

**Perfil:** Profissional que opera o equipamento diretamente. Pode ou não ter acesso a smartphone em campo. Recebe instruções do gestor.

**Dores:**

- Não tem informação sobre condições do solo antes de entrar em uma área
- Não sabe quais cuidados tomar com o equipamento após uma chuva forte
- Depende de comunicação verbal com o gestor para receber orientações

**Necessidades na solução:**

- Alertas simples e objetivos (verde/amarelo/vermelho) para a operação do dia
- Instruções claras de pós-evento (ex: "Após chuva acima de 30mm, inspecione o sistema de tração")
- Interface funcional mesmo em áreas com conexão limitada

**Como o Sompo RiskRadar ajuda:** O operador recebe pelo app ou SMS um resumo do status do dia: se a operação está liberada, restrita ou suspensa, com a justificativa em linguagem simples.

---

###  Persona 3 — Analista de Sinistros (Sompo Seguros)

**Perfil:** Profissional da seguradora responsável por avaliar e processar sinistros da carteira agro.

**Dores:**

- Dificuldade em correlacionar sinistros com eventos ambientais ocorridos no período
- Falta de histórico de comportamento operacional do segurado antes do sinistro
- Processo de análise lento por ausência de dados estruturados

**Necessidades na solução:**

- Acesso ao histórico de alertas emitidos e ações tomadas pelo gestor
- Relatório de condições ambientais no momento do sinistro
- Score de risco acumulado do equipamento no período

**Como a Sompo RiskRadar ajuda:** A seguradora acessa (mediante autorização do segurado) um relatório estruturado do histórico de risco e ações do equipamento sinistrado, acelerando a análise e permitindo uma tarifação mais precisa.

---

## 4. User Stories

> O grupo optou por desenvolver soluções para as seguintes user stories, priorizadas pela árvore de oportunidades com foco no outcome **redução na incidência de sinistros**:

### ✅ US-01 — Alerta Antecipado de Risco Climático (Alta Prioridade)

**Como** gestor de operações,  
**quero** receber alertas automáticos quando a previsão climática dos próximos dias representar risco elevado para equipamentos em campo,  
**para que** eu possa antecipar decisões de suspender, redirecionar ou preparar operações antes que o evento ocorra.

**Indicador:** Redução no acionamento de sinistros após eventos climáticos de médio e grande porte.

**Critérios de aceite:**

- O sistema consulta previsão climática com antecedência mínima de 24 horas
- Alertas são classificados em níveis de: atenção (amarelo), alerta (laranja) e suspensão recomendada (vermelho)
- O gestor recebe notificação por e-mail e/ou push notification
- O alerta indica quais equipamentos e regiões estão afetados

---

### ✅ US-02 — Recomendações de Manutenção Pós-Evento (Alta Prioridade)

**Como** gestor de operações,  
**quero** receber sugestões de ação específicas para cada equipamento após eventos climáticos cotidianos,  
**para que** eu possa orientar os operadores a realizarem os cuidados adequados e preservar o maquinário.

**Indicador:** Aumento no número de manutenções preventivas realizadas entre ciclos de renovação do seguro.

**Critérios de aceite:**

- O sistema detecta automaticamente a ocorrência de eventos climáticos relevantes (chuva acima de X mm, temperatura abaixo de Y°C, etc.)
- As recomendações são específicas por tipo de equipamento (colheitadeira, trator, plantadeira)
- As ações sugeridas são registradas e o gestor pode marcar como "realizada" ou "pendente"
- O histórico de recomendações cumpridas fica disponível no painel

---

### 🔄 US-03 — Painel de Economia e Risco Acumulado (Prioridade Média)

**Como** gestor de operações,  
**quero** visualizar o impacto financeiro estimado das ações preventivas realizadas com base nas recomendações do sistema,  
**para que** eu possa justificar o investimento em manutenção preventiva e demonstrar o valor do programa à diretoria e à seguradora.

**Indicador:** Aumento no engajamento com manutenção preventiva (medido pela taxa de recomendações cumpridas).

**Critérios de aceite:**

- O painel exibe economia estimada (sinistros evitados × custo médio histórico)
- O painel exibe risco acumulado para equipamentos com recomendações não cumpridas
- Os dados são apresentados por equipamento, período e categoria de risco
- A visualização é simples e interpretável sem conhecimento técnico

> **Nota sobre integração:** As três user stories foram desenhadas de forma complementar e integrada. A US-03 depende dos dados gerados pelas US-01 e US-02, portanto a sequência de desenvolvimento segue essa ordem. A integração entre os módulos é parte central da arquitetura proposta.

---

## 5. Estrutura dos Dados

### 5.1 Variáveis do Dataset

| Variável                 | Tipo       | Descrição                                                      | Exemplo                                   |
| ------------------------ | ---------- | -------------------------------------------------------------- | ----------------------------------------- |
| `equipamento_id`         | string     | Identificador único do equipamento                             | EQ-2024-001                               |
| `tipo_equipamento`       | categórico | Tipo da máquina agrícola                                       | colheitadeira, trator, plantadeira        |
| `data_hora`              | datetime   | Momento do registro                                            | 2024-08-15 14:30:00                       |
| `latitude`               | float      | Coordenada geográfica                                          | -23.5505                                  |
| `longitude`              | float      | Coordenada geográfica                                          | -46.6333                                  |
| `temperatura_c`          | float      | Temperatura em graus Celsius                                   | 28.5                                      |
| `precipitacao_mm`        | float      | Chuva acumulada nas últimas 24h (mm)                           | 45.2                                      |
| `umidade_relativa`       | float      | Umidade do ar (%)                                              | 82.0                                      |
| `velocidade_vento_kmh`   | float      | Velocidade do vento (km/h)                                     | 35.0                                      |
| `tipo_solo`              | categórico | Classificação pedológica da área                               | argiloso, arenoso, misto                  |
| `umidade_solo`           | float      | Umidade do solo (%)                                            | 73.0                                      |
| `distancia_corrego_m`    | float      | Distância do equipamento ao corpo d'água mais próximo (metros) | 120.0                                     |
| `declive_terreno`        | categórico | Inclinação da área de operação                                 | plano, suave, acentuado                   |
| `tipo_operacao`          | categórico | Natureza da atividade no momento                               | colheita, plantio, transporte, manutenção |
| `horas_uso_acumuladas`   | int        | Total de horas de uso do equipamento                           | 1250                                      |
| `dias_ultima_manutencao` | int        | Dias desde a última manutenção registrada                      | 45                                        |
| `previsao_chuva_48h_mm`  | float      | Precipitação prevista para as próximas 48h                     | 80.0                                      |
| `nivel_risco`            | categórico | **Variável-alvo** — nível de risco calculado                   | baixo, médio, alto, crítico               |
| `sinistro_ocorrido`      | bool       | Se ocorreu sinistro no período                                 | True / False                              |

### 5.2 Dataset Simulado — Exemplo

```csv
equipamento_id,tipo_equipamento,data_hora,latitude,longitude,temperatura_c,precipitacao_mm,umidade_relativa,velocidade_vento_kmh,tipo_solo,umidade_solo,distancia_corrego_m,declive_terreno,tipo_operacao,horas_uso_acumuladas,dias_ultima_manutencao,previsao_chuva_48h_mm,nivel_risco,sinistro_ocorrido
EQ-2024-001,colheitadeira,2024-08-15 08:00:00,-23.55,-46.63,26.0,12.0,75.0,18.0,argiloso,65.0,95.0,suave,colheita,1250,30,65.0,alto,False
EQ-2024-002,trator,2024-08-15 08:00:00,-23.48,-46.70,26.0,12.0,75.0,18.0,arenoso,40.0,350.0,plano,plantio,430,12,65.0,baixo,False
EQ-2024-003,colheitadeira,2024-08-15 08:00:00,-23.60,-46.55,26.0,12.0,75.0,18.0,argiloso,80.0,60.0,acentuado,colheita,2100,62,65.0,crítico,True
EQ-2024-004,plantadeira,2024-08-15 08:00:00,-23.52,-46.68,26.0,12.0,75.0,18.0,misto,55.0,200.0,plano,transporte,780,8,65.0,médio,False
```

### 5.3 Fontes de Dados

| Fonte                             | Tipo               | Dados                                    |
| --------------------------------- | ------------------ | ---------------------------------------- |
| INMET / Open-Meteo API            | Externa / Gratuita | Clima atual e histórico                  |
| OpenWeather API                   | Externa / Freemium | Previsão dos próximos 5 dias             |
| EMBRAPA / IBGE                    | Externa / Pública  | Tipo de solo por região                  |
| GPS do equipamento / IoT          | Interna (simulada) | Localização e operação em tempo real     |
| Sistema de manutenção             | Interna (simulada) | Histórico de manutenções                 |
| Base histórica de sinistros Sompo | Parceiro           | Sinistros reais por equipamento e região |

---

## 6. Arquitetura da Solução

```
┌─────────────────────────────────────────────────────────────┐
│                     FONTES DE DADOS                         │
│  [GPS/IoT Equipamento] [API Clima] [Base Solo] [Histórico]  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                  CAMADA DE INGESTÃO                         │
│        Pipeline de coleta e normalização de dados           │
│             (Python + Apache Kafka / Scheduler)             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│               CAMADA DE PROCESSAMENTO                       │
│     Limpeza, enriquecimento e feature engineering           │
│              (Python + Pandas / PySpark)                    │
│                                                             │
│  - Cruzamento: localização do equipamento × previsão clima  │
│  - Cruzamento: tipo de solo × umidade × proximidade d'água  │
│  - Cálculo de variáveis derivadas (dias sem manutenção etc) │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   CAMADA DE MODELO (IA)                     │
│           Classificador de Risco + Score de Risco           │
│         (Scikit-learn / XGBoost / Random Forest)            │
│                                                             │
│  Entrada: variáveis ambientais + operacionais               │
│  Saída: nível de risco (baixo/médio/alto/crítico) +         │
│         probabilidade de sinistro + recomendações           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                   CAMADA DE API                             │
│            Backend REST que serve os dados                  │
│                  (Python + FastAPI)                         │
└─────────┬─────────────────────────────┬─────────────────────┘
          │                             │
          ▼                             ▼
┌──────────────────┐          ┌──────────────────────────────┐
│  DASHBOARD WEB   │          │    NOTIFICAÇÕES AUTOMÁTICAS  │
│  (React / Vue)   │          │     (E-mail / SMS / Push)    │
│                  │          │                              │
│ - Mapa de risco  │          │ - Alertas de risco alto/     │
│ - Status frota   │          │   crítico em tempo real      │
│ - Recomendações  │          │ - Recomendações pós-evento   │
│ - Painel financ. │          │ - Resumo diário para gestor  │
└──────────────────┘          └──────────────────────────────┘
```

---

## 7. Proposta do Modelo Preditivo

### Abordagem Escolhida

O modelo principal será um **classificador multiclasse de risco**, treinado para prever o nível de risco operacional de cada equipamento em uma janela de tempo definida (próximas 24h ou 48h).

**Por que classificação e não regressão?**  
A saída mais útil para o gestor não é um número contínuo, mas sim uma **categoria de ação**: "libere", "monitore", "recomende manutenção" ou "suspenda a operação". A classificação multiclasse entrega diretamente esse valor.

### Estrutura do Modelo

| Elemento                 | Definição                                                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------- |
| **Tipo**                 | Classificação multiclasse (4 classes de risco)                                                                                                |
| **Algoritmo candidato**  | Random Forest / XGBoost                                                                                                                       |
| **Variáveis de entrada** | Precipitação prevista, umidade do solo, tipo de solo, distância a corpos d'água, declive, tipo de operação, dias sem manutenção, horas de uso |
| **Variável-alvo**        | `nivel_risco` (baixo, médio, alto, crítico)                                                                                                   |
| **Saídas do modelo**     | Classe de risco + probabilidade por classe + lista de fatores contribuintes                                                                   |

### Outputs para o Gestor

1. **Score de Risco** — índice 0 a 100 calculado a partir das probabilidades do modelo (facilita comunicação visual)
2. **Classificação** — baixo / médio / alto / crítico
3. **Fatores de risco** — quais variáveis mais contribuíram para o resultado (ex: "solo úmido + previsão de 80mm nas próximas 48h")
4. **Recomendações automáticas** — ações sugeridas mapeadas por categoria de risco e tipo de equipamento

### Módulo Complementar — Detecção de Eventos Cotidianos (US-02)

Além do modelo preditivo principal, haverá um módulo baseado em **regras e thresholds** para identificar eventos climáticos cotidianos e disparar recomendações de manutenção. Exemplo:

```
SE precipitacao_mm > 30 E tipo_equipamento = "colheitadeira"
ENTÃO recomendar: inspeção do sistema de tração e verificação de filtros
```

Este módulo complementa o modelo de ML com lógica determinística, garantindo rastreabilidade e explicabilidade das recomendações.

---

## 8. Stack Tecnológica

| Camada                     | Tecnologia                       | Justificativa                                          |
| -------------------------- | -------------------------------- | ------------------------------------------------------ |
| Coleta de dados climáticos | Open-Meteo API / OpenWeather     | Gratuitas, documentadas, cobertura nacional            |
| Pipeline de dados          | Python + Pandas                  | Ecossistema robusto para dados tabulares               |
| Banco de dados             | PostgreSQL                       | Relacional, confiável para dados operacionais          |
| Modelo de ML               | Scikit-learn / XGBoost           | Suporte nativo a classificação, boa interpretabilidade |
| Backend / API              | FastAPI (Python)                 | Leve, rápido, integração nativa com modelos Python     |
| Frontend / Dashboard       | React + Chart.js                 | Flexível, ampla documentação                           |
| Notificações               | SendGrid (e-mail) / Twilio (SMS) | APIs simples com planos gratuitos para prototipagem    |
| Versionamento de modelos   | MLflow (futuro)                  | Rastreabilidade de experimentos                        |
| Autenticação               | JWT + HTTPS                      | Padrão de mercado para APIs REST                       |

---

## 9. Segurança

A solução será projetada respeitando os seguintes princípios:

- **Autenticação e autorização:** Acesso ao dashboard e à API protegido por autenticação JWT. Cada usuário (gestor, operador, seguradora) terá permissões distintas e perfis de acesso diferenciados.
- **Controle de acesso por papel (RBAC):** O operador vê apenas seus equipamentos. O gestor vê a frota completa. A seguradora acessa apenas dados autorizados pelo segurado.
- **Integridade dos dados:** Todos os registros de eventos e recomendações serão imutáveis após gravação (append-only), garantindo rastreabilidade para fins de análise de sinistros.
- **Criptografia:** Comunicação via HTTPS. Dados sensíveis (localização, histórico de sinistros) armazenados com criptografia em repouso.
- **LGPD:** A coleta e uso de dados de localização e operação dos equipamentos seguirá os princípios da Lei Geral de Proteção de Dados, com consentimento explícito do segurado e política de retenção definida.

---

## 10. Planejamento das Próximas Sprints

### Sprint 2 — Dados e Modelo Base

- [ ] Geração do dataset simulado completo (mínimo 1.000 registros)
- [ ] Análise exploratória dos dados (correlações, distribuições, outliers)
- [ ] Treinamento do modelo classificador com dados simulados
- [ ] Avaliação de métricas (accuracy, F1, matriz de confusão)
- [ ] Documentação das decisões de feature engineering

### Sprint 3 — Backend e Integração

- [ ] Desenvolvimento da API REST com FastAPI
- [ ] Integração com API de clima (Open-Meteo ou OpenWeather)
- [ ] Módulo de regras para recomendações pós-evento (US-02)
- [ ] Sistema de notificações (e-mail/push)
- [ ] Testes de integração entre componentes

### Sprint 4 — Frontend e Protótipo Funcional

- [ ] Desenvolvimento do dashboard para o gestor
- [ ] Mapa interativo com status de risco da frota
- [ ] Painel de recomendações e histórico (US-01 e US-02)
- [ ] Painel financeiro de economia/risco acumulado (US-03)
- [ ] Testes com usuários simulados e ajustes de UX



<!-- > O Trello do projeto estará disponível futuramente -->

---

## 11. Equipe

| Nome     | RM       |
| -------- | -------- |
| Beatriz Moreira Barreto Pinto | RM-573311 |
| Gustavo de Oliveira Caldas | RM-573015|
| João Felipe das Neves Alves | RM-569270 |
| Paulo Cesar Barreto da Silva | RM-571441 |
| Tamires Vitória Ferreira dos Santos | RM-571256 |

---

## 12. Apresentação em Vídeo

📹 **Link para o vídeo de apresentação:** [inserir link após gravação]

---

_Projeto desenvolvido para o Challenge FIAP x Sompo Seguros — 2026._
