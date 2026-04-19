from pathlib import Path
import json


def _garantir_pasta(caminho_arquivo: str) -> None:
    Path(caminho_arquivo).parent.mkdir(parents=True, exist_ok=True)


def gerar_relatorio_txt(registros: list[dict], caminho_arquivo: str) -> tuple[bool, str]:
    try:
        _garantir_pasta(caminho_arquivo)

        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("RELATÓRIO DE COLHEITAS - AGROVISION - IR ALÉM\n")
            arquivo.write("=" * 70 + "\n\n")

            if not registros:
                arquivo.write("Nenhum registro cadastrado.\n")
            else:
                for registro in registros:
                    arquivo.write(f"ID: {registro['id']}\n")
                    arquivo.write(f"Talhão: {registro['talhao']}\n")
                    arquivo.write(f"Cultura: {registro['cultura']}\n")
                    arquivo.write(f"Base (m): {registro['base_m']}\n")
                    arquivo.write(f"Altura (m): {registro['altura_m']}\n")
                    arquivo.write(f"Área (m²): {registro['area_m2']}\n")
                    arquivo.write(f"Produção prevista (t): {registro['producao_prevista_t']}\n")
                    arquivo.write(f"Produção real (t): {registro['producao_real_t']}\n")
                    arquivo.write(f"Produtividade (t/m²): {registro['produtividade_t_m2']}\n")
                    arquivo.write(f"Perda percentual: {registro['perda_percentual']}%\n")
                    arquivo.write(f"Classificação da perda: {registro['classificacao_perda']}\n")
                    arquivo.write("-" * 70 + "\n")

        return True, f"Relatório TXT gerado com sucesso em: {caminho_arquivo}"
    except Exception as erro:
        return False, f"Falha ao gerar TXT: {erro}"


def exportar_json(registros: list[dict], caminho_arquivo: str) -> tuple[bool, str]:
    try:
        _garantir_pasta(caminho_arquivo)

        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(registros, arquivo, ensure_ascii=False, indent=4)

        return True, f"Arquivo JSON exportado com sucesso em: {caminho_arquivo}"
    except Exception as erro:
        return False, f"Falha ao exportar JSON: {erro}"
