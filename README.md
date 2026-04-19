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
- <a href="https://www.linkedin.com/in/sabrina-gomes-campos-13280642">Sabrina Gomes Campos</a>
- <a href="https://www.linkedin.com/in/thiago-oliveira-8b6a30291">Thiago Barbosa Silva de Oliveira</a>
- - <a href="https://www.linkedin.com/in/paulocbarreto">Paulo Cesar Barreto da Silva</a>

## 👩‍🏫 Professores:

### Tutor(a)

- <a href="https://www.linkedin.com/in/nicollycrsouza">Nicolly Candida Rodrigues de Souza</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato">André Godoi Chiovato</a>

## 📜 Descrição

### 📘 Projeto FarmTech Solutions: Agricultura Digital

Este projeto da FarmTech Solutions aplica Agricultura Digital para otimizar fazendas. A aplicação em Python usa vetores e menus para gerir culturas de Soja e Cana-de-açúcar.

#### ⚙️ Funcionalidades

- **CRUD:** Cadastro, edição e deleção de dados agrícolas em vetores.
- **Cálculos:** Gestão de área de plantio e manejo de insumos.
- **Análise em R:** Estatísticas (média/desvio) e integração com API de clima.

O sistema utiliza Git para versionamento, unindo lógica de programação, análise de dados e fundamentos da Embrapa para apoio à decisão no campo.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>.github</b>: Nesta pasta ficarão os arquivos de configuração específicos do GitHub que ajudam a gerenciar e automatizar processos no repositório.

- <b>assets</b>: aqui estão os arquivos relacionados a elementos não-estruturados deste repositório, como imagens.

- <b>config</b>: Posicione aqui arquivos de configuração que são usados para definir parâmetros e ajustes do projeto.

- <b>document</b>: aqui estão todos os documentos do projeto que as atividades poderão pedir. Na subpasta "other", adicione documentos complementares e menos importantes.

- <b>scripts</b>: Posicione aqui scripts auxiliares para tarefas específicas do seu projeto. Exemplo: deploy, migrações de banco de dados, backups.

- <b>src</b>: Todo o código fonte criado para o desenvolvimento do projeto ao longo das 7 fases.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto (o mesmo que você está lendo agora).

## 🔧 Como executar o código

### Pré-requisitos

- **Python 3.x**: Para o sistema principal de manejo (`manejo-de-insumos.py`).
- **R**: Para os scripts de análise (`calculo-media-e-desvio.r` e `analise-meteorologica.r`).

> **Nota**: A biblioteca `jsonlite` para R é necessária para a análise meteorológica. O script tentará instalá-la automaticamente caso não a encontre.

### Passo a Passo

1.  Após clonar o repositório, navegue com o terminal até a pasta `src`, onde os scripts estão localizados.

---

#### 1. Sistema de Manejo de Insumos (Python)

Este é o sistema principal para cadastrar, gerenciar e calcular dados de insumos e áreas.

**Como executar:**

```bash
python manejo-de-insumos.py
```

> **Importante:** Para que a análise estatística em R funcione com os dados mais recentes, utilize a **opção 8** do menu para exportar os dados para o arquivo `dados_agricolas.csv`.

---

#### 2. Análise Estatística (R)

Este script lê os dados do arquivo `dados_agricolas.csv` e calcula a média e o desvio padrão.

**Como executar:**

```bash
Rscript calculo-media-e-desvio.r
```

> Se o arquivo `dados_agricolas.csv` não for encontrado, o script utilizará um conjunto de dados de exemplo para demonstração.

---

#### 3. Análise Meteorológica (R)

Este script consulta uma API de clima para fornecer previsões e interpretações agrícolas para as culturas de Soja e Cana-de-açúcar.

**Como executar:**

```bash
Rscript analise-meteorologica.r
```

## 🗃 Histórico de lançamentos

- ## 0.1.0 - 21/03/2026

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

## Histórico de mudanças
Consulte o arquivo `CHANGELOG.md` para acompanhar as alterações relevantes do repositório.