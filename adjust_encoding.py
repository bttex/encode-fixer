import argparse
import os
import pandas as pd
import csv


def carregar_csv(caminho, sep=";"):
    """Abre CSV com suporte a quebras de linha internas e acentuação."""
    encodings_testar = ["utf-8", "latin1", "iso-8859-1", "windows-1252"]
    for enc in encodings_testar:
        try:
            df = pd.read_csv(
                caminho,
                encoding=enc,
                sep=sep,
                engine="python",  # parser mais tolerante
                quotechar='"',  # respeita texto entre aspas
                quoting=csv.QUOTE_MINIMAL,  # mantém quebras de linha dentro de aspas
                on_bad_lines="skip",
            )
            print(f"[OK] Lido com sucesso (encoding={enc}, sep='{sep}')")
            return df
        except Exception as e:
            print(f"[!] Falhou com {enc}: {e}")
            continue

    raise Exception("❌ Não foi possível ler o CSV com os encodings testados.")


def main():
    parser = argparse.ArgumentParser(
        description="Corrige acentuação de um arquivo CSV e salva em UTF-8-SIG (compatível com Excel)."
    )
    parser.add_argument(
        "--csv-path", required=True, help="Caminho completo do arquivo CSV original."
    )
    parser.add_argument(
        "--save-name",
        required=False,
        help="Nome do novo arquivo CSV (ex: ajustado.csv).",
    )
    parser.add_argument(
        "--sep",
        required=False,
        help="Separador de campos (padrão: ';'). Exemplo: --sep ','",
    )

    args = parser.parse_args()
    caminho_original = args.csv_path
    sep = args.sep

    if not os.path.exists(caminho_original):
        print(f"❌ Arquivo não encontrado: {caminho_original}")
        return

    if args.save_name:
        nome_saida = args.save_name
    else:
        nome_arquivo = os.path.basename(caminho_original)
        nome_base, ext = os.path.splitext(nome_arquivo)
        nome_saida = f"{nome_base}_utf8{ext}"

    pasta = os.path.dirname(caminho_original)
    caminho_saida = os.path.join(pasta, nome_saida)

    df = carregar_csv(caminho_original, sep=sep or ";")

    # Remove quebras internas (opcional)
    df = df.map(
        lambda x: str(x).replace("\r", " ").replace("\n", " ")
        if isinstance(x, str)
        else x
    )
    

    df.to_csv(caminho_saida, index=False, encoding="utf-8-sig", sep=sep or ";")

    print(f"✅ Arquivo corrigido salvo em: {caminho_saida}")


if __name__ == "__main__":
    main()
