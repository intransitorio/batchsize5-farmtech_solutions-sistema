dados <- read.csv("src/fase-2/um-mapa-do-tesouro/ir-alem-r/dados_exemplo.csv", stringsAsFactors = FALSE)

media_umidade <- mean(dados$umidade)
desvio_umidade <- sd(dados$umidade)
media_ph <- mean(dados$ph)

recomendacao <- if (media_umidade < 60) {
  "Ligar irrigacao"
} else {
  "Manter bomba desligada"
}

resultado <- paste0(
  "media_umidade=", round(media_umidade, 2), "
",
  "desvio_umidade=", round(desvio_umidade, 2), "
",
  "media_ph=", round(media_ph, 2), "
",
  "recomendacao=", recomendacao, "
"
)

cat(resultado)
writeLines(resultado, "resultado_analise.txt")
