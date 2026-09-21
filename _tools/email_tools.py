#!/usr/bin/env python3
"""
Ferramenta de e-mail (envio e leitura) para o Assistente Jurista.

Não guarda nenhuma credencial neste arquivo — lê tudo de variáveis de ambiente,
pra poder ser versionado no git sem risco. A credencial em si fica na memória
do Claude (base64), decodificada e passada por env var só no momento do uso
(mesmo padrão já usado para o FTP do projeto).

Variáveis de ambiente esperadas:
    EMAIL_USER       endereço completo (ex.: a.epifanio@advogado.sjc.br)
    EMAIL_PASS       senha em texto puro (decodificada do base64 antes de chamar)
    EMAIL_HOST       servidor de e-mail (ex.: mail.advogado.sjc.br)
    EMAIL_FROM_NAME  opcional, nome de exibição do remetente (padrão: "Angelo Epifanio")
    EMAIL_SMTP_PORT  opcional, padrão 465 (SSL)
    EMAIL_IMAP_PORT  opcional, padrão 993 (SSL)

Uso:
    python3 email_tools.py enviar --to dest@exemplo.com --assunto "..." \
        --corpo-arquivo corpo.txt [--anexo arquivo1.docx --anexo arquivo2.pdf]

    python3 email_tools.py listar [--limite 10] [--so-nao-lidas]
"""

import argparse
import imaplib
import email
import os
import smtplib
import sys
from email.header import decode_header
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from typing import Optional


def _config():
    user = os.environ.get("EMAIL_USER")
    pwd = os.environ.get("EMAIL_PASS")
    host = os.environ.get("EMAIL_HOST")
    if not (user and pwd and host):
        sys.exit("Faltam EMAIL_USER, EMAIL_PASS ou EMAIL_HOST no ambiente.")
    smtp_port = int(os.environ.get("EMAIL_SMTP_PORT", "465"))
    imap_port = int(os.environ.get("EMAIL_IMAP_PORT", "993"))
    from_name = os.environ.get("EMAIL_FROM_NAME", "Angelo Epifanio")
    return user, pwd, host, smtp_port, imap_port, from_name


def enviar(destinatario: str, assunto: str, corpo: str, anexos: Optional[list] = None):
    user, pwd, host, smtp_port, _, from_name = _config()

    msg = EmailMessage()
    msg["From"] = formataddr((from_name, user))
    msg["To"] = destinatario
    msg["Subject"] = assunto
    msg.set_content(corpo)

    for caminho in anexos or []:
        p = Path(caminho)
        if not p.exists():
            sys.exit(f"Anexo não encontrado: {caminho}")
        dados = p.read_bytes()
        if p.suffix == ".pdf":
            maintype, subtype = "application", "pdf"
        elif p.suffix == ".docx":
            maintype, subtype = (
                "application",
                "vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        else:
            maintype, subtype = "application", "octet-stream"
        msg.add_attachment(dados, maintype=maintype, subtype=subtype, filename=p.name)

    with smtplib.SMTP_SSL(host, smtp_port, timeout=20) as smtp:
        smtp.login(user, pwd)
        smtp.send_message(msg)

    print(f"E-mail enviado para {destinatario} — assunto: {assunto}")


def _decode(valor) -> str:
    if valor is None:
        return ""
    partes = decode_header(valor)
    out = ""
    for texto, cod in partes:
        if isinstance(texto, bytes):
            out += texto.decode(cod or "utf-8", errors="replace")
        else:
            out += texto
    return out


def listar(limite: int = 10, so_nao_lidas: bool = False):
    user, pwd, host, _, imap_port, _from_name = _config()

    imap = imaplib.IMAP4_SSL(host, imap_port, timeout=20)
    imap.login(user, pwd)
    imap.select("INBOX", readonly=True)

    criterio = "UNSEEN" if so_nao_lidas else "ALL"
    typ, data = imap.search(None, criterio)
    ids = data[0].split()
    ids = ids[-limite:] if limite else ids

    if not ids:
        print("Nenhuma mensagem encontrada.")
        imap.logout()
        return

    for msg_id in reversed(ids):
        typ, msg_data = imap.fetch(msg_id, "(RFC822)")
        raw = msg_data[0][1]
        m = email.message_from_bytes(raw)
        de = _decode(m.get("From"))
        assunto = _decode(m.get("Subject"))
        data_envio = m.get("Date")
        print(f"[{msg_id.decode()}] {data_envio} | De: {de} | Assunto: {assunto}")

    imap.logout()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="comando", required=True)

    p_enviar = sub.add_parser("enviar")
    p_enviar.add_argument("--to", required=True)
    p_enviar.add_argument("--assunto", required=True)
    p_enviar.add_argument("--corpo-arquivo", required=True)
    p_enviar.add_argument("--anexo", action="append", default=[])

    p_listar = sub.add_parser("listar")
    p_listar.add_argument("--limite", type=int, default=10)
    p_listar.add_argument("--so-nao-lidas", action="store_true")

    args = ap.parse_args()

    if args.comando == "enviar":
        corpo = Path(args.corpo_arquivo).read_text(encoding="utf-8")
        enviar(args.to, args.assunto, corpo, args.anexo)
    elif args.comando == "listar":
        listar(args.limite, args.so_nao_lidas)


if __name__ == "__main__":
    main()
