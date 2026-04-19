"""
banco.py — Conexão com Oracle Database via oracledb (FIAP).
Solicita as credenciais ao usuário na inicialização do sistema.
"""

import oracledb as cx_Oracle

DB_HOST = "oracle.fiap.com.br"
DB_PORT = 1521
DB_SID  = "ORCL"

# Credenciais preenchidas em tempo de execução
_credenciais = {"usuario": "", "senha": ""}


def solicitar_credenciais() -> None:
    """Pede usuário e senha Oracle uma única vez ao iniciar o sistema."""
    print("\n" + "═" * 50)
    print("  CONEXÃO COM BANCO DE DADOS ORACLE — FIAP")
    print("═" * 50)
    _credenciais["usuario"] = input("  Usuário Oracle (ex: rmXXXXXX): ").strip()
    _credenciais["senha"]   = input("  Senha Oracle: ").strip()
    print("═" * 50)


def conectar():
    """Retorna uma conexão ativa com o Oracle."""
    dsn = cx_Oracle.makedsn(DB_HOST, DB_PORT, sid=DB_SID)
    return cx_Oracle.connect(
        user=_credenciais["usuario"],
        password=_credenciais["senha"],
        dsn=dsn
    )


def inicializar_banco() -> None:
    """Solicita credenciais, testa conexão e cria tabelas se necessário."""
    solicitar_credenciais()

    # Testa a conexão antes de prosseguir
    try:
        conn = conectar()
    except Exception as e:
        print(f"\n  ❌ Falha na conexão: {e}")
        print("  Verifique usuário e senha e tente novamente.")
        raise SystemExit(1)

    cursor = conn.cursor()

    cursor.execute("""
        BEGIN
            EXECUTE IMMEDIATE '
                CREATE TABLE talhoes (
                    id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    nome          VARCHAR2(50)   NOT NULL UNIQUE,
                    area_ha       NUMBER(10,2)   NOT NULL,
                    variedade     VARCHAR2(30)   NOT NULL,
                    data_plantio  DATE           NOT NULL
                )
            ';
        EXCEPTION WHEN OTHERS THEN
            IF SQLCODE != -955 THEN RAISE; END IF;
        END;
    """)

    cursor.execute("""
        BEGIN
            EXECUTE IMMEDIATE '
                CREATE TABLE colheitas (
                    id                          NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    id_talhao                   NUMBER          NOT NULL,
                    data_colheita               VARCHAR2(10)    NOT NULL,
                    fazenda                     VARCHAR2(100)   NOT NULL,
                    cultura                     VARCHAR2(50)    DEFAULT ''Cana-de-acucar'',
                    tipo_colheita               VARCHAR2(11)    NOT NULL,
                    producao_colhida_t          NUMBER(12,2)    NOT NULL,
                    produtividade_estimada_t_ha NUMBER(10,2)    NOT NULL,
                    velocidade_colhedora_kmh    NUMBER(10,2)    NOT NULL,
                    altura_corte_cm             NUMBER(10,2)    NOT NULL,
                    estado_facas                VARCHAR2(20)    NOT NULL,
                    operador                    VARCHAR2(100)   NOT NULL,
                    maquina                     VARCHAR2(50)    NOT NULL,
                    umidade_solo                VARCHAR2(20)    NOT NULL,
                    chuva_recente               CHAR(1)         NOT NULL,
                    observacoes                 VARCHAR2(500),
                    producao_estimada_t         NUMBER(12,2),
                    perda_real_t                NUMBER(12,2),
                    perda_percentual            NUMBER(10,2),
                    classificacao               VARCHAR2(20),
                    situacao_referencia         VARCHAR2(40),
                    diagnostico                 VARCHAR2(2000),
                    recomendacao                VARCHAR2(2000),
                    prioridade_decisao          VARCHAR2(20),
                    CONSTRAINT fk_talhao FOREIGN KEY (id_talhao) REFERENCES talhoes(id)
                )
            ';
        EXCEPTION WHEN OTHERS THEN
            IF SQLCODE != -955 THEN RAISE; END IF;
        END;
    """)

    conn.commit()
    encerrar(conn)
    print("\n  ✅ Banco Oracle conectado e inicializado com sucesso!")


def encerrar(conn) -> None:
    """Fecha a conexão com o banco."""
    if conn:
        conn.close()
