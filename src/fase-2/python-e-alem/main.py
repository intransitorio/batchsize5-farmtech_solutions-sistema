"""
main.py — SACana v2.0
Sistema de Apoio à Decisão para Colheita de Cana-de-Açúcar

Unificação de:
  - trabalho_fiap: arquitetura modular, Oracle, talhões, testes
  - sad_agro: lógica agronômica rica, diagnóstico SAD, CSV, campos detalhados

Referências:
  SOCICANA: perdas mecanizadas até 15%; manuais raramente passam de 5%.
  Embrapa / FAO: agricultura digital na tomada de decisão no agronegócio.
  CHB Agro: estratégias de mitigação de perdas na colheita de cana.
  TOTVS / Aevo: conceito de agronegócio e agrotechs no Brasil.
"""

from banco import inicializar_banco
from talhoes import menu_talhoes
from colheita import menu_colheitas
from arquivos import menu_arquivos


def boas_vindas() -> None:
    print("\n" + "=" * 60)
    print("  SACana v2.0 — Sistema de Apoio à Decisão".center(60))
    print("  Cultura: Cana-de-Açúcar  🌿".center(60))
    print("=" * 60)
    print("""
  Problema: a colheita mecanizada gera perdas de até 15%
  (SOCICANA), contra menos de 5% na colheita manual.

  Este sistema permite registrar, analisar e apoiar a
  tomada de decisão para reduzir essas perdas com base
  em dados reais de campo e diagnóstico automatizado.
""")


def menu_principal() -> None:
    while True:
        print("\n╔══════════════════════════════════════╗")
        print("║           MENU PRINCIPAL             ║")
        print("╠══════════════════════════════════════╣")
        print("║  1. Gerenciar Talhões                ║")
        print("║  2. Colheitas / Análise / SAD        ║")
        print("║  3. Importar / Exportar Dados        ║")
        print("║  0. Sair                             ║")
        print("╚══════════════════════════════════════╝")
        escolha = input("  Opção: ").strip()

        if escolha == "1":
            menu_talhoes()
        elif escolha == "2":
            menu_colheitas()
        elif escolha == "3":
            menu_arquivos()
        elif escolha == "0":
            print("\n  Sistema encerrado. Até logo! 🌾\n")
            break
        else:
            print("  ⚠ Opção inválida.")


if __name__ == "__main__":
    inicializar_banco()
    boas_vindas()
    menu_principal()
