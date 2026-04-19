# Ir Além - AgroVision

## Descrição
Esta pasta contém a implementação da atividade **Ir Além**, desenvolvida em Python, com foco em demonstrar na prática os conteúdos estudados nos capítulos 3 ao 6 da disciplina.

A solução proposta foi a criação de um sistema simples de linha de comando para **controle de colheita e perdas no agronegócio**, utilizando as culturas **Soja** e **Cana-de-açúcar**, mantendo coerência com o restante do repositório.

O sistema permite cadastrar registros de colheita, calcular área, produtividade e perda percentual, gerar arquivos em TXT e JSON e realizar operações CRUD em banco de dados Oracle.

---

## Objetivo da atividade
Demonstrar o uso prático dos seguintes conteúdos em Python:

- Subalgoritmos com funções e procedimentos
- Passagem de parâmetros
- Estruturas de dados
- Manipulação de arquivos texto
- Manipulação de arquivos JSON
- Tratamento de erros com `try/except/else/finally`
- Conexão com banco de dados Oracle
- Operações CRUD

---

## Contexto no agronegócio
No agronegócio, acompanhar a diferença entre a **produção prevista** e a **produção real** é importante para identificar perdas e apoiar a tomada de decisão.

Esta aplicação simula esse controle por meio do cadastro de talhões e colheitas, calculando automaticamente indicadores úteis para a gestão agrícola.

---

## Culturas utilizadas
Para manter consistência com o restante do projeto, foram utilizadas as culturas:

- Soja
- Cana-de-açúcar

---

## Funcionalidades
O sistema possui as seguintes funcionalidades:

1. Cadastrar colheita em memória
2. Listar colheitas em memória
3. Gerar relatório em arquivo TXT
4. Exportar dados em arquivo JSON
5. Criar tabela no Oracle
6. Salvar registro no Oracle
7. Listar registros do Oracle
8. Alterar registro no Oracle
9. Excluir registro no Oracle
10. Excluir todos os registros do Oracle

---

## Regras de negócio
Os cálculos aplicados no sistema são:

- **Área plantada** = base × altura
- **Produtividade** = produção real / área
- **Perda percentual** = ((produção prevista - produção real) / produção prevista) × 100

### Classificação da perda
- Até 5% → **Baixa**
- Acima de 5% até 10% → **Média**
- Acima de 10% → **Alta**

---

## Estrutura da pasta
```text
ir-alem/
├── dados/
├── arquivos.py
├── banco_oracle.py
├── config.py
├── funcoes.py
├── main.py
├── README.md
├── requirements.txt
└── schema.sql