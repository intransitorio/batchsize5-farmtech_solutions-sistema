try:
    import oracledb
except ModuleNotFoundError:
    oracledb = None

try:
    import pandas as pd
except ModuleNotFoundError:
    pd = None

from config import (
    ORACLE_HOST,
    ORACLE_PORT,
    ORACLE_SERVICE_NAME,
    ORACLE_USER,
    ORACLE_PASSWORD,
)


def conectar():
    if oracledb is None:
        raise ModuleNotFoundError(
            "A biblioteca 'oracledb' não está instalada. "
            "Execute: pip install -r requirements.txt"
        )

    dsn = oracledb.makedsn(
        host=ORACLE_HOST,
        port=ORACLE_PORT,
        service_name=ORACLE_SERVICE_NAME,
    )
    return oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=dsn)


def criar_tabela() -> tuple[bool, str]:
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            BEGIN
                EXECUTE IMMEDIATE '
                    CREATE TABLE COLHEITAS_AGRO (
                        ID NUMBER PRIMARY KEY,
                        TALHAO VARCHAR2(100) NOT NULL,
                        CULTURA VARCHAR2(50) NOT NULL,
                        BASE_M NUMBER(10,2) NOT NULL,
                        ALTURA_M NUMBER(10,2) NOT NULL,
                        AREA_M2 NUMBER(12,2) NOT NULL,
                        PRODUCAO_PREVISTA_T NUMBER(12,2) NOT NULL,
                        PRODUCAO_REAL_T NUMBER(12,2) NOT NULL,
                        PRODUTIVIDADE_T_M2 NUMBER(12,6) NOT NULL,
                        PERDA_PERCENTUAL NUMBER(6,2) NOT NULL,
                        CLASSIFICACAO_PERDA VARCHAR2(20) NOT NULL,
                        DATA_CADASTRO DATE DEFAULT SYSDATE
                    )
                ';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE = -955 THEN
                        NULL;
                    ELSE
                        RAISE;
                    END IF;
            END;
            """
        )

        conn.commit()
        return True, "Tabela COLHEITAS_AGRO criada ou já existente."
    except Exception as erro:
        return False, f"Erro ao criar tabela: {erro}"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def inserir_colheita(registro: dict) -> tuple[bool, str]:
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO COLHEITAS_AGRO (
                ID, TALHAO, CULTURA, BASE_M, ALTURA_M, AREA_M2,
                PRODUCAO_PREVISTA_T, PRODUCAO_REAL_T, PRODUTIVIDADE_T_M2,
                PERDA_PERCENTUAL, CLASSIFICACAO_PERDA
            ) VALUES (
                :id, :talhao, :cultura, :base_m, :altura_m, :area_m2,
                :producao_prevista_t, :producao_real_t, :produtividade_t_m2,
                :perda_percentual, :classificacao_perda
            )
            """,
            registro,
        )

        conn.commit()
        return True, "Registro salvo no Oracle com sucesso."
    except Exception as erro:
        return False, f"Erro ao inserir registro: {erro}"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def listar_colheitas():
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                ID,
                TALHAO,
                CULTURA,
                BASE_M,
                ALTURA_M,
                AREA_M2,
                PRODUCAO_PREVISTA_T,
                PRODUCAO_REAL_T,
                PRODUTIVIDADE_T_M2,
                PERDA_PERCENTUAL,
                CLASSIFICACAO_PERDA,
                DATA_CADASTRO
            FROM COLHEITAS_AGRO
            ORDER BY ID
            """
        )

        linhas = cursor.fetchall()
        colunas = [col[0].lower() for col in cursor.description]

        if pd is None:
            raise ModuleNotFoundError(
                "A biblioteca 'pandas' não está instalada. "
                "Execute: pip install -r requirements.txt"
            )

        df = pd.DataFrame(linhas, columns=colunas)
        return True, "Consulta realizada com sucesso.", df
    except Exception as erro:
        return False, f"Erro ao listar registros: {erro}", None
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def atualizar_colheita(registro: dict) -> tuple[bool, str]:
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE COLHEITAS_AGRO
               SET TALHAO = :talhao,
                   CULTURA = :cultura,
                   BASE_M = :base_m,
                   ALTURA_M = :altura_m,
                   AREA_M2 = :area_m2,
                   PRODUCAO_PREVISTA_T = :producao_prevista_t,
                   PRODUCAO_REAL_T = :producao_real_t,
                   PRODUTIVIDADE_T_M2 = :produtividade_t_m2,
                   PERDA_PERCENTUAL = :perda_percentual,
                   CLASSIFICACAO_PERDA = :classificacao_perda
             WHERE ID = :id
            """,
            registro,
        )

        if cursor.rowcount == 0:
            return False, "Nenhum registro encontrado com esse ID."

        conn.commit()
        return True, "Registro alterado com sucesso."
    except Exception as erro:
        return False, f"Erro ao alterar registro: {erro}"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def excluir_colheita(id_registro: int) -> tuple[bool, str]:
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM COLHEITAS_AGRO WHERE ID = :id", {"id": id_registro})

        if cursor.rowcount == 0:
            return False, "Nenhum registro encontrado com esse ID."

        conn.commit()
        return True, "Registro excluído com sucesso."
    except Exception as erro:
        return False, f"Erro ao excluir registro: {erro}"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


def excluir_todas_colheitas() -> tuple[bool, str]:
    conn = None
    cursor = None

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM COLHEITAS_AGRO")
        conn.commit()

        return True, "Todos os registros foram excluídos com sucesso."
    except Exception as erro:
        return False, f"Erro ao excluir todos os registros: {erro}"
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()