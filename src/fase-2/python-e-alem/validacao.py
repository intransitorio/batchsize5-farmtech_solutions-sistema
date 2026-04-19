"""
validacao.py — Funções de validação e leitura segura de entradas do usuário.
Unifica as abordagens dos dois projetos originais.
"""

from datetime import datetime

FORMATOS_DATA = (
    "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d",
    "%Y/%m/%d", "%d%m%Y",   "%Y%m%d",
)


def limpar_texto(texto: str) -> str:
    return " ".join(texto.strip().split())


def ler_float(mensagem: str, minimo: float = None, maximo: float = None) -> float:
    while True:
        try:
            valor = float(limpar_texto(input(mensagem)).replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"  ⚠ Valor mínimo: {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠ Valor máximo: {maximo}")
                continue
            return valor
        except ValueError:
            print("  ⚠ Digite um número válido (ex: 12.5).")


def ler_inteiro(mensagem: str, minimo: int = None, maximo: int = None) -> int:
    while True:
        try:
            valor = int(limpar_texto(input(mensagem)))
            if minimo is not None and valor < minimo:
                print(f"  ⚠ Valor mínimo: {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠ Valor máximo: {maximo}")
                continue
            return valor
        except ValueError:
            print("  ⚠ Digite um número inteiro válido.")


# Alias para compatibilidade com sad_agro
ler_int = ler_inteiro


def ler_texto(mensagem: str, tamanho_min: int = 1, tamanho_max: int = 100,
              permitir_vazio: bool = False) -> str:
    while True:
        valor = limpar_texto(input(mensagem))
        if permitir_vazio and valor == "":
            return valor
        if len(valor) < tamanho_min:
            print(f"  ⚠ Mínimo de {tamanho_min} caractere(s).")
        elif len(valor) > tamanho_max:
            print(f"  ⚠ Máximo de {tamanho_max} caracteres.")
        else:
            return valor


def converter_data(texto: str) -> str:
    """Converte data em formato livre para DD/MM/AAAA. Retorna None se inválida."""
    for fmt in FORMATOS_DATA:
        try:
            return datetime.strptime(texto, fmt).strftime("%d/%m/%Y")
        except ValueError:
            continue
    return None


def data_iso(data_br: str) -> str:
    """Converte DD/MM/AAAA → AAAA-MM-DD para gravar no banco."""
    return datetime.strptime(data_br, "%d/%m/%Y").strftime("%Y-%m-%d")


def ler_data(mensagem: str) -> str:
    """Lê data em qualquer formato e retorna no padrão ISO (AAAA-MM-DD)."""
    while True:
        entrada = limpar_texto(input(mensagem))
        padronizada = converter_data(entrada)
        if padronizada:
            try:
                dt = datetime.strptime(padronizada, "%d/%m/%Y")
                if dt > datetime.now():
                    print(f"  ⚠ Atenção: {padronizada} é data futura.")
                return data_iso(padronizada)
            except ValueError:
                pass
        print("  ⚠ Data inválida. Use DD/MM/AAAA, DD-MM-AAAA ou AAAA-MM-DD.")


def ler_opcao(mensagem: str, opcoes_validas: tuple) -> str:
    """Lê uma opção dentro de um conjunto pré-definido."""
    fmt = "/".join(opcoes_validas)
    while True:
        valor = limpar_texto(input(f"{mensagem} [{fmt}]: ")).lower()
        if valor in [o.lower() for o in opcoes_validas]:
            return valor
        print(f"  ⚠ Opção inválida. Escolha: {fmt}")


def ler_tipo_colheita() -> str:
    """Aceita 1/manual ou 2/mecanizada."""
    mapa = {"1": "manual", "2": "mecanizada",
            "manual": "manual", "mecanizada": "mecanizada"}
    while True:
        valor = limpar_texto(
            input("  Tipo de colheita [1=Manual | 2=Mecanizada]: ")
        ).lower()
        if valor in mapa:
            return mapa[valor]
        print("  ⚠ Digite 1 para Manual ou 2 para Mecanizada.")


def ler_booleano(mensagem: str) -> bool:
    """Lê S/N e retorna True/False."""
    while True:
        valor = limpar_texto(input(mensagem)).lower()
        if valor in ("s", "sim"):
            return True
        if valor in ("n", "nao", "não"):
            return False
        print("  ⚠ Digite S para sim ou N para não.")
