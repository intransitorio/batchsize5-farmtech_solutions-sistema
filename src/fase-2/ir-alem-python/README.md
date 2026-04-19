# Ir Além 1 - Python + API pública

## Objetivo
Consultar uma API pública de clima para apoiar a lógica de irrigação do projeto da Fase 2.

## Arquivo principal
- `consulta_clima.py`

## O que o script faz
- consulta a API Open-Meteo;
- lê a probabilidade de chuva das próximas horas;
- decide se existe chuva prevista;
- gera um comando simples para ser usado no Serial Monitor do ESP32.

## Exemplo de integração com o ESP32
- Se `comando_serial=1`, o grupo envia `1` no monitor serial e o ESP32 entende que há chuva prevista.
- Se `comando_serial=0`, o grupo envia `0` e o ESP32 segue a lógica normal.
