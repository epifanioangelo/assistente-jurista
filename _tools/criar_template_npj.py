"""Gera NPJ_BASE.docx a partir do AGRAVO_INSTRUMENTO.docx.
Template neutro: sem identidade visual, sem nomes — apenas numeração de página no cabeçalho."""

import zipfile, os, re
from pathlib import Path

BASE_DIR  = Path(__file__).parent.parent / "Modelos jus"
SRC       = BASE_DIR / "AGRAVO_INSTRUMENTO.docx"
DST       = BASE_DIR / "NPJ_BASE.docx"
TMP       = BASE_DIR / "NPJ_BASE.tmp.docx"

# ── Namespaces mínimos para header/footer ─────────────────────────────────────
NS = (
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
    'mc:Ignorable="w14"'
)

# ── Header neutro: apenas numeração de página à direita ──────────────────────
NOVO_HEADER = f'''<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<w:hdr {NS}>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="header"/>
      <w:jc w:val="right"/>
    </w:pPr>
    <w:r><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:hdr>'''

# ── Footer neutro: vazio ──────────────────────────────────────────────────────
NOVO_FOOTER = f'''<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<w:ftr {NS}>
  <w:p/>
</w:ftr>'''


def criar_template_npj():
    with zipfile.ZipFile(SRC, 'r') as zin, zipfile.ZipFile(TMP, 'w', zipfile.ZIP_DEFLATED) as zout:
        names = zin.namelist()
        # Identificar quais headers existem
        headers = [n for n in names if re.match(r'word/header\d+\.xml$', n)]
        footers = [n for n in names if re.match(r'word/footer\d+\.xml$', n)]

        for item in names:
            if item in headers:
                zout.writestr(item, NOVO_HEADER.encode('utf-8'))
            elif item in footers:
                zout.writestr(item, NOVO_FOOTER.encode('utf-8'))
            else:
                zout.writestr(item, zin.read(item))

    os.replace(TMP, DST)
    print(f"Template NPJ criado: {DST}")


if __name__ == '__main__':
    criar_template_npj()
