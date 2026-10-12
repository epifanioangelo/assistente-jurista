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
        [--meu-nome "Maria Aparecida"]

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
import sys
import zipfile
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
PADRAO_OCULTA = re.compile(r"<?\s*(?:mídia oculta|media omitted|arquivo de mídia oculto)\s*>?", re.IGNORECASE)

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
                "remetente": (remetente or "Sistema").strip(),
                "texto": texto_msg.strip(),
                "midia": None,
            })
        elif mensagens:
            mensagens[-1]["texto"] += "\n" + linha

    for msg in mensagens:
        m_anexo = PADRAO_ANEXO.search(msg["texto"])
        if m_anexo:
            msg["midia"] = m_anexo.group(1).strip()
            msg["texto"] = PADRAO_ANEXO.sub("", msg["texto"]).strip()
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


def gerar_html(mensagens: list[dict], caso: str, meu_nome: str, doc_ref: dict, pasta_destino: Path) -> Path:
    tem_midia_local = any((pasta_destino / "midia").glob("*")) if (pasta_destino / "midia").exists() else False

    def classificar_midia(nome):
        if not nome:
            return "", ""
        if nome == "__OCULTA__":
            return "oculta_sem_arquivo", ""
        caminho = pasta_destino / "midia" / nome
        if not caminho.exists():
            return "ausente", nome
        ext = caminho.suffix.lower()
        if ext in EXT_IMAGEM:
            return "imagem", nome
        if ext in EXT_VIDEO:
            return "video", nome
        if ext in EXT_AUDIO:
            return "audio", nome
        return "arquivo", nome

    dados_js = []
    for i, msg in enumerate(mensagens):
        tipo_midia, nome_midia = classificar_midia(msg["midia"])
        dados_js.append({
            "id": i,
            "data": msg["data"], "hora": msg["hora"], "remetente": msg["remetente"],
            "texto": msg["texto"], "eu": msg["remetente"].strip().lower() == meu_nome.strip().lower() if meu_nome else False,
            "tipoMidia": tipo_midia, "nomeMidia": nome_midia,
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
  <button class="btn" id="btnExportar">Exportar seleção (.json)</button>
</div>

<script>
const MENSAGENS = __DADOS_JSON__;
const marcadas = new Set();

function bolhaHtml(m){
  let midiaHtml = '';
  if (m.tipoMidia === 'imagem') midiaHtml = `<div class="midia"><img src="midia/${encodeURIComponent(m.nomeMidia)}" loading="lazy"></div>`;
  else if (m.tipoMidia === 'video') midiaHtml = `<div class="midia"><video src="midia/${encodeURIComponent(m.nomeMidia)}" controls></video></div>`;
  else if (m.tipoMidia === 'audio') midiaHtml = `<div class="midia"><audio src="midia/${encodeURIComponent(m.nomeMidia)}" controls style="width:100%"></audio></div>`;
  else if (m.tipoMidia === 'ausente') midiaHtml = `<div class="midia ausente">📎 ${m.nomeMidia} (arquivo não encontrado na pasta midia/)</div>`;
  else if (m.tipoMidia === 'oculta_sem_arquivo') midiaHtml = `<div class="midia ausente">🎞️ Mídia não incluída nesta exportação</div>`;
  else if (m.tipoMidia === 'arquivo') midiaHtml = `<div class="midia"><span class="arquivo-generico">📎 ${m.nomeMidia}</span></div>`;

  return `<div class="msg ${m.eu ? 'eu' : ''}" data-id="${m.id}" data-busca="${(m.texto + ' ' + m.remetente).toLowerCase().replace(/"/g,'')}">
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
</script>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--arquivo", required=True, help="Caminho do .txt ou .zip exportado do WhatsApp")
    ap.add_argument("--caso", required=True, help="Nome ou nº do caso")
    ap.add_argument("--descricao", required=True, help="Descrição breve (vai pro catálogo do arquivo original)")
    ap.add_argument("--meu-nome", default="", dest="meu_nome", help="Nome exibido pro dono do celular, pra alinhar as mensagens dele à direita (opcional)")

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

    print("\n== 3. Gerando o visualizador ==")
    destino_html = gerar_html(mensagens, args.caso, args.meu_nome, doc_ref, pasta_caso)
    print(f"Visualizador: {destino_html}")
    print("Abra esse arquivo no navegador pra ler, buscar e marcar as mensagens relevantes.")


if __name__ == "__main__":
    main()
