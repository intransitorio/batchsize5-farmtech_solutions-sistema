"""
main.py
Ponto de entrada da ETAPA 8 do Sistema de Apoio à Decisão para Colheita de Cana-de-Açúcar.

Escopo final:
- cadastro validado de talhões e colheitas
- análises de perdas e eficiência
- persistência em JSON e exportação em TXT
- integração opcional com Oracle
- apoio à decisão com regras automatizadas
"""

from __future__ import annotations

import json
from typing import Any

from analise import (
    analisar_colheita_por_id_cli,
    analisar_talhao_cli,
    comparar_modos_cli,
    exibir_resumo_geral_cli,
)
from cadastro import (
    buscar_colheita_por_id,
    buscar_talhao_por_id,
    cadastrar_talhao_memoria,
    calcular_meses_desde_plantio,
    calcular_perda_toneladas,
    consultar_colheitas_por_talhao_memoria,
    consultar_talhao_memoria,
    listar_colheitas_memoria,
    listar_talhoes_memoria,
    registrar_colheita_memoria,
)
from decisao import diagnosticar_colheita_cli, diagnosticar_talhao_cli
from oracle_db import (
    atualizar_colheita,
    atualizar_talhao,
    carregar_oracle_para_memoria,
    conectar_oracle,
    criar_tabelas,
    driver_disponivel,
    excluir_colheita,
    excluir_talhao,
    fechar_conexao,
    listar_colheitas_db,
    listar_talhoes_db,
    sincronizar_memoria_para_oracle,
)
from persistencia import (
    ARQUIVO_JSON_PADRAO,
    ARQUIVO_TXT_PADRAO,
    carregar_dados_json,
    exportar_historico_txt,
    salvar_dados_json,
)
from validacao import ler_data, ler_float, ler_inteiro, ler_opcao, ler_texto

Dados = dict[str, list[dict[str, Any]]]
EstadoOracle = dict[str, Any]


def exibir_cabecalho() -> None:
    """Exibe o cabeçalho principal da aplicação."""
    print(
        """
╔══════════════════════════════════════════════════════════════╗
║   Sistema de Apoio à Decisão para Colheita de Cana-de-Açúcar║
║                 ETAPA 8 — Versão final CLI                  ║
╚══════════════════════════════════════════════════════════════╝
        """
    )


def _dados_vazios() -> Dados:
    """Cria a estrutura vazia padrão do sistema."""
    return {"talhoes": [], "colheitas": []}


def _oracle_conectado(estado_oracle: EstadoOracle) -> bool:
    """Verifica se há conexão Oracle ativa."""
    return estado_oracle.get("conexao") is not None


# -----------------------------------------------------------------------------
# Persistência local
# -----------------------------------------------------------------------------

def salvar_dados_cli(dados: Dados) -> None:
    """Salva os dados atuais em JSON."""
    nome_arquivo = input(
        f"  Nome do arquivo JSON [Enter = {ARQUIVO_JSON_PADRAO}]: "
    ).strip() or ARQUIVO_JSON_PADRAO

    try:
        caminho = salvar_dados_json(dados, nome_arquivo)
        print(f"\n  ✅ Dados salvos com sucesso em: {caminho}")
    except OSError as erro:
        print(f"\n  ⚠ Falha ao salvar JSON: {erro}")



def carregar_dados_cli(dados: Dados) -> None:
    """Carrega dados de um JSON para a memória."""
    nome_arquivo = input(
        f"  Nome do arquivo JSON para leitura [Enter = {ARQUIVO_JSON_PADRAO}]: "
    ).strip() or ARQUIVO_JSON_PADRAO

    try:
        dados_lidos = carregar_dados_json(nome_arquivo)
        dados["talhoes"] = dados_lidos["talhoes"]
        dados["colheitas"] = dados_lidos["colheitas"]
        print(
            f"\n  ✅ Dados carregados com sucesso. Talhões: {len(dados['talhoes'])} | "
            f"Colheitas: {len(dados['colheitas'])}"
        )
    except FileNotFoundError:
        print("\n  ⚠ Arquivo não encontrado.")
    except json.JSONDecodeError:
        print("\n  ⚠ O arquivo informado não contém um JSON válido.")
    except OSError as erro:
        print(f"\n  ⚠ Falha ao carregar JSON: {erro}")



def exportar_historico_cli(dados: Dados) -> None:
    """Exporta o histórico consolidado em TXT."""
    nome_arquivo = input(
        f"  Nome do arquivo TXT [Enter = {ARQUIVO_TXT_PADRAO}]: "
    ).strip() or ARQUIVO_TXT_PADRAO

    try:
        caminho = exportar_historico_txt(dados, nome_arquivo)
        print(f"\n  ✅ Histórico exportado com sucesso em: {caminho}")
    except OSError as erro:
        print(f"\n  ⚠ Falha ao exportar TXT: {erro}")


# -----------------------------------------------------------------------------
# Oracle CLI
# -----------------------------------------------------------------------------

def conectar_oracle_cli(estado_oracle: EstadoOracle) -> None:
    """Solicita credenciais e tenta abrir conexão com Oracle."""
    if not driver_disponivel():
        print("\n  ⚠ O driver 'oracledb' não está instalado neste ambiente.")
        print("  Para instalar: pip install oracledb")
        print("  O restante do sistema funciona normalmente sem o Oracle.")
        return

    usuario = ler_texto("  Usuário Oracle: ", tamanho_max=50)
    senha = input("  Senha Oracle: ").strip()
    dsn = ler_texto("  DSN (host:porta/serviço): ", tamanho_max=120)

    try:
        if _oracle_conectado(estado_oracle):
            fechar_conexao(estado_oracle["conexao"])

        conexao = conectar_oracle(usuario, senha, dsn)
        estado_oracle["conexao"] = conexao
        estado_oracle["usuario"] = usuario
        estado_oracle["dsn"] = dsn
        print("\n  ✅ Conexão Oracle estabelecida com sucesso.")
    except Exception as erro:
        estado_oracle["conexao"] = None
        print(f"\n  ⚠ Falha ao conectar no Oracle: {erro}")



def criar_tabelas_cli(estado_oracle: EstadoOracle) -> None:
    """Cria as tabelas do projeto no Oracle."""
    if not _oracle_conectado(estado_oracle):
        print("\n  ⚠ Conecte-se ao Oracle antes de criar as tabelas.")
        return

    try:
        mensagens = criar_tabelas(estado_oracle["conexao"])
        print()
        for mensagem in mensagens:
            print(f"  ✅ {mensagem}")
    except Exception as erro:
        print(f"\n  ⚠ Falha ao criar tabelas: {erro}")



def sincronizar_memoria_para_oracle_cli(estado_oracle: EstadoOracle, dados: Dados) -> None:
    """Envia registros da memória para o Oracle."""
    if not _oracle_conectado(estado_oracle):
        print("\n  ⚠ Conecte-se ao Oracle antes de sincronizar dados.")
        return

    try:
        resultado = sincronizar_memoria_para_oracle(
            estado_oracle["conexao"], dados["talhoes"], dados["colheitas"]
        )
        print("\n  ✅ Sincronização concluída.")
        print(f"     Talhões inseridos  : {resultado['talhoes_inseridos']}")
        print(f"     Colheitas inseridas: {resultado['colheitas_inseridas']}")
    except Exception as erro:
        print(f"\n  ⚠ Falha na sincronização: {erro}")



def listar_talhoes_oracle_cli(estado_oracle: EstadoOracle) -> None:
    """Lista talhões diretamente do Oracle."""
    if not _oracle_conectado(estado_oracle):
        print("\n  ⚠ Conecte-se ao Oracle antes de consultar.")
        return

    try:
        listar_talhoes_memoria(listar_talhoes_db(estado_oracle["conexao"]))
    except Exception as erro:
        print(f"\n  ⚠ Falha ao listar talhões do Oracle: {erro}")



def listar_colheitas_oracle_cli(estado_oracle: EstadoOracle) -> None:
    """Lista colheitas diretamente do Oracle."""
    if not _oracle_conectado(estado_oracle):
        print("\n  ⚠ Conecte-se ao Oracle antes de consultar.")
        return

    try:
        listar_colheitas_memoria(listar_colheitas_db(estado_oracle["conexao"]))
    except Exception as erro:
        print(f"\n  ⚠ Falha ao listar colheitas do Oracle: {erro}")



def carregar_oracle_para_memoria_cli(estado_oracle: EstadoOracle, dados: Dados) -> None:
    """Substitui a memória local pelo conteúdo atual do Oracle."""
    if not _oracle_conectado(estado_oracle):
        print("\n  ⚠ Conecte-se ao Oracle antes de carregar dados.")
        return

    try:
        dados_db = carregar_oracle_para_memoria(estado_oracle["conexao"])
        dados["talhoes"] = dados_db["talhoes"]
        dados["colheitas"] = dados_db["colheitas"]
        print(
            f"\n  ✅ Dados carregados do Oracle para memória. Talhões: {len(dados['talhoes'])} | "
            f"Colheitas: {len(dados['colheitas'])}"
        )
    except Exception as erro:
        print(f"\n  ⚠ Falha ao carregar dados do Oracle: {erro}")



def atualizar_talhao_oracle_cli(estado_oracle: EstadoOracle) -> None:
    """Atualiza um talhão diretamente no Oracle."""
    if not _oracle_conectado(estado_oracle):
        print("\n  ⚠ Conecte-se ao Oracle antes de atualizar.")
        return

    try:
        registros = listar_talhoes_db(estado_oracle["conexao"])
        listar_talhoes_memoria(registros)
        if not registros:
            return

        id_talhao = ler_inteiro("  ID do talhão para atualização: ", minimo=1)
        talhao = buscar_talhao_por_id(registros, id_talhao)
        if not talhao:
            print("  ⚠ Talhão não encontrado no Oracle.")
            return

        print("  Informe os novos dados do talhão:")
        nome = ler_texto("  Novo nome: ", tamanho_max=50)
        area_ha = ler_float("  Nova área (ha): ", minimo=0.1, maximo=50000)
        variedade = ler_texto("  Nova variedade: ", tamanho_max=30)
        data_plantio = ler_data("  Nova data de plantio (DD/MM/AAAA): ")

        atualizado = atualizar_talhao(
            estado_oracle["conexao"], id_talhao, nome, area_ha, variedade, data_plantio
        )
        print(
            "\n  ✅ Talhão atualizado com sucesso no Oracle."
            if atualizado
            else "\n  ⚠ Nenhum talhão foi atualizado."
        )
    except Exception as erro:
        print(f"\n  ⚠ Falha ao atualizar talhão no Oracle: {erro}")



def excluir_talhao_oracle_cli(estado_oracle: EstadoOracle) -> None:
    """Exclui um talhão diretamente no Oracle."""
    if not _oracle_conectado(estado_oracle):
        print("\n  ⚠ Conecte-se ao Oracle antes de excluir.")
        return

    try:
        registros = listar_talhoes_db(estado_oracle["conexao"])
        listar_talhoes_memoria(registros)
        if not registros:
            return

        id_talhao = ler_inteiro("  ID do talhão para exclusão: ", minimo=1)
        confirmacao = ler_opcao("  Confirma exclusão do talhão", ("sim", "nao"))
        if confirmacao != "sim":
            print("  Operação cancelada.")
            return

        excluido = excluir_talhao(estado_oracle["conexao"], id_talhao)
        print(
            "\n  ✅ Talhão excluído com sucesso no Oracle."
            if excluido
            else "\n  ⚠ Talhão não encontrado para exclusão."
        )
    except Exception as erro:
        print(f"\n  ⚠ Falha ao excluir talhão no Oracle: {erro}")



def atualizar_colheita_oracle_cli(estado_oracle: EstadoOracle) -> None:
    """Atualiza uma colheita diretamente no Oracle."""
    if not _oracle_conectado(estado_oracle):
        print("\n  ⚠ Conecte-se ao Oracle antes de atualizar.")
        return

    try:
        talhoes_db = listar_talhoes_db(estado_oracle["conexao"])
        colheitas_db = listar_colheitas_db(estado_oracle["conexao"])
        listar_colheitas_memoria(colheitas_db)
        if not colheitas_db:
            return

        id_colheita = ler_inteiro("  ID da colheita para atualização: ", minimo=1)
        colheita = buscar_colheita_por_id(colheitas_db, id_colheita)
        if not colheita:
            print("  ⚠ Colheita não encontrada no Oracle.")
            return

        talhao = buscar_talhao_por_id(talhoes_db, colheita["id_talhao"])
        if not talhao:
            print("  ⚠ Talhão associado não encontrado. Atualização cancelada.")
            return

        print("  Informe os novos dados da colheita:")
        data_colheita = ler_data("  Nova data da colheita (DD/MM/AAAA): ")
        modo = ler_opcao("  Novo modo de colheita", ("manual", "mecanizada"))
        producao_ton = ler_float("  Nova produção total (toneladas): ", minimo=0.1)
        perda_percentual = ler_float("  Nova perda estimada (%): ", minimo=0.0, maximo=100.0)
        umidade_pct = ler_float("  Nova umidade da cana (%): ", minimo=0.0, maximo=100.0)
        brix = ler_float("  Novo teor de sacarose - Brix (°): ", minimo=0.0, maximo=30.0)

        perda_toneladas = calcular_perda_toneladas(producao_ton, perda_percentual)
        meses_plantio = calcular_meses_desde_plantio(talhao["data_plantio"], data_colheita)

        atualizado = atualizar_colheita(
            estado_oracle["conexao"],
            id_colheita,
            data_colheita,
            modo,
            producao_ton,
            perda_percentual,
            perda_toneladas,
            umidade_pct,
            brix,
            meses_plantio,
        )
        print(
            "\n  ✅ Colheita atualizada com sucesso no Oracle."
            if atualizado
            else "\n  ⚠ Nenhuma colheita foi atualizada."
        )
    except Exception as erro:
        print(f"\n  ⚠ Falha ao atualizar colheita no Oracle: {erro}")



def excluir_colheita_oracle_cli(estado_oracle: EstadoOracle) -> None:
    """Exclui uma colheita diretamente no Oracle."""
    if not _oracle_conectado(estado_oracle):
        print("\n  ⚠ Conecte-se ao Oracle antes de excluir.")
        return

    try:
        colheitas_db = listar_colheitas_db(estado_oracle["conexao"])
        listar_colheitas_memoria(colheitas_db)
        if not colheitas_db:
            return

        id_colheita = ler_inteiro("  ID da colheita para exclusão: ", minimo=1)
        confirmacao = ler_opcao("  Confirma exclusão da colheita", ("sim", "nao"))
        if confirmacao != "sim":
            print("  Operação cancelada.")
            return

        excluido = excluir_colheita(estado_oracle["conexao"], id_colheita)
        print(
            "\n  ✅ Colheita excluída com sucesso no Oracle."
            if excluido
            else "\n  ⚠ Colheita não encontrada para exclusão."
        )
    except Exception as erro:
        print(f"\n  ⚠ Falha ao excluir colheita no Oracle: {erro}")



def submenu_oracle(estado_oracle: EstadoOracle, dados: Dados) -> None:
    """Exibe o submenu de operações Oracle."""
    while True:
        status = "conectado" if _oracle_conectado(estado_oracle) else "desconectado"
        print("\n╔═══════════════════════════════════════════════╗")
        print("║                 MENU ORACLE                  ║")
        print("╠═══════════════════════════════════════════════╣")
        print(f"║ Status: {status:<37}║")
        print("║  1. Conectar ao Oracle                       ║")
        print("║  2. Criar tabelas                            ║")
        print("║  3. Sincronizar memória -> Oracle            ║")
        print("║  4. Listar talhões do Oracle                 ║")
        print("║  5. Listar colheitas do Oracle               ║")
        print("║  6. Carregar Oracle -> memória               ║")
        print("║  7. Atualizar talhão no Oracle               ║")
        print("║  8. Excluir talhão no Oracle                 ║")
        print("║  9. Atualizar colheita no Oracle             ║")
        print("║ 10. Excluir colheita no Oracle               ║")
        print("║  0. Voltar                                   ║")
        print("╚═══════════════════════════════════════════════╝")

        escolha = input("  Opção Oracle: ").strip()
        if escolha == "1":
            conectar_oracle_cli(estado_oracle)
        elif escolha == "2":
            criar_tabelas_cli(estado_oracle)
        elif escolha == "3":
            sincronizar_memoria_para_oracle_cli(estado_oracle, dados)
        elif escolha == "4":
            listar_talhoes_oracle_cli(estado_oracle)
        elif escolha == "5":
            listar_colheitas_oracle_cli(estado_oracle)
        elif escolha == "6":
            carregar_oracle_para_memoria_cli(estado_oracle, dados)
        elif escolha == "7":
            atualizar_talhao_oracle_cli(estado_oracle)
        elif escolha == "8":
            excluir_talhao_oracle_cli(estado_oracle)
        elif escolha == "9":
            atualizar_colheita_oracle_cli(estado_oracle)
        elif escolha == "10":
            excluir_colheita_oracle_cli(estado_oracle)
        elif escolha == "0":
            break
        else:
            print("  ⚠ Opção inválida. Tente novamente.")



def menu_principal() -> None:
    """Controla o fluxo principal da aplicação."""
    dados = _dados_vazios()
    estado_oracle: EstadoOracle = {"conexao": None, "usuario": None, "dsn": None}

    try:
        while True:
            print("\n╔═══════════════════════════════════════════════╗")
            print("║                MENU PRINCIPAL                 ║")
            print("╠═══════════════════════════════════════════════╣")
            print("║  1. Cadastrar talhão                          ║")
            print("║  2. Listar talhões                            ║")
            print("║  3. Consultar talhão por ID                   ║")
            print("║  4. Registrar colheita                        ║")
            print("║  5. Listar todas as colheitas                 ║")
            print("║  6. Listar colheitas por talhão               ║")
            print("║  7. Analisar colheita por ID                  ║")
            print("║  8. Analisar desempenho de um talhão          ║")
            print("║  9. Comparar manual vs. mecanizada            ║")
            print("║ 10. Exibir resumo geral de indicadores        ║")
            print("║ 11. Salvar dados em JSON                      ║")
            print("║ 12. Carregar dados de JSON                    ║")
            print("║ 13. Exportar histórico em TXT                 ║")
            print("║ 14. Diagnóstico de decisão por colheita       ║")
            print("║ 15. Diagnóstico de decisão por talhão         ║")
            print("║ 16. Menu Oracle                               ║")
            print("║  0. Sair                                      ║")
            print("╚═══════════════════════════════════════════════╝")

            escolha = input("  Opção: ").strip()
            if escolha == "1":
                cadastrar_talhao_memoria(dados["talhoes"])
            elif escolha == "2":
                listar_talhoes_memoria(dados["talhoes"])
            elif escolha == "3":
                consultar_talhao_memoria(dados["talhoes"])
            elif escolha == "4":
                registrar_colheita_memoria(dados["talhoes"], dados["colheitas"])
            elif escolha == "5":
                listar_colheitas_memoria(dados["colheitas"])
            elif escolha == "6":
                consultar_colheitas_por_talhao_memoria(
                    dados["talhoes"], dados["colheitas"]
                )
            elif escolha == "7":
                analisar_colheita_por_id_cli(dados["colheitas"])
            elif escolha == "8":
                analisar_talhao_cli(dados["talhoes"], dados["colheitas"])
            elif escolha == "9":
                comparar_modos_cli(dados["colheitas"])
            elif escolha == "10":
                exibir_resumo_geral_cli(dados["colheitas"])
            elif escolha == "11":
                salvar_dados_cli(dados)
            elif escolha == "12":
                carregar_dados_cli(dados)
            elif escolha == "13":
                exportar_historico_cli(dados)
            elif escolha == "14":
                diagnosticar_colheita_cli(dados["colheitas"])
            elif escolha == "15":
                diagnosticar_talhao_cli(dados["talhoes"], dados["colheitas"])
            elif escolha == "16":
                submenu_oracle(estado_oracle, dados)
            elif escolha == "0":
                print("\n  Encerrando a aplicação final.\n")
                break
            else:
                print("  ⚠ Opção inválida. Tente novamente.")
    finally:
        if _oracle_conectado(estado_oracle):
            fechar_conexao(estado_oracle["conexao"])


if __name__ == "__main__":
    exibir_cabecalho()
    menu_principal()
