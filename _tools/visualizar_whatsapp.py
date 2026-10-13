#!/usr/bin/env python3
"""
Lê uma conversa exportada do WhatsApp (recurso nativo "Exportar conversa",
.txt solto ou .zip com mídia) e gera uma página HTML local, navegável, com
as mensagens em formato de balão, busca por palavra-chave e estrela pra
marcar as relevantes enquanto você lê. No fim, o botão "Exportar seleção"
baixa um .json com as mensagens marcadas, pra citar na peça.

Isso NÃO é o Veredata/IPED — esse arquivo já chega pronto e legível, exportado
pelo próprio dono do celular, não precisa de processamento forense nenhum.
O arquivo original (.txt/.zip) é catalogado como prova (hash SHA-256) antes
de qualquer coisa, via o mesmo mecanismo do catalogar_prova.py — o que esse
script gera depois é só uma ferramenta de leitura/seleção em cima dele.

Uso:
    python3 visualizar_whatsapp.py --arquivo ~/Downloads/conversa.zip \
        --caso "Maria Aparecida Amaral" \
        --descricao "Exportação da conversa com o locador, enviada pelo cliente" \
        [--meu-nome "Maria Aparecida"] [--transcrever-audio]

--transcrever-audio transcreve cada mensagem de voz (faster-whisper, local,
modelo "small") pra texto buscável — opcional porque é mais lento (processa
tudo antes de gerar a página) e exige `pip3 install faster-whisper` à parte.
Por padrão transcreve tudo (ou --limite-audios N mais recentes); pra escolher
exatamente quais, marque com ★ no visualizador, clique "Exportar seleção" e
rode de novo com --arquivo-selecao mensagens_selecionadas.json.

Transcrições ficam num cache (transcricoes.json, na pasta do caso) — rodar o
script de novo não retranscreve o que já foi feito. Pra corrigir um erro de
transcrição sem mexer no áudio original: edite direto no visualizador (ícone
✏️ ao lado da transcrição), clique "Exportar correções de transcrição", e
rode de novo com --importar-correcoes correcoes_transcricao.json — a versão
automática original fica preservada no cache, só a exibição passa a mostrar
a corrigida, sempre rotulada "(revisado manualmente)".

--exportar-veredata [caminho] escreve a conversa direto no Veredata (mesmo
padrão de visualização do IPED — login, busca, ★, Conversas/Galeria/
Documentos), em vez do HTML avulso. Caminho opcional, padrão
~/Documents/VisualizadorIPED. Reexecutar substitui os itens dessa mesma
fonte (nunca duplica).

Formato do .txt esperado (ambos reconhecidos):
    14/03/2026 23:41 - Roberto: Precisa terminar o relatório hoje
    [14/03/2026, 23:41:00] Roberto: Precisa terminar o relatório hoje
Mídia reconhecida via "<anexado: arquivo.jpg>" ou "<Mídia oculta>". O formato
varia um pouco por versão do WhatsApp/idioma do aparelho — se alguma mensagem
não for reconhecida, ela aparece colada na anterior; confira visualmente.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from catalogar_prova import catalogar  # noqa: E402

PADRAO_COLCHETE = re.compile(
    r"^\[(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(?:([^:]+?):\s*)?(.*)$"
)
PADRAO_TRACO = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*(?:([^:]+?):\s*)?(.*)$"
)
PADRAO_ANEXO = re.compile(r"<anexado:\s*(.+?)>", re.IGNORECASE)
PADRAO_ANEXO_ANTIGO = re.compile(r"[‎‏]*([\w,\.\-]+\.\w{2,5})\s*\(arquivo anexado\)", re.IGNORECASE)
PADRAO_OCULTA = re.compile(r"<?\s*(?:mídia oculta|media omitted|arquivo de mídia oculto)\s*>?", re.IGNORECASE)
MARCAS_INVISIVEIS = re.compile(r"[‎‏﻿]")

EXT_IMAGEM = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
EXT_VIDEO = {".mp4", ".mov", ".avi"}
EXT_AUDIO = {".opus", ".mp3", ".m4a", ".ogg"}


def parsear_mensagens(texto: str) -> list[dict]:
    mensagens = []
    for linha in texto.splitlines():
        linha = linha.strip("﻿‎‏ ")
        if not linha:
            continue
        m = PADRAO_COLCHETE.match(linha) or PADRAO_TRACO.match(linha)
        if m:
            data, hora, remetente, texto_msg = m.groups()
            mensagens.append({
                "data": data, "hora": hora,
                "remetente": MARCAS_INVISIVEIS.sub("", (remetente or "Sistema")).strip(),
                "texto": MARCAS_INVISIVEIS.sub("", texto_msg).strip(),
                "midia": None,
            })
        elif mensagens:
            mensagens[-1]["texto"] += "\n" + MARCAS_INVISIVEIS.sub("", linha)

    for msg in mensagens:
        m_anexo = PADRAO_ANEXO.search(msg["texto"]) or PADRAO_ANEXO_ANTIGO.search(msg["texto"])
        if m_anexo:
            msg["midia"] = m_anexo.group(1).strip()
            msg["texto"] = (PADRAO_ANEXO.sub("", msg["texto"]) if PADRAO_ANEXO.search(msg["texto"]) else PADRAO_ANEXO_ANTIGO.sub("", msg["texto"])).strip()
        elif PADRAO_OCULTA.search(msg["texto"]):
            msg["midia"] = "__OCULTA__"
            msg["texto"] = PADRAO_OCULTA.sub("", msg["texto"]).strip()
    return mensagens


def extrair_zip(caminho_zip: Path, destino_midia: Path) -> str:
    destino_midia.mkdir(parents=True, exist_ok=True)
    texto_chat = ""
    with zipfile.ZipFile(caminho_zip) as z:
        for nome in z.namelist():
            if nome.endswith(".txt"):
                texto_chat = z.read(nome).decode("utf-8", errors="replace")
            else:
                destino_arquivo = destino_midia / Path(nome).name
                with z.open(nome) as origem, destino_arquivo.open("wb") as dest:
                    shutil.copyfileobj(origem, dest)
    if not texto_chat:
        sys.exit("Não encontrei um arquivo .txt dentro do .zip.")
    return texto_chat


def converter_audios_mp3(pasta_midia: Path):
    """
    Gera uma cópia em .mp3 de cada áudio (.opus etc.) pra tocar no navegador.
    O Safari não toca Opus/Ogg de forma confiável em <audio>, mesmo com o
    arquivo original perfeito — a cópia .mp3 resolve isso sem mexer no
    arquivo original (que continua sendo o que foi catalogado/hasheado).
    """
    if not pasta_midia.exists():
        return
    arquivos = [f for f in pasta_midia.iterdir() if f.suffix.lower() in EXT_AUDIO and f.suffix.lower() != ".mp3"]
    pendentes = [f for f in arquivos if not f.with_suffix(".mp3").exists()]
    if not pendentes:
        return

    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("ffmpeg não encontrado — pulando conversão pra .mp3 (áudio pode não tocar em todos os navegadores).")
        return

    print(f"Convertendo {len(pendentes)} áudio(s) pra .mp3 (compatibilidade de navegador)...")
    falhas = 0
    for arq in pendentes:
        destino = arq.with_suffix(".mp3")
        r = subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(arq), "-codec:a", "libmp3lame", "-qscale:a", "4", str(destino)],
            capture_output=True,
        )
        if r.returncode != 0:
            falhas += 1
    if falhas:
        print(f"  {falhas} arquivo(s) não converteram — tocam só se o navegador suportar o formato original.")


def _chave_data_hora(msg: dict):
    try:
        dia, mes, ano = (int(p) for p in msg["data"].split("/"))
        if ano < 100:
            ano += 2000
        partes_hora = msg["hora"].split(":")
        h, mi = int(partes_hora[0]), int(partes_hora[1])
        s = int(partes_hora[2]) if len(partes_hora) > 2 else 0
        return (ano, mes, dia, h, mi, s)
    except (ValueError, IndexError):
        return (0, 0, 0, 0, 0, 0)


def _caminho_cache_transcricoes(pasta_caso: Path) -> Path:
    return pasta_caso / "transcricoes.json"


def carregar_cache_transcricoes(pasta_caso: Path) -> dict:
    caminho = _caminho_cache_transcricoes(pasta_caso)
    if caminho.exists():
        return json.loads(caminho.read_text(encoding="utf-8"))
    return {}


def salvar_cache_transcricoes(pasta_caso: Path, cache: dict):
    _caminho_cache_transcricoes(pasta_caso).write_text(
        json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def aplicar_transcricoes_em_mensagens(mensagens: list[dict], pasta_caso: Path) -> dict:
    """Preenche msg['transcricao'/'transcricaoAuto'/'transcricaoEditada'/'editadoEm']
    a partir do cache persistente — roda sempre, mesmo sem --transcrever-audio,
    pra não perder transcrições/correções já feitas em rodadas anteriores."""
    cache = carregar_cache_transcricoes(pasta_caso)
    for msg in mensagens:
        entrada = cache.get(msg.get("midia") or "")
        if not entrada:
            msg["transcricao"] = msg.get("transcricao", "")
            msg["transcricaoAuto"] = ""
            msg["transcricaoEditada"] = None
            msg["editadoEm"] = None
            continue
        msg["transcricaoAuto"] = entrada.get("transcricao_automatica", "")
        msg["transcricaoEditada"] = entrada.get("transcricao_editada")
        msg["editadoEm"] = entrada.get("editado_em")
        msg["transcricao"] = entrada.get("transcricao_editada") or entrada.get("transcricao_automatica", "")
    return cache


def carregar_filenames_da_selecao(caminho_json: str) -> set:
    """Lê o .json baixado pelo botão 'Exportar seleção' do visualizador e
    devolve o conjunto de nomes de arquivo de áudio marcados — pra transcrever
    só o que o advogado escolheu, não a conversa inteira."""
    dados = json.loads(Path(caminho_json).expanduser().read_text(encoding="utf-8"))
    return {d["nomeMidia"] for d in dados if d.get("tipoMidia") == "audio" and d.get("nomeMidia")}


def importar_correcoes_transcricao(caminho_json: str, pasta_caso: Path):
    """Lê o .json baixado pelo botão 'Exportar correções' (texto editado à mão
    pelo advogado) e grava no cache, sem nunca tocar no áudio original."""
    correcoes = json.loads(Path(caminho_json).expanduser().read_text(encoding="utf-8"))
    cache = carregar_cache_transcricoes(pasta_caso)
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")
    for nome_arquivo, texto in correcoes.items():
        cache.setdefault(nome_arquivo, {})
        cache[nome_arquivo]["transcricao_editada"] = texto
        cache[nome_arquivo]["editado_em"] = agora
    salvar_cache_transcricoes(pasta_caso, cache)
    print(f"{len(correcoes)} correção(ões) de transcrição importada(s).")


def transcrever_audios(mensagens: list[dict], pasta_caso: Path, cache: dict, limite: int = 0, arquivos_alvo: set = None):
    import warnings
    # RuntimeWarning (divide by zero/overflow) do numpy no cálculo do espectro
    # mel, no feature_extractor do faster-whisper — testado com áudios reais
    # (até 4min) sem efeito na qualidade da transcrição; só polui o terminal.
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="faster_whisper")

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper não instalado. Rode: pip3 install faster-whisper")

    candidatos = [m for m in mensagens if m["midia"] and m["midia"] != "__OCULTA__"
                  and Path(m["midia"]).suffix.lower() in EXT_AUDIO
                  and (pasta_caso / "midia" / m["midia"]).exists()]

    if arquivos_alvo is not None:
        candidatos = [m for m in candidatos if m["midia"] in arquivos_alvo]
        print(f"Transcrevendo só os {len(candidatos)} áudio(s) selecionado(s) no visualizador.")

    # nunca retranscreve o que já está no cache (economiza tempo em reexecuções)
    pendentes = [m for m in candidatos if not cache.get(m["midia"], {}).get("transcricao_automatica")]

    if not candidatos:
        print("Nenhum áudio encontrado pra transcrever (confira a seleção/arquivo).")
        return
    if not pendentes:
        print("Todos os áudios dessa seleção já tinham transcrição em cache — nada novo a fazer.")
        return

    if limite and arquivos_alvo is None:
        pendentes = sorted(pendentes, key=_chave_data_hora, reverse=True)[:limite]
        print(f"Limitado às {len(pendentes)} mensagens de áudio mais recentes.")

    print(f"Carregando modelo de transcrição (1ª vez pode levar um pouco)...")
    model = WhisperModel("small", device="cpu", compute_type="int8")

    for i, msg in enumerate(pendentes, 1):
        caminho = pasta_caso / "midia" / msg["midia"]
        try:
            segments, _info = model.transcribe(str(caminho), language="pt")
            texto = " ".join(s.text.strip() for s in segments).strip()
        except Exception as e:
            print(f"  [{i}/{len(pendentes)}] falhou ({msg['midia']}): {e}")
            continue
        cache.setdefault(msg["midia"], {})["transcricao_automatica"] = texto
        msg["transcricao"] = cache[msg["midia"]].get("transcricao_editada") or texto
        msg["transcricaoAuto"] = texto
        if i % 20 == 0 or i == len(pendentes):
            print(f"  [{i}/{len(pendentes)}] transcritos...")

    salvar_cache_transcricoes(pasta_caso, cache)


def gerar_html(mensagens: list[dict], caso: str, meu_nome: str, doc_ref: dict, pasta_destino: Path) -> Path:
    tem_midia_local = any((pasta_destino / "midia").glob("*")) if (pasta_destino / "midia").exists() else False

    def classificar_midia(nome):
        if not nome:
            return "", "", ""
        if nome == "__OCULTA__":
            return "oculta_sem_arquivo", "", ""
        caminho = pasta_destino / "midia" / nome
        if not caminho.exists():
            return "ausente", nome, nome
        ext = caminho.suffix.lower()
        if ext in EXT_IMAGEM:
            return "imagem", nome, nome
        if ext in EXT_VIDEO:
            return "video", nome, nome
        if ext in EXT_AUDIO:
            # cópia .mp3 (gerada por converter_audios_mp3) toca em qualquer
            # navegador; o .opus original continua sendo o arquivo catalogado
            caminho_mp3 = caminho.with_suffix(".mp3")
            tocavel = caminho_mp3.name if caminho_mp3.exists() else nome
            return "audio", nome, tocavel
        return "arquivo", nome, nome

    dados_js = []
    for i, msg in enumerate(mensagens):
        tipo_midia, nome_midia, arquivo_audio = classificar_midia(msg["midia"])
        dados_js.append({
            "id": i,
            "data": msg["data"], "hora": msg["hora"], "remetente": msg["remetente"],
            "texto": msg["texto"], "eu": msg["remetente"].strip().lower() == meu_nome.strip().lower() if meu_nome else False,
            "tipoMidia": tipo_midia, "nomeMidia": nome_midia, "arquivoAudio": arquivo_audio,
            "transcricao": msg.get("transcricao", ""),
            "transcricaoAuto": msg.get("transcricaoAuto", ""),
            "transcricaoEditada": msg.get("transcricaoEditada"),
            "editadoEm": msg.get("editadoEm"),
        })

    html = HTML_TEMPLATE.replace("__CASO__", caso.replace("</", "<\\/")) \
        .replace("__DOC_REF__", f"Doc. {doc_ref['doc_id']} · hash {doc_ref['hash'][:16]}...") \
        .replace("__TOTAL__", str(len(mensagens))) \
        .replace("__DADOS_JSON__", json.dumps(dados_js, ensure_ascii=False))

    destino = pasta_destino / "visualizador_conversa.html"
    destino.write_text(html, encoding="utf-8")
    return destino


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Conversa — __CASO__</title>
<style>
  :root{
    --bg:#efeae2; --surface:#fff; --surface-2:#f0f2f5; --border:#d8dbdf;
    --fg:#111b21; --fg-muted:#667781; --accent:#1e3a5f; --accent-fg:#fff;
    --bolha-outro:#fff; --bolha-eu:#d9fdd3; --warn:#9a6a1f; --warn-soft:#faf0dc;
  }
  @media (prefers-color-scheme: dark){
    :root{ --bg:#0b141a; --surface:#111b21; --surface-2:#202c33; --border:#2a3942;
      --fg:#e9edef; --fg-muted:#8696a0; --accent:#6f9bd4; --accent-fg:#0d1420;
      --bolha-outro:#202c33; --bolha-eu:#005c4b; --warn:#e0ad5c; --warn-soft:#2e2515; }
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--fg);font-family:-apple-system,system-ui,Arial,sans-serif;font-size:14px}
  .topo{position:sticky;top:0;z-index:5;background:var(--surface);border-bottom:1px solid var(--border);padding:10px 16px}
  .topo-linha1{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
  .topo h1{font-size:1rem;margin:0}
  .topo .ref{font-size:.72rem;color:var(--fg-muted);font-family:ui-monospace,Menlo,monospace}
  .busca{width:100%;margin-top:8px;padding:9px 12px;border-radius:8px;border:1px solid var(--border);background:var(--surface-2);color:var(--fg);font-size:.88rem}
  .aviso{background:var(--warn-soft);color:var(--warn);font-size:.76rem;padding:8px 16px;text-align:center}

  .lista{max-width:720px;margin:0 auto;padding:16px}
  .msg{display:flex;margin-bottom:8px}
  .msg.eu{justify-content:flex-end}
  .bolha{max-width:75%;padding:7px 10px 8px;border-radius:9px;background:var(--bolha-outro);position:relative;box-shadow:0 1px 1px rgba(0,0,0,.08)}
  .msg.eu .bolha{background:var(--bolha-eu)}
  .remetente{font-size:.76rem;font-weight:700;color:var(--accent);margin-bottom:2px}
  .texto{white-space:pre-wrap;font-size:.92rem;line-height:1.4}
  .rodape-msg{display:flex;justify-content:flex-end;align-items:center;gap:6px;margin-top:3px}
  .hora{font-size:.68rem;color:var(--fg-muted)}
  .estrela{cursor:pointer;font-size:1rem;color:var(--fg-muted);user-select:none;background:none;border:none;padding:0}
  .estrela.marcada{color:#f0ad4e}
  .midia{margin-bottom:5px}
  .midia img{max-width:100%;border-radius:6px;display:block}
  .midia video{max-width:100%;border-radius:6px}
  .midia .arquivo-generico{font-size:.8rem;background:var(--surface-2);padding:6px 10px;border-radius:6px;display:inline-block}
  .midia .ausente{font-size:.78rem;color:var(--fg-muted);font-style:italic}
  .btn-audio{background:var(--accent);color:var(--accent-fg);border:none;padding:8px 16px;border-radius:20px;font-size:.84rem;font-weight:600;cursor:pointer}
  .transcricao{font-size:.86rem;margin-top:5px;color:var(--fg)}
  .transcricao .rotulo-auto{font-size:.68rem;color:var(--fg-muted);font-style:italic}
  .btn-editar-transc{background:none;border:none;cursor:pointer;font-size:.8rem;opacity:.7;padding:0 0 0 4px}
  .btn-editar-transc:hover{opacity:1}
  .edit-transcricao{width:100%;min-height:60px;font-size:.86rem;font-family:inherit;padding:6px;border-radius:6px;border:1px solid var(--border);background:var(--surface);color:var(--fg);box-sizing:border-box}
  .acoes-edit-transc{display:flex;gap:8px;margin-top:4px}
  .acoes-edit-transc button{font-size:.76rem;padding:4px 10px;border-radius:6px;border:1px solid var(--border);background:var(--surface-2);cursor:pointer}
  .btn-salvar-transc{background:var(--accent) !important;color:var(--accent-fg) !important;border:none !important}
  .separador-dia{text-align:center;margin:18px 0 10px;font-size:.74rem;color:var(--fg-muted)}
  .oculta{display:none !important}

  .barra-inferior{position:sticky;bottom:0;background:var(--surface);border-top:1px solid var(--border);padding:10px 16px;display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap}
  .barra-inferior b{font-size:.85rem}
  .btn{background:var(--accent);color:var(--accent-fg);border:none;padding:9px 18px;border-radius:8px;font-weight:700;font-size:.82rem;cursor:pointer}
</style>
</head>
<body>

<div class="topo">
  <div class="topo-linha1">
    <h1>__CASO__</h1>
    <span class="ref">__DOC_REF__ · __TOTAL__ mensagens</span>
  </div>
  <input class="busca" id="busca" type="text" placeholder="Buscar por palavra ou remetente...">
</div>
<div class="aviso">Leitura local da conversa exportada pelo cliente — ainda não verificado tecnicamente (ver catalogo.md). Marque com ★ o que for relevante.</div>

<div class="lista" id="lista"></div>

<div class="barra-inferior">
  <b id="contador">0 marcadas</b>
  <div style="display:flex;gap:8px;flex-wrap:wrap">
    <button class="btn secundario" id="btnExportarCorrecoes">Exportar correções de transcrição (.json)</button>
    <button class="btn" id="btnExportar">Exportar seleção (.json)</button>
  </div>
</div>

<script>
const MENSAGENS = __DADOS_JSON__;
const marcadas = new Set();
const correcoes = {}; // nomeMidia -> texto corrigido à mão, só nesta sessão até exportar

function blocoTranscricao(m){
  if (!m.transcricaoAuto && !m.transcricaoEditada && !(m.nomeMidia in correcoes)) return '';
  const corrigidoNaSessao = m.nomeMidia in correcoes;
  const textoAtual = corrigidoNaSessao ? correcoes[m.nomeMidia] : (m.transcricaoEditada || m.transcricaoAuto);
  const foiRevisado = corrigidoNaSessao || !!m.transcricaoEditada;
  const rotulo = foiRevisado ? `(revisado manualmente${m.editadoEm ? ' em ' + m.editadoEm : ''})` : '(transcrição automática)';
  return `<div class="transcricao" data-id="${m.id}">
    <span class="texto-transcricao">🗣 ${(textoAtual || '').replace(/</g,'&lt;')}</span>
    <span class="rotulo-auto">${rotulo}</span>
    <button class="btn-editar-transc" data-editar="${m.id}" title="Editar transcrição">✏️</button>
  </div>`;
}

function bolhaHtml(m){
  let midiaHtml = '';
  if (m.tipoMidia === 'imagem') midiaHtml = `<div class="midia"><img src="midia/${encodeURIComponent(m.nomeMidia)}" loading="lazy"></div>`;
  else if (m.tipoMidia === 'video') midiaHtml = `<div class="midia"><video src="midia/${encodeURIComponent(m.nomeMidia)}" controls></video></div>`;
  else if (m.tipoMidia === 'audio') midiaHtml = `<div class="midia"><button class="btn-audio" data-tocar="midia/${encodeURIComponent(m.arquivoAudio)}">▶ Tocar áudio</button>${blocoTranscricao(m)}</div>`;
  else if (m.tipoMidia === 'ausente') midiaHtml = `<div class="midia ausente">📎 ${m.nomeMidia} (arquivo não encontrado na pasta midia/)</div>`;
  else if (m.tipoMidia === 'oculta_sem_arquivo') midiaHtml = `<div class="midia ausente">🎞️ Mídia não incluída nesta exportação</div>`;
  else if (m.tipoMidia === 'arquivo') midiaHtml = `<div class="midia"><span class="arquivo-generico">📎 ${m.nomeMidia}</span></div>`;

  return `<div class="msg ${m.eu ? 'eu' : ''}" data-id="${m.id}" data-busca="${(m.texto + ' ' + m.remetente + ' ' + m.transcricao).toLowerCase().replace(/"/g,'')}">
    <div class="bolha">
      ${m.eu ? '' : `<div class="remetente">${m.remetente}</div>`}
      ${midiaHtml}
      ${m.texto ? `<div class="texto">${m.texto.replace(/</g,'&lt;')}</div>` : ''}
      <div class="rodape-msg">
        <span class="hora">${m.data} ${m.hora}</span>
        <button class="estrela" data-marcar="${m.id}">★</button>
      </div>
    </div>
  </div>`;
}

function render(){
  document.getElementById('lista').innerHTML = MENSAGENS.map(bolhaHtml).join('');
  document.querySelectorAll('[data-marcar]').forEach(b => {
    b.addEventListener('click', () => {
      const id = parseInt(b.dataset.marcar);
      if (marcadas.has(id)) marcadas.delete(id); else marcadas.add(id);
      b.classList.toggle('marcada');
      document.getElementById('contador').textContent = marcadas.size + ' marcada' + (marcadas.size === 1 ? '' : 's');
    });
  });
}
render();

// Áudio só vira <audio> de verdade quando clicado — com milhares de
// mensagens de áudio na página, criar todos de uma vez estoura o limite de
// players do Chrome (erro real: "too many WebMediaPlayers already in
// existence"), e os áudios mais embaixo na conversa simplesmente não tocam.
document.getElementById('lista').addEventListener('click', (e) => {
  const btnAudio = e.target.closest('.btn-audio');
  if (btnAudio) {
    const audio = document.createElement('audio');
    audio.src = btnAudio.dataset.tocar;
    audio.controls = true;
    audio.autoplay = true;
    audio.style.width = '100%';
    btnAudio.replaceWith(audio);
    return;
  }

  const btnEditar = e.target.closest('.btn-editar-transc');
  if (btnEditar) {
    const bloco = btnEditar.closest('.transcricao');
    const m = MENSAGENS[parseInt(btnEditar.dataset.editar)];
    const textoAtual = (m.nomeMidia in correcoes) ? correcoes[m.nomeMidia] : (m.transcricaoEditada || m.transcricaoAuto || '');
    bloco.innerHTML = `<textarea class="edit-transcricao">${textoAtual}</textarea>
      <div class="acoes-edit-transc">
        <button class="btn-cancelar-transc" data-cancelar="${m.id}">Cancelar</button>
        <button class="btn-salvar-transc" data-salvar="${m.id}">Salvar correção</button>
      </div>`;
    return;
  }

  const btnCancelar = e.target.closest('.btn-cancelar-transc');
  if (btnCancelar) {
    const m = MENSAGENS[parseInt(btnCancelar.dataset.cancelar)];
    btnCancelar.closest('.transcricao').outerHTML = blocoTranscricao(m);
    return;
  }

  const btnSalvar = e.target.closest('.btn-salvar-transc');
  if (btnSalvar) {
    const bloco = btnSalvar.closest('.transcricao');
    const m = MENSAGENS[parseInt(btnSalvar.dataset.salvar)];
    const novoTexto = bloco.querySelector('textarea').value.trim();
    correcoes[m.nomeMidia] = novoTexto;
    m.transcricao = novoTexto;
    const msgEl = bloco.closest('.msg');
    if (msgEl) msgEl.dataset.busca = (m.texto + ' ' + m.remetente + ' ' + novoTexto).toLowerCase().replace(/"/g, '');
    bloco.outerHTML = blocoTranscricao(m);
    return;
  }
});

document.getElementById('busca').addEventListener('input', (e) => {
  const termo = e.target.value.toLowerCase();
  document.querySelectorAll('.msg').forEach(el => {
    el.classList.toggle('oculta', termo !== '' && !el.dataset.busca.includes(termo));
  });
});

document.getElementById('btnExportar').addEventListener('click', () => {
  const selecionadas = MENSAGENS.filter(m => marcadas.has(m.id));
  const blob = new Blob([JSON.stringify(selecionadas, null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'mensagens_selecionadas.json';
  a.click();
});

document.getElementById('btnExportarCorrecoes').addEventListener('click', () => {
  if (Object.keys(correcoes).length === 0) {
    alert('Nenhuma correção de transcrição feita nesta sessão ainda.');
    return;
  }
  const blob = new Blob([JSON.stringify(correcoes, null, 2)], {type: 'application/json'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'correcoes_transcricao.json';
  a.click();
});
</script>
</body>
</html>
"""


def _slug_fonte(caso: str, doc_id: int) -> str:
    base = re.sub(r"[^a-z0-9]+", "_", caso.lower()).strip("_")
    return f"wa_{base}_{doc_id}"


def _duracao_audio(caminho: Path) -> str:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(caminho)],
            capture_output=True, text=True, timeout=10,
        )
        seg = float(r.stdout.strip())
        return f"{int(seg // 60)}:{int(seg % 60):02d}"
    except (ValueError, subprocess.SubprocessError, FileNotFoundError):
        return ""


def _tamanho_legivel(caminho: Path) -> str:
    n = caminho.stat().st_size
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.0f} KB"
    return f"{n / 1024 / 1024:.1f} MB"


def exportar_para_veredata(mensagens: list[dict], caso: str, meu_nome: str, doc_ref: dict, pasta_caso: Path, pasta_veredata: Path):
    """
    Escreve a conversa direto no formato de dados do Veredata (casos.json +
    casos_itens.json) e copia a mídia pra _casos_midia/<fonte>/ de lá — a
    conversa passa a aparecer dentro do Veredata (Conversas/Galeria/
    Documentos), com login, busca e marcação ★, igual um caso forense do
    IPED. Mesma máquina, cópia de arquivo local — nenhuma rede envolvida.
    """
    pasta_dados = pasta_veredata / "_dados"
    if not pasta_dados.is_dir():
        sys.exit(f"Não encontrei {pasta_dados} — confira o caminho do Veredata (--exportar-veredata).")

    fonte_id = _slug_fonte(caso, doc_ref["doc_id"])
    pasta_midia_destino = pasta_veredata / "_casos_midia" / fonte_id
    pasta_midia_destino.mkdir(parents=True, exist_ok=True)
    pasta_midia_origem = pasta_caso / "midia"

    def caminho_json(nome):
        c = pasta_dados / nome
        if c.exists():
            return json.loads(c.read_text(encoding="utf-8"))
        return []

    def salvar_json(nome, dados):
        (pasta_dados / nome).write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

    casos = caminho_json("casos.json")
    casos = [c for c in casos if c.get("id") != fonte_id]
    casos.append({"id": fonte_id, "nome": caso})
    salvar_json("casos.json", casos)

    itens_existentes = caminho_json("casos_itens.json")
    itens_existentes = [i for i in itens_existentes if i.get("fonte") != fonte_id]
    proximo_id = max([10] + [int(i.get("id", 0)) for i in itens_existentes]) + 1

    novos_itens = []
    copiados = 0
    for msg in mensagens:
        quando_iso = ""
        try:
            d, m_, a = (int(p) for p in msg["data"].split("/"))
            if a < 100:
                a += 2000
            partes = msg["hora"].split(":")
            h, mi = partes[0], partes[1]
            s = partes[2] if len(partes) > 2 else "00"
            quando_iso = f"{a:04d}-{m_:02d}-{d:02d}T{h.zfill(2)}:{mi.zfill(2)}:{s.zfill(2)}"
        except (ValueError, IndexError):
            pass

        base = {
            "id": proximo_id, "fonte": fonte_id, "de": msg["remetente"],
            "eu": bool(meu_nome) and msg["remetente"].strip().lower() == meu_nome.strip().lower(),
            "quando": quando_iso, "hash": doc_ref["hash"],
        }

        midia_nome = msg.get("midia")
        if not midia_nome or midia_nome == "__OCULTA__":
            if msg["texto"]:
                novos_itens.append({**base, "categoria": "mensagens", "tipo": "whatsapp", "texto": msg["texto"]})
                proximo_id += 1
            continue

        ext = Path(midia_nome).suffix.lower()
        origem_arquivo = pasta_midia_origem / midia_nome
        arquivo_a_servir = None
        if origem_arquivo.exists():
            nome_servido = midia_nome
            if ext in EXT_AUDIO and ext != ".mp3" and origem_arquivo.with_suffix(".mp3").exists():
                origem_arquivo = origem_arquivo.with_suffix(".mp3")
                nome_servido = origem_arquivo.name
            destino_arquivo = pasta_midia_destino / nome_servido
            if not destino_arquivo.exists():
                shutil.copy2(origem_arquivo, destino_arquivo)
                copiados += 1
            arquivo_a_servir = nome_servido

        if ext in EXT_AUDIO:
            item = {**base, "categoria": "mensagens", "tipo": "audio", "texto": msg.get("transcricao", "")}
            if arquivo_a_servir:
                item["arquivo"] = arquivo_a_servir
                item["duracao"] = _duracao_audio(pasta_midia_destino / arquivo_a_servir)
        elif ext in EXT_IMAGEM:
            item = {**base, "categoria": "fotos", "tipo": "foto", "titulo": midia_nome}
            if arquivo_a_servir:
                item["arquivo"] = arquivo_a_servir
        elif ext in EXT_VIDEO:
            item = {**base, "categoria": "fotos", "tipo": "video", "titulo": midia_nome}
            if arquivo_a_servir:
                item["arquivo"] = arquivo_a_servir
        else:
            item = {**base, "categoria": "documentos", "tipo": ext.lstrip(".") or "arquivo", "titulo": midia_nome}
            if arquivo_a_servir:
                item["arquivo"] = arquivo_a_servir
                item["tamanho"] = _tamanho_legivel(pasta_midia_destino / arquivo_a_servir)

        novos_itens.append(item)
        proximo_id += 1

    itens_existentes.extend(novos_itens)
    salvar_json("casos_itens.json", itens_existentes)

    print(f"Exportado pro Veredata como fonte '{fonte_id}': {len(novos_itens)} item(ns), {copiados} arquivo(s) de mídia copiado(s).")
    print(f"Abra o Veredata (index.php) e selecione essa fonte no menu — a conversa aparece em Conversas/Galeria/Documentos.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arquivo", required=True, help="Caminho do .txt ou .zip exportado do WhatsApp")
    ap.add_argument("--caso", required=True, help="Nome ou nº do caso")
    ap.add_argument("--descricao", required=True, help="Descrição breve (vai pro catálogo do arquivo original)")
    ap.add_argument("--meu-nome", default="", dest="meu_nome", help="Nome exibido pro dono do celular, pra alinhar as mensagens dele à direita (opcional)")
    ap.add_argument("--transcrever-audio", action="store_true", dest="transcrever_audio", help="Transcreve cada mensagem de voz com faster-whisper (local), deixando-as buscáveis (opcional, mais lento)")
    ap.add_argument("--limite-audios", type=int, default=0, dest="limite_audios", help="Transcreve só as N mensagens de áudio mais recentes, em vez de todas (ignorado se --arquivo-selecao for usado)")
    ap.add_argument("--arquivo-selecao", default="", dest="arquivo_selecao", help="Transcreve só os áudios marcados com ★ e exportados pelo botão 'Exportar seleção' do visualizador (um mensagens_selecionadas.json)")
    ap.add_argument("--importar-correcoes", default="", dest="importar_correcoes", help="Importa o .json baixado pelo botão 'Exportar correções de transcrição' — grava as correções no cache sem alterar o áudio original")
    ap.add_argument("--exportar-veredata", nargs="?", const="~/Documents/VisualizadorIPED", default="", dest="exportar_veredata", help="Escreve a conversa direto no Veredata (casos.json/casos_itens.json), pra abrir lá com login/busca/★ — caminho opcional, padrão ~/Documents/VisualizadorIPED")

    args = ap.parse_args()
    origem = Path(args.arquivo).expanduser()
    if not origem.exists():
        sys.exit(f"Arquivo não encontrado: {args.arquivo}")

    print("== 1. Catalogando o arquivo original (hash) ==")
    doc_ref = catalogar(str(origem), args.caso, args.descricao, "")
    pasta_caso = doc_ref["pasta_caso"]

    print("\n== 2. Lendo as mensagens ==")
    if origem.suffix.lower() == ".zip":
        texto_chat = extrair_zip(origem, pasta_caso / "midia")
    else:
        texto_chat = origem.read_text(encoding="utf-8", errors="replace")

    mensagens = parsear_mensagens(texto_chat)
    if not mensagens:
        sys.exit("Não consegui reconhecer nenhuma mensagem no arquivo — confira o formato do .txt exportado.")
    print(f"{len(mensagens)} mensagens reconhecidas.")

    converter_audios_mp3(pasta_caso / "midia")

    if args.importar_correcoes:
        importar_correcoes_transcricao(args.importar_correcoes, pasta_caso)

    cache_transcricoes = aplicar_transcricoes_em_mensagens(mensagens, pasta_caso)

    if args.transcrever_audio:
        print("\n== 2.5. Transcrevendo áudios ==")
        arquivos_alvo = carregar_filenames_da_selecao(args.arquivo_selecao) if args.arquivo_selecao else None
        transcrever_audios(mensagens, pasta_caso, cache_transcricoes, limite=args.limite_audios, arquivos_alvo=arquivos_alvo)

    print("\n== 3. Gerando o visualizador ==")
    destino_html = gerar_html(mensagens, args.caso, args.meu_nome, doc_ref, pasta_caso)
    print(f"Visualizador: {destino_html}")
    print("Abra esse arquivo no navegador pra ler, buscar e marcar as mensagens relevantes.")

    if args.exportar_veredata:
        print("\n== 4. Exportando pro Veredata ==")
        pasta_veredata = Path(args.exportar_veredata).expanduser()
        exportar_para_veredata(mensagens, args.caso, args.meu_nome, doc_ref, pasta_caso, pasta_veredata)


if __name__ == "__main__":
    main()
