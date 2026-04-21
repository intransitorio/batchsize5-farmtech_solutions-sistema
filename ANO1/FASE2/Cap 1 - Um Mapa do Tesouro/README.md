# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="../../../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Sistema de Apoio à Agricultura Digital

## Grupo Batch Size 5

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

## 📜 Descrição

# FarmTech Solutions - Sistema de Irrigação e Fertirrigação Inteligente (Fase 2)

## 🌿 Sobre o Projeto

Este projeto integra o desenvolvimento da Fase 2 da disciplina de IA e IoT da FIAP. A **FarmTech Solutions** apresenta um protótipo avançado para a gestão hídrica e nutricional da **Cana-de-Açúcar**.

O sistema utiliza um ESP32 para monitorar sensores e decidir, via algoritmo, o acionamento de uma bomba d'água (Relé), focando na eficiência produtiva e na sustentabilidade ambiental (evitando o desperdício de adubo e a saturação do solo).

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🛠️ Hardware Simulado (Wokwi)

Para este protótipo, foram adotadas as seguintes substituições didáticas no simulador:

- **ESP32 DevKit V1**: Microcontrolador central.
- **DHT22 (Simulador de Solo)**: Utilizado para monitorar a umidade do solo.
- **LDR (Simulador de pH)**: Converte a intensidade de luz em uma escala de pH de 0 a 14.
- **3 Pushbuttons (Sensores de Nutrientes NPK)**: Atuam como sensores de deficiência nutricional.
- **Relé Azul (Atuador)**: Representa a bomba de irrigação/fertirrigação.

---

## 🧠 Lógica de Negócio e Funcionalidades

### 1. Monitoramento Nutricional

Diferente de botões comuns, implementamos uma lógica de **Interruptor via Software**:

- **Estado Padrão**: O solo é considerado saudável (Sem deficiência).
- **Ação**: Um clique no botão ativa o estado de "Deficiência" (N, P ou K). Um novo clique limpa o estado.
- **Objetivo**: Facilita a demonstração e simula sensores de nível que alertam quando o nutriente cai abaixo do ideal.

### 2. Trava de Encharcamento e Lixiviação

O sistema possui uma trava de segurança baseada na umidade:

- **Umidade > 75%**: A bomba é bloqueada, mesmo que falte nutriente. Isso evita o apodrecimento das raízes e a **lixiviação** (lavagem do adubo para o lençol freático).

### 3. Janela de pH e Fertirrigação

- **Gatilho de Irrigação**: Umidade < 60%.
- **Gatilho de Fertirrigação**: Ativado se houver deficiência de N, P ou K.
- **Condição Obrigatória**: O pH deve estar entre **5.5 e 6.5**. Se o solo estiver muito ácido ou muito alcalino, a bomba é desligada para evitar desperdício de insumos que a cana não conseguiria absorver.

---

## 📂 Estrutura de Dados (CSV)

O sistema exporta via Monitor Serial os dados em tempo real para análise em Python/R:
`Umidade, pH, Deficiencia_N, Deficiencia_P, Deficiencia_K, Status_Bomba`

---

## 🚀 Como Executar no Wokwi

1.  Importe o arquivo `src/fase-2/um-mapa-do-tesouro/diagram.json`.
2.  Importe o código do arquivo `src/fase-2/um-mapa-do-tesouro/sketch.ino`.
3.  **Para Testar a Inteligência**:
    - Com a umidade em 80%, tente ativar uma deficiência clicando em **N**. Observe que a bomba **não ligará** (Trava de encharcamento).
    - Baixe a umidade para 65% e clique em **N**. A bomba **ligará** (Fertirrigação).
    - Mude o pH no slider do LDR para 4.0. A bomba **desligará** (Trava química).

---

## 📺 Documentação Adicional

- **Link do Vídeo**: [Seu Link Aqui]
- **Link do Projeto**: [Projeto no Wokwi](https://wokwi.com/projects/461645404748264449)
- **Diagrama do circuito**:

  <img src="../../../assets/fase-2/um-mapa-do-tesouro/diagrama.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=100% height=100%>

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

Com isso, a decisão de irrigação deixa de ser apenas r

## 🗃 Histórico de lançamentos

- ## 0.1.0 - 19/04/2026

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
