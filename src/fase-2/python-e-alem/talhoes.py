"""
talhoes.py — CRUD de talhões (áreas de plantio).
Estrutura: dicionário por talhão, lista como tabela de memória.
"""

from banco import conectar, encerrar
from validacao import ler_texto, ler_float, ler_data, ler_inteiro


def cadastrar_talhao(nome: str, area_ha: float, variedade: str, data_plantio: str) -> dict:
    """Insere talhão no Oracle e retorna dicionário com os dados."""
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO talhoes (nome, area_ha, variedade, data_plantio)
            VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))
        """, (nome, area_ha, variedade, data_plantio))
        conn.commit()
        cursor.execute("SELECT MAX(id) FROM talhoes WHERE nome = :1", (nome,))
        id_gerado = cursor.fetchone()[0]
        talhao = {"id": id_gerado, "nome": nome, "area_ha": area_ha,
                  "variedade": variedade, "data_plantio": data_plantio}
        print(f"\n  ✅ Talhão '{nome}' cadastrado com ID {id_gerado}.")
        return talhao
    except Exception as e:
        if "ORA-00001" in str(e):
            print(f"\n  ⚠ Talhão '{nome}' já existe.")
        else:
            print(f"\n  ❌ Erro: {e}")
        return None
    finally:
        encerrar(conn)


def listar_talhoes() -> list:
    """Retorna lista de dicionários com todos os talhões (tabela de memória)."""
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, area_ha, variedade,
                   TO_CHAR(data_plantio, 'YYYY-MM-DD') AS data_plantio
            FROM talhoes ORDER BY nome
        """)
        cols = [c[0].lower() for c in cursor.description]
        return [dict(zip(cols, row)) for row in cursor.fetchall()]
    finally:
        encerrar(conn)


def buscar_talhao_por_id(id_talhao: int) -> dict:
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nome, area_ha, variedade,
                   TO_CHAR(data_plantio, 'YYYY-MM-DD') AS data_plantio
            FROM talhoes WHERE id = :1
        """, (id_talhao,))
        cols = [c[0].lower() for c in cursor.description]
        row  = cursor.fetchone()
        return dict(zip(cols, row)) if row else None
    finally:
        encerrar(conn)


def excluir_talhao(id_talhao: int) -> bool:
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM colheitas WHERE id_talhao = :1", (id_talhao,))
        if cursor.fetchone()[0] > 0:
            print("  ⚠ Não é possível excluir: existem colheitas vinculadas.")
            return False
        cursor.execute("DELETE FROM talhoes WHERE id = :1", (id_talhao,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        encerrar(conn)


def exibir_talhoes(talhoes: list) -> None:
    if not talhoes:
        print("\n  Nenhum talhão cadastrado.")
        return
    print("\n" + "─" * 65)
    print(f"  {'ID':<4} {'Nome':<20} {'Área (ha)':<12} {'Variedade':<15} {'Plantio'}")
    print("─" * 65)
    for t in talhoes:
        print(f"  {t['id']:<4} {t['nome']:<20} {t['area_ha']:<12.2f} "
              f"{t['variedade']:<15} {t['data_plantio']}")
    print("─" * 65)


def menu_talhoes() -> None:
    while True:
        print("\n╔══════════════════════════════╗")
        print("║      GESTÃO DE TALHÕES       ║")
        print("╠══════════════════════════════╣")
        print("║  1. Cadastrar talhão         ║")
        print("║  2. Listar talhões           ║")
        print("║  3. Excluir talhão           ║")
        print("║  0. Voltar                   ║")
        print("╚══════════════════════════════╝")
        escolha = input("  Opção: ").strip()

        if escolha == "1":
            print("\n--- Novo Talhão ---")
            nome         = ler_texto("  Nome do talhão: ", tamanho_max=50)
            area_ha      = ler_float("  Área (hectares): ", minimo=0.1, maximo=50000)
            variedade    = ler_texto("  Variedade da cana: ", tamanho_max=30)
            data_plantio = ler_data("  Data de plantio (DD/MM/AAAA): ")
            cadastrar_talhao(nome, area_ha, variedade, data_plantio)
        elif escolha == "2":
            exibir_talhoes(listar_talhoes())
        elif escolha == "3":
            exibir_talhoes(listar_talhoes())
            id_del = input("\n  ID do talhão a excluir (0 cancelar): ").strip()
            if id_del != "0":
                try:
                    ok = excluir_talhao(int(id_del))
                    print("  ✅ Excluído." if ok else "  ⚠ Não encontrado.")
                except ValueError:
                    print("  ⚠ ID inválido.")
        elif escolha == "0":
            break
        else:
            print("  ⚠ Opção inválida.")
