#!/usr/bin/env python3
"""
Converte um documento (PDF, DOCX, PPTX, XLSX) para Markdown usando o MarkItDown,
salvando o resultado ao lado do arquivo original com extensão .md.

Uso:
    python3 convert_to_md.py <caminho_do_arquivo> [--out <caminho_saida.md>]

Saída (stdout):
    Em sucesso, imprime apenas o caminho do arquivo .md gerado.
    Em falha, imprime "CONVERSION_FAILED: <motivo>" e sai com código 1 —
    quem chamou deve então ler o arquivo original normalmente.
"""

import argparse
import os
import sys

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx", ".xlsx"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Caminho do documento a converter")
    parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Caminho de saída do .md (default: mesmo diretório/nome do input, trocando a extensão)",
    )
    args = parser.parse_args()

    input_path = args.input_path
    ext = os.path.splitext(input_path)[1].lower()

    if not os.path.isfile(input_path):
        print(f"CONVERSION_FAILED: arquivo não encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)

    if ext not in SUPPORTED_EXTENSIONS:
        print(f"CONVERSION_FAILED: extensão não suportada por esta skill: {ext}", file=sys.stderr)
        sys.exit(1)

    # Anexa ".md" ao nome completo (em vez de trocar a extensão) para não colidir
    # quando arquivos com o mesmo nome-base e extensões diferentes existem no
    # mesmo diretório (ex.: "relatorio.docx" e "relatorio.xlsx").
    out_path = args.out_path or (input_path + ".md")

    try:
        from markitdown import MarkItDown
    except ImportError:
        print(
            "CONVERSION_FAILED: pacote 'markitdown' não instalado. "
            "Instale com: pip install markitdown --break-system-packages",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        md = MarkItDown()
        result = md.convert(input_path)
        content = result.text_content or ""

        if not content.strip():
            print("CONVERSION_FAILED: conversão retornou conteúdo vazio", file=sys.stderr)
            sys.exit(1)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)

    except Exception as exc:  # noqa: BLE001 - queremos capturar qualquer falha do markitdown
        print(f"CONVERSION_FAILED: {exc}", file=sys.stderr)
        sys.exit(1)

    # Sucesso: só o caminho no stdout, para ser fácil de capturar em script.
    print(out_path)


if __name__ == "__main__":
    main()
