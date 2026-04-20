# ============================================================
# Projeto FarmTech Solutions - Agricultura Digital
# Parte 3: Integração com API Meteorológica em R
# API pública utilizada: Open-Meteo
# Versão 2: interpretação agrícola por cultura
# ============================================================

# ------------------------------------------------------------
# Requisitos:
# install.packages("jsonlite")  # caso ainda não esteja instalado
# ------------------------------------------------------------

# ------------------------------
# Verificação de pacote
# ------------------------------
if (!require(jsonlite)) {
  install.packages("jsonlite", repos = "https://cloud.r-project.org")
  library(jsonlite)
}

# ------------------------------
# Funções utilitárias
# ------------------------------
linha <- function(tamanho = 70) {
  cat(paste(rep("-", tamanho), collapse = ""), "\n")
}

linha_em_branco <- function() {
  cat("\n")
}

cabecalho <- function(titulo) {
  linha()
  cat(titulo, "\n")
  linha()
}

pausar <- function() {
  readline(prompt = "\nPressione Enter para continuar...")
}

# ------------------------------
# Escolha da cultura
# ------------------------------
escolher_cultura <- function() {
  cabecalho("SELEÇÃO DA CULTURA AGRÍCOLA")
  cat("1 - Soja\n")
  cat("2 - Cana-de-açúcar\n")
  linha()

  repeat {
    opcao <- suppressWarnings(as.integer(readline(prompt = "Escolha a cultura: ")))

    if (is.na(opcao)) {
      cat("Opção inválida. Digite 1 ou 2.\n")
    } else if (opcao == 1) {
      return("Soja")
    } else if (opcao == 2) {
      return("Cana-de-açúcar")
    } else {
      cat("Opção inválida. Digite 1 ou 2.\n")
    }
  }
}

# ------------------------------
# Geocodificação da cidade
# ------------------------------
buscar_coordenadas <- function(cidade) {
  cidade_formatada <- URLencode(enc2utf8(cidade), reserved = TRUE)
  url <- paste0(
    "https://geocoding-api.open-meteo.com/v1/search?name=",
    cidade_formatada,
    "&count=1&language=pt&format=json"
  )

  resposta <- tryCatch(
    {
      fromJSON(url)
    },
    error = function(e) {
      cat("Erro ao consultar a API de geocodificação.\n")
      cat(e$message, "\n")
      return(NULL)
    }
  )

  if (is.null(resposta) || is.null(resposta$results) || length(resposta$results$name) == 0) {
    cat("Nenhuma cidade encontrada para a busca informada.\n")
    return(NULL)
  }

  list(
    nome = resposta$results$name[1],
    pais = resposta$results$country[1],
    latitude = resposta$results$latitude[1],
    longitude = resposta$results$longitude[1],
    timezone = resposta$results$timezone[1]
  )
}

# ------------------------------
# Consulta meteorológica
# ------------------------------
consultar_clima <- function(latitude, longitude, timezone = "auto") {
  variaveis_atuais <- paste(
    c(
      "temperature_2m",
      "relative_humidity_2m",
      "precipitation",
      "wind_speed_10m",
      "weather_code"
    ),
    collapse = ","
  )

  variaveis_diarias <- paste(
    c(
      "weather_code",
      "temperature_2m_max",
      "temperature_2m_min",
      "precipitation_sum",
      "wind_speed_10m_max"
    ),
    collapse = ","
  )

  url <- paste0(
    "https://api.open-meteo.com/v1/forecast?latitude=", latitude,
    "&longitude=", longitude,
    "&current=", variaveis_atuais,
    "&daily=", variaveis_diarias,
    "&forecast_days=3",
    "&timezone=", URLencode(timezone, reserved = TRUE)
  )

  resposta <- tryCatch(
    {
      fromJSON(url)
    },
    error = function(e) {
      cat("Erro ao consultar a API meteorológica.\n")
      cat(e$message, "\n")
      return(NULL)
    }
  )

  return(resposta)
}

# ------------------------------
# Interpretação do weather code
# ------------------------------
traduzir_weather_code <- function(codigo) {
  codigo <- as.integer(codigo)

  if (codigo == 0) return("Céu limpo")
  if (codigo %in% c(1, 2, 3)) return("Parcialmente nublado")
  if (codigo %in% c(45, 48)) return("Neblina")
  if (codigo %in% c(51, 53, 55)) return("Garoa")
  if (codigo %in% c(56, 57)) return("Garoa congelante")
  if (codigo %in% c(61, 63, 65)) return("Chuva")
  if (codigo %in% c(66, 67)) return("Chuva congelante")
  if (codigo %in% c(71, 73, 75, 77)) return("Neve")
  if (codigo %in% c(80, 81, 82)) return("Pancadas de chuva")
  if (codigo %in% c(85, 86)) return("Pancadas de neve")
  if (codigo %in% c(95)) return("Trovoada")
  if (codigo %in% c(96, 99)) return("Trovoada com granizo")

  return("Condição meteorológica não identificada")
}

# ------------------------------
# Exibição dos dados
# ------------------------------
mostrar_clima_atual <- function(local_info, clima) {
  cabecalho("CLIMA ATUAL")

  atual <- clima$current

  cat(sprintf("Local: %s - %s\n", local_info$nome, local_info$pais))
  cat(sprintf("Latitude: %.4f\n", local_info$latitude))
  cat(sprintf("Longitude: %.4f\n", local_info$longitude))
  cat(sprintf("Fuso horário: %s\n", local_info$timezone))
  linha()
  cat(sprintf("Data e hora da leitura: %s\n", atual$time))
  cat(sprintf("Condição do tempo: %s\n", traduzir_weather_code(atual$weather_code)))
  cat(sprintf("Temperatura: %.1f °C\n", atual$temperature_2m))
  cat(sprintf("Umidade relativa: %.0f %%\n", atual$relative_humidity_2m))
  cat(sprintf("Precipitação atual: %.1f mm\n", atual$precipitation))
  cat(sprintf("Velocidade do vento: %.1f km/h\n", atual$wind_speed_10m))
}

mostrar_previsao_diaria <- function(local_info, clima) {
  cabecalho("PREVISÃO PARA OS PRÓXIMOS 3 DIAS")

  diario <- clima$daily

  cat(sprintf("Local: %s - %s\n", local_info$nome, local_info$pais))
  linha()

  for (i in seq_along(diario$time)) {
    cat(sprintf("Data: %s\n", diario$time[i]))
    cat(sprintf("Condição: %s\n", traduzir_weather_code(diario$weather_code[i])))
    cat(sprintf("Temperatura mínima: %.1f °C\n", diario$temperature_2m_min[i]))
    cat(sprintf("Temperatura máxima: %.1f °C\n", diario$temperature_2m_max[i]))
    cat(sprintf("Precipitação acumulada: %.1f mm\n", diario$precipitation_sum[i]))
    cat(sprintf("Vento máximo: %.1f km/h\n", diario$wind_speed_10m_max[i]))
    linha()
  }
}

mostrar_alerta_agricola_geral <- function(clima) {
  cabecalho("INTERPRETAÇÃO AGRÍCOLA GERAL")

  atual <- clima$current
  diario <- clima$daily

  if (atual$temperature_2m >= 32) {
    cat("Alerta: Temperatura elevada no momento. Pode haver estresse térmico na lavoura.\n")
  } else {
    cat("Temperatura atual sem indicativo crítico imediato.\n")
  }

  if (sum(diario$precipitation_sum) < 5) {
    cat("Atenção: Baixa previsão de chuva nos próximos dias. Avaliar necessidade de irrigação.\n")
  } else {
    cat("Há previsão de chuva suficiente para acompanhamento da umidade do solo.\n")
  }

  if (max(diario$wind_speed_10m_max) > 30) {
    cat("Atenção: Vento forte previsto. Aplicações agrícolas podem exigir replanejamento.\n")
  } else {
    cat("Não há indicação de vento forte relevante para operações agrícolas.\n")
  }
}

# ------------------------------
# Interpretação específica por cultura
# ------------------------------
mostrar_interpretacao_por_cultura <- function(cultura, clima) {
  cabecalho("INTERPRETAÇÃO ESPECÍFICA POR CULTURA")

  atual <- clima$current
  diario <- clima$daily

  temperatura_atual <- atual$temperature_2m
  chuva_total <- sum(diario$precipitation_sum)
  vento_maximo <- max(diario$wind_speed_10m_max)
  temperatura_maxima_periodo <- max(diario$temperature_2m_max)

  cat(sprintf("Cultura selecionada: %s\n", cultura))
  linha()

  if (cultura == "Soja") {
    if (chuva_total < 8) {
      cat("Precipitação: Previsão de chuva baixa para os próximos dias. Monitorar umidade do solo e possível necessidade de irrigação.\n")
    } else {
      cat("Precipitação: Previsão de chuva razoável para manutenção da umidade do solo.\n")
    }

    if (temperatura_maxima_periodo > 34) {
      cat("Temperatura: Temperaturas máximas elevadas podem aumentar estresse hídrico e afetar o desenvolvimento da cultura.\n")
    } else {
      cat("Temperatura: Faixa térmica sem sinal forte de estresse extremo no curto prazo.\n")
    }

    if (vento_maximo > 25) {
      cat("Vento: Vento forte pode prejudicar pulverizações. Avaliar janela operacional antes da aplicação de defensivos.\n")
    } else {
      cat("Vento: Condição de vento mais favorável para manejo operacional.\n")
    }

  } else if (cultura == "Cana-de-açúcar") {
    if (chuva_total < 5) {
      cat("Precipitação: Baixa chuva prevista. Em áreas recém-implantadas, convém atenção à disponibilidade hídrica.\n")
    } else {
      cat("Precipitação: Volume de chuva previsto pode favorecer a manutenção do vigor vegetativo.\n")
    }

    if (temperatura_atual >= 33 || temperatura_maxima_periodo > 35) {
      cat("Temperatura: Calor elevado pode aumentar a perda de água e exigir monitoramento do campo.\n")
    } else {
      cat("Temperatura: Temperatura dentro de faixa sem alerta térmico imediato.\n")
    }

    if (vento_maximo > 30) {
      cat("Vento: Vento forte pode interferir em aplicações e operações mecanizadas.\n")
    } else {
      cat("Vento: Vento sem impacto operacional expressivo previsto.\n")
    }
  }
}

# ------------------------------
# Fluxo principal de consulta
# ------------------------------
executar_consulta_completa <- function() {
  cabecalho("CONSULTA METEOROLÓGICA")

  cultura <- escolher_cultura()
  cidade <- readline(prompt = "Digite o nome da cidade desejada: ")
  cidade <- trimws(cidade)

  if (cidade == "") {
    cat("Erro: o nome da cidade não pode ficar vazio.\n")
    return()
  }

  local_info <- buscar_coordenadas(cidade)
  if (is.null(local_info)) {
    return()
  }

  clima <- consultar_clima(local_info$latitude, local_info$longitude, local_info$timezone)
  if (is.null(clima)) {
    return()
  }

  linha_em_branco()
  mostrar_clima_atual(local_info, clima)

  linha_em_branco()
  mostrar_previsao_diaria(local_info, clima)

  linha_em_branco()
  mostrar_alerta_agricola_geral(clima)

  linha_em_branco()
  mostrar_interpretacao_por_cultura(cultura, clima)

  linha()
  calcular_estatisticas(clima)
   
}

# ------------------------------
# Menu interativo
# ------------------------------
mostrar_menu <- function() {
  cabecalho("FARMTECH SOLUTIONS - API METEOROLÓGICA EM R")
  cat("1 - Consultar clima por cidade e cultura\n")
  cat("0 - Encerrar sistema\n")
  linha()
}

# ------------------------------
# Programa principal
# ------------------------------
main <- function() {
  repeat {
    mostrar_menu()
    opcao <- suppressWarnings(as.integer(readline(prompt = "Escolha uma opção: ")))

    if (is.na(opcao)) {
      cat("Opção inválida. Digite um número do menu.\n")
      pausar()
      next
    }

    if (opcao == 1) {
      executar_consulta_completa()
      pausar()

    } else if (opcao == 0) {
      cabecalho("ENCERRANDO O SISTEMA")
      cat("Consulta meteorológica finalizada com sucesso.\n")
      break

    } else {
      cat("Opção inválida. Tente novamente.\n")
      pausar()
    }
  }
}
# ------------------------------
# Estatísticas básicas
# ------------------------------
calcular_estatisticas <- function(clima) {
  diario <- clima$daily
  temperaturas <- diario$temperature_2m_max

  media <- mean(temperaturas)
  desvio <- sd(temperaturas)

  linha()
  cat("ESTATÍSTICAS CLIMÁTICAS\n")
  linha()
  cat(sprintf("Média da temperatura máxima: %.2f °C\n", media))
  cat(sprintf("Desvio padrão da temperatura máxima: %.2f\n", desvio))
}
# Ponto de entrada
main()
