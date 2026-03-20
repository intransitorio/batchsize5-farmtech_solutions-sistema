# ==========================================================
# FarmTech Solutions - Grupo Batch Size 5
# ==========================================================

# Vetor principal para armazenar os dados das lavouras
dados_lavouras = []

def calcular_soja():
    print("\n--- Manejo de Soja (Plantio em Ruas) ---")
    ruas = int(input("Quantas ruas a lavoura de Soja tem? "))
    comp = float(input("Qual o comprimento de cada rua (em metros)? "))
    largura = float(input("Qual a largura total da lavoura (em metros)? "))
    
    # Figura Geométrica: Retângulo
    area_m2 = comp * largura
    # Manejo: Pulverizar 500 mL (0.5 L) de defensivo (ex: Glifosato) por rua
    insumo_total = ruas * 0.5 
    
    return "Soja", area_m2, "Herbicida (Litros)", insumo_total

def calcular_cana():
    print("\n--- Manejo de Cana-de-açúcar (Terreno Irregular) ---")
    print("Para a Cana, calcularemos a área baseada em um terreno trapezoidal.")
    base_maior = float(input("Qual a medida da base maior do terreno (em metros)? "))
    base_menor = float(input("Qual a medida da base menor do terreno (em metros)? "))
    altura = float(input("Qual a profundidade/altura do terreno (em metros)? "))
    
    # Figura Geométrica: Trapézio
    area_m2 = ((base_maior + base_menor) * altura) / 2
    hectares = area_m2 / 10000
    
    # Manejo: Aplicação de fertirrigação com Vinhaça (30 m³ por hectare)
    insumo_total = hectares * 30
    
    return "Cana-de-açúcar", area_m2, "Vinhaça (m³)", insumo_total

def inserir_dados():
    print("\n[1] Soja  |  [2] Cana-de-açúcar")
    escolha = input("Selecione a cultura: ")
    
    if escolha == '1':
        cultura, area, produto, qtd = calcular_soja()
    elif escolha == '2':
        cultura, area, produto, qtd = calcular_cana()
    else:
        print("Opção inválida!")
        return

    dados_lavouras.append({
        "cultura": cultura,
        "area_m2": round(area, 2),
        "produto": produto,
        "quantidade": round(qtd, 2)
    })
    print("Dados inseridos com sucesso!")

def listar_dados():
    print("\n--- Lavouras Registradas ---")
    if not dados_lavouras:
        print("Nenhum dado cadastrado.")
        return
    
    for i, lavoura in enumerate(dados_lavouras):
        print(f"[{i}] Cultura: {lavoura['cultura']} | Área: {lavoura['area_m2']} m² | {lavoura['produto']}: {lavoura['quantidade']}")

def atualizar_dados():
    listar_dados()
    if not dados_lavouras: return
    
    try:
        indice = int(input("\nDigite o índice da lavoura que deseja atualizar: "))
        if 0 <= indice < len(dados_lavouras):
            print("Insira os novos dados para esta posição:")
            inserir_dados()
            # Substitui o dado antigo pelo novo recém inserido no final da lista
            dados_lavouras[indice] = dados_lavouras.pop() 
            print("Lavoura atualizada!")
        else:
            print("Índice não encontrado.")
    except ValueError:
        print("Por favor, digite um número válido.")

def remover_dados():
    listar_dados()
    if not dados_lavouras: return
    
    try:
        indice = int(input("\nDigite o índice da lavoura para deletar: "))
        if 0 <= indice < len(dados_lavouras):
            removido = dados_lavouras.pop(indice)
            print(f"Lavoura de {removido['cultura']} removida com sucesso!")
        else:
            print("Índice não encontrado.")
    except ValueError:
        print("Por favor, digite um número válido.")

# Loop principal do Menu
while True:
    print("\n======================================")
    print("  FarmTech Solutions - Batch Size 5   ")
    print("======================================")
    print("1. Entrada de dados")
    print("2. Saída de dados (Listar)")
    print("3. Atualização de dados")
    print("4. Deleção de dados")
    print("5. Sair do programa")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == '1':
        inserir_dados()
    elif opcao == '2':
        listar_dados()
    elif opcao == '3':
        atualizar_dados()
    elif opcao == '4':
        remover_dados()
    elif opcao == '5':
        print("Encerrando o sistema da FarmTech. Até logo!")
        break
    else:
        print("Opção inválida. Tente novamente.")