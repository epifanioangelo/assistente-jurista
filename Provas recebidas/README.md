# Provas recebidas — catálogo por caso

Pasta pra organizar provas que o cliente manda direto (print, PDF, foto, documento escaneado) — fora do fluxo do Veredata (análise forense de celular/disco, que fica em `../Análises Forenses/`).

## Convenção

Cada caso tem sua própria subpasta, dentro da pasta do dia em que a primeira prova chegou:

```
Provas recebidas/
└── DD-MM-2026/
    └── <nome ou nº do caso>/
        ├── catalogo.md
        ├── doc01_print_whatsapp_14-03.jpg
        ├── doc02_comprovante_pagamento.pdf
        └── ...
```

## Regras

1. **Todo arquivo recebido entra no catálogo antes de ser citado em qualquer peça** — nunca citar "o print que o cliente mandou" sem ter salvo o arquivo e dado um ID.
2. **Catalogar com o script, não na mão**: `python3 _tools/catalogar_prova.py --arquivo <caminho> --caso "<caso>" --descricao "<descrição>" [--data-exibida "DD/MM/AAAA HH:MM"]` — copia o arquivo, calcula o hash SHA-256 e já grava a linha no `catalogo.md`, com ID sequencial automático (Doc. 1, Doc. 2, ...), nunca reaproveitado nem pulado.
3. **Distinguir sempre a data que aparece na prova (não verificada) da data real do evento** — usar exatamente a redação `conforme exibido na captura, não verificado tecnicamente` quando citar a peça. Isso é diferente de prova vinda do Veredata (análise forense), que carrega metadado verificado tecnicamente — nunca tratar as duas como equivalentes em força probatória.
4. **O hash SHA-256** prova que o arquivo não foi alterado desde que entrou no catálogo — não prova a autenticidade do conteúdo em si. Se o caso exigir peso probatório maior, reforçar com ata notarial (cartório certifica o que viu na tela, fé pública — mas não é perícia técnica do aparelho) ou carimbo do tempo de autoridade certificadora ICP-Brasil (mais rigoroso tecnicamente, prova existência e integridade num momento específico).
5. As tabelas geradas pela skill `tipografia-juridica` (coluna "Documento/Prova") citam o ID daqui — consistência entre todas as peças do mesmo caso.
6. Pra inserir a imagem de verdade dentro da peça (não só citar), usar o marcador `@IMAGEM caminho/do/arquivo [largura_cm]` do `_tools/gerar_docx.py`.

## Modelo do `catalogo.md`

Ver `_modelo_catalogo.md` nesta pasta — gerado automaticamente pelo `_tools/catalogar_prova.py` na primeira prova de cada caso; só copiar manualmente se precisar catalogar sem o script.
