# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br> # SADCC — Sistema de Apoio à Decisão para Colheita de Cana-de-Açúcar



## Grupo Batch Size 5

## 👨‍🎓 Integrantes:

- <a href="https://www.linkedin.com/in/beatriz-barreto-pinto-btrz">Beatriz Moreira Barreto Pinto</a>
- <a href="https://www.linkedin.com/in/gustoliver-caldas-7a9a33350">Gustavo de Oliveira Caldas</a>
- <a href="https://www.linkedin.com/in/jfnalves">João Felipe das Neves Alves</a>
- <a href="https://www.linkedin.com/in/paulocbarreto">Paulo Cesar Barreto da Silva</a>
- <a href="https://www.linkedin.com/in/tamiresvferreiras/">Tamires Ferreira</a>

## 👩‍🏫 Professores:

### Tutor(a)

- <a href="https://www.linkedin.com/in/nicollycrsouza">Nicolly Candida Rodrigues de Souza</a>

### Coordenador(a)

- <a href="https://www.linkedin.com/in/andregodoichiovato">André Godoi Chiovato</a>



<br>



## 📜 Descrição

O **SADCC — Sistema de Apoio à Decisão para Colheita de Cana-de-Açúcar** foi desenvolvido com foco no contexto do agronegócio brasileiro, especialmente no processo de colheita da cana, em que perdas operacionais podem comprometer significativamente a produtividade e a rentabilidade do produtor. O projeto propõe uma solução em Python capaz de registrar dados operacionais de campo, analisar indicadores de desempenho e gerar diagnósticos automáticos para apoiar a tomada de decisão.

A aplicação foi estruturada de forma modular e simula um cenário real de uso em propriedades agrícolas ou operações de gestão agrícola. O sistema permite o cadastro de **talhões**, armazenando informações como nome, área plantada, variedade da cana e data de plantio. A partir desses talhões, o usuário pode registrar **colheitas**, informando dados relevantes como data da operação, fazenda, tipo de colheita, produção colhida, produtividade estimada, velocidade da colhedora, altura de corte, estado das facas, operador, máquina, umidade do solo, chuva recente e observações adicionais.

Com base nesses dados, o sistema calcula automaticamente a **produção estimada**, a **perda real em toneladas** e a **perda percentual**, classificando a eficiência da colheita e comparando o desempenho com referências do setor. Além disso, o projeto implementa um conjunto de regras de negócio que permite identificar padrões de ineficiência e gerar **diagnósticos automatizados**, como excesso de velocidade, desgaste das facas, altura de corte inadequada e operação em solo úmido após chuva. Essas análises são apresentadas ao usuário com recomendações objetivas para correção do processo.

Outro diferencial do projeto é a integração com **banco de dados Oracle**, permitindo persistência dos registros e uma estrutura mais próxima da realidade corporativa. Também foram implementadas funcionalidades de **importação e exportação de dados**, com geração de arquivos em **JSON**, **CSV** e **TXT**, ampliando a rastreabilidade das informações e facilitando a criação de relatórios gerenciais.

Do ponto de vista técnico, o projeto aplica conceitos fundamentais estudados ao longo das fases, como modularização, funções, validação de dados, estruturas de repetição, listas, dicionários, arquivos e tratamento de erros. Dessa forma, o SADCC não apenas atende ao problema proposto no PBL, mas também consolida a aplicação prática de conteúdos essenciais de programação e desenvolvimento de soluções orientadas a dados no agronegócio.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets</b>: pasta destinada aos arquivos visuais do repositório, como logotipos, imagens e elementos gráficos utilizados na documentação do projeto.

- <b>document</b>: contém a documentação do projeto, como relatórios, entregáveis, apresentações, diagramas e demais materiais acadêmicos relacionados ao desenvolvimento do sistema.

- <b>src</b>: contém o código-fonte principal da aplicação. Nessa pasta, destacam-se:
  - <b>main.py</b>: arquivo principal responsável por inicializar o sistema e exibir o menu principal.
  - <b>banco.py</b>: módulo responsável pela conexão com o banco de dados Oracle e criação das tabelas do projeto.
  - <b>talhoes.py</b>: módulo de cadastro, listagem, busca e exclusão de talhões.
  - <b>colheita.py</b>: módulo central do sistema, responsável pelo registro das colheitas, cálculos de perda, análise dos dados e geração do diagnóstico automatizado.
  - <b>arquivos.py</b>: módulo de importação e exportação de dados em formatos JSON, CSV e TXT.
  - <b>validacao.py</b>: módulo de validação de entradas, garantindo maior robustez e segurança no uso da aplicação.
  - <b>dados</b>: subpasta utilizada para armazenar arquivos gerados pelo sistema, como relatórios e exportações.

- <b>README.md</b>: arquivo que serve como guia e explicação geral sobre o projeto.

## 🔧 Como executar o código

### Pré-requisitos

Para executar o projeto corretamente, é necessário ter instalado em sua máquina:

- <b>Python 3.10 ou superior</b>
- <b>VS Code</b>, PyCharm ou outra IDE/editor de sua preferência
- A biblioteca <b>oracledb</b> para conexão com o Oracle
- Acesso ao ambiente Oracle da FIAP com usuário e senha válidos

### Instalação das dependências

No terminal, execute:

```bash
pip install oracledb
```

Caso deseje manipular relatórios e dados com mais facilidade em futuras evoluções do projeto, também pode instalar:

```bash
pip install pandas
```

### Passo a passo para execução

1. Clone o repositório ou baixe os arquivos do projeto:

```bash
git clone [URL_DO_REPOSITORIO]
```

2. Acesse a pasta do projeto:

```bash
cd [NOME_DO_PROJETO]
```

3. Entre na pasta onde está o código-fonte:

```bash
cd src
```

4. Execute o arquivo principal:

```bash
python main.py
```

5. Ao iniciar o sistema, informe suas credenciais do Oracle FIAP quando solicitado:

- <b>Host</b>: `oracle.fiap.com.br`
- <b>Porta</b>: `1521`
- <b>SID/Service</b>: `ORCL`
- <b>Usuário</b>: seu RM
- <b>Senha</b>: sua senha cadastrada no ambiente Oracle

### Funcionalidades disponíveis no sistema

Ao executar a aplicação, o menu principal permitirá:

- Gerenciar talhões
- Registrar colheitas
- Consultar colheitas cadastradas
- Visualizar estatísticas globais
- Acompanhar painel de decisão com prioridades
- Importar e exportar dados do sistema

## 🗃 Histórico de lançamentos

* 0.5.0 - 19/04/2026
    * Estruturação final do sistema com integração entre cadastro de talhões, colheitas, análise e exportação de dados.
* 0.4.0 - 18/04/2026
    * Implementação das regras de negócio para diagnóstico automático e painel de decisão.
* 0.3.0 - 18/04/2026
    * Integração com banco de dados Oracle e persistência dos registros.
* 0.2.0 - 17/04/2026
    * Modularização do sistema em arquivos separados para banco, colheitas, talhões, arquivos e validação.
* 0.1.0 - 17/04/2026
    * Criação da estrutura inicial do projeto e definição do problema de negócio.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution