# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href="https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Administração Paulista" border="0" width="40%" height="40%"></a>
</p>

<br>

# Sistema de Apoio à Decisão para Colheita de Cana-de-Açúcar

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

O projeto **Sistema de Apoio à Decisão para Colheita de Cana-de-Açúcar** foi desenvolvido com o objetivo de apoiar o produtor rural e a gestão operacional no processo de colheita, reduzindo perdas e melhorando a tomada de decisão a partir de dados estruturados.

No contexto do agronegócio brasileiro, a cana-de-açúcar possui grande relevância econômica, e a eficiência da colheita impacta diretamente a produtividade, os custos operacionais e a rentabilidade da produção. Dentro desse cenário, a colheita mecanizada, embora mais escalável e produtiva, pode apresentar perdas superiores à colheita manual quando ocorre em condições inadequadas de solo, umidade, maturidade da cultura ou regulagem do maquinário. Assim, o sistema foi projetado para registrar informações operacionais, analisar indicadores e emitir recomendações automáticas para apoiar decisões mais seguras e eficientes.

A aplicação foi construída em **Python**, com arquitetura modular, interface em linha de comando (CLI), persistência local em **JSON** e **TXT**, além de integração opcional com **Oracle Database**. O sistema permite cadastrar talhões, registrar colheitas, calcular perdas em percentual e toneladas, medir produtividade por hectare, consolidar histórico e gerar diagnósticos operacionais com base em regras de negócio.

Entre os principais recursos implementados, destacam-se:

- cadastro e listagem de talhões;
- registro de colheitas manuais e mecanizadas;
- cálculo de perdas reais;
- comparação entre modos de colheita;
- análise de produtividade e eficiência operacional;
- exportação de histórico em arquivo;
- integração com Oracle para operações básicas de banco de dados;
- módulo de apoio à decisão com diagnóstico de perdas e sugestões práticas.

O sistema considera variáveis como **Brix**, **umidade**, **maturidade do plantio** e **histórico de perdas do talhão** para calcular um score de prontidão e indicar se a colheita deve ser realizada no momento, se deve aguardar ou se convém alterar o modo de execução. Com isso, a solução proposta transforma registros operacionais em informação útil para gestão rural.

Trata-se de um projeto acadêmico aplicado, com foco em organização de dados, análise operacional e apoio à decisão no agronegócio, reunindo conceitos de lógica de programação, estruturas de dados, persistência em arquivos, banco de dados e automação de regras de negócio.

## 🎯 Objetivo do projeto

Desenvolver um sistema em Python capaz de:

- registrar dados operacionais da colheita de cana-de-açúcar;
- calcular perdas estimadas e reais;
- identificar padrões de ineficiência;
- comparar colheita manual e mecanizada;
- gerar recomendações automáticas para apoiar a tomada de decisão no campo.

## ✅ Funcionalidades

- Cadastro de talhões
- Listagem de talhões cadastrados
- Registro de colheitas
- Listagem de colheitas
- Cálculo de perda em toneladas
- Cálculo de produtividade por hectare
- Cálculo de eficiência operacional
- Comparação entre colheita manual e mecanizada
- Exportação de dados em JSON
- Exportação de histórico em TXT
- Integração com Oracle Database
- Diagnóstico automatizado por colheita
- Diagnóstico consolidado por talhão

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets</b>: arquivos de imagem e elementos visuais utilizados na documentação do projeto.

- <b>data</b>: arquivos de apoio e dados de teste, como exemplos em JSON e TXT para carga e validação do sistema.

- <b>document</b>: documentação do projeto, incluindo relatório da pesquisa, modelagem da solução e script Oracle.

- <b>src</b>: código-fonte principal da aplicação, organizado em módulos.

- <b>sad_agro_cana.py</b>: arquivo principal de execução simplificada do projeto.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto.

- <b>requirements.txt</b>: dependências necessárias para execução da aplicação.

## 🧩 Arquitetura do sistema

Os módulos do sistema foram organizados da seguinte forma:

- <b>main.py</b>: fluxo principal e menus da aplicação.
- <b>cadastro.py</b>: rotinas de cadastro e manipulação de talhões e colheitas.
- <b>analise.py</b>: cálculos de perdas, produtividade, eficiência e comparativos.
- <b>persistencia.py</b>: salvamento e leitura em JSON/TXT.
- <b>oracle_db.py</b>: integração com Oracle Database.
- <b>decisao.py</b>: regras automatizadas, diagnósticos e sugestões práticas.
- <b>validacao.py</b>: validação e padronização das entradas do usuário.

## 🔧 Como executar o código

### Pré-requisitos

Antes de executar o projeto, certifique-se de possuir instalado em sua máquina:

- Python 3.10 ou superior
- VS Code, PyCharm ou outra IDE/editor de sua preferência
- Terminal ou prompt de comando
- Oracle Database / Oracle SQL Developer (opcional, apenas para a parte de banco de dados)

### Bibliotecas utilizadas

As principais dependências do projeto são:

- `oracledb`
- `json` *(biblioteca padrão do Python)*
- `datetime` *(biblioteca padrão do Python)*
- `os` *(biblioteca padrão do Python)*

Para instalar a dependência externa principal:

```bash
pip install oracledb
```

### Passo a passo para execução

#### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
```

#### 2. Acesse a pasta do projeto

cd sad_agro_cana_final

#### 3. Execute o sistema

##### Opção 1 — arquivo principal simplificado:

python sad_agro_cana.py

##### Opção 2 — execução direta do módulo principal:

python src/main.py
Execução por fases
Fase de cadastro e análise local

### Permite:

cadastrar talhões;
registrar colheitas;
listar dados;
analisar perdas e produtividade;
gerar diagnósticos.
Fase de persistência
salvar dados em JSON;
carregar dados salvos;
exportar histórico em TXT.
Fase de banco de dados
conectar ao Oracle;
criar tabelas;
sincronizar dados de memória com o banco;
consultar registros persistidos.
Configuração do Oracle
Para conexão com o Oracle, o sistema espera o DSN no formato:

```bash 
host:porta/serviço
```

##### Exemplo:

```bash 
oracle.fiap.com.br:1521/ORCL
```

Além disso, será necessário informar:

usuário;
senha;
DSN.

## 🧪 Dados de teste

O projeto já acompanha arquivos de apoio para testes:

data/dados_teste.json
data/historico_exemplo.txt

Eles podem ser utilizados para validar a persistência local e a estrutura de saída do sistema.

## 📊 Indicadores calculados pelo sistema

Entre os principais indicadores implementados estão:

perda percentual;
perda em toneladas;
produtividade por hectare;
eficiência operacional;
média histórica de perdas;
desvio em relação à referência do modo de colheita;
score de prontidão de colheita.

## 🤖 Regras de apoio à decisão

O módulo de decisão considera regras simples e objetivas para apoiar o usuário, como:

Brix ideal entre 18 e 22;
umidade ideal entre 65% e 75%;
maturidade mínima de 12 meses;
perda de referência de 5% para colheita manual;
perda de referência de 15% para colheita mecanizada.

Com base nesses critérios, o sistema pode:

sugerir colher agora;
sugerir aguardar;
recomendar colheita manual ou mecanizada;
emitir sugestões práticas para redução de perdas.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>