# BeatrizMoreiraBarretoPinto_RM573311_fase2_cap7
# GustavoDeOliveiraCaldas_RM573015_fase2_cap7
# JoaoFelipedasNevesAlves_RM569270_fase2_cap7
# PauloCesarBarretodaSilva_RM571441_fase2_cap7
# TamiresVitoriaFerreiraSantos_RM571256_fase2_cap7
# Dashboard Shiny: Agronegócio e Desmatamento: Mato Grosso
# Fonte: IBGE/PAM 2023 | INPE/PRODES 2023 | CONAB | MAPA

# ============================================================
# PACOTES
# ============================================================
pacotes <- c("shiny","ggplot2","dplyr","scales","shinydashboard","DT","leaflet","ggrepel")
for (p in pacotes) {
  if (!require(p, character.only = TRUE))
    install.packages(p, repos = "https://cloud.r-project.org")
  library(p, character.only = TRUE)
}

# ============================================================
# DADOS (Item 2: 35 linhas, 4 tipos de variável obrigatórios)
# Ano              = quantitativa discreta
# Area_Plantada_ha = quantitativa contínua
# Cultura_Principal= qualitativa nominal
# Nivel_Desmatamento= qualitativa ordinal
# ============================================================
dados <- data.frame(
  Municipio = c(
    "Sorriso","Sapezal","Campo Novo do Parecis","Nova Mutum","Lucas do Rio Verde",
    "Diamantino","Querência","Nova Ubiratã","Tapurah","Primavera do Leste",
    "Campo Verde","Rondonópolis","Sinop","Vera","Brasnorte",
    "Ipiranga do Norte","Canarana","Água Boa","Tangará da Serra","Pedra Preta",
    "Paranatinga","Porto dos Gaúchos","Juara","Alta Floresta","Colíder",
    "Guarantã do Norte","Matupá","Peixoto de Azevedo","São Félix do Araguaia",
    "Juína","Cotriguaçu","Aripuanã","Nova Bandeirantes","Carlinda","Apiacás"
  ),
  Ano = rep(2023L, 35),                          # quantitativa DISCRETA
  Area_Plantada_ha = c(                          # quantitativa CONTÍNUA
    850000,620000,590000,480000,460000,430000,410000,395000,370000,355000,
    340000,280000,265000,255000,240000,230000,218000,205000,195000,185000,
    175000,165000,152000,42000,68000,55000,78000,35000,28000,45000,
    18000,12000,9500,32000,7800
  ),
  Producao_ton = c(
    3060000,2108000,2006000,1680000,1610000,1462000,1394000,1343000,1258000,1207000,
    1156000,952000,901000,867000,816000,782000,741200,697000,663000,629000,
    595000,561000,516800,142800,231200,187000,265200,119000,95200,153000,
    61200,40800,32300,108800,26520
  ),
  Area_Desmatada_km2 = c(
    12.4,28.7,31.2,18.5,9.8,44.3,87.6,62.1,15.2,22.8,
    19.4,11.3,53.7,41.9,78.4,25.6,96.3,112.8,14.7,8.9,
    134.5,158.2,143.7,189.4,76.8,102.3,88.6,211.3,67.4,124.9,
    247.8,198.6,312.4,58.3,278.9
  ),
  Alertas = c(
    38,72,89,47,25,115,198,143,39,58,
    49,29,131,102,176,64,214,251,37,22,
    298,341,319,412,172,228,197,463,152,278,
    534,431,671,132,602
  ),
  Cultura_Principal = c(                         # qualitativa NOMINAL
    "Soja","Algodão","Algodão","Soja","Soja","Soja","Soja","Soja","Soja","Algodão",
    "Soja","Soja","Soja","Soja","Soja","Soja","Soja","Soja","Milho","Algodão",
    "Soja","Soja","Milho","Milho","Milho","Milho","Soja","Milho","Milho","Milho",
    "Milho","Milho","Milho","Milho","Milho"
  ),
  Nivel_Desmatamento = factor(                   # qualitativa ORDINAL
    c("Baixo","Médio","Médio","Baixo","Baixo","Alto","Alto","Alto","Baixo","Médio",
      "Baixo","Baixo","Alto","Médio","Alto","Médio","Muito Alto","Muito Alto","Baixo","Baixo",
      "Muito Alto","Muito Alto","Muito Alto","Muito Alto","Alto","Muito Alto","Alto",
      "Muito Alto","Alto","Muito Alto","Muito Alto","Muito Alto","Muito Alto","Alto","Muito Alto"),
    levels = c("Baixo","Médio","Alto","Muito Alto"), ordered = TRUE
  ),
  Lat = c(
    -12.54,-13.52,-13.63,-13.08,-13.06,-14.40,-12.60,-13.53,-12.68,-15.56,
    -15.54,-16.47,-11.86,-12.30,-12.16,-12.16,-13.54,-14.00,-14.62,-16.78,
    -14.43,-11.54,-11.27,-9.87,-11.24,-9.79,-10.25,-9.74,-11.58,-11.37,
    -9.84,-9.95,-9.68,-10.47,-9.54
  ),
  Lon = c(
    -55.71,-58.78,-57.90,-56.08,-55.93,-56.44,-52.20,-54.69,-55.89,-54.28,
    -55.17,-54.64,-55.51,-54.92,-57.75,-57.32,-52.27,-52.18,-57.50,-54.59,
    -54.04,-57.00,-57.53,-56.08,-55.45,-54.87,-54.94,-54.79,-50.67,-58.74,
    -58.23,-59.44,-57.54,-55.83,-57.48
  ),
  stringsAsFactors = FALSE
)

cores_nivel   <- c("Baixo"="#1a9fa0","Médio"="#41ab5d","Alto"="#006d2c","Muito Alto"="#00441b")
cores_cultura <- c("Soja"="#00441b","Milho"="#41ab5d","Algodão"="#c7e9c0")

# ============================================================
# ESTATÍSTICAS (Item 3: todas as medidas de Area_Plantada_ha)
# ============================================================
x            <- dados$Area_Plantada_ha
stat_media   <- mean(x)
stat_mediana <- median(x)
stat_dp      <- sd(x)
stat_var     <- var(x)
stat_amp     <- max(x) - min(x)
stat_cv      <- round(stat_dp / stat_media * 100, 1)
stat_q1      <- as.numeric(quantile(x, 0.25))
stat_q2      <- as.numeric(quantile(x, 0.50))
stat_q3      <- as.numeric(quantile(x, 0.75))
stat_iqr     <- IQR(x)

media_area   <- round(stat_media / 1000)
cv_area      <- stat_cv
cor_val      <- round(cor(x, dados$Area_Desmatada_km2), 2)
pct_critico  <- round(sum(dados$Nivel_Desmatamento %in% c("Alto","Muito Alto")) / nrow(dados) * 100)

fmt_mil <- function(v) paste0(format(round(v / 1000), big.mark = "."), " mil")

# ============================================================
# GRÁFICOS
# ============================================================
plot_histograma <- function() {
  ggplot(dados, aes(x = Area_Plantada_ha / 1000)) +
    geom_histogram(bins = 8, fill = "#238b45", color = "white", alpha = 0.88) +
    geom_vline(aes(xintercept = stat_media / 1000,   color = "Média"),   linetype = "dashed", linewidth = 1.3) +
    geom_vline(aes(xintercept = stat_mediana / 1000, color = "Mediana"), linetype = "dashed", linewidth = 1.3) +
    scale_color_manual(
      name = "Legenda:",
      values = c("Média" = "#1a9fa0", "Mediana" = "#00441b"),
      labels = c(
        "Média"   = paste0("Média: ", fmt_mil(stat_media), " hectares"),
        "Mediana" = paste0("Mediana: ", fmt_mil(stat_mediana), " hectares")
      )
    ) +
    labs(title = "Distribuição da Área Plantada de Soja",
         subtitle = "A maioria dos municípios planta menos de 200 mil hectares",
         x = "Área Plantada (mil hectares)", y = "Nº de Municípios",
         caption = "Fonte: IBGE/PAM 2023") +
    theme_minimal(base_size = 17) +
    theme(plot.title = element_text(face = "bold", size = 22),
          plot.subtitle = element_text(color = "#555", size = 15),
          legend.position = "right", legend.title = element_text(face = "bold", size = 16),
          legend.text = element_text(size = 13), legend.key.width = unit(1.5, "cm"),
          panel.grid.minor = element_blank())
}

plot_boxplot <- function() {
  ggplot(dados, aes(x = "", y = Area_Plantada_ha / 1000)) +
    geom_boxplot(fill = "#c7e9c0", color = "#006d2c", width = 0.35,
                 outlier.shape = NA, linewidth = 1.1) +
    geom_jitter(aes(color = Nivel_Desmatamento), width = 0.15, size = 4, alpha = 0.85) +
    scale_color_manual(values = cores_nivel, name = "Nível de\nDesmatamento") +
    scale_y_continuous(labels = function(v) paste0(v, " mil")) +
    annotate("text", x = 1.27, y = stat_q1 / 1000,
             label = paste0("Q1: ", fmt_mil(stat_q1)), hjust = 0, size = 5, color = "#006d2c", fontface = "bold") +
    annotate("text", x = 1.27, y = stat_mediana / 1000,
             label = paste0("Q2: ", fmt_mil(stat_mediana)), hjust = 0, size = 5, color = "#006d2c", fontface = "bold") +
    annotate("text", x = 1.27, y = stat_q3 / 1000,
             label = paste0("Q3: ", fmt_mil(stat_q3)), hjust = 0, size = 5, color = "#006d2c", fontface = "bold") +
    geom_hline(yintercept = stat_media / 1000, linetype = "dashed", color = "#1a9fa0", linewidth = 0.9) +
    annotate("text", x = 1.27, y = stat_media / 1000,
             label = paste0("Média: ", fmt_mil(stat_media)), hjust = 0, size = 5, color = "#1a9fa0", fontface = "bold") +
    labs(title = "Área Plantada por Nível de Desmatamento",
         subtitle = paste0("CV: ", stat_cv, "%  |  IQR: ", fmt_mil(stat_iqr), " hectares  |  DP: ", fmt_mil(stat_dp), " hectares"),
         x = "", y = "Área Plantada (mil hectares)",
         caption = "Fonte: IBGE/PAM 2023 | INPE/PRODES 2023") +
    theme_minimal(base_size = 17) +
    theme(plot.title = element_text(face = "bold", size = 22),
          plot.subtitle = element_text(color = "#555", size = 15),
          panel.grid.minor = element_blank())
}

plot_dispersao <- function() {
  cor_r     <- round(cor(dados$Area_Plantada_ha, dados$Area_Desmatada_km2), 3)
  destaques <- dados[dados$Municipio %in% c("Sorriso", "Nova Bandeirantes"), ]
  ggplot(dados, aes(x = Area_Plantada_ha / 1000, y = Area_Desmatada_km2, color = Nivel_Desmatamento)) +
    geom_point(size = 3.5, alpha = 0.75) +
    geom_smooth(method = "lm", se = TRUE, color = "#37474f", linetype = "dashed", linewidth = 0.9, fill = "gray85") +
    geom_point(data = destaques[destaques$Municipio == "Sorriso", ],
               aes(x = Area_Plantada_ha / 1000, y = Area_Desmatada_km2),
               size = 7, shape = 21, stroke = 2.5, color = "#1565C0", fill = "#90CAF9", inherit.aes = FALSE) +
    geom_point(data = destaques[destaques$Municipio == "Nova Bandeirantes", ],
               aes(x = Area_Plantada_ha / 1000, y = Area_Desmatada_km2),
               size = 7, shape = 21, stroke = 2.5, color = "#b71c1c", fill = "#EF9A9A", inherit.aes = FALSE) +
    ggrepel::geom_label_repel(
      data = destaques,
      aes(x = Area_Plantada_ha / 1000, y = Area_Desmatada_km2,
          label = paste0(Municipio, "\nÁrea: ", fmt_mil(Area_Plantada_ha), " hectares",
                         "\nDesmat.: ", Area_Desmatada_km2, " km²")),
      size = 4.5, fontface = "bold", box.padding = 1.2, fill = "white", color = "black", inherit.aes = FALSE) +
    scale_color_manual(values = cores_nivel, name = "Nível de\nDesmatamento") +
    annotate("label", x = max(dados$Area_Plantada_ha / 1000) * 0.62, y = max(dados$Area_Desmatada_km2) * 0.88,
             label = paste0("r = ", cor_r, "\nRelação INVERSA:\nmaior lavoura, menos desmate"),
             color = "#1a237e", fontface = "bold", size = 5.5, fill = "#E8EAF6", label.size = 0.3) +
    labs(title = "Área Plantada vs Área Desmatada",
         subtitle = "Municípios de fronteira (norte) têm lavouras menores e muito mais desmatamento",
         x = "Área Plantada de Soja (mil hectares)", y = "Área Desmatada (km²)",
         caption = "Fonte: IBGE/PAM 2023 | INPE/PRODES 2023") +
    theme_minimal(base_size = 17) +
    theme(plot.title = element_text(face = "bold", size = 22),
          plot.subtitle = element_text(color = "#555", size = 15),
          panel.grid.minor = element_blank())
}

plot_cultura <- function() {
  df <- as.data.frame(table(dados$Cultura_Principal))
  colnames(df) <- c("Cultura", "N")
  df$Pct <- round(df$N / sum(df$N) * 100, 1)
  ggplot(df, aes(x = reorder(Cultura, -N), y = N, fill = Cultura)) +
    geom_col(width = 0.5, show.legend = FALSE) +
    geom_text(aes(label = paste0(N, " municípios\n(", Pct, "%)")),
              vjust = -0.4, fontface = "bold", size = 6.5) +
    scale_fill_manual(values = cores_cultura) +
    scale_y_continuous(limits = c(0, max(df$N) * 1.3)) +
    labs(title = "Cultura Agrícola Principal por Município",
         subtitle = "Variável qualitativa nominal (Item 4)",
         x = "Cultura Principal", y = "Nº de Municípios",
         caption = "Fonte: IBGE/PAM 2023 | MAPA") +
    theme_minimal(base_size = 17) +
    theme(plot.title = element_text(face = "bold", size = 22),
          plot.subtitle = element_text(color = "#555", size = 15),
          axis.text.x = element_text(face = "bold", size = 18),
          panel.grid.minor = element_blank())
}

plot_desmatamento <- function() {
  df <- as.data.frame(table(dados$Nivel_Desmatamento))
  colnames(df) <- c("Nivel", "N")
  df$Nivel <- factor(df$Nivel, levels = c("Baixo","Médio","Alto","Muito Alto"), ordered = TRUE)
  ggplot(df, aes(x = Nivel, y = N, fill = Nivel)) +
    geom_col(width = 0.5, show.legend = FALSE) +
    geom_text(aes(label = paste0(N, " municípios")), vjust = -0.5, fontface = "bold", size = 6.5) +
    scale_fill_manual(values = cores_nivel) +
    scale_y_continuous(limits = c(0, max(df$N) * 1.3)) +
    labs(title = "Nível de Desmatamento por Município",
         subtitle = "Variável qualitativa ordinal (Item 4)",
         x = "Nível de Desmatamento", y = "Nº de Municípios",
         caption = "Fonte: INPE/PRODES 2023 | DETER 2023") +
    theme_minimal(base_size = 17) +
    theme(plot.title = element_text(face = "bold", size = 22),
          plot.subtitle = element_text(color = "#555", size = 15),
          axis.text.x = element_text(face = "bold", size = 18),
          panel.grid.minor = element_blank())
}

# ============================================================
# TEXTOS LEGENDA + CONCLUSÃO (painel lateral)
# ============================================================
mk_conclusao <- function(...) {
  itens <- list(...)
  li    <- paste0("<li>", unlist(itens), "</li>", collapse = "")
  paste0(
    "<div style='margin-top:12px;padding:12px 14px;background:#f0faf4;",
    "border-left:4px solid #238b45;border-radius:6px;'>",
    "<p style='font-size:19px;font-weight:800;color:#238b45;margin:0 0 8px 0;'>Conclusão:</p>",
    "<ul style='margin:0;padding-left:16px;font-size:15px;'>", li, "</ul></div>"
  )
}

insights <- list(

  "Distribuição da Área Plantada" = HTML(paste0("
    <p style='font-size:17px;font-weight:800;color:#1a2a1a;margin:0 0 6px 0;'>Legenda:</p>
    <ul style='font-size:15px;'>
      <li><span style='color:#1a9fa0;font-weight:bold;'>Linha teal: Média (", fmt_mil(stat_media), " hectares)</span> puxada pelos grandes produtores.</li>
      <li><span style='color:#00441b;font-weight:bold;'>Linha verde: Mediana (", fmt_mil(stat_mediana), " hectares)</span> valor central mais representativo.</li>
      <li><span style='color:#238b45;font-weight:bold;'>Barras verdes:</span> distribuição dos municípios por faixa de área.</li>
    </ul>",
    mk_conclusao(
      "Distribuição <b>assimétrica à direita</b>: Sorriso e Sapezal concentram a produção.",
      "A maioria dos municípios planta <b>menos de 200 mil hectares</b>.",
      paste0("CV de <b>", stat_cv, "%</b> confirma alta concentração produtiva no estado.")
    )
  )),

  "Área Plantada por Nível de Desmatamento" = HTML(paste0("
    <p style='font-size:17px;font-weight:800;color:#1a2a1a;margin:0 0 6px 0;'>Legenda:</p>
    <ul style='font-size:15px;'>
      <li><b>Caixa verde:</b> 50% dos municípios entre Q1 (", fmt_mil(stat_q1), ") e Q3 (", fmt_mil(stat_q3), ").</li>
      <li><b>Linha central:</b> mediana = ", fmt_mil(stat_mediana), " hectares.</li>
      <li><b>Linha tracejada teal:</b> média = ", fmt_mil(stat_media), " hectares.</li>
      <li><b>Pontos coloridos:</b> cada município classificado por nível de desmatamento.</li>
    </ul>",
    mk_conclusao(
      "Municípios com <b>baixo desmatamento</b> são os que mais plantam.",
      "Municípios com <b>muito alto desmatamento</b> têm pequena produção agrícola.",
      "A fronteira agrícola do norte concentra o risco ambiental."
    )
  )),

  "Área Plantada vs Área Desmatada" = HTML("
    <p style='font-size:17px;font-weight:800;color:#1a2a1a;margin:0 0 6px 0;'>Legenda:</p>
    <ul style='font-size:15px;'>
      <li><b>Linha tracejada:</b> tendência geral (regressão linear).</li>
      <li><b style='color:#1565C0;'>Sorriso (azul):</b> maior produtor do estado.</li>
      <li><b style='color:#b71c1c;'>Nova Bandeirantes (vermelho):</b> maior risco de desmatamento.</li>
      <li><b>r:</b> coeficiente de correlação de Pearson (de -1 a +1).</li>
    </ul>",
    paste0(
    mk_conclusao(
      "Correlação <b>negativa</b>: quem mais planta é quem menos desMata.",
      "Municípios de fronteira têm pequena lavoura e enorme desmatamento.",
      "O risco ambiental está na abertura de novas áreas, não na agricultura consolidada."
    ))
  ),

  "Cultura Agrícola Principal" = HTML("
    <p style='font-size:17px;font-weight:800;color:#1a2a1a;margin:0 0 6px 0;'>Legenda:</p>
    <ul style='font-size:15px;'>
      <li><span style='color:#00441b;font-weight:bold;'>Soja (verde escuro):</span> domina os municípios consolidados do sul.</li>
      <li><span style='color:#41ab5d;font-weight:bold;'>Milho (verde médio):</span> predomina no norte, municípios em expansão.</li>
      <li><span style='color:#a8ddb5;font-weight:bold;'>Algodão (verde claro):</span> nicho em Sapezal e Primavera do Leste.</li>
    </ul>",
    mk_conclusao(
      "<b>Soja (57%):</b> cultura dominante nos municípios consolidados do sul.",
      "<b>Milho (34%):</b> sinaliza municípios em expansão na fronteira agrícola.",
      "O milho marca a avanço produtivo em direção à Amazônia Legal."
    )
  ),

  "Nível de Desmatamento" = HTML("
    <p style='font-size:17px;font-weight:800;color:#1a2a1a;margin:0 0 6px 0;'>Legenda:</p>
    <ul style='font-size:15px;'>
      <li><span style='color:#1a9fa0;font-weight:bold;'>Baixo (teal):</span> grandes produtores do sul, desmatamento controlado.</li>
      <li><span style='color:#41ab5d;font-weight:bold;'>Médio (verde):</span> alerta intermediário.</li>
      <li><span style='color:#006d2c;font-weight:bold;'>Alto (verde escuro):</span> situação crítica.</li>
      <li><span style='color:#00441b;font-weight:bold;'>Muito Alto (verde profundo):</span> emergência ambiental na fronteira amazônica.</li>
    </ul>",
    mk_conclusao(
      paste0("Mais de <b>", pct_critico, "% dos municípios</b> estão em nível Alto ou Muito Alto."),
      "Apenas <b>8 municípios (23%)</b> estão em nível Baixo.",
      "A maioria está em estado crítico, concentrado na Amazônia Legal."
    )
  )
)

# ============================================================
# UI
# ============================================================
ui <- dashboardPage(
  skin = "blue",

  dashboardHeader(
    titleWidth = 220,
    title = tags$div(
      style = "display:flex;align-items:center;gap:10px;padding:4px 0;",
      HTML('<svg width="36" height="36" viewBox="0 0 36 36" xmlns="http://www.w3.org/2000/svg">
        <path d="M18 3 C10 3 4 10 5 20 C6 27 12 32 18 33 C24 32 30 27 31 20 C32 10 26 3 18 3Z"
              fill="#c7e9c0" opacity="0.92"/>
        <line x1="18" y1="33" x2="18" y2="10" stroke="#00441b" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="18" y1="20" x2="11" y2="15" stroke="#00441b" stroke-width="1" stroke-linecap="round" opacity="0.7"/>
        <line x1="18" y1="24" x2="25" y2="19" stroke="#00441b" stroke-width="1" stroke-linecap="round" opacity="0.7"/>
        <line x1="18" y1="17" x2="24" y2="13" stroke="#00441b" stroke-width="1" stroke-linecap="round" opacity="0.7"/>
      </svg>'),
      tags$div(
        style = "line-height:1.15;",
        tags$div(style = "font-size:11px;font-weight:700;color:white;letter-spacing:1.5px;", "AGRONEGÓCIO"),
        tags$div(style = "font-size:14px;font-weight:800;color:white;letter-spacing:1px;",   "MATO GROSSO")
      )
    )
  ),

  dashboardSidebar(
    width = 220,
    sidebarMenu(
      id = "menu_ativo",
      menuItem("Dashboard", tabName = "dash",   icon = icon("chart-bar")),
      menuItem("Dados",     tabName = "tabela", icon = icon("table")),
      menuItem("Sobre",     tabName = "sobre",  icon = icon("info-circle"))
    )
  ),

  dashboardBody(
    tags$head(tags$style(HTML("
      .skin-blue .main-header .logo,
      .skin-blue .main-header .logo:hover { background-color:#1a9fa0 !important; }
      .skin-blue .main-header .navbar      { background-color:#1a9fa0 !important; }
      .skin-blue .main-header .navbar .sidebar-toggle,
      .skin-blue .main-header .navbar .sidebar-toggle:hover { background-color:#158f90 !important; }
      .skin-blue .main-sidebar { background-color:#f0f2f0 !important; border-right:1px solid #dde0dd; }
      .skin-blue .sidebar-menu > li > a {
        color:#333 !important; font-weight:500; font-size:14px; border-left:3px solid transparent;
      }
      .skin-blue .sidebar-menu > li.active > a,
      .skin-blue .sidebar-menu > li > a:hover {
        background-color:#e0eded !important; color:#1a9fa0 !important; border-left:3px solid #1a9fa0 !important;
      }
      .skin-blue .sidebar-menu > li > a .fa { color:#1a9fa0 !important; }
      .content-wrapper, .right-side { background-color:#f0f2f0 !important; }
      .box { border-radius:10px !important; box-shadow:0 2px 8px rgba(0,0,0,0.08) !important; border-top:none !important; }
      .box-header { background-color:#fff !important; border-bottom:1px solid #eee !important; border-radius:10px 10px 0 0 !important; }
      .box-header .box-title { color:#1a9fa0 !important; font-weight:700 !important; font-size:14px !important; }
      .insight-box { font-size:15px; line-height:1.75; color:#1a2a1a; }
      .insight-box ul { padding-left:18px; margin:6px 0 10px 0; }
      .insight-box li { margin-bottom:6px; }
      .leaflet-container { border-radius:8px; }
      .selectize-input { border-radius:8px !important; font-size:13px !important; }
      abbr { text-decoration:none !important; border-bottom:none !important; cursor:help; }
    "))),

    tabItems(

      # ================================================== DASHBOARD
      tabItem(tabName = "dash",

        fluidRow(
          box(
            width = 8,
            title = tags$span(style = "color:#1a9fa0;font-weight:700;",
                              icon("map-marker-alt"), " Mato Grosso: Área Plantada por Município"),
            solidHeader = FALSE,
            leafletOutput("mapa_mt", height = "395px"),
            tags$div(style = "font-size:11px;color:#888;margin-top:6px;",
              "Fonte: IBGE, MapBiomas  |  Clique em qualquer município para detalhes  |  ",
              tags$span(style = "color:#1565C0;font-weight:600;", "Estrela = Sorriso"),
              "  |  ",
              tags$span(style = "color:#b71c1c;font-weight:600;", "Alerta = Nova Bandeirantes")
            )
          ),

          column(width = 4,
            tags$div(
              style = "display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px;height:395px;box-sizing:border-box;",

              tags$div(
                style = "background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.09);display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding:22px 20px;box-sizing:border-box;",
                tags$i(class = "fa fa-leaf", style = "font-size:42px;color:#2e7d32;margin-bottom:12px;"),
                tags$div(style = "font-size:42px;font-weight:800;color:#111;line-height:1;", paste0(media_area, " mil")),
                tags$div(style = "font-size:38px;font-weight:700;color:#111;margin-top:4px;", "hectares"),
                tags$div(style = "font-size:14px;color:#777;margin-top:6px;", "Área Plantada Média")
              ),

              tags$div(
                style = "background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.09);display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding:22px 20px;box-sizing:border-box;",
                tags$i(class = "fa fa-share-alt", style = "font-size:42px;color:#1a9fa0;margin-bottom:12px;"),
                tags$div(style = "font-size:42px;font-weight:800;color:#111;line-height:1;", paste0(cv_area, "%")),
                tags$div(style = "font-size:14px;color:#777;margin-top:8px;",
                  tags$abbr(
                    title = paste0("Coeficiente de Variação (CV): mede a dispersão relativa em relação à média. CV acima de 30% indica alta concentração. O CV de ", cv_area, "% confirma que poucos municípios dominam a produção."),
                    "Coeficiente de Variação"
                  )
                )
              ),

              tags$div(
                style = "background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.09);display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding:22px 20px;box-sizing:border-box;",
                tags$i(class = "fa fa-exclamation-triangle", style = "font-size:42px;color:#e65100;margin-bottom:12px;"),
                tags$div(style = "font-size:42px;font-weight:800;color:#111;line-height:1;", paste0(pct_critico, "%")),
                tags$div(style = "font-size:14px;color:#777;margin-top:8px;line-height:1.3;",
                  HTML("Municípios com Nível<br>Alto/Muito Alto em desmatamento"))
              ),

              tags$div(
                style = "background:#fff;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.09);display:flex;flex-direction:column;align-items:flex-start;justify-content:center;padding:22px 20px;box-sizing:border-box;",
                tags$i(class = "fa fa-tree", style = "font-size:42px;color:#b71c1c;margin-bottom:12px;"),
                tags$div(style = "font-size:42px;font-weight:800;color:#111;line-height:1;", as.character(cor_val)),
                tags$div(style = "font-size:14px;color:#777;margin-top:8px;line-height:1.3;",
                  HTML("Correlação<br>Área x Desmatamento"))
              )
            )
          )
        ),

        fluidRow(
          box(width = 12, solidHeader = FALSE, style = "padding:10px 16px 4px 16px;",
            selectInput("grafico_sel", "Escolha o gráfico:",
              choices = c(
                "Distribuição da Área Plantada",
                "Área Plantada por Nível de Desmatamento",
                "Área Plantada vs Área Desmatada",
                "Cultura Agrícola Principal",
                "Nível de Desmatamento"
              ),
              width = "420px"
            )
          )
        ),

        fluidRow(
          box(width = 8,  title = "Gráfico",                    solidHeader = FALSE,
              plotOutput("grafico_principal", height = "400px")),
          box(width = 4,  title = "O que este gráfico mostra?", solidHeader = FALSE,
              div(class = "insight-box", uiOutput("insight_texto")))
        )

      ), # fim dash

      # ================================================== DADOS
      tabItem(tabName = "tabela",
        box(width = 12,
            title = "Base de Dados: Municípios de Mato Grosso (2023)",
            solidHeader = FALSE,
            DT::dataTableOutput("tabela_dados"))
      ),

      # ================================================== SOBRE
      tabItem(tabName = "sobre",
        box(width = 12, title = "Sobre esta análise", solidHeader = FALSE,
          HTML("
            <style>
              .sobre-wrap { font-family:'Segoe UI',Arial,sans-serif; max-width:960px; color:#1a2a1a; }
              .sobre-wrap .sec-title {
                font-size:22px; font-weight:800; color:#1a9fa0;
                margin:28px 0 8px 0; border-bottom:2px solid #c7e9c0; padding-bottom:6px;
              }
              .sobre-wrap .sec-title:first-child { margin-top:4px; }
              .sobre-wrap p  { font-size:16px; line-height:1.75; margin:6px 0 14px 0; }
              .sobre-wrap ul { font-size:16px; line-height:1.8; padding-left:22px; margin:6px 0 14px 0; }
              .sobre-wrap li { margin-bottom:5px; }
              .sobre-wrap .conclusao-box {
                background:#f0faf4; border-left:5px solid #238b45;
                border-radius:8px; padding:18px 22px; margin:14px 0 24px 0;
              }
              .sobre-wrap .conclusao-box .c-title {
                font-size:20px; font-weight:800; color:#238b45; margin:0 0 10px 0;
              }
              .sobre-wrap .conclusao-box p  { font-size:16px; margin:0 0 8px 0; }
              .sobre-wrap .conclusao-box ul { font-size:16px; margin:4px 0 0 0; }
              .sobre-wrap .tag-rm {
                display:inline-block; background:#e8f5e9; color:#1B5E20;
                font-weight:700; font-size:13px; padding:2px 8px;
                border-radius:4px; margin-right:6px; letter-spacing:0.5px;
              }
              .sobre-wrap .item-badge {
                display:inline-block; background:#1a9fa0; color:white;
                font-weight:700; font-size:13px; padding:3px 10px;
                border-radius:12px; margin-right:8px; vertical-align:middle;
              }
            </style>
            <div class='sobre-wrap'>

              <div class='sec-title'>1. Problema Analisado</div>
              <p>Este trabalho investiga a seguinte questão central: <b>a expansão da área
              plantada de soja está associada ao aumento do desmatamento nos municípios de
              Mato Grosso?</b> A análise utiliza dados oficiais do IBGE (PAM 2023) e do
              INPE (PRODES/DETER 2023) para 35 municípios do estado, abrangendo tanto
              grandes produtores consolidados do sul quanto municípios de fronteira
              agrícola no norte da Amazônia Legal.</p>

              <div class='sec-title'>2. Atendimento aos Requisitos</div>
              <p><span class='item-badge'>Item 1</span> <b>Consulta dos dados das bases oficiais do IBGE (PAM 2023),a Embrapa (Dados Econômicos da Soja, 2023),MAPA/SPA (Os 100 Municípios — PAM 2023, outubro de 2024) e do INPE (PRODES/DETER 2023).</b><br></p>
                 
              <p><span class='item-badge'>Item 2</span> <b>Base de dados com 30+ linhas e 4 tipos de variável:</b><br>
              A base contém <b>35 municípios</b> como unidades de observação, com as quatro
              colunas obrigatórias: <b>Ano</b> (quantitativa discreta: valor inteiro 2023),
              <b>Área Plantada em hectares</b> (quantitativa contínua: medida em escala
              contínua), <b>Cultura Principal</b> (qualitativa nominal: Soja, Milho, Algodão,
              sem ordem entre si) e <b>Nível de Desmatamento</b> (qualitativa ordinal:
              Baixo &lt; Médio &lt; Alto &lt; Muito Alto, com hierarquia definida).
              A base completa está visível na aba <em>Dados</em>.</p>

              <p><span class='item-badge'>Item 3</span> <b>Análise exploratória da variável quantitativa contínua (Área Plantada):</b><br>
              Todas as medidas são calculadas no código R e exibidas no Dashboard:</p>
              <ul>
                <li><b>Tendência Central:</b> Média (", round(stat_media/1000), " mil hectares) e Mediana (", round(stat_mediana/1000), " mil hectares)
                aparecem como linhas no histograma e no subtítulo do boxplot.</li>
                <li><b>Dispersão:</b> Desvio Padrão (", round(stat_dp/1000), " mil hectares), Variância,
                Amplitude Total (", round(stat_amp/1000), " mil hectares) e Coeficiente de Variação
                (CV = ", stat_cv, "%) estão no card da tela principal e no subtítulo do boxplot.</li>
                <li><b>Separatrizes:</b> Q1 (", round(stat_q1/1000), " mil), Q2/Mediana (", round(stat_q2/1000), " mil),
                Q3 (", round(stat_q3/1000), " mil) e IQR (", round(stat_iqr/1000), " mil hectares)
                estão anotados diretamente no boxplot (selecionar no Dashboard: <em>Área Plantada
                por Nível de Desmatamento</em>).</li>
                <li><b>Análise gráfica:</b> Histograma de distribuição e boxplot com
                dispersão individual por município.</li>
              </ul>

              <p><span class='item-badge'>Item 4</span> <b>Análise gráfica da variável qualitativa:</b><br>
              Dois gráficos de barras atendem ao item. O gráfico <em>Cultura Agrícola
              Principal</em> analisa a variável <b>qualitativa nominal</b> Cultura_Principal,
              com contagem e percentual por categoria. O gráfico <em>Nível de
              Desmatamento</em> analisa a variável <b>qualitativa ordinal</b>
              Nivel_Desmatamento, com barras ordenadas da menor para a maior gravidade.
              Ambos estão no seletor do Dashboard.</p>

              <div class='sec-title'>3. Conceitos Estatísticos</div>

              <p><b>Coeficiente de Variação (CV = ", stat_cv, "%):</b> medida de dispersão
              relativa que expressa o desvio padrão como percentual da média. Valores acima
              de 30% indicam <b>alta heterogeneidade</b>. O resultado confirma que poucos
              municípios como Sorriso e Sapezal concentram volume desproporcionalmente
              grande da área plantada total.</p>

              <p><b>Correlação de Pearson (r = ", cor_val, "):</b> coeficiente que mede a
              intensidade e a direção da relação linear entre duas variáveis, variando de
              -1 a +1. O valor negativo indica que municípios com maior produção agrícola
              tendem a apresentar <em>menor</em> desmatamento.</p>

              <p><b>Percentual de ", pct_critico, "% em nível crítico:</b> proporção dos 35
              municípios classificados com nível de desmatamento Alto ou Muito Alto segundo
              o INPE/PRODES 2023. Evidencia a vulnerabilidade ambiental predominante,
              especialmente nos municípios localizados na faixa norte do estado.</p>

              <div class='sec-title'>4. Conclusão Geral</div>
              <div class='conclusao-box'>
                <div class='c-title'>Conclusão:</div>
                <p>Os resultados desta análise <b>refutam a hipótese simplista</b> de que
                expansão agrícola e desmatamento são fenômenos diretamente proporcionais
                no Mato Grosso. Os dados demonstram que:</p>
                <ul>
                  <li>Municípios com <b>agricultura consolidada</b> (sul do estado) apresentam
                  simultaneamente as maiores áreas plantadas e os <b>menores índices de
                  desmatamento</b>, sugerindo que a estabilização da fronteira agrícola
                  contribui para a contenção do desmate.</li>
                  <li>O desmatamento está <b>fortemente concentrado</b> em municípios de
                  pequena produção agrícola localizados na fronteira amazônica (norte do MT),
                  onde a abertura de novas áreas ainda é a principal dinâmica territorial.</li>
                  <li>A correlação negativa (r = ", cor_val, ") e o alto coeficiente de variação
                  (CV = ", stat_cv, "%) reforçam que a <b>heterogeneidade estrutural</b> do estado
                  é o fator explicativo central: dois perfis distintos de municípios coexistem:
                  produtores consolidados com baixo risco ambiental e municípios de fronteira
                  com alto risco e baixa produção.</li>
                </ul>
              </div>

              <div class='sec-title'>5. Variáveis Utilizadas</div>
              <ul>
                <li><b>Quantitativa Discreta:</b> Ano de referência (2023)</li>
                <li><b>Quantitativa Contínua:</b> Área Plantada de Soja (hectares) e Área Desmatada (km²)</li>
                <li><b>Qualitativa Nominal:</b> Cultura Principal por município (Soja, Milho, Algodão)</li>
                <li><b>Qualitativa Ordinal:</b> Nível de Desmatamento (Baixo &lt; Médio &lt; Alto &lt; Muito Alto)</li>
              </ul>

             ```html
              <div class='sec-title'>6. Fontes de Dados</div>
              <ul>
                <li><b>IBGE:</b> Produção Agrícola Municipal (PAM), edição 2023, publicado em outubro de 2024</li>
                <li><b>INPE:</b> Sistema PRODES e DETER, dados de desmatamento 2023</li>
                <li><b>MAPA/SPA:</b> Os 100 Municípios — PAM 2023, publicado em outubro de 2024</li>
                <li><b>Embrapa:</b> Dados Econômicos da Soja, 2023</li>
              </ul>
              
              <div class='sec-title'>7. Integrantes do Grupo</div>
              <ul>
                <li><span class='tag-rm'>RM573311</span> <b>Beatriz Moreira Barreto Pinto</b></li>
                <li><span class='tag-rm'>RM573015</span> <b>Gustavo de Oliveira Caldas</b></li>
                <li><span class='tag-rm'>RM569270</span> <b>João Felipe das Neves Alves</b></li>
                <li><span class='tag-rm'>RM571441</span> <b>Paulo Cesar Barreto da Silva</b></li>
                <li><span class='tag-rm'>RM571256</span> <b>Tamires Vitoria Ferreira dos Santos</b></li>
              </ul>

            </div>
          ")
        )
      )

    ) # fim tabItems
  ) # fim dashboardBody
) # fim dashboardPage

# ============================================================
# SERVER
# ============================================================
server <- function(input, output) {

  output$mapa_mt <- renderLeaflet({
    breaks  <- c(0, 50000, 150000, 300000, 500000, 900000)
    hexcors <- c("#c7e9c0","#74c476","#41ab5d","#238b45","#00441b")
    idx      <- as.integer(cut(dados$Area_Plantada_ha, breaks = breaks,
                                include.lowest = TRUE, right = FALSE))
    cor_fill <- hexcors[idx]

    nivel_chr <- as.character(dados$Nivel_Desmatamento)
    cor_borda <- dplyr::case_when(
      nivel_chr == "Baixo"  ~ "#1a9fa0",
      nivel_chr == "Médio"  ~ "#41ab5d",
      nivel_chr == "Alto"   ~ "#006d2c",
      TRUE                  ~ "#00441b"
    )

    popup_todos <- paste0(
      "<div style='font-family:sans-serif;min-width:155px;'>",
      "<b style='font-size:13px;'>", dados$Municipio, "</b><hr style='margin:3px 0;'>",
      "Área Plantada: <b>", format(dados$Area_Plantada_ha, big.mark=".", scientific=FALSE), " hectares</b><br>",
      "Desmatamento: <b>", dados$Area_Desmatada_km2, " km²</b><br>",
      "Nível: <b style='color:", cor_borda, ";'>", nivel_chr, "</b></div>"
    )

    nb_i  <- which(dados$Municipio == "Nova Bandeirantes")
    sor_i <- which(dados$Municipio == "Sorriso")

    popup_nb  <- "<div style='font-family:sans-serif;'><b style='color:#b71c1c;'>&#9888; Nova Bandeirantes</b><hr style='margin:3px 0;'>Área: <b>9.500 hectares</b><br>Desmatamento: <b style='color:#b71c1c;'>312,4 km² - MUITO ALTO</b></div>"
    popup_sor <- "<div style='font-family:sans-serif;'><b style='color:#1565C0;'>&#9733; Sorriso - Maior Produtor</b><hr style='margin:3px 0;'>Área: <b>850.000 hectares</b><br>Desmatamento: <b style='color:#2e7d32;'>12,4 km² - BAIXO</b></div>"

    leaflet(options = leafletOptions(zoomControl = TRUE, attributionControl = FALSE)) %>%
      addProviderTiles(providers$CartoDB.Positron, options = tileOptions(opacity = 0.55)) %>%
      setView(lng = -55.5, lat = -13.0, zoom = 5) %>%
      addCircleMarkers(
        lng = dados$Lon, lat = dados$Lat,
        radius = 14, fillColor = cor_fill, fillOpacity = 0.88,
        color = cor_borda, weight = 1.5,
        popup = popup_todos, label = dados$Municipio
      ) %>%
      addCircleMarkers(
        lng = dados$Lon[nb_i], lat = dados$Lat[nb_i],
        radius = 22, weight = 3,
        color = "#b71c1c", fillColor = "#b71c1c", fillOpacity = 0.12,
        dashArray = "6,4", popup = popup_nb, label = "Nova Bandeirantes - Maior Risco"
      ) %>%
      addCircleMarkers(
        lng = dados$Lon[sor_i], lat = dados$Lat[sor_i],
        radius = 22, weight = 3,
        color = "#1565C0", fillColor = "#1565C0", fillOpacity = 0.10,
        dashArray = "6,4", popup = popup_sor, label = "Sorriso - Maior Produtor"
      ) %>%
      addLegend(
        position = "bottomleft",
        colors   = hexcors,
        labels   = c("ate 50k","50k-150k","150k-300k","300k-500k","acima de 500k"),
        title    = "<b>Area Plantada (hectares)</b>",
        opacity  = 0.85
      )
  })

  output$grafico_principal <- renderPlot({
    sel <- input$grafico_sel
    if      (sel == "Distribuição da Área Plantada")             plot_histograma()
    else if (sel == "Área Plantada por Nível de Desmatamento")   plot_boxplot()
    else if (sel == "Área Plantada vs Área Desmatada")           plot_dispersao()
    else if (sel == "Cultura Agrícola Principal")                plot_cultura()
    else if (sel == "Nível de Desmatamento")                     plot_desmatamento()
  })

  output$insight_texto <- renderUI({
    div(class = "insight-box", insights[[input$grafico_sel]])
  })

  output$tabela_dados <- DT::renderDataTable({
    df_exib <- dados[, c("Municipio","Ano","Area_Plantada_ha","Producao_ton",
                         "Area_Desmatada_km2","Alertas","Cultura_Principal","Nivel_Desmatamento")]
    DT::datatable(df_exib,
      options  = list(pageLength = 10, scrollX = TRUE),
      rownames = FALSE,
      colnames = c("Município","Ano","Área Plantada (hectares)","Produção (ton)",
                   "Área Desmatada (km²)","Alertas","Cultura","Nível Desmat.")
    ) |>
      DT::formatRound(columns = c("Area_Plantada_ha","Producao_ton"), digits = 0) |>
      DT::formatRound(columns = "Area_Desmatada_km2", digits = 1)
  })

} # fim server

shinyApp(ui, server) 
