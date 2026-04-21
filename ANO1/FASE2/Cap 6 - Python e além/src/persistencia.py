"""
persistencia.py
Responsável pela persistência local da ETAPA 5.

Escopo atual:
- salvar dados em JSON
- carregar dados de JSON
- exportar histórico e relatórios em TXT
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from analise import gerar_comparativo_por_modo, gerar_resumo_geral

ARQUIVO_JSON_PADRAO = "dados_sad_cana.json"
ARQUIVO_TXT_PADRAO = "historico_sad_cana.txt"


def _normalizar_dados(dados: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Garante a estrutura mínima esperada para os dados do sistema."""
    talhoes = dados.get("talhoes", []) if isinstance(dados, dict) else []
    colheitas = dados.get("colheitas", []) if isinstance(dados, dict) else []

    if not isinstance(talhoes, list):
        talhoes = []
    if not isinstance(colheitas, list):
        colheitas = []

    return {
        "talhoes": talhoes,
        "colheitas": colheitas,
    }



def salvar_dados_json(dados: dict[str, Any], caminho_arquivo: str = ARQUIVO_JSON_PADRAO) -> str:
    """Salva talhões e colheitas em um arquivo JSON."""
    dados_normalizados = _normalizar_dados(dados)
    caminho = Path(caminho_arquivo)
    if caminho.parent != Path("."):
        caminho.parent.mkdir(parents=True, exist_ok=True)

    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados_normalizados, arquivo, ensure_ascii=False, indent=4)

    return str(caminho)



def carregar_dados_json(caminho_arquivo: str = ARQUIVO_JSON_PADRAO) -> dict[str, list[dict[str, Any]]]:
    """Carrega dados a partir de um arquivo JSON e devolve a estrutura esperada."""
    caminho = Path(caminho_arquivo)
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    with caminho.open("r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return _normalizar_dados(dados)



def _linhas_relatorio_talhoes(talhoes: list[dict[str, Any]]) -> list[str]:
    """Gera bloco de texto para os talhões."""
    linhas = []
    linhas.append("TALHÕES CADASTRADOS")
    linhas.append("-" * 72)

    if not talhoes:
        linhas.append("Nenhum talhão cadastrado.")
        linhas.append("")
        return linhas

    for talhao in talhoes:
        linhas.append(
            f"ID {talhao['id']:>3} | Nome: {talhao['nome']} | Área: {talhao['area_ha']:.2f} ha | "
            f"Variedade: {talhao['variedade']} | Plantio: {talhao['data_plantio']}"
        )
    linhas.append("")
    return linhas



def _linhas_relatorio_colheitas(colheitas: list[dict[str, Any]]) -> list[str]:
    """Gera bloco de texto para as colheitas."""
    linhas = []
    linhas.append("HISTÓRICO DE COLHEITAS")
    linhas.append("-" * 72)

    if not colheitas:
        linhas.append("Nenhuma colheita registrada.")
        linhas.append("")
        return linhas

    for colheita in colheitas:
        linhas.append(
            f"ID {colheita['id']:>3} | Talhão: {colheita['nome_talhao']} | Data: {colheita['data_colheita']} | "
            f"Modo: {colheita['modo']} | Produção: {colheita['producao_ton']:.2f} t | "
            f"Perda: {colheita['perda_percentual']:.2f}% ({colheita['perda_toneladas']:.2f} t) | "
            f"Umidade: {colheita['umidade_pct']:.2f}% | Brix: {colheita['brix']:.2f}"
        )
    linhas.append("")
    return linhas



def _linhas_resumo_geral(colheitas: list[dict[str, Any]]) -> list[str]:
    """Gera bloco de resumo geral com base nas análises já existentes."""
    resumo = gerar_resumo_geral(colheitas)
    linhas = []
    linhas.append("RESUMO GERAL")
    linhas.append("-" * 72)
    linhas.append(f"Quantidade de colheitas : {resumo['quantidade_colheitas']}")
    linhas.append(f"Produção total (t)       : {resumo['producao_total_ton']:.2f}")
    linhas.append(f"Perda total (t)          : {resumo['perda_total_ton']:.2f}")
    linhas.append(f"Média de perda (%)       : {resumo['media_perda_pct']:.2f}")
    linhas.append(f"Média de eficiência      : {resumo['media_eficiencia']:.2f}")
    linhas.append(f"Média de produtividade   : {resumo['media_produtividade_t_ha']:.2f} t/ha")
    linhas.append(f"Colheitas manuais        : {resumo['manual_qtd']}")
    linhas.append(f"Colheitas mecanizadas    : {resumo['mecanizada_qtd']}")
    linhas.append("")
    return linhas



def _linhas_comparativo_modos(colheitas: list[dict[str, Any]]) -> list[str]:
    """Gera bloco textual com o comparativo entre modos de colheita."""
    linhas = []
    linhas.append("COMPARATIVO MANUAL VS. MECANIZADA")
    linhas.append("-" * 72)
    comparativo = gerar_comparativo_por_modo(colheitas)

    if not comparativo:
        linhas.append("Não há colheitas suficientes para comparação.")
        linhas.append("")
        return linhas

    for item in comparativo:
        linhas.append(
            f"Modo: {item['modo']} | Qtd: {item['quantidade']} | Produção média: {item['media_producao_ton']:.2f} t | "
            f"Perda média: {item['media_perda_pct']:.2f}% | Eficiência média: {item['media_eficiencia']:.2f} | "
            f"Desvio médio ref.: {item['desvio_medio_referencia']:+.2f}"
        )
    linhas.append("")
    return linhas



def exportar_historico_txt(dados: dict[str, Any], caminho_arquivo: str = ARQUIVO_TXT_PADRAO) -> str:
    """Exporta um relatório histórico consolidado em arquivo TXT."""
    dados_normalizados = _normalizar_dados(dados)
    caminho = Path(caminho_arquivo)
    if caminho.parent != Path("."):
        caminho.parent.mkdir(parents=True, exist_ok=True)

    linhas: list[str] = []
    linhas.append("SISTEMA DE APOIO À DECISÃO PARA COLHEITA DE CANA-DE-AÇÚCAR")
    linhas.append("ETAPA 5 — Histórico persistido em TXT")
    linhas.append("=" * 72)
    linhas.append("")
    linhas.extend(_linhas_relatorio_talhoes(dados_normalizados["talhoes"]))
    linhas.extend(_linhas_relatorio_colheitas(dados_normalizados["colheitas"]))
    linhas.extend(_linhas_resumo_geral(dados_normalizados["colheitas"]))
    linhas.extend(_linhas_comparativo_modos(dados_normalizados["colheitas"]))

    with caminho.open("w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(linhas))

    return str(caminho)
