from typing import Any, Dict, Optional

CULTURAS = ("Soja", "Cana-de-açúcar")


def exibir_menu() -> None:
    print("\n" + "=" * 60)
    print("AGROVISION - IR ALÉM - CONTROLE DE COLHEITA E PERDAS")
    print("=" * 60)
    print("1  - Cadastrar colheita em memória")
    print("2  - Listar colheitas em memória")
    print("3  - Gerar relatório TXT")
    print("4  - Exportar JSON")
    print("5  - Criar tabela no Oracle")
    print("6  - Salvar registro da memória no Oracle")
    print("7  - Listar registros do Oracle")
    print("8  - Alterar registro no Oracle")
    print("9  - Excluir registro no Oracle")
    print("10 - Excluir todos os registros do Oracle")
    print("0  - Sair")
    print("=" * 60)


def ler_texto(mensagem: str) -> str:
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("ERRO! O campo não pode ficar vazio.")


def ler_int_positivo(mensagem: str) -> int:
    while True:
        try:
            valor = int(input(mensagem).strip())
            if valor > 0:
                return valor
            print("ERRO! Digite um número inteiro maior que zero.")
        except ValueError:
            print("ERRO! Digite um número inteiro válido.")


def ler_float_positivo(mensagem: str) -> float:
    while True:
        try:
            valor_str = input(mensagem).strip().replace(",", ".")
            valor = float(valor_str)
            if valor > 0:
                return valor
            print("ERRO! Digite um número maior que zero.")
        except ValueError:
            print("ERRO! Digite um número válido.")


def escolher_cultura() -> str:
    while True:
        print("\nCulturas disponíveis:")
        for indice, cultura in enumerate(CULTURAS, start=1):
            print(f"{indice} - {cultura}")

        try:
            opcao = int(input("Escolha a cultura: ").strip())
            if 1 <= opcao <= len(CULTURAS):
                return CULTURAS[opcao - 1]
            print("ERRO! Escolha uma opção válida.")
        except ValueError:
            print("ERRO! Digite um número inteiro válido.")


def calcular_area_retangular(base: float, altura: float) -> float:
    return base * altura


def calcular_produtividade(producao_real: float, area_m2: float) -> float:
    if area_m2 <= 0:
        return 0.0
    return producao_real / area_m2


def calcular_perda_percentual(producao_prevista: float, producao_real: float) -> float:
    if producao_prevista <= 0:
        return 0.0
    perda = ((producao_prevista - producao_real) / producao_prevista) * 100
    return max(perda, 0.0)


def classificar_perda(perda_percentual: float) -> str:
    if perda_percentual <= 5:
        return "Baixa"
    if perda_percentual <= 10:
        return "Média"
    return "Alta"


def montar_registro(id_fixo: Optional[int] = None) -> Dict[str, Any]:
    print("\nCADASTRO DE COLHEITA")
    id_registro = id_fixo if id_fixo is not None else ler_int_positivo("ID do registro: ")
    talhao = ler_texto("Nome do talhão: ")
    cultura = escolher_cultura()
    base_m = ler_float_positivo("Base do terreno (m): ")
    altura_m = ler_float_positivo("Altura do terreno (m): ")
    producao_prevista_t = ler_float_positivo("Produção prevista (toneladas): ")
    producao_real_t = ler_float_positivo("Produção real (toneladas): ")

    area_m2 = calcular_area_retangular(base_m, altura_m)
    produtividade_t_m2 = calcular_produtividade(producao_real_t, area_m2)
    perda_percentual = calcular_perda_percentual(producao_prevista_t, producao_real_t)
    classificacao_perda = classificar_perda(perda_percentual)

    return {
        "id": id_registro,
        "talhao": talhao,
        "cultura": cultura,
        "base_m": round(base_m, 2),
        "altura_m": round(altura_m, 2),
        "area_m2": round(area_m2, 2),
        "producao_prevista_t": round(producao_prevista_t, 2),
        "producao_real_t": round(producao_real_t, 2),
        "produtividade_t_m2": round(produtividade_t_m2, 6),
        "perda_percentual": round(perda_percentual, 2),
        "classificacao_perda": classificacao_perda,
    }


def exibir_registro(registro: Dict[str, Any]) -> None:
    print("-" * 60)
    print(f"ID................: {registro['id']}")
    print(f"Talhão............: {registro['talhao']}")
    print(f"Cultura...........: {registro['cultura']}")
    print(f"Base (m)..........: {registro['base_m']}")
    print(f"Altura (m)........: {registro['altura_m']}")
    print(f"Área (m²).........: {registro['area_m2']}")
    print(f"Produção prevista.: {registro['producao_prevista_t']} t")
    print(f"Produção real.....: {registro['producao_real_t']} t")
    print(f"Produtividade.....: {registro['produtividade_t_m2']} t/m²")
    print(f"Perda.............: {registro['perda_percentual']}%")
    print(f"Classificação.....: {registro['classificacao_perda']}")


def buscar_registro_por_id(registros: list[Dict[str, Any]], id_registro: int) -> Optional[Dict[str, Any]]:
    for registro in registros:
        if registro["id"] == id_registro:
            return registro
    return None
