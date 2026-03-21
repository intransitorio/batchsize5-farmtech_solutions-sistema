# ============================================================
# Projeto FarmTech Solutions - Agricultura Digital
# Parte 1: Aplicação em Python
# Culturas suportadas: Soja e Cana-de-açúcar
# ============================================================

import csv

# ------------------------------
# Vetores paralelos do sistema
# ------------------------------
ids = []
nomes_talhoes = []
culturas = []
comprimentos_m = []
larguras_m = []
areas_m2 = []
areas_ha = []
produtos = []
doses_por_ha = []
quantidades_insumo = []

# ------------------------------
# Base de manejo de insumos
# ------------------------------
INSUMOS = {
    "Soja": {
        "Fertilizante NPK": 350.0,
        "Herbicida": 3.5,
        "Inseticida": 0.8,
        "Fungicida": 0.6
    },
    "Cana-de-açúcar": {
        "Fertilizante NPK": 500.0,
        "Herbicida": 4.0,
        "Inseticida": 1.2,
        "Maturador": 2.0
    }
}


# ------------------------------
# Funções utilitárias
# ------------------------------

def linha(tamanho=70):
    print("-" * tamanho)



def pausar():
    linha()
    input("\nPressione Enter para continuar...")



def ler_int(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Erro: informe um valor maior ou igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Erro: informe um valor menor ou igual a {maximo}.")
                continue
            return valor
        except ValueError:
            mostrar_cabecalho("Erro: digite uma opção válida do menu.")



def ler_float(mensagem, minimo=None):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"Erro: informe um valor maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Erro: digite um número válido.")



def escolher_cultura():
    mostrar_cabecalho("Escolha a cultura:")
    print("1 - Soja")
    print("2 - Cana-de-açúcar")
    linha()

    opcao = ler_int("Opção: ", 1, 2)
    if opcao == 1:
        return "Soja"
    return "Cana-de-açúcar"



def escolher_produto(cultura):
    produtos_cultura = list(INSUMOS[cultura].keys())

    mostrar_cabecalho(f"Produtos disponíveis para {cultura}:")
    for i, produto in enumerate(produtos_cultura, start=1):
        dose = INSUMOS[cultura][produto]
        unidade = "kg/ha" if "Fertilizante" in produto else "L/ha"
        print(f"{i} - {produto} ({dose} {unidade})")

    linha()
    opcao = ler_int("Escolha o produto: ", 1, len(produtos_cultura))
    produto_escolhido = produtos_cultura[opcao - 1]
    dose = INSUMOS[cultura][produto_escolhido]
    return produto_escolhido, dose



def calcular_area(comprimento, largura):
    area_m2 = comprimento * largura
    area_ha = area_m2 / 10000
    return area_m2, area_ha



def calcular_quantidade_insumo(area_hectares, dose_hectare):
    return area_hectares * dose_hectare



def existe_registro():
    return len(ids) > 0



def mostrar_cabecalho(titulo):
    print("\n")
    linha()
    print(titulo.center(70))
    linha()


# ------------------------------
# Funções principais do sistema
# ------------------------------

def cadastrar_registro():
    mostrar_cabecalho("CADASTRO DE REGISTRO AGRÍCOLA")

    novo_id = len(ids) + 1
    nome_talhao = input("Nome do talhão/área: ").strip()
    while not nome_talhao:
        print("Erro: o nome do talhão não pode ficar vazio.")
        nome_talhao = input("Nome do talhão/área: ").strip()

    cultura = escolher_cultura()
    comprimento = ler_float("Comprimento do terreno (m): ", 0.01)
    largura = ler_float("Largura do terreno (m): ", 0.01)

    area_m2, area_ha = calcular_area(comprimento, largura)
    produto, dose = escolher_produto(cultura)
    quantidade = calcular_quantidade_insumo(area_ha, dose)

    ids.append(novo_id)
    nomes_talhoes.append(nome_talhao)
    culturas.append(cultura)
    comprimentos_m.append(comprimento)
    larguras_m.append(largura)
    areas_m2.append(area_m2)
    areas_ha.append(area_ha)
    produtos.append(produto)
    doses_por_ha.append(dose)
    quantidades_insumo.append(quantidade)

    mostrar_cabecalho("Registro cadastrado com sucesso")
    print(f"ID: {novo_id}")
    print(f"Área: {area_m2:.0f} m² | {area_ha:.2f} ha")

    unidade = "kg" if "Fertilizante" in produto else "L"
    print(f"Insumo calculado: {produto} -> {quantidade:.2f} {unidade}")



def listar_registros():
    mostrar_cabecalho("LISTAGEM DE REGISTROS")

    if not existe_registro():
        print("Nenhum registro cadastrado.")
        return

    for i in range(len(ids)):
        print(f"Posição no vetor: {i}")
        print(f"ID: {ids[i]}")
        print(f"Talhão: {nomes_talhoes[i]}")
        print(f"Cultura: {culturas[i]}")
        print(f"Comprimento: {comprimentos_m[i]:.0f} m")
        print(f"Largura: {larguras_m[i]:.0f} m")
        print(f"Área: {areas_m2[i]:.0f} m² | {areas_ha[i]:.2f} ha")
        print(f"Produto: {produtos[i]}")

        unidade_dose = "kg/ha" if "Fertilizante" in produtos[i] else "L/ha"
        unidade_qtd = "kg" if "Fertilizante" in produtos[i] else "L"

        print(f"Dose aplicada: {doses_por_ha[i]:.2f} {unidade_dose}")
        print(f"Quantidade total de insumo: {quantidades_insumo[i]:.2f} {unidade_qtd}")
        linha()



def atualizar_registro():
    mostrar_cabecalho("ATUALIZAÇÃO DE REGISTRO")

    if not existe_registro():
        print("Nenhum registro cadastrado para atualizar.")
        return

    listar_resumo_posicoes()
    posicao = ler_int("Informe a posição do vetor que deseja atualizar: ", 0, len(ids) - 1)

    print("\nDigite os novos dados do registro selecionado.")
    nome_talhao = input("Novo nome do talhão/área: ").strip()
    while not nome_talhao:
        print("Erro: o nome do talhão não pode ficar vazio.")
        nome_talhao = input("Novo nome do talhão/área: ").strip()

    cultura = escolher_cultura()
    comprimento = ler_float("Novo comprimento (m): ", 0.01)
    largura = ler_float("Nova largura (m): ", 0.01)

    area_m2, area_ha = calcular_area(comprimento, largura)
    produto, dose = escolher_produto(cultura)
    quantidade = calcular_quantidade_insumo(area_ha, dose)

    nomes_talhoes[posicao] = nome_talhao
    culturas[posicao] = cultura
    comprimentos_m[posicao] = comprimento
    larguras_m[posicao] = largura
    areas_m2[posicao] = area_m2
    areas_ha[posicao] = area_ha
    produtos[posicao] = produto
    doses_por_ha[posicao] = dose
    quantidades_insumo[posicao] = quantidade

    print("\nRegistro atualizado com sucesso.")



def deletar_registro():
    mostrar_cabecalho("DELEÇÃO DE REGISTRO")

    if not existe_registro():
        print("Nenhum registro cadastrado para deletar.")
        return

    listar_resumo_posicoes()
    posicao = ler_int("Informe a posição do vetor que deseja deletar: ", 0, len(ids) - 1)

    print("\nRegistro selecionado:")
    print(f"Talhão: {nomes_talhoes[posicao]}")
    print(f"Cultura: {culturas[posicao]}")

    confirmacao = input("Confirma a exclusão? (S/N): ").strip().upper()
    if confirmacao == "S":
        ids.pop(posicao)
        nomes_talhoes.pop(posicao)
        culturas.pop(posicao)
        comprimentos_m.pop(posicao)
        larguras_m.pop(posicao)
        areas_m2.pop(posicao)
        areas_ha.pop(posicao)
        produtos.pop(posicao)
        doses_por_ha.pop(posicao)
        quantidades_insumo.pop(posicao)

        reorganizar_ids()
        print("Registro deletado com sucesso.")
    else:
        print("Operação cancelada.")



def calcular_area_individual():
    mostrar_cabecalho("CÁLCULO DE ÁREA")

    if not existe_registro():
        print("Nenhum registro cadastrado.")
        return

    listar_resumo_posicoes()
    posicao = ler_int("Informe a posição do vetor para consultar a área: ", 0, len(ids) - 1)

    print(f"\nTalhão: {nomes_talhoes[posicao]}")
    print(f"Cultura: {culturas[posicao]}")
    print(f"Comprimento: {comprimentos_m[posicao]:.0f} m")
    print(f"Largura: {larguras_m[posicao]:.0f} m")
    print(f"Área calculada: {areas_m2[posicao]:.0f} m²")
    print(f"Área em hectares: {areas_ha[posicao]:.0f} ha")



def calcular_insumo_individual():
    mostrar_cabecalho("CÁLCULO DE MANEJO DE INSUMOS")

    if not existe_registro():
        print("Nenhum registro cadastrado.")
        return

    listar_resumo_posicoes()
    linha()
    posicao = ler_int("Informe a posição do vetor para consultar o insumo: ", 0, len(ids) - 1)

    produto = produtos[posicao]
    unidade_dose = "kg/ha" if "Fertilizante" in produto else "L/ha"
    unidade_qtd = "kg" if "Fertilizante" in produto else "L"

    print(f"\nTalhão: {nomes_talhoes[posicao]}")
    print(f"Cultura: {culturas[posicao]}")
    print(f"Área: {areas_ha[posicao]:.2f} ha")
    print(f"Produto utilizado: {produto}")
    print(f"Dose por hectare: {doses_por_ha[posicao]:.2f} {unidade_dose}")
    print(f"Quantidade necessária: {quantidades_insumo[posicao]:.2f} {unidade_qtd}")



def exibir_resumo_geral():
    mostrar_cabecalho("RESUMO GERAL DA PRODUÇÃO")

    if not existe_registro():
        print("Nenhum registro cadastrado.")
        return

    total_registros = len(ids)
    total_area_m2 = sum(areas_m2)
    total_area_ha = sum(areas_ha)

    qtd_soja = culturas.count("Soja")
    qtd_cana = culturas.count("Cana-de-açúcar")

    area_soja = 0
    area_cana = 0

    for i in range(len(culturas)):
        if culturas[i] == "Soja":
            area_soja += areas_ha[i]
        elif culturas[i] == "Cana-de-açúcar":
            area_cana += areas_ha[i]

    print(f"Total de registros cadastrados: {total_registros}")
    print(f"Área total cultivada: {total_area_m2:.0f} m² | {total_area_ha:.2f} ha")
    print(f"Quantidade de registros de Soja: {qtd_soja}")
    print(f"Quantidade de registros de Cana-de-açúcar: {qtd_cana}")
    print(f"Área total de Soja: {area_soja:.2f} ha")
    print(f"Área total de Cana-de-açúcar: {area_cana:.2f} ha")



def exportar_para_csv():
    mostrar_cabecalho("EXPORTAÇÃO DE DADOS PARA CSV")

    if not existe_registro():
        print("Nenhum registro cadastrado para exportar.")
        return

    nome_arquivo = input("Informe o nome do arquivo CSV [dados_agricolas.csv]: ").strip()
    if not nome_arquivo:
        nome_arquivo = "dados_agricolas.csv"

    if not nome_arquivo.lower().endswith(".csv"):
        nome_arquivo += ".csv"

    try:
        with open(nome_arquivo, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow([
                "id",
                "talhao",
                "cultura",
                "comprimento_m",
                "largura_m",
                "area_m2",
                "area_ha",
                "produto",
                "dose_por_ha",
                "quantidade_insumo"
            ])

            for i in range(len(ids)):
                escritor.writerow([
                    ids[i],
                    nomes_talhoes[i],
                    culturas[i],
                    f"{comprimentos_m[i]:.2f}",
                    f"{larguras_m[i]:.2f}",
                    f"{areas_m2[i]:.2f}",
                    f"{areas_ha[i]:.4f}",
                    produtos[i],
                    f"{doses_por_ha[i]:.2f}",
                    f"{quantidades_insumo[i]:.4f}"
                ])

        print(f"Dados exportados com sucesso para o arquivo: {nome_arquivo}")
        print("Esse arquivo pode ser lido diretamente pelo script em R.")

    except OSError as erro:
        print("Erro ao salvar o arquivo CSV.")
        print(f"Detalhes: {erro}")



def listar_resumo_posicoes():
    print("\nPosições disponíveis no vetor:")
    for i in range(len(ids)):
        print(f"{i} - {nomes_talhoes[i]} | {culturas[i]} | {areas_ha[i]:.2f} ha")



def reorganizar_ids():
    for i in range(len(ids)):
        ids[i] = i + 1



def exibir_menu():
    mostrar_cabecalho("FARMTECH SOLUTIONS - AGRICULTURA DIGITAL")
    print("1 - Cadastrar registro")
    print("2 - Listar registros")
    print("3 - Atualizar registro")
    print("4 - Deletar registro")
    print("5 - Calcular área de plantio")
    print("6 - Calcular manejo de insumos")
    print("7 - Exibir resumo geral")
    print("8 - Exportar dados para CSV")
    print("0 - Encerrar sistema")
    linha()



def main():
    while True:
        exibir_menu()
        opcao = ler_int("Escolha uma opção: ")

        if opcao == 1:
            cadastrar_registro()
            pausar()
        elif opcao == 2:
            listar_registros()
            pausar()
        elif opcao == 3:
            atualizar_registro()
            pausar()
        elif opcao == 4:
            deletar_registro()
            pausar()
        elif opcao == 5:
            calcular_area_individual()
            pausar()
        elif opcao == 6:
            calcular_insumo_individual()
            pausar()
        elif opcao == 7:
            exibir_resumo_geral()
            pausar()
        elif opcao == 8:
            exportar_para_csv()
            pausar()
        elif opcao == 0:
            mostrar_cabecalho("ENCERRANDO O SISTEMA")
            print("Obrigado por utilizar o sistema FarmTech Solutions.")
            break
        else:
            print("Opção inválida. Tente novamente.")
            pausar()


# Ponto de entrada do programa
if __name__ == "__main__":
    main()
