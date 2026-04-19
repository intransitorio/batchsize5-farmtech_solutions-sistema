from pathlib import Path

from arquivos import exportar_json, gerar_relatorio_txt
from banco_oracle import (
    atualizar_colheita,
    criar_tabela,
    excluir_colheita,
    excluir_todas_colheitas,
    inserir_colheita,
    listar_colheitas,
)
from funcoes import (
    buscar_registro_por_id,
    exibir_menu,
    exibir_registro,
    ler_int_positivo,
    montar_registro,
)

BASE_DIR = Path(__file__).resolve().parent
DADOS_DIR = BASE_DIR / "dados"

registros_memoria: list[dict] = []


def cadastrar_em_memoria() -> None:
    try:
        registro = montar_registro()

        if buscar_registro_por_id(registros_memoria, registro["id"]):
            print("ERRO! Já existe um registro com esse ID na memória.")
            return

        registros_memoria.append(registro)
        print("Registro cadastrado em memória com sucesso.")
    except Exception as erro:
        print(f"Falha inesperada no cadastro em memória: {erro}")
    finally:
        print("Operação de cadastro em memória finalizada.")


def listar_memoria() -> None:
    if not registros_memoria:
        print("Nenhum registro cadastrado em memória.")
        return

    print("\nLISTAGEM DE REGISTROS EM MEMÓRIA")
    for registro in registros_memoria:
        exibir_registro(registro)


def salvar_no_oracle() -> None:
    if not registros_memoria:
        print("Não há registros em memória para enviar ao Oracle.")
        return

    id_registro = ler_int_positivo("Informe o ID do registro da memória que deseja salvar: ")
    registro = buscar_registro_por_id(registros_memoria, id_registro)

    if registro is None:
        print("Registro não encontrado em memória.")
        return

    sucesso, mensagem = inserir_colheita(registro)
    print(mensagem)


def listar_oracle() -> None:
    sucesso, mensagem, df = listar_colheitas()
    print(mensagem)

    if sucesso and df is not None:
        if df.empty:
            print("Nenhum registro encontrado no Oracle.")
        else:
            print("\nREGISTROS DO ORACLE")
            print(df.to_string(index=False))


def alterar_no_oracle() -> None:
    id_registro = ler_int_positivo("Informe o ID do registro que deseja alterar no Oracle: ")

    try:
        novo_registro = montar_registro(id_fixo=id_registro)
        sucesso, mensagem = atualizar_colheita(novo_registro)
        print(mensagem)
    except Exception as erro:
        print(f"Falha ao montar dados para alteração: {erro}")
    finally:
        print("Operação de alteração finalizada.")


def excluir_no_oracle() -> None:
    id_registro = ler_int_positivo("Informe o ID do registro que deseja excluir: ")
    sucesso, mensagem = excluir_colheita(id_registro)
    print(mensagem)


def excluir_todos_no_oracle() -> None:
    confirmacao = input("Tem certeza que deseja excluir TODOS os registros? [S/N]: ").strip().upper()
    if confirmacao == "S":
        sucesso, mensagem = excluir_todas_colheitas()
        print(mensagem)
    else:
        print("Operação cancelada.")


def gerar_txt() -> None:
    sucesso, mensagem = gerar_relatorio_txt(
        registros_memoria,
        str(DADOS_DIR / "relatorio_colheitas.txt")
    )
    print(mensagem)


def gerar_json() -> None:
    sucesso, mensagem = exportar_json(
        registros_memoria,
        str(DADOS_DIR / "colheitas.json")
    )
    print(mensagem)


def main() -> None:
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        try:
            if opcao == "1":
                cadastrar_em_memoria()
            elif opcao == "2":
                listar_memoria()
            elif opcao == "3":
                gerar_txt()
            elif opcao == "4":
                gerar_json()
            elif opcao == "5":
                sucesso, mensagem = criar_tabela()
                print(mensagem)
            elif opcao == "6":
                salvar_no_oracle()
            elif opcao == "7":
                listar_oracle()
            elif opcao == "8":
                alterar_no_oracle()
            elif opcao == "9":
                excluir_no_oracle()
            elif opcao == "10":
                excluir_todos_no_oracle()
            elif opcao == "0":
                print("Encerrando o sistema.")
                break
            else:
                print("Opção inválida.")
        except Exception as erro:
            print(f"Ocorreu um erro inesperado no menu: {erro}")
        finally:
            print("\nRetornando ao menu principal...")


if __name__ == "__main__":
    main()