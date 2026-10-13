#!/usr/bin/env python3
"""
Jeito rápido de processar uma conversa exportada do WhatsApp — só aponta pro
arquivo, o resto é automático: detecta o nome do contato (o próprio WhatsApp
já coloca isso no nome do arquivo de chat dentro do export), cataloga com
hash, converte áudio pra mp3, gera o visualizador avulso, escreve no Veredata
local E sincroniza com o remoto — tudo de uma vez.

É um atalho em cima do visualizar_whatsapp.py (mesmo projeto, _tools/) —
pra controle fino (escolher áudios específicos pra transcrever, importar
correção de transcrição, etc.) use aquele script diretamente.

Uso:
    python3 processar_zap.py ~/Downloads/conversa.zip
    python3 processar_zap.py ~/Downloads/conversa.zip --caso "Nome do caso"   (se não detectar sozinho)
    python3 processar_zap.py ~/Downloads/conversa.zip --so-local             (não sincroniza com o remoto)
    python3 processar_zap.py ~/Downloads/conversa.zip --transcrever-audio --limite-audios 10
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalogar_prova import catalogar  # noqa: E402
from visualizar_whatsapp import (  # noqa: E402
    aplicar_transcricoes_em_mensagens,
    converter_audios_mp3,
    exportar_para_veredata,
    extrair_zip,
    gerar_html,
    parsear_mensagens,
    sincronizar_veredata_remoto,
    transcrever_audios,
)

PASTA_VEREDATA_PADRAO = "~/Documents/VisualizadorIPED"
PADRAO_NOME_CONTATO = re.compile(
    r"(?:Conversa do WhatsApp com|WhatsApp Chat with)\s+(.+?)\.txt$", re.IGNORECASE
)


def detectar_nome_contato(caminho_arquivo: Path):
    nomes_candidatos = []
    if caminho_arquivo.suffix.lower() == ".zip":
        with zipfile.ZipFile(caminho_arquivo) as z:
            nomes_candidatos = [n for n in z.namelist() if n.lower().endswith(".txt")]
    else:
        nomes_candidatos = [caminho_arquivo.name]

    for nome in nomes_candidatos:
        m = PADRAO_NOME_CONTATO.search(Path(nome).name)
        if m:
            return m.group(1).strip()
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo", help="Caminho do .txt ou .zip exportado do WhatsApp")
    ap.add_argument("--caso", default="", help="Nome do caso — detectado automaticamente se não informado")
    ap.add_argument("--meu-nome", default="Angelo Epifanio", dest="meu_nome", help="Padrão: Angelo Epifanio")
    ap.add_argument("--so-local", action="store_true", dest="so_local", help="Não sincroniza com o Veredata remoto, só com a cópia local")
    ap.add_argument("--transcrever-audio", action="store_true", dest="transcrever_audio")
    ap.add_argument("--limite-audios", type=int, default=0, dest="limite_audios")
    ap.add_argument("--converter-audio-mp3", action="store_true", dest="converter_audio_mp3", help="Gera cópia .mp3 de cada áudio (opcional — Chrome/Firefox já tocam .opus nativamente; só precisa pra Safari, e exige ffmpeg)")
    ap.add_argument("--veredata", default=PASTA_VEREDATA_PADRAO, help=f"Caminho do Veredata local (padrão: {PASTA_VEREDATA_PADRAO})")

    args = ap.parse_args()
    origem = Path(args.arquivo).expanduser()
    if not origem.exists():
        sys.exit(f"Arquivo não encontrado: {args.arquivo}")

    caso = args.caso.strip() or detectar_nome_contato(origem)
    if not caso:
        sys.exit(
            "Não consegui detectar o nome do caso a partir do arquivo "
            "(o export não seguiu o padrão esperado) — rode de novo com --caso \"Nome\"."
        )
    descricao = f"Conversa de WhatsApp exportada ({caso})"
    print(f"Caso detectado: {caso}")

    print("\n== 1. Catalogando o arquivo original (hash) ==")
    doc_ref = catalogar(str(origem), caso, descricao, "")
    pasta_caso = doc_ref["pasta_caso"]

    print("\n== 2. Lendo as mensagens ==")
    if origem.suffix.lower() == ".zip":
        texto_chat = extrair_zip(origem, pasta_caso / "midia")
    else:
        texto_chat = origem.read_text(encoding="utf-8", errors="replace")

    mensagens = parsear_mensagens(texto_chat)
    if not mensagens:
        sys.exit("Não consegui reconhecer nenhuma mensagem no arquivo.")
    print(f"{len(mensagens)} mensagens reconhecidas.")

    if args.converter_audio_mp3:
        converter_audios_mp3(pasta_caso / "midia")
    cache_transcricoes = aplicar_transcricoes_em_mensagens(mensagens, pasta_caso)

    if args.transcrever_audio:
        print("\n== 2.5. Transcrevendo áudios ==")
        transcrever_audios(mensagens, pasta_caso, cache_transcricoes, limite=args.limite_audios)

    print("\n== 3. Gerando o visualizador avulso ==")
    destino_html = gerar_html(mensagens, caso, args.meu_nome, doc_ref, pasta_caso)
    print(f"Visualizador: {destino_html}")

    pasta_veredata = Path(args.veredata).expanduser()
    print("\n== 4. Exportando pro Veredata local ==")
    fonte, itens_exportados, pasta_midia_destino = exportar_para_veredata(
        mensagens, caso, args.meu_nome, doc_ref, pasta_caso, pasta_veredata
    )

    if not args.so_local:
        print("\n== 5. Sincronizando com o Veredata remoto ==")
        sincronizar_veredata_remoto(fonte, itens_exportados, pasta_midia_destino, pasta_veredata)

    print(f"\nPronto. Abra o Veredata (local: http://localhost:8080{'' if args.so_local else ' ou remoto'}) e selecione a fonte '{caso}'.")


if __name__ == "__main__":
    main()
