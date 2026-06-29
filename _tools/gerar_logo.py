#!/usr/bin/env python3
"""
Gerador do logo Angelo Epifanio — Sociedade de Advocacia.
Produz 3 arquivos em _assets/:
  logo_horizontal.png  — logo completo (nome + monograma) para cabeçalhos de documentos
  logo_documento.png   — versão reduzida para inserção em Word
  logo_mark.png        — marca quadrada [AE] para ícones, stamps, WhatsApp

Uso:
    python3 gerar_logo.py
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE  = Path(__file__).parent.parent / "_assets"
BASE.mkdir(exist_ok=True)

NAVY  = (13, 35, 64)       # #0D2340 — azul-marinho primário
NAVY2 = (26, 58, 92)       # #1A3A5C — azul-marinho secundário
WHITE = (255, 255, 255)
SCALE = 4                   # fator de superamostragem para antialiasing

TNR_B = "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf"
HEL   = "/System/Library/Fonts/HelveticaNeue.ttc"


def make_logo(w=540, h=90, scale=SCALE) -> Image.Image:
    sw, sh = w * scale, h * scale
    img = Image.new("RGBA", (sw, sh), WHITE + (255,))
    d   = ImageDraw.Draw(img)
    s   = scale
    cy  = sh // 2

    f_ae   = ImageFont.truetype(TNR_B, 58 * s)
    f_name = ImageFont.truetype(TNR_B, 27 * s)
    f_sub  = ImageFont.truetype(HEL,    9 * s, index=0)

    PAD       = 14
    BRACK_W   = 20
    BRACK_TK  = 3
    GAP       = 8

    # -- Letras AE centralizadas no bloco do monograma --
    bbox_ae = d.textbbox((0, 0), "AE", font=f_ae)
    ae_w = bbox_ae[2] - bbox_ae[0]
    ae_h = bbox_ae[3] - bbox_ae[1]
    mono_cx = (PAD + BRACK_W + ae_w // (2 * s) + GAP) * s
    ae_x = mono_cx - ae_w // 2 - bbox_ae[0]
    ae_y = cy - ae_h // 2 - bbox_ae[1]
    d.text((ae_x, ae_y), "AE", font=f_ae, fill=NAVY)

    # -- Colchetes --
    tk = BRACK_TK * s
    bh = int(ae_h * 1.18)
    by0 = cy - bh // 2
    by1 = by0 + bh
    gap = GAP * s
    bw  = BRACK_W * s

    lx = ae_x - gap - bw                  # colchete esquerdo
    d.rectangle([lx,       by0, lx+tk, by1],    fill=NAVY)
    d.rectangle([lx,       by0, lx+bw, by0+tk], fill=NAVY)
    d.rectangle([lx,       by1-tk, lx+bw, by1], fill=NAVY)

    rx = ae_x + ae_w + gap - bbox_ae[0]   # colchete direito
    d.rectangle([rx+bw-tk, by0, rx+bw, by1],    fill=NAVY)
    d.rectangle([rx,       by0, rx+bw, by0+tk], fill=NAVY)
    d.rectangle([rx,       by1-tk, rx+bw, by1], fill=NAVY)

    # -- Separador vertical --
    sep_x = rx + bw + 20 * s
    d.rectangle([sep_x, by0, sep_x + max(1, tk//3), by1], fill=NAVY2 + (130,))

    # -- Nome --
    nx = sep_x + 16 * s
    bbox_n = d.textbbox((0, 0), "Angelo Epifanio", font=f_name)
    ny = cy - (bbox_n[3]-bbox_n[1])//2 - bbox_n[1] - 5*s
    d.text((nx, ny), "Angelo Epifanio", font=f_name, fill=NAVY)

    # -- Linha fina --
    line_y = ny + (bbox_n[3]-bbox_n[1]) + 6*s
    d.rectangle([nx, line_y, sw - PAD*s, line_y + max(1, tk//4)], fill=NAVY2+(90,))

    # -- Subtítulo com letter-spacing --
    sub_y  = line_y + 5*s
    cx2    = nx
    sp     = 3.8 * s
    for ch in "SOCIEDADE DE ADVOCACIA":
        b = d.textbbox((0, 0), ch, font=f_sub)
        d.text((cx2 - b[0], sub_y - b[1]), ch, font=f_sub, fill=NAVY2)
        cx2 += (b[2] - b[0]) + sp

    return img.resize((w, h), Image.LANCZOS)


def make_mark(size=200, scale=SCALE) -> Image.Image:
    sq = size * scale
    img = Image.new("RGBA", (sq, sq), WHITE + (255,))
    d   = ImageDraw.Draw(img)
    s   = scale

    f = ImageFont.truetype(TNR_B, 90 * s)
    bbox = d.textbbox((0, 0), "AE", font=f)
    x0 = (sq - (bbox[2]-bbox[0])) // 2 - bbox[0]
    y0 = (sq - (bbox[3]-bbox[1])) // 2 - bbox[1]
    d.text((x0, y0), "AE", font=f, fill=NAVY)

    tk = 5 * s
    bw = 28 * s
    bx0 = x0 - 14*s
    by0 = y0 - 8*s
    bx1 = bx0 + (bbox[2]-bbox[0]) + 28*s
    by1 = y0 + (bbox[3]-bbox[1]) + 8*s

    for bxa, bxb in [(bx0, bx0+bw), (bx1-bw, bx1)]:
        vx = bxa if bxa == bx0 else bxb - tk
        d.rectangle([vx,  by0, vx+tk,   by1],      fill=NAVY)
        d.rectangle([bxa, by0, bxb,     by0+tk],   fill=NAVY)
        d.rectangle([bxa, by1-tk, bxb,  by1],      fill=NAVY)

    return img.resize((size, size), Image.LANCZOS)


if __name__ == "__main__":
    logo = make_logo(540, 90)
    logo.save(str(BASE / "logo_horizontal.png"), dpi=(300, 300))
    print(f"logo_horizontal.png  {logo.size}")

    logo.resize((380, 63), Image.LANCZOS).save(str(BASE / "logo_documento.png"), dpi=(300, 300))
    print(f"logo_documento.png   (380, 63)")

    mark = make_mark(200)
    mark.save(str(BASE / "logo_mark.png"), dpi=(300, 300))
    print(f"logo_mark.png        {mark.size}")
