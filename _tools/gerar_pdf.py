#!/usr/bin/env python3
"""
Gerador de PDF para peças jurídicas — formatação ABNT forense.

Uso:
    python3 gerar_pdf.py entrada.txt saida.pdf

O arquivo de entrada usa marcadores simples:
    @CENTRO      linha centralizada (endereçamento)
    @TITULO      capítulo principal (romano — negrito, centralizado, caixa alta)
    @SUBTITULO   subseção (negrito, alinhado à esquerda)
    @CITACAO     início de bloco de citação longa (recuo 4cm, 10pt)
    @FIM         fim de bloco de citação longa
    @ASSINATURA  início do bloco de assinatura (centralizado)
    @AVISO       aviso final (itálico, borda superior)
    linhas normais → parágrafo justificado com recuo de 1ª linha

Linhas que começam com a), b), c)... são tratadas como itens de lista.
"""

import sys
import re
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable, PageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Margens ABNT ──────────────────────────────────────────────────────────────
MARGIN_TOP    = 3 * cm
MARGIN_BOTTOM = 2 * cm
MARGIN_LEFT   = 3 * cm
MARGIN_RIGHT  = 2 * cm

PAGE_W, PAGE_H = A4  # 595.27 x 841.89 pt

# ── Estilos ───────────────────────────────────────────────────────────────────
def build_styles():
    corpo = ParagraphStyle(
        'corpo', fontName='Times-Roman', fontSize=12, leading=18,
        alignment=TA_JUSTIFY, firstLineIndent=1.25*cm, spaceAfter=6, spaceBefore=0,
    )
    sem_recuo = ParagraphStyle(
        'sem_recuo', fontName='Times-Roman', fontSize=12, leading=18,
        alignment=TA_JUSTIFY, firstLineIndent=0, spaceAfter=6, spaceBefore=0,
    )
    centro = ParagraphStyle(
        'centro', fontName='Times-Bold', fontSize=12, leading=18,
        alignment=TA_CENTER, firstLineIndent=0, spaceAfter=6, spaceBefore=0,
    )
    titulo = ParagraphStyle(
        'titulo', fontName='Times-Bold', fontSize=12, leading=18,
        alignment=TA_CENTER, firstLineIndent=0, spaceAfter=6, spaceBefore=12,
    )
    subtitulo = ParagraphStyle(
        'subtitulo', fontName='Times-Bold', fontSize=12, leading=18,
        alignment=TA_LEFT, firstLineIndent=0, spaceAfter=3, spaceBefore=6,
    )
    citacao = ParagraphStyle(
        'citacao', fontName='Times-Roman', fontSize=10, leading=12,
        leftIndent=4*cm, alignment=TA_JUSTIFY, firstLineIndent=0,
        spaceBefore=6, spaceAfter=6,
    )
    lista = ParagraphStyle(
        'lista', fontName='Times-Roman', fontSize=12, leading=18,
        alignment=TA_JUSTIFY, firstLineIndent=0, leftIndent=1.25*cm,
        spaceAfter=6, spaceBefore=0,
    )
    assinatura = ParagraphStyle(
        'assinatura', fontName='Times-Roman', fontSize=12, leading=18,
        alignment=TA_CENTER, firstLineIndent=0, spaceAfter=4, spaceBefore=0,
    )
    assinatura_bold = ParagraphStyle(
        'assinatura_bold', fontName='Times-Bold', fontSize=12, leading=18,
        alignment=TA_CENTER, firstLineIndent=0, spaceAfter=4, spaceBefore=0,
    )
    aviso = ParagraphStyle(
        'aviso', fontName='Times-Italic', fontSize=10, leading=14,
        alignment=TA_JUSTIFY, firstLineIndent=0, spaceBefore=12,
        textColor=colors.HexColor('#333333'),
    )

    return {
        'corpo': corpo, 'sem_recuo': sem_recuo, 'centro': centro,
        'titulo': titulo, 'subtitulo': subtitulo, 'citacao': citacao,
        'lista': lista, 'assinatura': assinatura,
        'assinatura_bold': assinatura_bold, 'aviso': aviso,
    }


# ── Numeração de páginas ──────────────────────────────────────────────────────
def add_page_number(canvas, doc):
    page = doc.page
    if page < 2:
        return
    canvas.saveState()
    canvas.setFont('Times-Roman', 12)
    canvas.drawRightString(
        PAGE_W - MARGIN_RIGHT,
        PAGE_H - MARGIN_TOP + 0.5 * cm,
        str(page),
    )
    canvas.restoreState()


# ── Parser do texto de entrada ────────────────────────────────────────────────
def limpar(txt):
    """Remove marcadores markdown residuais simples."""
    txt = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', txt)
    txt = re.sub(r'\*(.*?)\*', r'<i>\1</i>', txt)
    return txt


def parse(texto, styles):
    flowables = []
    linhas = texto.splitlines()
    i = 0
    modo_citacao = False
    modo_assinatura = False
    modo_aviso = False

    while i < len(linhas):
        linha = linhas[i].rstrip()

        # Diretiva @CITACAO / @FIM
        if linha.strip() == '@CITACAO':
            modo_citacao = True
            i += 1
            continue
        if linha.strip() == '@FIM':
            modo_citacao = False
            i += 1
            continue

        # Diretiva @ASSINATURA
        if linha.strip() == '@ASSINATURA':
            modo_assinatura = True
            flowables.append(Spacer(1, 2 * cm))
            i += 1
            continue

        # Diretiva @AVISO — ignorada nas peças finais
        if linha.strip() == '@AVISO':
            modo_aviso = True
            i += 1
            continue

        # Linha em branco
        if linha.strip() == '':
            flowables.append(Spacer(1, 0.3 * cm))
            i += 1
            continue

        # Separador ---
        if re.match(r'^-{3,}$', linha.strip()):
            flowables.append(Spacer(1, 0.3 * cm))
            i += 1
            continue

        # Modo citação
        if modo_citacao:
            flowables.append(Paragraph(limpar(linha), styles['citacao']))
            i += 1
            continue

        # Modo aviso
        if modo_aviso:
            flowables.append(Paragraph(limpar(linha), styles['aviso']))
            i += 1
            continue

        # Modo assinatura
        if modo_assinatura:
            if re.match(r'^OAB/', linha.strip()) or re.match(r'^CPF', linha.strip()):
                flowables.append(Paragraph(limpar(linha), styles['assinatura']))
            else:
                flowables.append(Paragraph(limpar(linha), styles['assinatura_bold']))
            i += 1
            continue

        # Diretiva @CENTRO
        if linha.startswith('@CENTRO'):
            conteudo = linha[7:].strip()
            flowables.append(Paragraph(limpar(conteudo), styles['centro']))
            i += 1
            continue

        # Diretiva @TITULO
        if linha.startswith('@TITULO'):
            conteudo = linha[7:].strip().upper()
            flowables.append(Paragraph(limpar(conteudo), styles['titulo']))
            i += 1
            continue

        # Diretiva @SUBTITULO
        if linha.startswith('@SUBTITULO'):
            conteudo = linha[10:].strip()
            flowables.append(Paragraph(limpar(conteudo), styles['subtitulo']))
            i += 1
            continue

        # Item de lista a), b), c)...
        if re.match(r'^[a-z]\)', linha.strip()):
            flowables.append(Paragraph(limpar(linha.strip()), styles['lista']))
            i += 1
            continue

        # Parágrafo normal
        flowables.append(Paragraph(limpar(linha.strip()), styles['corpo']))
        i += 1

    return flowables


# ── Geração do PDF ────────────────────────────────────────────────────────────
def gerar(entrada: Path, saida: Path):
    texto = entrada.read_text(encoding='utf-8')
    styles = build_styles()
    flowables = parse(texto, styles)

    doc = SimpleDocTemplate(
        str(saida),
        pagesize=A4,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        title=saida.stem,
    )
    doc.build(flowables, onLaterPages=add_page_number, onFirstPage=add_page_number)
    print(f'PDF gerado: {saida}')


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Uso: python3 gerar_pdf.py entrada.txt saida.pdf')
        sys.exit(1)
    gerar(Path(sys.argv[1]), Path(sys.argv[2]))
