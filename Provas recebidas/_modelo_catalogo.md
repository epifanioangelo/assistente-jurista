# Catálogo de provas — <nome/nº do caso>

Gerado/atualizado por `_tools/catalogar_prova.py` — não editar o hash manualmente. Se precisar catalogar sem o script, copiar este arquivo pra `Provas recebidas/DD-MM-2026/<caso>/catalogo.md` e preencher conforme as provas forem chegando (nunca pular um ID nem reaproveitar), calculando o hash com `shasum -a 256 arquivo`.

| ID | Arquivo | Recebido em | Descrição | Data exibida na prova | Hash SHA-256 | Verificado tecnicamente? |
|----|---------|-------------|-----------|------------------------|--------------|---------------------------|
| Doc. 1 | doc01_exemplo.jpg | DD/MM/AAAA | Print de conversa WhatsApp com [nome], sobre [assunto] | DD/MM/AAAA HH:MM (conforme exibido na captura) | `a1b2c3...` | Não |
| Doc. 2 | doc02_exemplo.pdf | DD/MM/AAAA | Comprovante de pagamento | — | `d4e5f6...` | Não |

**Nota**: "Verificado tecnicamente" só é "Sim" pra prova vinda de análise forense processada no Veredata (ver `../../Análises Forenses/`) — prova manual (print, foto, PDF enviado pelo cliente) é sempre "Não", mesmo quando a data pareça clara na própria imagem. O hash SHA-256 prova que o arquivo não foi alterado **desde o momento em que entrou no catálogo** — não prova a autenticidade do conteúdo em si (isso continua exigindo ata notarial ou carimbo do tempo ICP-Brasil, se o caso precisar de peso probatório maior).
