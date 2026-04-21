"""
cadastro.py
Responsável pelo cadastro e consulta operacional de talhões e colheitas.

Escopo atual:
- entrada validada
- armazenamento em memória
- listagem e busca simples
- cálculo básico já necessário ao registro da colheita
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from validacao import ler_data, ler_float, ler_inteiro, ler_opcao, ler_texto


# -----------------------------------------------------------------------------
# Utilitários internos
# -----------------------------------------------------------------------------

def _proximo_id(registros: list[dict[str, Any]]) -> int:
    """Gera o próximo ID sequencial para uma lista de registros em memória."""
    if not registros:
        return 1
    return max(int(registro["id"]) for registro in registros) + 1



def buscar_talhao_por_id(talhoes: list[dict[str, Any]], id_talhao: int) -> dict[str, Any] | None:
    """Busca um talhão pelo ID."""
    for talhao in talhoes:
        if talhao["id"] == id_talhao:
            return talhao
    return None



def buscar_colheita_por_id(colheitas: list[dict[str, Any]], id_colheita: int) -> dict[str, Any] | None:
    """Busca uma colheita pelo ID."""
    for colheita in colheitas:
        if colheita["id"] == id_colheita:
            return colheita
    return None



def nome_talhao_ja_existe(talhoes: list[dict[str, Any]], nome: str) -> bool:
    """Verifica duplicidade de nome de talhão, ignorando maiúsculas/minúsculas."""
    nome_normalizado = nome.strip().lower()
    return any(t["nome"].strip().lower() == nome_normalizado for t in talhoes)


# -----------------------------------------------------------------------------
# Talhões
# -----------------------------------------------------------------------------

def cadastrar_talhao_memoria(talhoes: list[dict[str, Any]]) -> dict[str, Any]:
    """Lê, valida e armazena um novo talhão em memória."""
    print("\n--- Cadastro de Talhão ---")

    while True:
        nome = ler_texto("  Nome do talhão: ", tamanho_max=50)
        if nome_talhao_ja_existe(talhoes, nome):
            print("  ⚠ Já existe um talhão com esse nome. Informe outro nome.")
            continue
        break

    area_ha = ler_float("  Área do talhão (ha): ", minimo=0.1, maximo=50000)
    variedade = ler_texto("  Variedade da cana: ", tamanho_max=30)
    data_plantio = ler_data("  Data de plantio (DD/MM/AAAA): ")

    talhao = {
        "id": _proximo_id(talhoes),
        "nome": nome,
        "area_ha": area_ha,
        "variedade": variedade,
        "data_plantio": data_plantio,
    }
    talhoes.append(talhao)

    print(f"\n  ✅ Talhão '{nome}' cadastrado com sucesso. ID: {talhao['id']}")
    return talhao



def listar_talhoes_memoria(talhoes: list[dict[str, Any]]) -> None:
    """Exibe todos os talhões cadastrados em memória."""
    if not talhoes:
        print("\n  Nenhum talhão cadastrado.")
        return

    print("\n" + "─" * 74)
    print(f"  {'ID':<4} {'Nome':<20} {'Área (ha)':<12} {'Variedade':<18} {'Plantio'}")
    print("─" * 74)
    for talhao in talhoes:
        print(
            f"  {talhao['id']:<4} {talhao['nome']:<20} {talhao['area_ha']:<12.2f} "
            f"{talhao['variedade']:<18} {talhao['data_plantio']}"
        )
    print("─" * 74)



def consultar_talhao_memoria(talhoes: list[dict[str, Any]]) -> None:
    """Consulta um talhão por ID."""
    if not talhoes:
        print("\n  Nenhum talhão cadastrado.")
        return

    id_talhao = ler_inteiro("  ID do talhão para consulta: ", minimo=1)
    talhao = buscar_talhao_por_id(talhoes, id_talhao)

    if not talhao:
        print("  ⚠ Talhão não encontrado.")
        return

    print("\n--- Dados do Talhão ---")
    print(f"  ID           : {talhao['id']}")
    print(f"  Nome         : {talhao['nome']}")
    print(f"  Área (ha)    : {talhao['area_ha']:.2f}")
    print(f"  Variedade    : {talhao['variedade']}")
    print(f"  Data plantio : {talhao['data_plantio']}")


# -----------------------------------------------------------------------------
# Colheitas
# -----------------------------------------------------------------------------

def calcular_perda_toneladas(producao_ton: float, perda_percentual: float) -> float:
    """Calcula a perda absoluta em toneladas."""
    return producao_ton * (perda_percentual / 100)



def calcular_meses_desde_plantio(data_plantio_iso: str, data_colheita_iso: str) -> int:
    """Calcula a diferença aproximada em meses entre plantio e colheita."""
    data_plantio = datetime.strptime(data_plantio_iso, "%Y-%m-%d")
    data_colheita = datetime.strptime(data_colheita_iso, "%Y-%m-%d")

    meses = (data_colheita.year - data_plantio.year) * 12 + (data_colheita.month - data_plantio.month)
    if data_colheita.day < data_plantio.day:
        meses -= 1
    return max(meses, 0)



def registrar_colheita_memoria(
    talhoes: list[dict[str, Any]],
    colheitas: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Lê, valida e registra uma colheita em memória."""
    if not talhoes:
        print("\n  ⚠ Cadastre ao menos um talhão antes de registrar colheitas.")
        return None

    print("\n--- Registro de Colheita ---")
    listar_talhoes_memoria(talhoes)
    id_talhao = ler_inteiro("  ID do talhão: ", minimo=1)
    talhao = buscar_talhao_por_id(talhoes, id_talhao)

    if not talhao:
        print("  ⚠ Talhão não encontrado.")
        return None

    data_colheita = ler_data("  Data da colheita (DD/MM/AAAA): ")
    modo = ler_opcao("  Modo de colheita", ("manual", "mecanizada"))
    producao_ton = ler_float("  Produção total (toneladas): ", minimo=0.1)
    perda_percentual = ler_float("  Perda estimada (%): ", minimo=0.0, maximo=100.0)
    umidade_pct = ler_float("  Umidade da cana (%): ", minimo=0.0, maximo=100.0)
    brix = ler_float("  Teor de sacarose - Brix (°): ", minimo=0.0, maximo=30.0)

    perda_toneladas = calcular_perda_toneladas(producao_ton, perda_percentual)
    meses_plantio = calcular_meses_desde_plantio(talhao["data_plantio"], data_colheita)

    colheita = {
        "id": _proximo_id(colheitas),
        "id_talhao": talhao["id"],
        "nome_talhao": talhao["nome"],
        "area_ha": talhao["area_ha"],
        "data_colheita": data_colheita,
        "modo": modo,
        "producao_ton": producao_ton,
        "perda_percentual": perda_percentual,
        "perda_toneladas": perda_toneladas,
        "umidade_pct": umidade_pct,
        "brix": brix,
        "meses_plantio": meses_plantio,
    }
    colheitas.append(colheita)

    print("\n  ✅ Colheita registrada em memória com sucesso.")
    print(f"     Talhão           : {colheita['nome_talhao']}")
    print(f"     Perda calculada  : {colheita['perda_toneladas']:.2f} t")
    print(f"     Meses do plantio : {colheita['meses_plantio']}")
    return colheita



def listar_colheitas_memoria(colheitas: list[dict[str, Any]]) -> None:
    """Exibe todas as colheitas registradas em memória."""
    if not colheitas:
        print("\n  Nenhuma colheita registrada.")
        return

    print("\n" + "─" * 112)
    print(
        f"  {'ID':<4} {'Talhão':<18} {'Data':<12} {'Modo':<11} {'Prod(t)':<10} "
        f"{'Perda%':<8} {'Perda(t)':<10} {'Umid.%':<8} {'Brix':<6} {'Meses':<6}"
    )
    print("─" * 112)
    for colheita in colheitas:
        print(
            f"  {colheita['id']:<4} {colheita['nome_talhao']:<18} {colheita['data_colheita']:<12} "
            f"{colheita['modo']:<11} {colheita['producao_ton']:<10.2f} {colheita['perda_percentual']:<8.2f} "
            f"{colheita['perda_toneladas']:<10.2f} {colheita['umidade_pct']:<8.2f} "
            f"{colheita['brix']:<6.2f} {colheita['meses_plantio']:<6}"
        )
    print("─" * 112)



def consultar_colheitas_por_talhao_memoria(
    talhoes: list[dict[str, Any]],
    colheitas: list[dict[str, Any]],
) -> None:
    """Mostra as colheitas vinculadas a um talhão específico."""
    if not talhoes:
        print("\n  Nenhum talhão cadastrado.")
        return

    listar_talhoes_memoria(talhoes)
    id_talhao = ler_inteiro("  ID do talhão para listar colheitas: ", minimo=1)
    talhao = buscar_talhao_por_id(talhoes, id_talhao)

    if not talhao:
        print("  ⚠ Talhão não encontrado.")
        return

    colheitas_filtradas = [colheita for colheita in colheitas if colheita["id_talhao"] == id_talhao]
    if not colheitas_filtradas:
        print(f"\n  Nenhuma colheita registrada para o talhão '{talhao['nome']}'.")
        return

    listar_colheitas_memoria(colheitas_filtradas)
