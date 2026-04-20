# Ir Além 1 - Python + API pública

## Objetivo
Este módulo representa o item opcional **Ir Além 1** da Fase 2.

A proposta é consultar dados meteorológicos com Python e transformar essa informação em uma variável simples que possa influenciar a lógica de irrigação no ESP32.

Neste projeto, o Python:
- consulta ou simula dados de clima;
- avalia a probabilidade de chuva nas próximas horas;
- define se há chuva prevista ou não;
- gera um valor que pode ser enviado ao ESP32 via monitor serial ou copiado manualmente para o código.

---

## Arquivo principal
- `consulta_clima.py`

---

## O que o script faz
O script processa dados meteorológicos e devolve três informações principais:

- `maior_probabilidade_6h`
- `chuva_prevista`
- `comando_serial`

### Significado de cada campo
- **maior_probabilidade_6h**: maior probabilidade de chuva encontrada no período analisado;
- **chuva_prevista**: resultado lógico final (`true` ou `false`);
- **comando_serial**:
  - `1` = chuva prevista
  - `0` = sem chuva prevista

Esse valor pode ser usado na lógica do ESP32 para impedir ou permitir irrigação.

---

## Como executar
Dentro da pasta do módulo, execute:

```bash
python consulta_clima.py
```

Se preferir executar pela raiz do projeto, ajuste o caminho conforme a estrutura do seu repositório.

---

## Saída esperada com o exemplo atual
Com os dados de exemplo atuais, a saída esperada é:

```text
maior_probabilidade_6h=13
chuva_prevista=false
comando_serial=0
```

---

## Como interpretar essa saída
Essa saída significa que:

- a maior probabilidade de chuva encontrada foi **13%**;
- como esse valor é baixo, o sistema conclui que **não há chuva prevista**;
- por isso, o comando gerado é **0**.

### Interpretação prática
- `chuva_prevista=false` → o clima **não bloqueia** a irrigação;
- `comando_serial=0` → o ESP32 pode continuar usando a lógica local dos sensores para decidir se liga ou não a bomba.

---

## Relação com o projeto da Fase 2
Este módulo não substitui o sistema principal do ESP32.

Ele funciona como uma camada extra de inteligência:
- se houver chuva prevista, o sistema pode suspender a irrigação;
- se não houver chuva prevista, a decisão continua baseada em umidade, pH e NPK.

---

## Exemplo de uso com ESP32
Uma forma simples de integração é:

- `1` → vai chover → não irrigar
- `0` → não vai chover → seguir regra normal dos sensores

Exemplo conceitual:

```cpp
if (comandoSerial == 1) {
  // chuva prevista
  // manter bomba desligada
} else {
  // sem chuva prevista
  // seguir lógica normal dos sensores
}
```

---

## Resultado esperado em outro cenário
Se vocês alterarem os dados de entrada para simular chuva forte, o comportamento esperado é algo como:

```text
maior_probabilidade_6h=75
chuva_prevista=true
comando_serial=1
```

Nesse caso:
- existe chuva prevista;
- o sistema pode suspender a irrigação para economizar água.

---

## Conclusão
O Ir Além em Python acrescenta contexto climático à irrigação inteligente.

Com isso, o projeto não depende apenas dos sensores locais, mas também considera previsão de chuva para tomar uma decisão mais eficiente.
