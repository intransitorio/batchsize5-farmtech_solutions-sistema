# Ir Além 2 - Análise em R

## Objetivo
Este módulo representa o item opcional **Ir Além 2** da Fase 2.

A proposta é usar R para realizar uma análise estatística simples dos dados simulados da plantação e gerar uma recomendação objetiva sobre ligar ou não a irrigação.

---

## Arquivo principal
- `analise_irrigacao.R`

---

## O que o script faz
O script lê dados de exemplo contendo informações de umidade e pH e calcula:

- média da umidade;
- desvio padrão da umidade;
- média do pH;
- recomendação final de irrigação.

---

## Como executar
Dentro da pasta do módulo, execute:

```bash
Rscript analise_irrigacao.R
```

Se preferir executar pela raiz do projeto, ajuste o caminho conforme a estrutura do seu repositório.

---

## Saída esperada com os dados de exemplo atuais
Com os dados atuais, a saída esperada é:

```text
media_umidade=59
desvio_umidade=2.74
media_ph=6.1
recomendacao=Ligar irrigacao
```

---

## Como interpretar essa saída
### 1. Média da umidade
```text
media_umidade=59
```

Isso indica que a umidade média medida no conjunto de dados ficou em **59**.

Pela regra atual do script, quando a média da umidade fica abaixo do limite definido, a irrigação deve ser ligada.

### 2. Desvio padrão da umidade
```text
desvio_umidade=2.74
```

Esse valor mostra que as leituras de umidade não variaram muito entre si, então os dados estão relativamente consistentes.

### 3. Média do pH
```text
media_ph=6.1
```

O pH médio calculado foi **6.1**, um valor plausível para análise agrícola.

No estado atual do script, o pH é exibido como apoio analítico e ajuda a contextualizar os dados.

### 4. Recomendação final
```text
recomendacao=Ligar irrigacao
```

Como a umidade média ficou abaixo do limiar configurado, a recomendação final foi **ligar a irrigação**.

---

## Regra atual usada no script
De forma simples, a lógica atual é:

- se a média da umidade for **menor que 60**, então:
  - `Ligar irrigacao`
- caso contrário:
  - `Manter bomba desligada`

Exemplo conceitual em R:

```r
if (media_umidade < 60) {
  recomendacao <- "Ligar irrigacao"
} else {
  recomendacao <- "Manter bomba desligada"
}
```

---

## Relação com o projeto da Fase 2
O módulo em R não substitui o ESP32.

Ele funciona como apoio analítico para a tomada de decisão, permitindo que o grupo:
- interprete os dados medidos;
- avalie tendências simples;
- justifique melhor a decisão de irrigação.

---

## Relação com o módulo em Python
Os dois módulos opcionais podem ser usados em conjunto:

- o **Python** verifica se existe chuva prevista;
- o **R** verifica se os dados internos sugerem necessidade de irrigação.

### Exemplo com os resultados atuais
- Python:
  - `chuva_prevista=false`
- R:
  - `recomendacao=Ligar irrigacao`

Nesse cenário:
- não há bloqueio climático;
- os dados locais recomendam irrigação;
- portanto, a decisão final fica coerente.

---

## Resultado esperado em outro cenário
Se vocês alterarem os dados de exemplo para uma umidade média maior, por exemplo acima de 60, a saída esperada passa a ser algo como:

```text
media_umidade=68
desvio_umidade=3.10
media_ph=6.3
recomendacao=Manter bomba desligada
```

Nesse caso, o sistema entende que não há necessidade imediata de irrigação.

---

## Conclusão
O Ir Além em R acrescenta uma camada de análise estatística ao projeto.

Com isso, a decisão de irrigação deixa de ser apenas reativa e passa a ser também apoiada por interpretação de dados.
