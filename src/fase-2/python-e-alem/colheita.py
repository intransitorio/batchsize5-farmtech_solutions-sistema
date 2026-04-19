"""
colheita.py — Cadastro, análise e diagnóstico de colheitas de cana-de-açúcar.

Unifica:
- Estrutura modular do trabalho_fiap (Oracle, talhões, módulos separados)
- Lógica agronômica rica do sad_agro (diagnóstico, SAD, campos detalhados)

Estruturas de dados:
  - Tuplas: faixas de eficiência, estados de facas, umidades (imutáveis)
  - Dicionários: cada registro de colheita
  - Listas: tabela de memória e histórico
"""

from banco import conectar, encerrar
from validacao import (ler_float, ler_data, ler_inteiro, ler_texto,
                       ler_tipo_colheita, ler_opcao, ler_booleano)
from talhoes import listar_talhoes, exibir_talhoes, buscar_talhao_por_id


# ─────────────────────────────────────────────
# CONSTANTES — tuplas imutáveis de referência
# ─────────────────────────────────────────────

TIPOS_COLHEITA:  tuple = ("manual", "mecanizada")
ESTADOS_FACAS:   tuple = ("novas", "boas", "desgastadas")
UMIDADES_SOLO:   tuple = ("baixa", "media", "alta")

# Faixas de eficiência por perda percentual (rótulo, min_inclusivo, max_exclusivo)
FAIXAS_EFICIENCIA: tuple = (
    ("excelente", 0.0,  5.0),
    ("boa",        5.0,  8.0),
    ("moderada",   8.0, 10.0),
    ("baixa",     10.0, float("inf")),
)

# Referência SOCICANA de perda máxima aceitável por tipo
REFERENCIA_PERDA: dict = {"manual": 5.0, "mecanizada": 15.0}

# Limites operacionais para diagnóstico automático
VELOCIDADE_LIMITE_KMH:    float = 5.0
ALTURA_CORTE_REF_CM:      float = 5.0
PERDA_ATENCAO_PERCENTUAL: float = 8.0
PERDA_CRITICA_PERCENTUAL: float = 10.0

CULTURA_PADRAO = "Cana-de-açúcar"


# ─────────────────────────────────────────────
# CÁLCULOS — funções puras com parâmetros
# ─────────────────────────────────────────────

def calcular_producao_estimada(area_ha: float, prod_est_t_ha: float) -> float:
    return area_ha * prod_est_t_ha


def calcular_perda_real(producao_estimada: float, producao_colhida: float) -> float:
    return max(0.0, producao_estimada - producao_colhida)


def calcular_perda_percentual(perda_real: float, producao_estimada: float) -> float:
    if producao_estimada <= 0:
        return 0.0
    return (perda_real / producao_estimada) * 100


def classificar_eficiencia(perda_pct: float) -> str:
    for rotulo, minimo, maximo in FAIXAS_EFICIENCIA:
        if minimo <= perda_pct < maximo:
            return rotulo
    return "não classificada"


def avaliar_referencia(tipo_colheita: str, perda_pct: float) -> str:
    limite = REFERENCIA_PERDA.get(tipo_colheita, 15.0)
    return "dentro da referência" if perda_pct <= limite else "acima da referência"


def analisar_registro(registro: dict) -> None:
    """Preenche campos calculados de análise no dicionário do registro."""
    prod_est  = calcular_producao_estimada(
        registro["area_ha"], registro["produtividade_estimada_t_ha"]
    )
    perda_t   = calcular_perda_real(prod_est, registro["producao_colhida_t"])
    perda_pct = calcular_perda_percentual(perda_t, prod_est)

    registro["producao_estimada_t"] = prod_est
    registro["perda_real_t"]        = perda_t
    registro["perda_percentual"]    = perda_pct
    registro["classificacao"]       = classificar_eficiencia(perda_pct)
    registro["situacao_referencia"] = avaliar_referencia(
        registro["tipo_colheita"], perda_pct
    )


# ─────────────────────────────────────────────
# DIAGNÓSTICO — Sistema de Apoio à Decisão
# ─────────────────────────────────────────────

def contar_alertas_talhao(tabela: list, talhao: str) -> int:
    return sum(
        1 for r in tabela
        if r.get("talhao") == talhao
        and r.get("perda_percentual") is not None
        and float(r["perda_percentual"]) >= PERDA_ATENCAO_PERCENTUAL
    )


def definir_prioridade(perda_pct: float, n_diagnosticos: int) -> str:
    if perda_pct > PERDA_CRITICA_PERCENTUAL or n_diagnosticos >= 3:
        return "alta"
    if perda_pct > PERDA_ATENCAO_PERCENTUAL or n_diagnosticos == 2:
        return "media"
    return "baixa"


def diagnosticar_registro(registro: dict, tabela: list) -> None:
    """
    Aplica 6 regras de negócio agronômico e preenche:
    - diagnostico, recomendacao, prioridade_decisao
    """
    analisar_registro(registro)

    perda_pct    = float(registro.get("perda_percentual") or 0.0)
    velocidade   = float(registro.get("velocidade_colhedora_kmh") or 0.0)
    altura_corte = float(registro.get("altura_corte_cm") or 0.0)
    estado_facas = str(registro.get("estado_facas") or "")
    tipo         = str(registro.get("tipo_colheita") or "")
    umidade_solo = str(registro.get("umidade_solo") or "")
    chuva        = bool(registro.get("chuva_recente"))
    talhao       = str(registro.get("talhao") or "")

    diags, recs = [], []

    # Regra 1: velocidade elevada com perda crítica
    if perda_pct > PERDA_CRITICA_PERCENTUAL and velocidade > VELOCIDADE_LIMITE_KMH:
        diags.append("Perda crítica associada à velocidade operacional elevada")
        recs.append("Reduzir velocidade da colhedora e reaferir o talhão")

    # Regra 2: facas desgastadas com perda alta
    if perda_pct >= PERDA_ATENCAO_PERCENTUAL and estado_facas == "desgastadas":
        diags.append("Indício de perda por desgaste das facas de corte")
        recs.append("Revisar ou substituir as facas e acompanhar nova operação")

    # Regra 3: altura de corte elevada
    if perda_pct >= PERDA_ATENCAO_PERCENTUAL and altura_corte > ALTURA_CORTE_REF_CM:
        diags.append("Altura de corte elevada pode gerar perdas de cana de base")
        recs.append("Ajustar altura de corte para reduzir perdas no toco")

    # Regra 4: mecanizada em solo úmido com chuva
    if tipo == "mecanizada" and chuva and umidade_solo == "alta":
        diags.append("Solo úmido com risco de compactação e perda operacional")
        recs.append("Aguardar janela operacional adequada; intensificar inspeção")

    # Regra 5: talhão com perdas recorrentes
    if contar_alertas_talhao(tabela, talhao) >= 3:
        diags.append("Perdas recorrentes identificadas neste talhão")
        recs.append("Revisar planejamento operacional deste talhão")

    # Regra 6: operação excelente
    if perda_pct <= 5.0:
        diags.append("Operação dentro do padrão de referência do setor")
        recs.append("Manter regulagem atual e continuar monitoramento rotineiro")

    if not diags:
        diags.append("Sem causa dominante identificada")
        recs.append("Coletar mais dados operacionais e manter monitoramento")

    registro["diagnostico"]        = "; ".join(diags)
    registro["recomendacao"]       = "; ".join(recs)
    registro["prioridade_decisao"] = definir_prioridade(perda_pct, len(diags))


# ─────────────────────────────────────────────
# PERSISTÊNCIA — Oracle
# ─────────────────────────────────────────────

def registrar_colheita_bd(id_talhao: int, registro: dict) -> dict:
    """Insere colheita completa no Oracle e retorna com ID gerado."""
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO colheitas (
                id_talhao, data_colheita, fazenda, cultura, tipo_colheita,
                producao_colhida_t, produtividade_estimada_t_ha,
                velocidade_colhedora_kmh, altura_corte_cm, estado_facas,
                operador, maquina, umidade_solo, chuva_recente, observacoes,
                producao_estimada_t, perda_real_t, perda_percentual,
                classificacao, situacao_referencia,
                diagnostico, recomendacao, prioridade_decisao
            ) VALUES (
                :1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15,
                :16,:17,:18,:19,:20,:21,:22,:23
            )
        """, (
            id_talhao,
            registro["data_colheita"],
            registro["fazenda"],
            registro.get("cultura", CULTURA_PADRAO),
            registro["tipo_colheita"],
            registro["producao_colhida_t"],
            registro["produtividade_estimada_t_ha"],
            registro["velocidade_colhedora_kmh"],
            registro["altura_corte_cm"],
            registro["estado_facas"],
            registro["operador"],
            registro["maquina"],
            registro["umidade_solo"],
            "S" if registro["chuva_recente"] else "N",
            registro["observacoes"],
            registro.get("producao_estimada_t"),
            registro.get("perda_real_t"),
            registro.get("perda_percentual"),
            registro.get("classificacao"),
            registro.get("situacao_referencia"),
            registro.get("diagnostico"),
            registro.get("recomendacao"),
            registro.get("prioridade_decisao"),
        ))
        conn.commit()
        cursor.execute("SELECT MAX(id) FROM colheitas WHERE id_talhao = :1", (id_talhao,))
        registro["id"] = cursor.fetchone()[0]
        print(f"\n  ✅ Colheita registrada com ID {registro['id']}.")
        return registro
    except Exception as e:
        print(f"  ❌ Erro ao registrar: {e}")
        return None
    finally:
        encerrar(conn)


def listar_colheitas_bd(id_talhao: int = None) -> list:
    """Retorna lista de dicionários com colheitas do banco (tabela de memória)."""
    conn = conectar()
    try:
        cursor = conn.cursor()
        if id_talhao:
            cursor.execute("""
                SELECT c.id, c.id_talhao, c.data_colheita, c.fazenda,
                       c.tipo_colheita, c.producao_colhida_t,
                       c.produtividade_estimada_t_ha, c.velocidade_colhedora_kmh,
                       c.altura_corte_cm, c.estado_facas, c.operador, c.maquina,
                       c.umidade_solo, c.chuva_recente, c.observacoes,
                       c.producao_estimada_t, c.perda_real_t, c.perda_percentual,
                       c.classificacao, c.situacao_referencia,
                       c.diagnostico, c.recomendacao, c.prioridade_decisao,
                       t.nome AS nome_talhao, t.area_ha
                FROM colheitas c JOIN talhoes t ON c.id_talhao = t.id
                WHERE c.id_talhao = :1 ORDER BY c.data_colheita DESC
            """, (id_talhao,))
        else:
            cursor.execute("""
                SELECT c.id, c.id_talhao, c.data_colheita, c.fazenda,
                       c.tipo_colheita, c.producao_colhida_t,
                       c.produtividade_estimada_t_ha, c.velocidade_colhedora_kmh,
                       c.altura_corte_cm, c.estado_facas, c.operador, c.maquina,
                       c.umidade_solo, c.chuva_recente, c.observacoes,
                       c.producao_estimada_t, c.perda_real_t, c.perda_percentual,
                       c.classificacao, c.situacao_referencia,
                       c.diagnostico, c.recomendacao, c.prioridade_decisao,
                       t.nome AS nome_talhao, t.area_ha
                FROM colheitas c JOIN talhoes t ON c.id_talhao = t.id
                ORDER BY c.data_colheita DESC
            """)
        cols = [c[0].lower() for c in cursor.description]
        rows = []
        for row in cursor.fetchall():
            d = dict(zip(cols, row))
            d["chuva_recente"] = d.get("chuva_recente") == "S"
            # garante compatibilidade com sad_agro
            d["talhao"] = d.get("nome_talhao", "")
            rows.append(d)
        return rows
    finally:
        encerrar(conn)


# ─────────────────────────────────────────────
# EXIBIÇÃO
# ─────────────────────────────────────────────

def exibir_registro_completo(r: dict) -> None:
    print(f"\n  ID.......................: {r.get('id', '—')}")
    print(f"  Data.....................: {r.get('data_colheita', '—')}")
    print(f"  Fazenda..................: {r.get('fazenda', '—')}")
    print(f"  Talhão...................: {r.get('nome_talhao', r.get('talhao', '—'))}")
    print(f"  Tipo de colheita.........: {r.get('tipo_colheita', '—')}")
    print(f"  Área (ha)................: {float(r.get('area_ha') or 0):.2f}")
    print(f"  Prod. estimada t/ha......: {float(r.get('produtividade_estimada_t_ha') or 0):.2f}")
    print(f"  Produção colhida (t).....: {float(r.get('producao_colhida_t') or 0):.2f}")
    print(f"  Velocidade (km/h)........: {float(r.get('velocidade_colhedora_kmh') or 0):.2f}")
    print(f"  Altura corte (cm)........: {float(r.get('altura_corte_cm') or 0):.2f}")
    print(f"  Estado das facas.........: {r.get('estado_facas', '—')}")
    print(f"  Operador.................: {r.get('operador', '—')}")
    print(f"  Máquina..................: {r.get('maquina', '—')}")
    print(f"  Umidade do solo..........: {r.get('umidade_solo', '—')}")
    print(f"  Chuva recente............: {'Sim' if r.get('chuva_recente') else 'Não'}")
    print(f"  Observações..............: {r.get('observacoes', '—')}")
    if r.get("perda_percentual") is not None:
        print(f"  ── Análise ──")
        print(f"  Produção estimada (t)....: {float(r.get('producao_estimada_t') or 0):.2f}")
        print(f"  Perda real (t)...........: {float(r.get('perda_real_t') or 0):.2f}")
        print(f"  Perda percentual (%).....: {float(r.get('perda_percentual') or 0):.2f}%")
        print(f"  Eficiência...............: {r.get('classificacao', '—')}")
        print(f"  Situação ref. setor......: {r.get('situacao_referencia', '—')}")
    if r.get("diagnostico"):
        print(f"  ── Diagnóstico SAD ──")
        print(f"  Prioridade...............: {r.get('prioridade_decisao', '—').upper()}")
        print(f"  Diagnóstico..............: {r.get('diagnostico', '—')}")
        print(f"  Recomendação.............: {r.get('recomendacao', '—')}")
    print("  " + "─" * 60)


def exibir_colheitas_resumo(colheitas: list) -> None:
    if not colheitas:
        print("\n  Nenhuma colheita registrada.")
        return
    print("\n" + "─" * 95)
    print(f"  {'ID':<4} {'Talhão':<15} {'Data':<12} {'Tipo':<11} "
          f"{'Colhida(t)':<12} {'Perda%':<8} {'Efic.':<12} {'Prior.'}")
    print("─" * 95)
    for c in colheitas:
        print(
            f"  {str(c.get('id','')):<4} "
            f"{str(c.get('nome_talhao', c.get('talhao',''))):<15} "
            f"{str(c.get('data_colheita','')):<12} "
            f"{str(c.get('tipo_colheita','')):<11} "
            f"{float(c.get('producao_colhida_t') or 0):<12.1f} "
            f"{float(c.get('perda_percentual') or 0):<8.1f} "
            f"{str(c.get('classificacao','—')):<12} "
            f"{str(c.get('prioridade_decisao','—'))}"
        )
    print("─" * 95)


# ─────────────────────────────────────────────
# CADASTRO INTERATIVO
# ─────────────────────────────────────────────

def coletar_dados_colheita(id_talhao: int, talhao: dict) -> dict:
    """Coleta interativamente todos os dados de uma colheita."""
    print("\n--- Nova Colheita ---")
    data_col      = ler_data("  Data da colheita (DD/MM/AAAA): ")
    fazenda       = ler_texto("  Nome da fazenda: ", tamanho_min=3)
    tipo          = ler_tipo_colheita()
    prod_colhida  = ler_float("  Produção colhida real (t): ", minimo=0.1)
    prod_est_ha   = ler_float("  Produtividade estimada (t/ha): ", minimo=1.0)
    velocidade    = ler_float("  Velocidade da colhedora (km/h): ", minimo=0.0)
    altura_corte  = ler_float("  Altura de corte (cm): ", minimo=0.0)
    estado_facas  = ler_opcao("  Estado das facas", ESTADOS_FACAS)
    operador      = ler_texto("  Nome do operador: ", tamanho_min=3)
    maquina       = ler_texto("  Identificação da máquina: ", tamanho_min=2)
    umidade_solo  = ler_opcao("  Umidade do solo", UMIDADES_SOLO)
    chuva         = ler_booleano("  Houve chuva recente? (S/N): ")
    observacoes   = ler_texto("  Observações: ", tamanho_min=3, tamanho_max=500)

    registro = {
        "id_talhao":                  id_talhao,
        "data_colheita":              data_col,
        "fazenda":                    fazenda,
        "cultura":                    CULTURA_PADRAO,
        "tipo_colheita":              tipo,
        "area_ha":                    talhao["area_ha"],
        "producao_colhida_t":         prod_colhida,
        "produtividade_estimada_t_ha": prod_est_ha,
        "velocidade_colhedora_kmh":   velocidade,
        "altura_corte_cm":            altura_corte,
        "estado_facas":               estado_facas,
        "operador":                   operador,
        "maquina":                    maquina,
        "umidade_solo":               umidade_solo,
        "chuva_recente":              chuva,
        "observacoes":                observacoes,
        "talhao":                     talhao["nome"],
    }
    return registro


# ─────────────────────────────────────────────
# ANÁLISE E ESTATÍSTICAS
# ─────────────────────────────────────────────

def resumo_estatistico(colheitas: list) -> dict:
    if not colheitas:
        return {}
    n             = len(colheitas)
    total_prod    = sum(float(c.get("producao_colhida_t") or 0) for c in colheitas)
    total_est     = sum(float(c.get("producao_estimada_t") or 0) for c in colheitas)
    total_perda   = sum(float(c.get("perda_real_t") or 0) for c in colheitas)
    perdas_pct    = [float(c.get("perda_percentual") or 0) for c in colheitas]
    media_perda   = sum(perdas_pct) / n
    return {
        "total": n,
        "total_colhida_t": total_prod,
        "total_estimada_t": total_est,
        "total_perda_t": total_perda,
        "media_perda_pct": media_perda,
        "max_perda_pct": max(perdas_pct),
        "min_perda_pct": min(perdas_pct),
    }


def painel_decisao(colheitas: list) -> None:
    """Exibe painel ordenado por prioridade e perda percentual."""
    print("\n" + "═" * 75)
    print("  PAINEL DE DECISÃO — Registros ordenados por prioridade")
    print("═" * 75)
    if not colheitas:
        print("  Sem dados.")
        return
    ordem = {"alta": 0, "media": 1, "baixa": 2}
    ordenados = sorted(
        colheitas,
        key=lambda r: (
            ordem.get(str(r.get("prioridade_decisao") or "baixa"), 2),
            -(float(r.get("perda_percentual") or 0.0)),
        ),
    )
    print(f"  {'ID':<4} {'Talhão':<15} {'Tipo':<12} {'Perda%':<8} {'Prior.':<8} Diagnóstico")
    print("─" * 75)
    for r in ordenados:
        diag  = str(r.get("diagnostico") or "—")[:45]
        prio  = str(r.get("prioridade_decisao") or "—")
        perda = float(r.get("perda_percentual") or 0.0)
        nome  = str(r.get("nome_talhao", r.get("talhao", "—")))
        print(f"  {str(r.get('id','')):<4} {nome:<15} "
              f"{str(r.get('tipo_colheita','')):<12} {perda:<8.2f} {prio:<8} {diag}")
    print("═" * 75)


# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────

def menu_colheitas() -> None:
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║       COLHEITAS E ANÁLISE            ║")
        print("╠══════════════════════════════════════╣")
        print("║  1. Registrar colheita               ║")
        print("║  2. Listar todas (resumo)            ║")
        print("║  3. Colheitas por talhão             ║")
        print("║  4. Detalhe completo de uma colheita ║")
        print("║  5. Estatísticas globais             ║")
        print("║  6. Painel de decisão                ║")
        print("║  0. Voltar                           ║")
        print("╚══════════════════════════════════════╝")
        escolha = input("  Opção: ").strip()

        if escolha == "1":
            talhoes = listar_talhoes()
            if not talhoes:
                print("  ⚠ Cadastre um talhão antes.")
                continue
            exibir_talhoes(talhoes)
            id_t = ler_inteiro("  ID do talhão: ", minimo=1)
            talhao = buscar_talhao_por_id(id_t)
            if not talhao:
                print("  ⚠ Talhão não encontrado.")
                continue
            tabela_mem = listar_colheitas_bd(id_t)
            reg = coletar_dados_colheita(id_t, talhao)
            analisar_registro(reg)
            diagnosticar_registro(reg, tabela_mem)
            registrar_colheita_bd(id_t, reg)
            print(f"\n  Perda: {reg['perda_percentual']:.2f}%  →  {reg['classificacao'].upper()}")
            print(f"  Prioridade: {reg['prioridade_decisao'].upper()}")
            print(f"  Diagnóstico: {reg['diagnostico']}")

        elif escolha == "2":
            exibir_colheitas_resumo(listar_colheitas_bd())

        elif escolha == "3":
            exibir_talhoes(listar_talhoes())
            id_t = ler_inteiro("  ID do talhão: ", minimo=1)
            exibir_colheitas_resumo(listar_colheitas_bd(id_t))

        elif escolha == "4":
            todas = listar_colheitas_bd()
            exibir_colheitas_resumo(todas)
            id_c = ler_inteiro("  ID da colheita: ", minimo=1)
            match = [c for c in todas if c.get("id") == id_c]
            if match:
                exibir_registro_completo(match[0])
            else:
                print("  ⚠ Não encontrada.")

        elif escolha == "5":
            todas = listar_colheitas_bd()
            res = resumo_estatistico(todas)
            if not res:
                print("  Sem dados.")
            else:
                print(f"\n  Total de registros.......: {res['total']}")
                print(f"  Produção colhida total...: {res['total_colhida_t']:.2f} t")
                print(f"  Produção estimada total..: {res['total_estimada_t']:.2f} t")
                print(f"  Perda total..............: {res['total_perda_t']:.2f} t")
                print(f"  Média de perda...........: {res['media_perda_pct']:.2f}%")
                print(f"  Maior perda..............: {res['max_perda_pct']:.2f}%")
                print(f"  Menor perda..............: {res['min_perda_pct']:.2f}%")

        elif escolha == "6":
            painel_decisao(listar_colheitas_bd())

        elif escolha == "0":
            break
        else:
            print("  ⚠ Opção inválida.")
