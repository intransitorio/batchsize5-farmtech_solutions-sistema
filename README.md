# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Sistema de Apoio à Agricultura Digital

## Grupo Batch Size 5

## 👨‍🎓 Integrantes:

- <a href="https://www.linkedin.com/in/beatriz-barreto-pinto-btrz">Beatriz Moreira Barreto Pinto</a>
- <a href="https://www.linkedin.com/in/gustoliver-caldas-7a9a33350">Gustavo de Oliveira Caldas</a>
- <a href="https://www.linkedin.com/in/jfnalves">João Felipe das Neves Alves</a>
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

1.  Importe o arquivo `diagram.json`.
2.  Importe o código do arquivo `sketch.ino`.
3.  **Para Testar a Inteligência**:
    - Com a umidade em 80%, tente ativar uma deficiência clicando em **N**. Observe que a bomba **não ligará** (Trava de encharcamento).
    - Baixe a umidade para 65% e clique em **N**. A bomba **ligará** (Fertirrigação).
    - Mude o pH no slider do LDR para 4.0. A bomba **desligará** (Trava química).

---

## 📺 Documentação Adicional


## 🗃 Histórico de lançamentos

- ## 0.1.0 - 19/04/2026

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>
