#!/usr/bin/env python3
"""
Cataloga uma prova recebida do cliente (print, PDF, foto) em
"Provas recebidas/DD-MM-2026/<caso>/" — copia o arquivo, calcula o hash
SHA-256 e já registra a linha no catalogo.md daquele caso, com ID
sequencial automático. Nunca sobrescreve nem pula ID.

O hash prova que o arquivo não foi alterado DESDE que entrou no catálogo
— não prova a autenticidade do conteúdo em si (pra isso, ata notarial ou
carimbo do tempo ICP-Brasil, se o caso exigir peso probatório maior).

Uso:
    python3 catalogar_prova.py --arquivo ~/Downloads/print_whatsapp.jpg \
        --caso "Maria Aparecida Amaral" \
        --descricao "Print de conversa WhatsApp com o locador, sobre devolução do imóvel" \
        --data-exibida "14/03/2026 23:41"
"""

import argparse
import hashlib
import re
import shutil
import sys
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
PASTA_PROVAS = BASE / "Provas recebidas"
MODELO = PASTA_PROVAS / "_modelo_catalogo.md"


def sha256_de(caminho: Path) -> str:
    h = hashlib.sha256()
    with caminho.open("rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def slug(nome_caso: str) -> str:
    return nome_caso.strip()


def proximo_id_e_linhas(catalogo: Path) -> tuple[int, list[str]]:
    if not catalogo.exists():
        return 1, []
    linhas = catalogo.read_text(encoding="utf-8").splitlines(keepends=True)
    ids = [int(m.group(1)) for l in linhas for m in [re.search(r"\|\s*Doc\.\s*(\d+)\s*\|", l)] if m]
    proximo = max(ids) + 1 if ids else 1
    return proximo, linhas


def catalogar(arquivo: str, caso: str, descricao: str, data_exibida: str):
    origem = Path(arquivo).expanduser()
    if not origem.exists():
        sys.exit(f"Arquivo não encontrado: {arquivo}")

    pasta_dia = PASTA_PROVAS / date.today().strftime("%d-%m-%Y")
    pasta_caso = pasta_dia / slug(caso)
    pasta_caso.mkdir(parents=True, exist_ok=True)

    catalogo = pasta_caso / "catalogo.md"
    doc_id, linhas = proximo_id_e_linhas(catalogo)

    extensao = origem.suffix
    nome_destino = f"doc{doc_id:02d}_{origem.stem}{extensao}"
    destino = pasta_caso / nome_destino
    if destino.exists():
        sys.exit(f"Já existe um arquivo com esse nome no destino: {destino}")

    hash_sha256 = sha256_de(origem)
    shutil.copy2(origem, destino)

    recebido_em = date.today().strftime("%d/%m/%Y")
    data_exibida_fmt = f"{data_exibida} (conforme exibido na captura)" if data_exibida else "—"
    linha_nova = (
        f"| Doc. {doc_id} | {nome_destino} | {recebido_em} | {descricao} | "
        f"{data_exibida_fmt} | `{hash_sha256}` | Não |\n"
    )

    if not catalogo.exists():
        cabecalho = MODELO.read_text(encoding="utf-8").splitlines(keepends=True)[:6]
        cabecalho[0] = f"# Catálogo de provas — {caso}\n"
        catalogo.write_text("".join(cabecalho) + linha_nova, encoding="utf-8")
    else:
        with catalogo.open("a", encoding="utf-8") as f:
            f.write(linha_nova)

    print(f"Catalogado como Doc. {doc_id}")
    print(f"Arquivo: {destino}")
    print(f"Hash SHA-256: {hash_sha256}")
    print(f"Catálogo: {catalogo}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arquivo", required=True, help="Caminho do arquivo recebido (print, PDF, foto)")
    ap.add_argument("--caso", required=True, help="Nome ou nº do caso")
    ap.add_argument("--descricao", required=True, help="Descrição breve da prova")
    ap.add_argument("--data-exibida", default="", dest="data_exibida", help="Data/hora que aparece na própria prova (opcional)")

    args = ap.parse_args()
    catalogar(args.arquivo, args.caso, args.descricao, args.data_exibida)


if __name__ == "__main__":
    main()
