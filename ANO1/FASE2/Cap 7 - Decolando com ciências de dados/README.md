# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="../../../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" width="40%">
  </a>
</p>

---

# 🌿 Dashboard — Agronegócio e Desmatamento no Mato Grosso

> Análise interativa da relação entre produção agrícola e desmatamento em 35 municípios do Mato Grosso (2023), desenvolvida com R Shiny.


## Grupo Batch Size 5

## 👨‍🎓 Integrantes:
- <a href="https://www.linkedin.com/in/beatriz-barreto-pinto-btrz">Beatriz Moreira Barreto Pinto</a>
- <a href="https://www.linkedin.com/in/gustoliver-caldas-7a9a33350">Gustavo de Oliveira Caldas</a>
- <a href="https://www.linkedin.com/in/jfnalves">João Felipe das Neves Alves</a>
- <a href="https://www.linkedin.com/in/paulocbarreto">Paulo Oliveira</a>
- <a href="https://www.linkedin.com/in/tamiresvferreiras/">Tamires Ferreira</a>

> Disciplina: Fase 2 — Cap. 7

## 👩‍🏫 Professores:
### Tutor(a)
- <a href="https://www.linkedin.com/in/nicollycrsouza">Nicolly Candida Rodrigues de Souza</a>

### Coordenador(a)
- <a href="https://www.linkedin.com/in/andregodoichiovato">André Godoi Chiovato</a>

---

## 📜 Descrição

Dashboard interativo desenvolvido em **R (Shiny)** que cruza dados de área plantada, produção agrícola e desmatamento em municípios do Mato Grosso. O projeto integra visualizações estatísticas, mapa georreferenciado e tabela exploratória para investigar a dinâmica territorial entre a expansão do agronegócio e a pressão sobre a Amazônia Legal.

---

## 🎯 Objetivo

Investigar, por meio de análise estatística e visualização de dados, a relação entre a produção agrícola consolidada e os índices de desmatamento nos municípios do Mato Grosso — testando a hipótese de que a estabilização da fronteira agrícola pode contribuir para a contenção do desmate.

---

## 📁 Estrutura do Projeto

```
.
├── Analise_Agro_MT_ProducaoVSDesmatamento_Excel.R   # Script principal (Shiny app)
└── Planilha_Agro_Desmatamento_no_Mato_Grosso.xlsx   # Base de dados (Excel)
    ├── Dados_MT_2023                                 # Dados dos 35 municípios
    └── Estatísticas_R                                # Resumo estatístico exportado
```

> ⚠️ O arquivo `.xlsx` **deve estar na mesma pasta** que o script `.R`. O caminho é detectado automaticamente — nenhuma alteração é necessária.

---

## 📊 Base de Dados

**35 municípios do Mato Grosso — ano-base 2023.**

| Tipo | Variável |
|---|---|
| Quantitativa Discreta | Ano de referência |
| Quantitativa Contínua | Área plantada (hectares), Área desmatada (km²), Produção (ton), Alertas de desmatamento |
| Qualitativa Nominal | Cultura principal (Soja, Milho, Algodão) |
| Qualitativa Ordinal | Nível de desmatamento (Baixo < Médio < Alto < Muito Alto) |
| Georreferenciamento | Latitude e Longitude por município |

**Fontes:**
- **IBGE** — Produção Agrícola Municipal (PAM 2023), publicado em outubro de 2024
- **INPE** — Sistema PRODES e DETER, dados de desmatamento 2023
- **MAPA/SPA** — Os 100 Municípios (PAM 2023)
- **Embrapa** — Dados Econômicos da Soja, 2023

---

## 📈 Análise Estatística

Aplicada à variável **Área Plantada (hectares)**:

**Tendência Central**
- Média e Mediana

**Dispersão**
- Desvio padrão e Variância
- Amplitude total
- Coeficiente de Variação (CV)

**Posição**
- Quartis (Q1, Q2, Q3) e IQR

**Correlação**
- Pearson entre Área Plantada e Área Desmatada (resultado: correlação negativa)

---

## 📊 Visualizações do Dashboard

O dashboard possui **5 abas principais**:

| Aba | Conteúdo |
|---|---|
| 🗺️ Mapa | Mapa interativo (Leaflet) com círculos georreferenciados por área plantada e nível de desmatamento |
| 📈 Gráficos | Seletor com 5 visualizações estáticas (ggplot2) |
| 📋 Tabela | Tabela exploratória completa (DT) com filtro e paginação |
| 📊 Estatísticas | Cards com KPIs e tabela completa de medidas estatísticas |
| 📄 Sobre | Metodologia, fontes, interpretação dos resultados e integrantes |

**Gráficos disponíveis:**
- Histograma da distribuição de Área Plantada
- Boxplot por nível de desmatamento
- Dispersão: Área Plantada × Área Desmatada
- Distribuição por cultura agrícola principal
- Distribuição dos níveis de desmatamento

---

## 🔍 Principal Achado

A correlação **negativa** (r < 0) entre área plantada e desmatamento evidencia dois perfis distintos coexistindo no Mato Grosso:

- **Municípios do sul** (agricultura consolidada): maiores áreas plantadas + **menores índices de desmatamento** — fronteira agrícola estabilizada.
- **Municípios do norte** (fronteira amazônica): pequena produção agrícola + **alto desmatamento** — abertura de novas áreas ainda é a dinâmica dominante.

---

## 📦 Pacotes R Utilizados

```r
shiny · shinydashboard · ggplot2 · dplyr · scales · DT · leaflet · ggrepel · readxl
```

---

## ▶️ Como Executar

**Pré-requisito:** R ≥ 4.1 instalado.

1. Coloque o arquivo `.xlsx` e o script `.R` **na mesma pasta**.
2. Abra o script no RStudio (ou terminal R).
3. Execute:

```r
shiny::runApp("Analise_Agro_MT_ProducaoVSDesmatamento_Excel.R")
```

> **Fallback automático:** se o arquivo Excel não for encontrado, o script carrega os dados internos embutidos (idênticos à planilha) e emite um aviso — o dashboard funciona normalmente.

Os pacotes ausentes são instalados automaticamente na primeira execução.

---

## 🛠️ Dependências Detalhadas

| Pacote | Finalidade |
|---|---|
| `shiny` + `shinydashboard` | Framework do dashboard |
| `ggplot2` | Gráficos estáticos |
| `dplyr` | Manipulação de dados |
| `scales` | Formatação de eixos |
| `DT` | Tabela interativa |
| `leaflet` | Mapa interativo |
| `ggrepel` | Rótulos sem sobreposição |
| `readxl` | Leitura do arquivo Excel |

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/SabrinaOtoni/TEMPLATE-FIAP-GRAD-ON-IA">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>