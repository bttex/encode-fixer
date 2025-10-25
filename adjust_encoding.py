import pandas as pd
import csv
import typer
from pathlib import Path
from typing import Optional, Annotated
import chardet


def carregar_csv(caminho: Path, sep: str = ";"):
    """
    Abre CSV com detecção automática de encoding e suporte a quebras de linha.
    """

    # --- Início da Lógica de Detecção Automática ---
    try:
        with open(caminho, "rb") as f:
            # Lê uma amostra do arquivo (ex: os primeiros 1MB) para detecção.
            # Não é necessário ler o arquivo inteiro para detectar o encoding.
            raw_data = f.read(1024 * 1024)
    except FileNotFoundError:
        # (Embora o Typer já verifique, é uma boa prática)
        print(f"❌ Arquivo não encontrado: {caminho}")
        raise typer.Exit(code=1)
    except Exception as e:
        print(f"❌ Erro ao ler arquivo para detecção: {e}")
        raise typer.Exit(code=1)

    # Detecta o encoding a partir da amostra
    result = chardet.detect(raw_data)
    detected_encoding = result["encoding"]
    confidence = result.get("confidence", 0) * 100

    encodings_testar = []

    if detected_encoding:
        print(
            f"[i] Detecção automática (chardet): {detected_encoding} (Confiança: {confidence:.0f}%)"
        )
        # Adiciona o encoding detectado como primeira opção
        encodings_testar.append(detected_encoding)
    else:
        print("[i] Chardet não conseguiu detectar um encoding. Tentando fallbacks...")

    # Adiciona os fallbacks comuns, garantindo que não haja duplicatas
    # (Ex: se chardet detectar 'utf-8', não o adicionamos duas vezes)
    fallbacks = ["utf-8", "windows-1252", "latin1", "iso-8859-1"]
    for enc in fallbacks:
        if enc.lower() not in [e.lower() for e in encodings_testar]:
            encodings_testar.append(enc)
    # --- Fim da Lógica de Detecção ---

    print(f"[i] Ordem de tentativa: {encodings_testar}")

    for enc in encodings_testar:
        try:
            df = pd.read_csv(
                caminho,
                encoding=enc,
                sep=sep,
                engine="python",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
                on_bad_lines="skip",
            )
            print(f"✅ [OK] Lido com sucesso (encoding={enc}, sep='{sep}')")
            return df
        except (UnicodeDecodeError, LookupError) as e:  # Erros esperados de encoding
            print(f"[!] Falhou com {enc}: {type(e).__name__}")
            continue
        except Exception as e:  # Outros erros (ex: permissão)
            print(f"[!] Erro inesperado com {enc}: {e}")
            continue

    # Se o loop terminar sem sucesso
    print(
        "❌ Não foi possível ler o CSV com nenhum dos encodings testados (nem com a detecção automática)."
    )
    raise typer.Exit(code=1)


def main(
    csv_path: Annotated[
        Path,
        typer.Option(
            "--csv-path",
            help="Caminho completo do arquivo CSV original.",
            exists=True,  # O Typer já verifica se o arquivo existe
            file_okay=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    save_name: Annotated[
        Optional[Path],
        typer.Option(
            "--save-name",
            help="Nome do novo arquivo CSV (ex: ajustado.csv). Se não informado, adiciona _utf8.",
        ),
    ] = None,
    sep: Annotated[
        str,
        typer.Option(
            "--sep",
            help="Separador de campos. Exemplo: --sep ','",
        ),
    ] = ";",  # O padrão ';' é definido aqui
):
    """
    Corrige acentuação de um arquivo CSV e salva em UTF-8-SIG (compatível com Excel).
    """

    # A verificação 'os.path.exists' não é mais necessária,
    # pois 'exists=True' no typer.Option já faz isso.

    # A lógica de definição do caminho de saída foi mantida, mas usando pathlib
    if save_name:
        # Se o save_name for relativo, salva na mesma pasta do original
        if not save_name.is_absolute():
            caminho_saida = csv_path.parent / save_name
        else:
            caminho_saida = save_name
    else:
        nome_base = csv_path.stem  # Nome do arquivo sem extensão
        ext = csv_path.suffix  # Extensão do arquivo (ex: .csv)
        nome_saida = f"{nome_base}_utf8{ext}"
        caminho_saida = csv_path.parent / nome_saida

    # A lógica de 'sep or ";"' foi simplificada, pois 'sep' agora tem o default=";"
    df = carregar_csv(csv_path, sep=sep)

    # Remove quebras internas (opcional)
    df = df.map(
        lambda x: str(x).replace("\r", " ").replace("\n", " ")
        if isinstance(x, str)
        else x
    )

    df.to_csv(caminho_saida, index=False, encoding="utf-8-sig", sep=sep)

    print(f"✅ Arquivo corrigido salvo em: {caminho_saida}")


if __name__ == "__main__":
    typer.run(main)
