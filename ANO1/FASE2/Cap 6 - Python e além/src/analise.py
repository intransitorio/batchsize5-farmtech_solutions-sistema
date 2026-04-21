"""
analise.py
Responsável pelos cálculos e indicadores da ETAPA 4.

Escopo atual:
- cálculo de perdas
- comparação manual vs. mecanizada
- indicadores de eficiência
- leitura analítica por colheita, por talhão e consolidada
"""

from __future__ import annotations

from statistics import mean
from typing import Any

from cadastro import buscar_colheita_por_id, buscar_talhao_por_id
from validacao import ler_inteiro

REFERENCIA_PERDA = {
    "manual": 5.0,
    "mecanizada": 15.0,
}

FAIXAS_PERDA = (
    (5.0, "Excelente"),
    (8.0, "Aceitável"),
    (12.0, "Atenção"),
    (15.0, "Crítico"),
    (100.0, "Inviável"),
)


# -----------------------------------------------------------------------------
# Cálculos atômicos
# -----------------------------------------------------------------------------

def classificar_perda(perda_percentual: float) -> str:
    """Classifica a perda percentual em uma faixa operacional."""
    for limite, descricao in FAIXAS_PERDA:
        if perda_percentual <= limite:
            return descricao
    return "Inviável"



def calcular_produtividade_t_ha(producao_ton: float, area_ha: float) -> float:
    """Calcula a produtividade em toneladas por hectare."""
    if area_ha <= 0:
        return 0.0
    return producao_ton / area_ha



def calcular_eficiencia_operacional(perda_percentual: float) -> float:
    """Calcula um índice simples de eficiência operacional."""
    eficiencia = 100.0 - perda_percentual
    return max(0.0, eficiencia)



def calcular_desvio_referencia(perda_percentual: float, modo: str) -> float:
    """Calcula o desvio da perda observada em relação à referência do modo."""
    referencia = REFERENCIA_PERDA.get(modo, 0.0)
    return perda_percentual - referencia


# -----------------------------------------------------------------------------
# Montagem de indicadores
# -----------------------------------------------------------------------------

def gerar_indicadores_colheita(colheita: dict[str, Any]) -> dict[str, Any]:
    """Monta um dicionário analítico para uma colheita individual."""
    produtividade = calcular_produtividade_t_ha(colheita["producao_ton"], colheita["area_ha"])
    eficiencia = calcular_eficiencia_operacional(colheita["perda_percentual"])
    classificacao = classificar_perda(colheita["perda_percentual"])
    desvio = calcular_desvio_referencia(colheita["perda_percentual"], colheita["modo"])

    return {
        "id": colheita["id"],
        "talhao": colheita["nome_talhao"],
        "modo": colheita["modo"],
        "producao_ton": colheita["producao_ton"],
        "perda_percentual": colheita["perda_percentual"],
        "perda_toneladas": colheita["perda_toneladas"],
        "produtividade_t_ha": produtividade,
        "eficiencia_operacional": eficiencia,
        "classificacao_perda": classificacao,
        "desvio_referencia": desvio,
    }



def gerar_indicadores_talhao(talhao: dict[str, Any], colheitas_talhao: list[dict[str, Any]]) -> dict[str, Any]:
    """Consolida métricas históricas de um talhão."""
    if not colheitas_talhao:
        return {
            "talhao": talhao["nome"],
            "quantidade_colheitas": 0,
            "producao_total_ton": 0.0,
            "perda_total_ton": 0.0,
            "media_perda_pct": 0.0,
            "media_produtividade_t_ha": 0.0,
            "media_eficiencia": 0.0,
            "media_brix": 0.0,
            "media_umidade": 0.0,
            "melhor_modo": "Sem dados",
        }

    indicadores_individuais = [gerar_indicadores_colheita(colheita) for colheita in colheitas_talhao]
    medias_por_modo = gerar_comparativo_por_modo(colheitas_talhao)
    melhor_modo = "Sem comparação"

    if medias_por_modo:
        melhor_modo = min(medias_por_modo, key=lambda item: item["media_perda_pct"])["modo"]

    return {
        "talhao": talhao["nome"],
        "quantidade_colheitas": len(colheitas_talhao),
        "producao_total_ton": sum(item["producao_ton"] for item in colheitas_talhao),
        "perda_total_ton": sum(item["perda_toneladas"] for item in colheitas_talhao),
        "media_perda_pct": mean(item["perda_percentual"] for item in colheitas_talhao),
        "media_produtividade_t_ha": mean(item["produtividade_t_ha"] for item in indicadores_individuais),
        "media_eficiencia": mean(item["eficiencia_operacional"] for item in indicadores_individuais),
        "media_brix": mean(item["brix"] for item in colheitas_talhao),
        "media_umidade": mean(item["umidade_pct"] for item in colheitas_talhao),
        "melhor_modo": melhor_modo,
    }



def gerar_comparativo_por_modo(colheitas: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Gera um comparativo consolidado entre colheitas manuais e mecanizadas."""
    if not colheitas:
        return []

    resultados: list[dict[str, Any]] = []
    for modo in ("manual", "mecanizada"):
        grupo = [colheita for colheita in colheitas if colheita["modo"] == modo]
        if not grupo:
            continue

        indicadores = [gerar_indicadores_colheita(colheita) for colheita in grupo]
        resultados.append(
            {
                "modo": modo,
                "quantidade": len(grupo),
                "media_producao_ton": mean(colheita["producao_ton"] for colheita in grupo),
                "media_perda_pct": mean(colheita["perda_percentual"] for colheita in grupo),
                "media_perda_ton": mean(colheita["perda_toneladas"] for colheita in grupo),
                "media_produtividade_t_ha": mean(item["produtividade_t_ha"] for item in indicadores),
                "media_eficiencia": mean(item["eficiencia_operacional"] for item in indicadores),
                "desvio_medio_referencia": mean(item["desvio_referencia"] for item in indicadores),
            }
        )

    return resultados



def gerar_resumo_geral(colheitas: list[dict[str, Any]]) -> dict[str, Any]:
    """Gera indicadores gerais do conjunto de colheitas."""
    if not colheitas:
        return {
            "quantidade_colheitas": 0,
            "producao_total_ton": 0.0,
            "perda_total_ton": 0.0,
            "media_perda_pct": 0.0,
            "media_eficiencia": 0.0,
            "media_produtividade_t_ha": 0.0,
            "manual_qtd": 0,
            "mecanizada_qtd": 0,
        }

    indicadores = [gerar_indicadores_colheita(colheita) for colheita in colheitas]
    return {
        "quantidade_colheitas": len(colheitas),
        "producao_total_ton": sum(colheita["producao_ton"] for colheita in colheitas),
        "perda_total_ton": sum(colheita["perda_toneladas"] for colheita in colheitas),
        "media_perda_pct": mean(colheita["perda_percentual"] for colheita in colheitas),
        "media_eficiencia": mean(item["eficiencia_operacional"] for item in indicadores),
        "media_produtividade_t_ha": mean(item["produtividade_t_ha"] for item in indicadores),
        "manual_qtd": sum(1 for colheita in colheitas if colheita["modo"] == "manual"),
        "mecanizada_qtd": sum(1 for colheita in colheitas if colheita["modo"] == "mecanizada"),
    }


# -----------------------------------------------------------------------------
# Exibição CLI
# -----------------------------------------------------------------------------

def analisar_colheita_por_id_cli(colheitas: list[dict[str, Any]]) -> None:
    """Exibe os indicadores de uma colheita escolhida pelo usuário."""
    if not colheitas:
        print("\n  Nenhuma colheita registrada para análise.")
        return

    id_colheita = ler_inteiro("  ID da colheita para análise: ", minimo=1)
    colheita = buscar_colheita_por_id(colheitas, id_colheita)
    if not colheita:
        print("  ⚠ Colheita não encontrada.")
        return

    indicadores = gerar_indicadores_colheita(colheita)
    print("\n--- Análise da Colheita ---")
    print(f"  ID                    : {indicadores['id']}")
    print(f"  Talhão                : {indicadores['talhao']}")
    print(f"  Modo                  : {indicadores['modo']}")
    print(f"  Produção (t)          : {indicadores['producao_ton']:.2f}")
    print(f"  Perda (%)             : {indicadores['perda_percentual']:.2f}")
    print(f"  Perda (t)             : {indicadores['perda_toneladas']:.2f}")
    print(f"  Produtividade (t/ha)  : {indicadores['produtividade_t_ha']:.2f}")
    print(f"  Eficiência operacional: {indicadores['eficiencia_operacional']:.2f}")
    print(f"  Classificação         : {indicadores['classificacao_perda']}")
    print(f"  Desvio da referência  : {indicadores['desvio_referencia']:+.2f}")



def analisar_talhao_cli(talhoes: list[dict[str, Any]], colheitas: list[dict[str, Any]]) -> None:
    """Exibe a consolidação analítica de um talhão específico."""
    if not talhoes:
        print("\n  Nenhum talhão cadastrado.")
        return

    id_talhao = ler_inteiro("  ID do talhão para análise: ", minimo=1)
    talhao = buscar_talhao_por_id(talhoes, id_talhao)
    if not talhao:
        print("  ⚠ Talhão não encontrado.")
        return

    colheitas_talhao = [colheita for colheita in colheitas if colheita["id_talhao"] == id_talhao]
    indicadores = gerar_indicadores_talhao(talhao, colheitas_talhao)

    print("\n--- Análise do Talhão ---")
    print(f"  Talhão                    : {indicadores['talhao']}")
    print(f"  Quantidade de colheitas   : {indicadores['quantidade_colheitas']}")
    print(f"  Produção total (t)        : {indicadores['producao_total_ton']:.2f}")
    print(f"  Perda total (t)           : {indicadores['perda_total_ton']:.2f}")
    print(f"  Média de perda (%)        : {indicadores['media_perda_pct']:.2f}")
    print(f"  Média de produtividade    : {indicadores['media_produtividade_t_ha']:.2f} t/ha")
    print(f"  Média de eficiência       : {indicadores['media_eficiencia']:.2f}")
    print(f"  Média de Brix             : {indicadores['media_brix']:.2f}")
    print(f"  Média de umidade (%)      : {indicadores['media_umidade']:.2f}")
    print(f"  Melhor modo observado     : {indicadores['melhor_modo']}")



def comparar_modos_cli(colheitas: list[dict[str, Any]]) -> None:
    """Exibe o comparativo entre colheitas manuais e mecanizadas."""
    comparativo = gerar_comparativo_por_modo(colheitas)
    if not comparativo:
        print("\n  Não há colheitas suficientes para comparação.")
        return

    print("\n" + "─" * 108)
    print(
        f"  {'Modo':<12} {'Qtd':<6} {'Prod. Méd(t)':<14} {'Perda Méd%':<12} {'Perda Méd(t)':<14} "
        f"{'Produt.(t/ha)':<15} {'Eficiência':<12} {'Desvio Ref.':<12}"
    )
    print("─" * 108)
    for item in comparativo:
        print(
            f"  {item['modo']:<12} {item['quantidade']:<6} {item['media_producao_ton']:<14.2f} "
            f"{item['media_perda_pct']:<12.2f} {item['media_perda_ton']:<14.2f} "
            f"{item['media_produtividade_t_ha']:<15.2f} {item['media_eficiencia']:<12.2f} "
            f"{item['desvio_medio_referencia']:<+12.2f}"
        )
    print("─" * 108)

    melhor = min(comparativo, key=lambda item: item["media_perda_pct"])
    print(f"\n  ► Melhor desempenho médio de perda: {melhor['modo']}")



def exibir_resumo_geral_cli(colheitas: list[dict[str, Any]]) -> None:
    """Exibe indicadores gerais da operação cadastrada em memória."""
    resumo = gerar_resumo_geral(colheitas)
    if resumo["quantidade_colheitas"] == 0:
        print("\n  Nenhuma colheita registrada para análise.")
        return

    print("\n--- Resumo Geral de Indicadores ---")
    print(f"  Quantidade de colheitas   : {resumo['quantidade_colheitas']}")
    print(f"  Produção total (t)        : {resumo['producao_total_ton']:.2f}")
    print(f"  Perda total (t)           : {resumo['perda_total_ton']:.2f}")
    print(f"  Média de perda (%)        : {resumo['media_perda_pct']:.2f}")
    print(f"  Média de eficiência       : {resumo['media_eficiencia']:.2f}")
    print(f"  Média de produtividade    : {resumo['media_produtividade_t_ha']:.2f} t/ha")
    print(f"  Colheitas manuais         : {resumo['manual_qtd']}")
    print(f"  Colheitas mecanizadas     : {resumo['mecanizada_qtd']}")
