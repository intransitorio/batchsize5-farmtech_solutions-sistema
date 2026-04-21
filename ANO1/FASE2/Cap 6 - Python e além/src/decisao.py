"""
decisao.py
Responsável pelas regras automatizadas de apoio à decisão da ETAPA 7.

Escopo atual:
- score de prontidão para colheita
- diagnóstico de perdas
- recomendação do modo de colheita
- sugestões práticas de mitigação
"""

from __future__ import annotations

from typing import Any

from analise import classificar_perda, calcular_desvio_referencia, gerar_indicadores_talhao
from cadastro import buscar_colheita_por_id, buscar_talhao_por_id
from validacao import ler_inteiro

BRIX_IDEAL_MIN = 18.0
BRIX_IDEAL_MAX = 22.0
UMIDADE_IDEAL_MIN = 65.0
UMIDADE_IDEAL_MAX = 75.0
UMIDADE_ALTA = 85.0
MATURIDADE_MIN_MESES = 12


def pontuar_brix(brix: float) -> int:
    """Pontua o teor de Brix para o score de prontidão."""
    if BRIX_IDEAL_MIN <= brix <= BRIX_IDEAL_MAX:
        return 40
    if 16.0 <= brix < BRIX_IDEAL_MIN or BRIX_IDEAL_MAX < brix <= 24.0:
        return 20
    return 0


def pontuar_umidade(umidade_pct: float) -> int:
    """Pontua a umidade para o score de prontidão."""
    if UMIDADE_IDEAL_MIN <= umidade_pct <= UMIDADE_IDEAL_MAX:
        return 30
    if 60.0 <= umidade_pct < UMIDADE_IDEAL_MIN or UMIDADE_IDEAL_MAX < umidade_pct <= UMIDADE_ALTA:
        return 15
    return 0


def pontuar_maturidade(meses_plantio: int) -> int:
    """Pontua a maturidade da cana para o score de prontidão."""
    if meses_plantio >= MATURIDADE_MIN_MESES:
        return 30
    if meses_plantio >= 10:
        return 15
    return 0


def calcular_score_prontidao(colheita: dict[str, Any]) -> int:
    """Calcula um score simples de prontidão da colheita."""
    return (
        pontuar_brix(float(colheita["brix"]))
        + pontuar_umidade(float(colheita["umidade_pct"]))
        + pontuar_maturidade(int(colheita["meses_plantio"]))
    )


def classificar_prontidao(score: int) -> str:
    """Classifica o score de prontidão em uma ação principal."""
    if score >= 80:
        return "Colher agora"
    if score >= 50:
        return "Aguardar e monitorar"
    return "Não colher"


def diagnosticar_perda(colheita: dict[str, Any]) -> str:
    """Gera um diagnóstico textual para o nível de perda observado."""
    perda = float(colheita["perda_percentual"])
    classificacao = classificar_perda(perda)
    desvio = calcular_desvio_referencia(perda, str(colheita["modo"]))

    mensagens = {
        "Excelente": "Perda muito baixa. A operação está sob controle.",
        "Aceitável": "Perda administrável. Manter monitoramento da operação.",
        "Atenção": "Perda acima do desejável. Há sinais de ineficiência operacional.",
        "Crítico": "Perda em faixa crítica. Revisão imediata da operação é recomendada.",
        "Inviável": "Perda excessiva. A operação deve ser reavaliada antes de prosseguir.",
    }
    base = mensagens.get(classificacao, "Perda fora do padrão esperado.")

    if desvio > 0:
        return f"{base} A perda ficou {desvio:.2f} ponto(s) acima da referência do modo {colheita['modo']}."
    if desvio < 0:
        return f"{base} A perda ficou {abs(desvio):.2f} ponto(s) abaixo da referência do modo {colheita['modo']}."
    return f"{base} A perda coincidiu com a referência do modo {colheita['modo']}."


def sugerir_modo_colheita(colheita: dict[str, Any], historico_talhao: dict[str, Any] | None = None) -> str:
    """Sugere o modo mais seguro ou eficiente de colheita."""
    umidade = float(colheita["umidade_pct"])
    media_perda = float((historico_talhao or {}).get("media_perda_pct", 0.0))

    if umidade >= UMIDADE_ALTA:
        return "manual"
    if media_perda > 15.0:
        return "manual"
    if umidade > UMIDADE_IDEAL_MAX or media_perda > 12.0:
        return "mecanizada com cautela"
    return "mecanizada"


def gerar_sugestoes_praticas(colheita: dict[str, Any], historico_talhao: dict[str, Any] | None = None) -> list[str]:
    """Monta uma lista de sugestões práticas a partir dos dados observados."""
    sugestoes: list[str] = []
    perda = float(colheita["perda_percentual"])
    umidade = float(colheita["umidade_pct"])
    brix = float(colheita["brix"])
    meses = int(colheita["meses_plantio"])
    media_perda = float((historico_talhao or {}).get("media_perda_pct", 0.0))

    if perda > 15.0:
        sugestoes.append("Parar a operação e revisar regulagem das facas, extratores e velocidade da máquina.")
    elif perda > 12.0:
        sugestoes.append("Revisar parâmetros operacionais e fazer manutenção preventiva antes do próximo ciclo.")
    elif perda > 8.0:
        sugestoes.append("Monitorar o desempenho da equipe e recalibrar o conjunto mecanizado.")

    if umidade > UMIDADE_IDEAL_MAX:
        sugestoes.append("Verificar condição do solo e evitar mecanização agressiva em cenário muito úmido.")
    if umidade >= UMIDADE_ALTA:
        sugestoes.append("Priorizar colheita manual ou adiar a operação até redução da umidade.")

    if brix < BRIX_IDEAL_MIN:
        sugestoes.append("Aguardar maior maturação da cana antes de colher.")
    elif brix > BRIX_IDEAL_MAX:
        sugestoes.append("Priorizar a colheita deste talhão para evitar perda do ponto ótimo de sacarose.")

    if meses < MATURIDADE_MIN_MESES:
        sugestoes.append("Reavaliar a data de corte: o talhão ainda está abaixo da maturidade mínima recomendada.")

    if media_perda > 12.0:
        sugestoes.append("Usar o histórico do talhão para revisar o plano operacional e reduzir reincidência de perdas.")

    if not sugestoes:
        sugestoes.append("Manter o plano atual e seguir monitorando os indicadores operacionais do talhão.")

    return sugestoes


def gerar_regras_acionadas(colheita: dict[str, Any], historico_talhao: dict[str, Any] | None = None) -> list[str]:
    """Lista as regras de negócio acionadas no diagnóstico."""
    regras: list[str] = []
    umidade = float(colheita["umidade_pct"])
    brix = float(colheita["brix"])
    meses = int(colheita["meses_plantio"])
    media_perda = float((historico_talhao or {}).get("media_perda_pct", 0.0))

    if meses < MATURIDADE_MIN_MESES:
        regras.append("Talhão abaixo da maturidade mínima de 12 meses.")
    if brix < BRIX_IDEAL_MIN:
        regras.append("Brix abaixo da faixa ideal de 18 a 22.")
    elif BRIX_IDEAL_MIN <= brix <= BRIX_IDEAL_MAX:
        regras.append("Brix dentro da faixa ideal de colheita.")
    else:
        regras.append("Brix acima da faixa ideal; colheita deve ser priorizada.")

    if UMIDADE_IDEAL_MIN <= umidade <= UMIDADE_IDEAL_MAX:
        regras.append("Umidade dentro da faixa ideal de 65% a 75%.")
    elif umidade >= UMIDADE_ALTA:
        regras.append("Umidade muito alta; mecanização fica sob risco elevado.")
    else:
        regras.append("Umidade fora da faixa ideal; operação pede cautela.")

    if media_perda > 15.0:
        regras.append("Histórico do talhão supera a referência crítica da colheita mecanizada.")
    elif media_perda > 12.0:
        regras.append("Histórico do talhão sinaliza perdas elevadas e exige revisão operacional.")

    return regras


def diagnosticar_colheita(colheita: dict[str, Any], historico_talhao: dict[str, Any] | None = None) -> dict[str, Any]:
    """Consolida o diagnóstico decisório de uma colheita."""
    score = calcular_score_prontidao(colheita)
    status_prontidao = classificar_prontidao(score)
    recomendacao_modo = sugerir_modo_colheita(colheita, historico_talhao)
    diagnostico = diagnosticar_perda(colheita)
    sugestoes = gerar_sugestoes_praticas(colheita, historico_talhao)
    regras = gerar_regras_acionadas(colheita, historico_talhao)

    if status_prontidao == "Colher agora":
        recomendacao_final = f"Recomendação: colher agora, preferencialmente em modo {recomendacao_modo}."
    elif status_prontidao == "Aguardar e monitorar":
        recomendacao_final = "Recomendação: aguardar e monitorar maturidade, umidade e perdas antes do corte."
    else:
        recomendacao_final = "Recomendação: não colher neste momento; reavaliar o talhão depois de novo monitoramento."

    return {
        "score_prontidao": score,
        "status_prontidao": status_prontidao,
        "diagnostico_perda": diagnostico,
        "recomendacao_modo": recomendacao_modo,
        "recomendacao_final": recomendacao_final,
        "regras_acionadas": regras,
        "sugestoes": sugestoes,
    }


def diagnosticar_talhao(talhao: dict[str, Any], colheitas_talhao: list[dict[str, Any]]) -> dict[str, Any]:
    """Gera o diagnóstico consolidado de um talhão com base no histórico."""
    indicadores = gerar_indicadores_talhao(talhao, colheitas_talhao)

    if not colheitas_talhao:
        return {
            "talhao": talhao["nome"],
            "quantidade_colheitas": 0,
            "status_talhao": "Sem histórico",
            "mensagem": "O talhão ainda não possui colheitas registradas para diagnóstico.",
        }

    ultima_colheita = max(colheitas_talhao, key=lambda item: item["data_colheita"])
    decisao_ultima = diagnosticar_colheita(ultima_colheita, indicadores)

    media_perda = float(indicadores["media_perda_pct"])
    if media_perda <= 8.0:
        status_talhao = "Estável"
    elif media_perda <= 12.0:
        status_talhao = "Em atenção"
    else:
        status_talhao = "Crítico"

    return {
        "talhao": talhao["nome"],
        "quantidade_colheitas": indicadores["quantidade_colheitas"],
        "status_talhao": status_talhao,
        "media_perda_pct": indicadores["media_perda_pct"],
        "media_umidade": indicadores["media_umidade"],
        "media_brix": indicadores["media_brix"],
        "melhor_modo": indicadores["melhor_modo"],
        "ultima_colheita": ultima_colheita,
        "decisao_ultima": decisao_ultima,
    }


def diagnosticar_colheita_cli(colheitas: list[dict[str, Any]]) -> None:
    """Exibe o diagnóstico decisório de uma colheita específica."""
    if not colheitas:
        print("\n  Nenhuma colheita registrada para diagnóstico.")
        return

    id_colheita = ler_inteiro("  ID da colheita para diagnóstico: ", minimo=1)
    colheita = buscar_colheita_por_id(colheitas, id_colheita)
    if not colheita:
        print("  ⚠ Colheita não encontrada.")
        return

    grupo_talhao = [item for item in colheitas if item["id_talhao"] == colheita["id_talhao"]]
    historico_talhao = {"media_perda_pct": 0.0}
    if grupo_talhao:
        historico_talhao = {
            "media_perda_pct": sum(item["perda_percentual"] for item in grupo_talhao) / len(grupo_talhao),
        }

    diagnostico = diagnosticar_colheita(colheita, historico_talhao)

    print("\n--- Apoio à Decisão da Colheita ---")
    print(f"  ID da colheita         : {colheita['id']}")
    print(f"  Talhão                 : {colheita['nome_talhao']}")
    print(f"  Score de prontidão     : {diagnostico['score_prontidao']}")
    print(f"  Status de prontidão    : {diagnostico['status_prontidao']}")
    print(f"  Modo sugerido          : {diagnostico['recomendacao_modo']}")
    print(f"  Diagnóstico da perda   : {diagnostico['diagnostico_perda']}")
    print(f"  Parecer final          : {diagnostico['recomendacao_final']}")

    print("\n  Regras acionadas:")
    for regra in diagnostico["regras_acionadas"]:
        print(f"   - {regra}")

    print("\n  Sugestões práticas:")
    for sugestao in diagnostico["sugestoes"]:
        print(f"   - {sugestao}")


def diagnosticar_talhao_cli(talhoes: list[dict[str, Any]], colheitas: list[dict[str, Any]]) -> None:
    """Exibe o diagnóstico consolidado de um talhão."""
    if not talhoes:
        print("\n  Nenhum talhão cadastrado.")
        return

    id_talhao = ler_inteiro("  ID do talhão para diagnóstico: ", minimo=1)
    talhao = buscar_talhao_por_id(talhoes, id_talhao)
    if not talhao:
        print("  ⚠ Talhão não encontrado.")
        return

    colheitas_talhao = [item for item in colheitas if item["id_talhao"] == id_talhao]
    diagnostico = diagnosticar_talhao(talhao, colheitas_talhao)

    print("\n--- Apoio à Decisão do Talhão ---")
    print(f"  Talhão                 : {diagnostico['talhao']}")
    print(f"  Quantidade de colheitas: {diagnostico['quantidade_colheitas']}")
    print(f"  Status do talhão       : {diagnostico['status_talhao']}")

    if diagnostico['quantidade_colheitas'] == 0:
        print(f"  Mensagem               : {diagnostico['mensagem']}")
        return

    print(f"  Média de perda (%)     : {diagnostico['media_perda_pct']:.2f}")
    print(f"  Média de umidade (%)   : {diagnostico['media_umidade']:.2f}")
    print(f"  Média de Brix          : {diagnostico['media_brix']:.2f}")
    print(f"  Melhor modo histórico  : {diagnostico['melhor_modo']}")
    print(f"  Última colheita        : {diagnostico['ultima_colheita']['data_colheita']}")
    print(f"  Parecer final          : {diagnostico['decisao_ultima']['recomendacao_final']}")

    print("\n  Sugestões prioritárias para o talhão:")
    for sugestao in diagnostico['decisao_ultima']['sugestoes']:
        print(f"   - {sugestao}")
