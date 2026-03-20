# ============================================================
# Projeto FarmTech Solutions - Agricultura Digital
# Parte 2: Análise estatística em R
# Objetivo: calcular média e desvio padrão a partir dos dados
# coletados no projeto principal.
# ============================================================

# ------------------------------------------------------------
# Estrutura esperada do arquivo CSV:
# id,talhao,cultura,comprimento_m,largura_m,area_m2,area_ha,produto,dose_por_ha,quantidade_insumo
# 1,Talhao A,Soja,200,150,30000,3,Fertilizante NPK,350,1050
# ------------------------------------------------------------

# ------------------------------
# Funções utilitárias
# ------------------------------
linha <- function(tamanho = 70) {
  cat(paste(rep("-", tamanho), collapse = ""), "\n")
}

cabecalho <- function(titulo) {
  linha()
  cat(titulo, "\n")
  linha()
}

pausar <- function() {
  readline(prompt = "\nPressione Enter para continuar...")
}

arquivo_existe <- function(caminho) {
  file.exists(caminho)
}

# ------------------------------
# Dados de exemplo
# ------------------------------
carregar_dados_exemplo <- function() {
  data.frame(
    id = c(1, 2, 3, 4),
    talhao = c("Talhão A", "Talhão B", "Talhão C", "Talhão D"),
    cultura = c("Soja", "Cana-de-açúcar", "Soja", "Cana-de-açúcar"),
    comprimento_m = c(200, 300, 150, 250),
    largura_m = c(100, 120, 80, 140),
    area_m2 = c(20000, 36000, 12000, 35000),
    area_ha = c(2.0, 3.6, 1.2, 3.5),
    produto = c("Fertilizante NPK", "Herbicida", "Fungicida", "Maturador"),
    dose_por_ha = c(350, 4.0, 0.6, 2.0),
    quantidade_insumo = c(700, 14.4, 0.72, 7.0),
    stringsAsFactors = FALSE
  )
}

# ------------------------------
# Leitura e validação do CSV
# ------------------------------
validar_colunas <- function(dados) {
  colunas_obrigatorias <- c(
    "id", "talhao", "cultura", "comprimento_m", "largura_m",
    "area_m2", "area_ha", "produto", "dose_por_ha", "quantidade_insumo"
  )

  colunas_faltantes <- setdiff(colunas_obrigatorias, names(dados))

  if (length(colunas_faltantes) > 0) {
    cat("Erro: o arquivo não possui as seguintes colunas obrigatórias:\n")
    print(colunas_faltantes)
    return(FALSE)
  }

  return(TRUE)
}

ler_dados_csv <- function(caminho_arquivo = "dados_agricolas.csv") {
  if (!arquivo_existe(caminho_arquivo)) {
    cat("Arquivo CSV não encontrado.\n")
    cat("Será utilizada a base de exemplo para testes.\n")
    return(carregar_dados_exemplo())
  }

  dados <- tryCatch(
    {
      read.csv(caminho_arquivo, stringsAsFactors = FALSE)
    },
    error = function(e) {
      cat("Erro ao ler o arquivo CSV:\n")
      cat(e$message, "\n")
      return(NULL)
    }
  )

  if (is.null(dados)) {
    cat("Será utilizada a base de exemplo para evitar interrupção do programa.\n")
    return(carregar_dados_exemplo())
  }

  if (!validar_colunas(dados)) {
    cat("Será utilizada a base de exemplo para testes.\n")
    return(carregar_dados_exemplo())
  }

  return(dados)
}

# ------------------------------
# Funções estatísticas
# ------------------------------
calcular_media <- function(vetor) {
  mean(vetor)
}

calcular_desvio_padrao <- function(vetor) {
  sd(vetor)
}

mostrar_estatisticas_gerais <- function(dados) {
  cabecalho("ESTATÍSTICAS GERAIS")

  media_area <- calcular_media(dados$area_ha)
  desvio_area <- calcular_desvio_padrao(dados$area_ha)
  media_insumo <- calcular_media(dados$quantidade_insumo)
  desvio_insumo <- calcular_desvio_padrao(dados$quantidade_insumo)

  cat(sprintf("Média da área (ha): %.4f\n", media_area))
  cat(sprintf("Desvio padrão da área (ha): %.4f\n", desvio_area))
  cat(sprintf("Média da quantidade de insumo: %.4f\n", media_insumo))
  cat(sprintf("Desvio padrão da quantidade de insumo: %.4f\n", desvio_insumo))
}

mostrar_media_area <- function(dados) {
  cabecalho("MÉDIA DA ÁREA EM HECTARES")
  media_area <- calcular_media(dados$area_ha)
  cat(sprintf("A média das áreas cadastradas é: %.4f ha\n", media_area))
}

mostrar_desvio_area <- function(dados) {
  cabecalho("DESVIO PADRÃO DA ÁREA EM HECTARES")
  desvio_area <- calcular_desvio_padrao(dados$area_ha)
  cat(sprintf("O desvio padrão das áreas cadastradas é: %.4f ha\n", desvio_area))
}

mostrar_media_insumo <- function(dados) {
  cabecalho("MÉDIA DA QUANTIDADE DE INSUMO")
  media_insumo <- calcular_media(dados$quantidade_insumo)
  cat(sprintf("A média da quantidade de insumo é: %.4f\n", media_insumo))
}

mostrar_desvio_insumo <- function(dados) {
  cabecalho("DESVIO PADRÃO DA QUANTIDADE DE INSUMO")
  desvio_insumo <- calcular_desvio_padrao(dados$quantidade_insumo)
  cat(sprintf("O desvio padrão da quantidade de insumo é: %.4f\n", desvio_insumo))
}

mostrar_resumo_por_cultura <- function(dados) {
  cabecalho("RESUMO ESTATÍSTICO POR CULTURA")

  culturas_unicas <- unique(dados$cultura)

  for (cultura_atual in culturas_unicas) {
    subconjunto <- dados[dados$cultura == cultura_atual, ]

    cat(sprintf("Cultura: %s\n", cultura_atual))
    cat(sprintf("Quantidade de registros: %d\n", nrow(subconjunto)))
    cat(sprintf("Média de área (ha): %.4f\n", mean(subconjunto$area_ha)))

    if (nrow(subconjunto) > 1) {
      cat(sprintf("Desvio padrão da área (ha): %.4f\n", sd(subconjunto$area_ha)))
      cat(sprintf("Média da quantidade de insumo: %.4f\n", mean(subconjunto$quantidade_insumo)))
      cat(sprintf("Desvio padrão da quantidade de insumo: %.4f\n", sd(subconjunto$quantidade_insumo)))
    } else {
      cat("Desvio padrão: não pode ser calculado com apenas 1 registro.\n")
      cat(sprintf("Média da quantidade de insumo: %.4f\n", mean(subconjunto$quantidade_insumo)))
    }

    linha()
  }
}

mostrar_dados <- function(dados) {
  cabecalho("DADOS CARREGADOS")
  print(dados)
}

salvar_base_exemplo_csv <- function(caminho = "dados_agricolas_exemplo.csv") {
  dados_exemplo <- carregar_dados_exemplo()
  write.csv(dados_exemplo, caminho, row.names = FALSE)
  cat(sprintf("Arquivo de exemplo salvo com sucesso em: %s\n", caminho))
}

# ------------------------------
# Menu interativo
# ------------------------------
mostrar_menu <- function() {
  cabecalho("FARMTECH SOLUTIONS - ANÁLISE ESTATÍSTICA EM R")
  cat("1 - Carregar dados do CSV\n")
  cat("2 - Exibir dados carregados\n")
  cat("3 - Calcular média da área em hectares\n")
  cat("4 - Calcular desvio padrão da área em hectares\n")
  cat("5 - Calcular média da quantidade de insumo\n")
  cat("6 - Calcular desvio padrão da quantidade de insumo\n")
  cat("7 - Exibir resumo estatístico por cultura\n")
  cat("8 - Exibir estatísticas gerais\n")
  cat("9 - Gerar arquivo CSV de exemplo\n")
  cat("0 - Encerrar sistema\n")
  linha()
}

# ------------------------------
# Programa principal
# ------------------------------
main <- function() {
  dados <- carregar_dados_exemplo()

  repeat {
    mostrar_menu()
    opcao <- suppressWarnings(as.integer(readline(prompt = "Escolha uma opção: ")))

    if (is.na(opcao)) {
      cat("Opção inválida. Digite um número do menu.\n")
      pausar()
      next
    }

    if (opcao == 1) {
      cabecalho("CARREGAMENTO DE DADOS")
      caminho <- readline(prompt = "Informe o nome do arquivo CSV (ou pressione Enter para usar dados_agricolas.csv): ")

      if (trimws(caminho) == "") {
        caminho <- "dados_agricolas.csv"
      }

      dados <- ler_dados_csv(caminho)
      cat("Dados carregados com sucesso.\n")
      pausar()

    } else if (opcao == 2) {
      mostrar_dados(dados)
      pausar()

    } else if (opcao == 3) {
      mostrar_media_area(dados)
      pausar()

    } else if (opcao == 4) {
      mostrar_desvio_area(dados)
      pausar()

    } else if (opcao == 5) {
      mostrar_media_insumo(dados)
      pausar()

    } else if (opcao == 6) {
      mostrar_desvio_insumo(dados)
      pausar()

    } else if (opcao == 7) {
      mostrar_resumo_por_cultura(dados)
      pausar()

    } else if (opcao == 8) {
      mostrar_estatisticas_gerais(dados)
      pausar()

    } else if (opcao == 9) {
      cabecalho("GERAÇÃO DE BASE DE EXEMPLO")
      salvar_base_exemplo_csv()
      pausar()

    } else if (opcao == 0) {
      cabecalho("ENCERRANDO O SISTEMA")
      cat("Análise estatística finalizada com sucesso.\n")
      break

    } else {
      cat("Opção inválida. Tente novamente.\n")
      pausar()
    }
  }
}

# Ponto de entrada
main()
