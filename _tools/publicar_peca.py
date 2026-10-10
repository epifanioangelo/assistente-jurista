#!/usr/bin/env python3
"""
Publica uma peça processual já gerada (Pecas geradas/DD-MM-2026/*.docx|*.pdf)
no Visualizador IPED (advogado.sjc.br), pra consulta remota autenticada.

Publicação é sempre manual — o Angelo escolhe qual peça publicar depois de
revisar. Não guarda nenhuma credencial neste arquivo — lê tudo de variáveis
de ambiente, pra poder ser versionado no git sem risco. A credencial em si
fica na memória do Claude (base64), decodificada e passada por env var só no
momento do uso (mesmo padrão já usado para o FTP e pro e-mail do projeto).

Variáveis de ambiente esperadas:
    PECAS_SEGREDO   segredo compartilhado (SEGREDO_PECAS do config.php remoto)
    PECAS_URL       opcional, padrão https://advogado.sjc.br/publicar_peca.php

Uso:
    python3 publicar_peca.py --arquivo "../Pecas geradas/09-10-2026/Peticao_X.docx" \
        --caso "1500234-56.2026.8.26.0577" \
        --tipo-peca "Petição Inicial" \
        --area "Cível" \
        [--enviado-por "Angelo Epifanio"]
"""

import argparse
import os
import sys
from pathlib import Path

import requests


def _config():
    segredo = os.environ.get("PECAS_SEGREDO")
    if not segredo:
        sys.exit("Falta PECAS_SEGREDO no ambiente.")
    url = os.environ.get("PECAS_URL", "https://advogado.sjc.br/publicar_peca.php")
    return segredo, url


def publicar(arquivo: str, caso: str, tipo_peca: str, area: str, enviado_por: str):
    segredo, url = _config()

    caminho = Path(arquivo)
    if not caminho.exists():
        sys.exit(f"Arquivo não encontrado: {arquivo}")
    if caminho.suffix.lower() not in (".docx", ".pdf"):
        sys.exit("Só é possível publicar .docx ou .pdf.")

    dados = {
        "segredo": segredo,
        "caso": caso,
        "tipo_peca": tipo_peca,
        "area": area or "",
    }
    if enviado_por:
        dados["enviado_por"] = enviado_por

    # O servidor bloqueia o User-Agent padrão do requests (WAF do hosting
    # responde 406 Not Acceptable) — precisa de um UA próprio, não genérico.
    cabecalhos = {"User-Agent": "AssistenteJurista-PublicarPeca/1.0"}

    with caminho.open("rb") as fh:
        arquivos = {"arquivo": (caminho.name, fh)}
        resp = requests.post(url, data=dados, files=arquivos, headers=cabecalhos, timeout=30)

    resp.raise_for_status()
    corpo = resp.json()
    if not corpo.get("ok"):
        sys.exit(f"Falha ao publicar: {corpo.get('erro')}")

    base = url.rsplit("/publicar_peca.php", 1)[0]
    link = f"{base}/baixar_peca.php?id={corpo['id']}&token={corpo['token']}"

    print(f"Peça publicada com sucesso — id: {corpo['id']}")
    print(f"Arquivo: {caminho.name}")
    print(f"Caso: {caso}")
    print(f"Link p/ compartilhar (sem login, baixa só esse arquivo): {link}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arquivo", required=True, help="Caminho do .docx ou .pdf já gerado")
    ap.add_argument("--caso", required=True, help="Nome do caso ou nº do processo")
    ap.add_argument("--tipo-peca", required=True, dest="tipo_peca", help="Ex: Petição Inicial, Habeas Corpus")
    ap.add_argument("--area", default="", help="Ex: Cível, Penal, Trabalhista")
    ap.add_argument("--enviado-por", default="", dest="enviado_por", help="Opcional — padrão é o nome da instalação remota")

    args = ap.parse_args()
    publicar(args.arquivo, args.caso, args.tipo_peca, args.area, args.enviado_por)


if __name__ == "__main__":
    main()
