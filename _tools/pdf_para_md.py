#!/usr/bin/env python3
"""
Converte PDFs jurídicos em arquivos .md estruturados.

Uso:
    python3 pdf_para_md.py                    # converte todos os PDFs em _analises/
    python3 pdf_para_md.py caminho/arquivo.pdf # converte um PDF específico

Resultado:
    - Arquivo .md ao lado do PDF original
    - INDICE.md atualizado em _analises/
"""

import sys
import re
import datetime
from pathlib import Path

import fitz  # pymupdf


BASE_DIR  = Path(__file__).parent.parent
ANALISES  = BASE_DIR / "_analises"
INDICE    = ANALISES / "INDICE.md"

# Subpastas reconhecidas como áreas jurídicas
AREAS = {
    "penal":       "Penal",
    "vd":          "Violência Doméstica",
    "canabico":    "Direito Canábico",
    "consumidor":  "Consumidor / CDC",
    "civel":       "Cível",
    "trabalhista": "Trabalhista",
    "previdencia": "Previdenciário",
    "tributario":  "Tributário",
    "familia":     "Família",
    "empresarial": "Empresarial",
}


# ── Extração de texto ─────────────────────────────────────────────────────────

def extrair_texto(pdf_path: Path) -> str:
    doc = fitz.open(str(pdf_path))
    paginas = []
    for i, page in enumerate(doc, start=1):
        texto = page.get_text("text")
        texto = texto.strip()
        if texto:
            paginas.append(f"<!-- página {i} -->\n{texto}")
    doc.close()
    return "\n\n".join(paginas)


def limpar_texto(texto: str) -> str:
    # Remove quebras de linha dentro de frases (heurística: linha curta seguida de minúscula)
    texto = re.sub(r"(?<!\n)\n(?=[a-záéíóúàãõâêîôûç])", " ", texto)
    # Colapsa múltiplas linhas em branco
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


# ── Inferência de metadados ───────────────────────────────────────────────────

def inferir_area(pdf_path: Path) -> str:
    partes = [p.lower() for p in pdf_path.parts]
    for chave, nome in AREAS.items():
        if any(chave in parte for parte in partes):
            return nome
    return "Geral"


def inferir_tema(texto: str, nome_arquivo: str) -> str:
    """Extrai o provável tema do início do texto ou do nome do arquivo."""
    # Tenta pegar a primeira linha não-vazia com conteúdo útil
    for linha in texto.splitlines():
        linha = linha.strip()
        if len(linha) > 10 and not linha.startswith("<!--"):
            return linha[:120]
    # Fallback: nome do arquivo sem extensão
    return nome_arquivo.replace("_", " ").replace("-", " ").title()


# ── Geração do .md ────────────────────────────────────────────────────────────

CABECALHO = """\
---
arquivo_original: {pdf}
area: {area}
tema: {tema}
convertido_em: {data}
---

# {tema}

**Área:** {area}
**Arquivo original:** `{pdf}`
**Convertido em:** {data}

---

"""


def converter(pdf_path: Path) -> Path:
    print(f"  → {pdf_path.name}")
    texto_bruto = extrair_texto(pdf_path)
    texto = limpar_texto(texto_bruto)

    area  = inferir_area(pdf_path)
    tema  = inferir_tema(texto, pdf_path.stem)
    data  = datetime.date.today().isoformat()

    cabecalho = CABECALHO.format(
        pdf=pdf_path.name,
        area=area,
        tema=tema,
        data=data,
    )

    md_path = pdf_path.with_suffix(".md")
    md_path.write_text(cabecalho + texto, encoding="utf-8")
    print(f"     ✓ salvo: {md_path.name}")
    return md_path


# ── Índice ────────────────────────────────────────────────────────────────────

def atualizar_indice(arquivos_md: list[Path]) -> None:
    """Regenera o INDICE.md a partir de todos os .md em _analises/."""
    # Coleta todos os .md existentes + os recém-criados
    todos = sorted(ANALISES.rglob("*.md"))
    todos = [f for f in todos if f.name != "INDICE.md"]

    linhas = [
        "# ÍNDICE DE ANÁLISES JURÍDICAS",
        "",
        "> Arquivo gerado automaticamente por `pdf_para_md.py`.",
        "> Para buscar um tema: `grep -ri 'palavra-chave' _analises/`",
        "",
        f"**Total de arquivos:** {len(todos)}  ",
        f"**Última atualização:** {datetime.date.today().isoformat()}",
        "",
        "---",
        "",
    ]

    # Agrupa por área
    por_area: dict[str, list[Path]] = {}
    for md in todos:
        area = _ler_campo(md, "area") or "Geral"
        por_area.setdefault(area, []).append(md)

    for area in sorted(por_area):
        linhas.append(f"## {area}")
        linhas.append("")
        for md in sorted(por_area[area]):
            tema  = _ler_campo(md, "tema") or md.stem
            caminho_rel = md.relative_to(ANALISES)
            linhas.append(f"- [{tema[:80]}]({caminho_rel})")
        linhas.append("")

    INDICE.write_text("\n".join(linhas), encoding="utf-8")
    print(f"\n  ✓ INDICE.md atualizado ({len(todos)} arquivo(s))")


def _ler_campo(md_path: Path, campo: str) -> str:
    """Lê um campo do frontmatter YAML do .md."""
    try:
        conteudo = md_path.read_text(encoding="utf-8")
        match = re.search(rf"^{campo}:\s*(.+)$", conteudo, re.MULTILINE)
        return match.group(1).strip() if match else ""
    except Exception:
        return ""


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ANALISES.mkdir(parents=True, exist_ok=True)

    if len(sys.argv) > 1:
        # Arquivo específico
        alvos = [Path(sys.argv[1])]
    else:
        # Todos os PDFs em _analises/
        alvos = sorted(ANALISES.rglob("*.pdf"))

    if not alvos:
        print("Nenhum PDF encontrado em _analises/")
        print("Coloque seus PDFs em subpastas de _analises/ e rode novamente.")
        print("Exemplo: _analises/penal/minha_analise.pdf")
        return

    print(f"\nConvertendo {len(alvos)} arquivo(s)...\n")
    convertidos = []
    erros = []

    for pdf in alvos:
        try:
            md = converter(pdf)
            convertidos.append(md)
        except Exception as e:
            print(f"     ✗ erro em {pdf.name}: {e}")
            erros.append(pdf)

    atualizar_indice(convertidos)

    print(f"\nPronto: {len(convertidos)} convertido(s)", end="")
    if erros:
        print(f", {len(erros)} com erro(s): {[e.name for e in erros]}", end="")
    print()


if __name__ == "__main__":
    main()
