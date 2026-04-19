"""Consulta clima na Open-Meteo para apoiar a lógica de irrigação.

Exemplo de uso:
    python consulta_clima.py

Saída esperada:
    chuva_prevista=true|false
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlopen

LATITUDE = -23.5505 # podemos mudar
LONGITUDE = -46.6333 # podemos mudar
URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LATITUDE}&longitude={LONGITUDE}"
    "&hourly=precipitation_probability"
    "&forecast_days=1"
)

BASE_DIR = Path(__file__).resolve().parent


def consultar_api() -> dict:
    with urlopen(URL, timeout=20) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def processar_resposta(dados: dict) -> dict:
    probabilidades = dados.get("hourly", {}).get("precipitation_probability", [])
    maior_probabilidade = max(probabilidades[:6]) if probabilidades else 0
    chuva_prevista = maior_probabilidade >= 60

    return {
        "maior_probabilidade_6h": maior_probabilidade,
        "chuva_prevista": chuva_prevista,
        "comando_serial": "1" if chuva_prevista else "0",
    }


def salvar_exemplos(dados_api: dict, saida: dict) -> None:
    (BASE_DIR / "exemplo_resposta_api.json").write_text(
        json.dumps(dados_api, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    conteudo = (
        f"maior_probabilidade_6h={saida['maior_probabilidade_6h']}\n"
        f"chuva_prevista={str(saida['chuva_prevista']).lower()}\n"
        f"comando_serial={saida['comando_serial']}\n"
    )
    (BASE_DIR / "saida_processada.txt").write_text(conteudo, encoding="utf-8")


def main() -> None:
    dados_api = consultar_api()
    saida = processar_resposta(dados_api)
    salvar_exemplos(dados_api, saida)

    print(f"maior_probabilidade_6h={saida['maior_probabilidade_6h']}")
    print(f"chuva_prevista={str(saida['chuva_prevista']).lower()}")
    print(f"comando_serial={saida['comando_serial']}")


if __name__ == "__main__":
    main()
