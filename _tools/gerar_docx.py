#!/usr/bin/env python3
"""
Gerador de DOCX para peças jurídicas — formatação ABNT forense.

Uso:
    python3 gerar_docx.py entrada.txt saida.docx

Marcadores no arquivo de entrada:
    @CENTRO      linha centralizada em negrito (endereçamento, nome da peça)
    @TITULO      capítulo romano (negrito, centralizado, caixa alta)
    @SUBTITULO   subseção (negrito, alinhado à esquerda)
    @CITACAO     início de bloco de citação longa (recuo 4cm, 10pt)
    @FIM         fim de bloco de citação longa
    @ASSINATURA  início do bloco de assinatura (centralizado)
    @AVISO       ignorado — avisos de IA não constam nas peças
    linhas normais → parágrafo justificado com recuo de 1ª linha
    a), b), c)... → item de lista com recuo
"""

import sys
import re
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


# ── Configurações ABNT ────────────────────────────────────────────────────────
FONTE          = 'Times New Roman'
FONTE_PT       = 12
FONTE_CITACAO  = 10
ENTRELINHA     = 1.5       # múltiplo de linha (LINE_SPACING_RULE_MULTIPLE)
RECUO_1A_LINHA = Cm(1.25)
RECUO_CITACAO  = Cm(4.0)
ESPACO_DEPOIS  = Pt(6)
ESPACO_ANTES   = Pt(0)


# ── Helpers de formatação ─────────────────────────────────────────────────────
def set_spacing(para, before=ESPACO_ANTES, after=ESPACO_DEPOIS, line=ENTRELINHA):
    from docx.oxml.ns import qn
    from docx.shared import Pt
    pPr = para._p.get_or_add_pPr()
    spacing = OxmlElement('w:spacing')
    spacing.set(qn('w:before'), str(int(before.pt * 20)))
    spacing.set(qn('w:after'),  str(int(after.pt  * 20)))
    spacing.set(qn('w:line'),   str(int(line * 240)))
    spacing.set(qn('w:lineRule'), 'auto')
    pPr.append(spacing)


def add_run(para, texto, bold=False, italic=False, size=FONTE_PT):
    run = para.add_run(texto)
    run.font.name  = FONTE
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    return run


def parse_inline(texto):
    """Divide o texto em segmentos com marcação **bold** e *italic*."""
    partes = []
    pattern = re.compile(r'\*\*(.*?)\*\*|\*(.*?)\*')
    pos = 0
    for m in pattern.finditer(texto):
        if m.start() > pos:
            partes.append({'t': texto[pos:m.start()], 'b': False, 'i': False})
        if m.group(1) is not None:
            partes.append({'t': m.group(1), 'b': True, 'i': False})
        else:
            partes.append({'t': m.group(2), 'b': False, 'i': True})
        pos = m.end()
    if pos < len(texto):
        partes.append({'t': texto[pos:], 'b': False, 'i': False})
    return partes


def fill_para(para, texto, bold=False, size=FONTE_PT):
    """Preenche um parágrafo interpretando marcação inline."""
    for seg in parse_inline(texto):
        add_run(para, seg['t'], bold=bold or seg['b'], italic=seg['i'], size=size)


def set_margins(doc):
    """Margens ABNT: sup 3cm, inf 2cm, esq 3cm, dir 2cm."""
    for section in doc.sections:
        section.top_margin    = Cm(3)
        section.bottom_margin = Cm(2)
        section.left_margin   = Cm(3)
        section.right_margin  = Cm(2)


def add_page_number(doc):
    """Numeração de página no canto superior direito (Header)."""
    section = doc.sections[0]
    section.different_first_page_header_footer = True  # sem número na p.1

    header = section.header
    para = header.paragraphs[0] if header.paragraphs else header.add_paragraph()
    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    para.clear()

    run = para.add_run()
    run.font.name = FONTE
    run.font.size = Pt(FONTE_PT)

    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = 'PAGE'
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')

    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)


# ── Geração do documento ──────────────────────────────────────────────────────
def gerar(entrada: Path, saida: Path):
    doc = Document()
    set_margins(doc)
    add_page_number(doc)

    # Remove parágrafo em branco inicial do python-docx
    if doc.paragraphs:
        p = doc.paragraphs[0]._element
        p.getparent().remove(p)

    linhas = entrada.read_text(encoding='utf-8').splitlines()
    i = 0
    modo_citacao    = False
    modo_assinatura = False
    modo_aviso      = False

    while i < len(linhas):
        linha = linhas[i].rstrip()

        # ── Diretivas de modo ──────────────────────────────────────────────
        if linha.strip() == '@CITACAO':
            modo_citacao = True;  i += 1;  continue
        if linha.strip() == '@FIM':
            modo_citacao = False; i += 1;  continue
        if linha.strip() == '@ASSINATURA':
            modo_assinatura = True
            doc.add_paragraph()   # espaço para assinatura manuscrita (≈ 2 linhas)
            doc.add_paragraph()
            i += 1; continue
        if linha.strip() == '@AVISO':
            modo_aviso = True;    i += 1;  continue

        # Linha em branco
        if linha.strip() == '':
            if not modo_aviso:
                p = doc.add_paragraph()
                set_spacing(p, after=Pt(0))
            i += 1; continue

        # Separador ---
        if re.match(r'^-{3,}$', linha.strip()):
            i += 1; continue

        # ── Modo aviso — ignorado ──────────────────────────────────────────
        if modo_aviso:
            i += 1; continue

        # ── Modo citação ───────────────────────────────────────────────────
        if modo_citacao:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf = p.paragraph_format
            pf.left_indent       = RECUO_CITACAO
            pf.first_line_indent = Cm(0)
            set_spacing(p, after=Pt(6))
            fill_para(p, linha.strip(), size=FONTE_CITACAO)
            i += 1; continue

        # ── Modo assinatura ────────────────────────────────────────────────
        if modo_assinatura:
            bold = not re.match(r'^OAB/', linha.strip())
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_spacing(p, after=Pt(2))
            fill_para(p, linha.strip(), bold=bold)
            i += 1; continue

        # ── Diretiva @CENTRO ───────────────────────────────────────────────
        if linha.startswith('@CENTRO'):
            conteudo = linha[7:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_spacing(p, after=Pt(6))
            fill_para(p, conteudo, bold=True)
            i += 1; continue

        # ── Diretiva @TITULO ───────────────────────────────────────────────
        if linha.startswith('@TITULO'):
            conteudo = linha[7:].strip().upper()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_spacing(p, before=Pt(12), after=Pt(6))
            fill_para(p, conteudo, bold=True)
            i += 1; continue

        # ── Diretiva @SUBTITULO ────────────────────────────────────────────
        if linha.startswith('@SUBTITULO'):
            conteudo = linha[10:].strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            set_spacing(p, before=Pt(6), after=Pt(3))
            fill_para(p, conteudo, bold=True)
            i += 1; continue

        # ── Item de lista a), b), c)... ────────────────────────────────────
        if re.match(r'^[a-z]\)', linha.strip()):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            pf = p.paragraph_format
            pf.left_indent       = RECUO_1A_LINHA
            pf.first_line_indent = Cm(0)
            set_spacing(p, after=Pt(6))
            fill_para(p, linha.strip())
            i += 1; continue

        # ── Parágrafo normal ───────────────────────────────────────────────
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        pf = p.paragraph_format
        pf.first_line_indent = RECUO_1A_LINHA
        set_spacing(p, after=Pt(6))
        fill_para(p, linha.strip())
        i += 1

    doc.save(str(saida))
    print(f'DOCX gerado: {saida}')


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Uso: python3 gerar_docx.py entrada.txt saida.docx')
        sys.exit(1)
    gerar(Path(sys.argv[1]), Path(sys.argv[2]))
