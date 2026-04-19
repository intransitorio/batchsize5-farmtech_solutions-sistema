"""
arquivos.py — Manipulação de arquivos: JSON, TXT e CSV.
Unifica as funcionalidades dos dois projetos originais.
"""

import json
import csv
import os
from datetime import datetime

from talhoes import listar_talhoes, cadastrar_talhao
from colheita import listar_colheitas_bd, analisar_registro

PASTA_DADOS = os.path.join(os.path.dirname(__file__), "dados")
os.makedirs(PASTA_DADOS, exist_ok=True)

ARQUIVO_JSON = os.path.join(PASTA_DADOS, "historico_colheitas.json")
ARQUIVO_TXT  = os.path.join(PASTA_DADOS, "relatorio_colheitas.txt")
ARQUIVO_CSV  = os.path.join(PASTA_DADOS, "relatorio_colheitas.csv")

COLUNAS_CSV = [
    "id", "data_colheita", "fazenda", "nome_talhao", "cultura", "tipo_colheita",
    "area_ha", "produtividade_estimada_t_ha", "producao_colhida_t",
    "velocidade_colhedora_kmh", "altura_corte_cm", "estado_facas",
    "operador", "maquina", "umidade_solo", "chuva_recente", "observacoes",
    "producao_estimada_t", "perda_real_t", "perda_percentual",
    "classificacao", "situacao_referencia", "diagnostico",
    "recomendacao", "prioridade_decisao",
]


def gerar_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ─────────────────────────────────────────────
# JSON
# ─────────────────────────────────────────────

def exportar_talhoes_json(caminho: str = None) -> str:
    """Exporta talhões para JSON."""
    if not caminho:
        caminho = os.path.join(PASTA_DADOS, "talhoes.json")
    talhoes = listar_talhoes()
    payload = {
        "exportado_em": gerar_timestamp(),
        "total": len(talhoes),
        "talhoes": talhoes
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)
    print(f"  ✅ {len(talhoes)} talhão(ões) exportado(s) → {caminho}")
    return caminho


def importar_talhoes_json(caminho: str = None) -> int:
    """Importa talhões de um JSON."""
    if not caminho:
        caminho = os.path.join(PASTA_DADOS, "talhoes.json")
    if not os.path.exists(caminho):
        print(f"  ⚠ Arquivo não encontrado: {caminho}")
        return 0
    with open(caminho, "r", encoding="utf-8") as f:
        payload = json.load(f)
    importados = 0
    for t in payload.get("talhoes", []):
        if cadastrar_talhao(t["nome"], t["area_ha"], t["variedade"], t["data_plantio"]):
            importados += 1
    print(f"  ✅ {importados} talhão(ões) importado(s).")
    return importados


def salvar_colheitas_json(caminho: str = None) -> str:
    """Exporta todas as colheitas para JSON (formato sad_agro)."""
    if not caminho:
        caminho = ARQUIVO_JSON
    colheitas = listar_colheitas_bd()
    payload = {
        "projeto":              "SACana — SAD Cana-de-açúcar",
        "versao":               "2.0",
        "ultima_atualizacao":   gerar_timestamp(),
        "quantidade_registros": len(colheitas),
        "colheitas":            colheitas,
    }
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=4, default=str)
    print(f"  ✅ {len(colheitas)} colheita(s) exportada(s) → {caminho}")
    return caminho


def resumo_historico_json(caminho: str = None) -> None:
    """Exibe metadados do JSON sem carregar tudo."""
    if not caminho:
        caminho = ARQUIVO_JSON
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        print(f"\n  Projeto.........: {dados.get('projeto', '—')}")
        print(f"  Versão..........: {dados.get('versao', '—')}")
        print(f"  Atualização.....: {dados.get('ultima_atualizacao', '—')}")
        print(f"  Registros.......: {dados.get('quantidade_registros', 0)}")
    except Exception as e:
        print(f"  ⚠ Erro: {e}")


# ─────────────────────────────────────────────
# TXT
# ─────────────────────────────────────────────

def exportar_relatorio_txt(caminho: str = None) -> str:
    """Gera relatório TXT agrupado por talhão."""
    if not caminho:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho = os.path.join(PASTA_DADOS, f"relatorio_{ts}.txt")

    colheitas = listar_colheitas_bd()
    linhas = [
        "=" * 78 + "\n",
        "  SACana — RELATÓRIO DE COLHEITAS\n",
        f"  Gerado em: {gerar_timestamp()}\n",
        f"  Total de registros: {len(colheitas)}\n",
        "=" * 78 + "\n\n",
    ]

    if not colheitas:
        linhas.append("  Nenhuma colheita registrada.\n")
    else:
        por_talhao = {}
        for c in colheitas:
            chave = str(c.get("nome_talhao", "—"))
            por_talhao.setdefault(chave, []).append(c)

        for nome_talhao, cols in por_talhao.items():
            linhas.append(f"  TALHÃO: {nome_talhao}\n")
            linhas.append("  " + "-" * 74 + "\n")
            total_prod  = 0.0
            total_perda = 0.0
            for c in cols:
                linhas.append(
                    f"  ID:{c.get('id','—')} | {c.get('data_colheita','—')} | "
                    f"{c.get('tipo_colheita','—')} | "
                    f"Colhida:{float(c.get('producao_colhida_t') or 0):.1f}t | "
                    f"Perda:{float(c.get('perda_percentual') or 0):.1f}% | "
                    f"Ef.:{c.get('classificacao','—')} | "
                    f"Prior.:{c.get('prioridade_decisao','—')}\n"
                )
                linhas.append(
                    f"    Diag.: {c.get('diagnostico','—')}\n"
                )
                linhas.append(
                    f"    Rec..: {c.get('recomendacao','—')}\n"
                )
                total_prod  += float(c.get("producao_colhida_t") or 0)
                total_perda += float(c.get("perda_real_t") or 0)
            linhas.append(f"    ► Total colhido: {total_prod:.2f} t  |  "
                          f"Total perdido: {total_perda:.2f} t\n\n")

    linhas += ["=" * 78 + "\n", "  FIM DO RELATÓRIO\n", "=" * 78 + "\n"]

    with open(caminho, "w", encoding="utf-8") as f:
        f.writelines(linhas)
    print(f"  ✅ Relatório TXT → {caminho}")
    return caminho


# ─────────────────────────────────────────────
# CSV
# ─────────────────────────────────────────────

def exportar_csv(caminho: str = None) -> str:
    """Exporta colheitas em CSV compatível com Excel."""
    if not caminho:
        caminho = ARQUIVO_CSV
    colheitas = listar_colheitas_bd()
    if not colheitas:
        print("  Sem registros para exportar.")
        return caminho

    campos_num = (
        "area_ha", "produtividade_estimada_t_ha", "producao_colhida_t",
        "velocidade_colhedora_kmh", "altura_corte_cm",
        "producao_estimada_t", "perda_real_t", "perda_percentual",
    )

    with open(caminho, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=COLUNAS_CSV, delimiter=";", extrasaction="ignore"
        )
        writer.writeheader()
        for c in colheitas:
            linha = {col: c.get(col) for col in COLUNAS_CSV}
            if isinstance(linha.get("chuva_recente"), bool):
                linha["chuva_recente"] = "Sim" if linha["chuva_recente"] else "Não"
            for col in campos_num:
                if linha.get(col) is not None:
                    linha[col] = f"{float(linha[col]):.2f}"
            writer.writerow(linha)

    print(f"  ✅ CSV exportado → {caminho}")
    print("  Dica: abra no Excel via Dados > De Texto/CSV, separador ';'.")
    return caminho


# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────

def menu_arquivos() -> None:
    while True:
        print("\n╔════════════════════════════════════╗")
        print("║     IMPORTAR / EXPORTAR DADOS      ║")
        print("╠════════════════════════════════════╣")
        print("║  1. Exportar talhões (JSON)        ║")
        print("║  2. Importar talhões (JSON)        ║")
        print("║  3. Exportar colheitas (JSON)      ║")
        print("║  4. Resumo do arquivo JSON         ║")
        print("║  5. Exportar relatório (TXT)       ║")
        print("║  6. Exportar relatório (CSV)       ║")
        print("║  0. Voltar                         ║")
        print("╚════════════════════════════════════╝")
        escolha = input("  Opção: ").strip()

        if escolha == "1":
            exportar_talhoes_json()
        elif escolha == "2":
            importar_talhoes_json()
        elif escolha == "3":
            salvar_colheitas_json()
        elif escolha == "4":
            resumo_historico_json()
        elif escolha == "5":
            exportar_relatorio_txt()
        elif escolha == "6":
            exportar_csv()
        elif escolha == "0":
            break
        else:
            print("  ⚠ Opção inválida.")
