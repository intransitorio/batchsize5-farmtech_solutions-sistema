"""
validacao.py
Funções utilitárias para leitura segura e validação de entradas do usuário.

Escopo atual:
- validação de textos, inteiros, floats e datas
- apoio à interface CLI das etapas 3 e 4
"""

from __future__ import annotations

from datetime import datetime


def ler_texto(mensagem: str, tamanho_max: int = 100) -> str:
    """Lê um texto obrigatório e respeita o tamanho máximo informado."""
    while True:
        valor = input(mensagem).strip()
        if not valor:
            print("  ⚠ Campo obrigatório. Não pode ser vazio.")
            continue
        if len(valor) > tamanho_max:
            print(f"  ⚠ Máximo de {tamanho_max} caracteres.")
            continue
        return valor



def ler_float(mensagem: str, minimo: float | None = None, maximo: float | None = None) -> float:
    """Lê um número decimal com suporte a vírgula ou ponto."""
    while True:
        try:
            valor = float(input(mensagem).strip().replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"  ⚠ Valor mínimo permitido: {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠ Valor máximo permitido: {maximo}")
                continue
            return valor
        except ValueError:
            print("  ⚠ Digite um número válido. Ex.: 12.5")



def ler_inteiro(mensagem: str, minimo: int | None = None, maximo: int | None = None) -> int:
    """Lê um número inteiro com validação de faixa."""
    while True:
        try:
            valor = int(input(mensagem).strip())
            if minimo is not None and valor < minimo:
                print(f"  ⚠ Valor mínimo permitido: {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"  ⚠ Valor máximo permitido: {maximo}")
                continue
            return valor
        except ValueError:
            print("  ⚠ Digite um número inteiro válido.")



def ler_data(mensagem: str) -> str:
    """Lê uma data no formato DD/MM/AAAA e devolve em ISO (AAAA-MM-DD)."""
    while True:
        entrada = input(mensagem).strip()
        try:
            data = datetime.strptime(entrada, "%d/%m/%Y")
            if data.year < 1900:
                print("  ⚠ Ano inválido.")
                continue
            return data.strftime("%Y-%m-%d")
        except ValueError:
            print("  ⚠ Formato inválido. Use DD/MM/AAAA.")



def ler_opcao(mensagem: str, opcoes_validas: tuple[str, ...]) -> str:
    """Lê uma opção textual dentre um conjunto permitido."""
    opcoes_formatadas = "/".join(opcoes_validas)
    opcoes_normalizadas = tuple(op.lower() for op in opcoes_validas)

    while True:
        valor = input(f"{mensagem} [{opcoes_formatadas}]: ").strip().lower()
        if valor in opcoes_normalizadas:
            return valor
        print(f"  ⚠ Opção inválida. Escolha entre: {opcoes_formatadas}")
