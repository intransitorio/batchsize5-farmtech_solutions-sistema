# batchsize5-farmtech_solutions-sistema

## Descrição do Projeto

Este projeto foi desenvolvido para a startup **FarmTech Solutions** como uma solução inicial para um cliente do setor agrícola que busca migrar para a Agricultura Digital. O objetivo é criar um sistema para auxiliar no gerenciamento e planejamento de culturas, otimizando a produtividade através da tecnologia.

A solução é composta por duas aplicações principais: uma desenvolvida em Python para o gerenciamento de dados da lavoura e outra em R para análise estatística desses dados.

## Funcionalidades

### Aplicação em Python

A aplicação principal, desenvolvida em Python (`sistema.py`), oferece um sistema de gerenciamento de dados para duas culturas agrícolas. Ela opera através de um menu interativo no terminal e armazena os dados em vetores.

As principais funcionalidades incluem:

- **Gerenciamento de Culturas**: Suporte para duas culturas distintas, a serem definidas pela equipe com base na relevância para o estado.
- **Cálculo de Área de Plantio**: Permite calcular a área de plantio para cada cultura, com base em figuras geométricas pré-definidas.
- **Cálculo de Manejo de Insumos**: Calcula a quantidade necessária de insumos (como fertilizantes ou pesticidas) com base nas dimensões da lavoura e nas especificações de aplicação.
- **Operações CRUD em Vetores**:
  - **Entrada de Dados**: Inserção de informações para os cálculos.
  - **Saída de Dados**: Exibição dos dados e resultados no terminal.
  - **Atualização de Dados**: Modificação de um registro em uma posição específica do vetor.
  - **Deleção de Dados**: Remoção de um registro do vetor.
- **Menu Interativo**: Uma interface de linha de comando para navegar entre as funcionalidades, incluindo uma opção para sair do programa.
- **Estruturas de Controle**: O código utiliza laços de repetição (`loop`) e estruturas de decisão para garantir a funcionalidade do menu e dos cálculos.

### Análise de Dados com R

Utilizando os dados gerados pela aplicação Python, uma segunda aplicação em R foi desenvolvida para realizar análises estatísticas básicas, como o cálculo de **média** e **desvio padrão**.

### Desafio Extra: API Meteorológica com R

Como um recurso adicional, o projeto inclui um script em R que se conecta a uma API meteorológica pública para:

1.  Coletar dados climáticos atuais.
2.  Processar essas informações.
3.  Exibir um resumo meteorológico em formato de texto no terminal.

## Versionamento

O projeto utiliza o **GitHub** para controle de versão, simulando um ambiente de desenvolvimento colaborativo e permitindo o trabalho em equipe.

## Disciplina de Formação Social

O projeto também contempla um resumo do artigo Agricultura, sustentabilidade e ciência, conforme solicitado na disciplina de Formação Social.
