"""Arquivo principal para executar o sistema a partir da raiz do projeto."""

from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from main import exibir_cabecalho, menu_principal  # noqa: E402


if __name__ == "__main__":
    exibir_cabecalho()
    menu_principal()
