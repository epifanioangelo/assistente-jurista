"""Remove o logo padrão (imagens dos cabeçalhos) dos 7 modelos .docx."""

import zipfile
import re
import shutil
import os
from pathlib import Path

BASE = Path(__file__).parent.parent / "Modelos jus"

MODELOS = [
    "1._INICIAL.docx",
    "2._CONTESTAÇÃO.docx",
    "3._RÉPLICA.docx",
    "4._EMBARGOS_DE_DECLARAÇÃO.docx",
    "5. MANDADO_DE_SEGURANÇA.docx",
    "6. AGRAVO_DE_INSTRUMENTO.docx",
    "7._APELAÇÃO.docx",
]


def remover_drawing_do_header(xml: str) -> str:
    """Remove todos os blocos <w:drawing> que contêm imagem (<pic:pic>) do XML do header."""
    # Remove o run inteiro que contém o drawing com imagem
    # Padrão: <w:r>...<w:drawing>...<pic:pic>...</pic:pic>...</w:drawing>...</w:r>
    padrao = re.compile(
        r'<w:r[^>]*>(?:(?!</w:r>).)*?<w:drawing>(?:(?!</w:drawing>).)*?<pic:pic(?:(?!</w:r>).)*?</w:r>',
        re.DOTALL
    )
    resultado = padrao.sub('', xml)
    return resultado


def limpar_rels_header(rels_xml: str, imagens_a_remover: list) -> str:
    """Remove as entradas de relacionamento das imagens dos headers."""
    for img in imagens_a_remover:
        nome = img.split('/')[-1]
        rels_xml = re.sub(
            rf'<Relationship[^/]*/media/{re.escape(nome)}[^/]*/>', '', rels_xml
        )
        rels_xml = re.sub(
            rf'<Relationship[^>]+Target="media/{re.escape(nome)}"[^>]*/>', '', rels_xml
        )
    return rels_xml


def processar_modelo(nome_arquivo: str):
    caminho = BASE / nome_arquivo
    tmp = caminho.with_suffix('.tmp.docx')

    with zipfile.ZipFile(caminho, 'r') as zin, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        names = zin.namelist()

        # Mapear imagens que estão nos headers (logos a remover)
        header_rels_files = [n for n in names if re.match(r'word/_rels/header\d+\.xml\.rels', n)]
        logos = set()
        for rel_file in header_rels_files:
            content = zin.read(rel_file).decode('utf-8')
            imgs = re.findall(r'Target="(media/[^"]+)"', content)
            logos.update(imgs)

        logos_paths = {f'word/{img}' for img in logos}

        for item in names:
            data = zin.read(item)

            # Pular as imagens de logo
            if item in logos_paths:
                print(f"  Removendo imagem: {item}")
                continue

            # Limpar drawing das imagens nos headers
            if re.match(r'word/header\d+\.xml', item):
                xml = data.decode('utf-8')
                xml_limpo = remover_drawing_do_header(xml)
                if xml != xml_limpo:
                    print(f"  Logo removido de: {item}")
                data = xml_limpo.encode('utf-8')

            # Limpar .rels dos headers
            if re.match(r'word/_rels/header\d+\.xml\.rels', item):
                xml = data.decode('utf-8')
                xml_limpo = limpar_rels_header(xml, list(logos))
                data = xml_limpo.encode('utf-8')

            zout.writestr(item, data)

    # Substituir original pelo limpo
    os.replace(tmp, caminho)
    print(f"OK: {nome_arquivo}")


if __name__ == '__main__':
    for modelo in MODELOS:
        print(f"\nProcessando: {modelo}")
        try:
            processar_modelo(modelo)
        except Exception as e:
            print(f"  ERRO: {e}")
