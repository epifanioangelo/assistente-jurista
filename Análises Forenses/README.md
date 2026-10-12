# Análises Forenses — exports do Veredata

Pasta pra guardar o que for exportado do Veredata (`~/Documents/VisualizadorIPED`, produto baseado no IPED — análise forense independente de celular/disco apreendido) pra uso neste projeto. Ver [[project-visualizador-iped]] na memória pro desenho completo do produto.

## Convenção

```
Análises Forenses/
└── DD-MM-2026/
    └── <nome ou nº do caso>/
        └── relatorio_achados.docx   (ou .pdf — export do Veredata, mensagens selecionadas + anotações)
```

## Diferença em relação a `../Provas recebidas/`

Prova aqui vem de **processamento forense verificado tecnicamente** (data/hora/remetente direto da extração) — diferente de prova manual (print, PDF, foto que o cliente manda), que só tem a data visível na própria captura, não verificada. Nunca tratar as duas como equivalentes em força probatória na peça — ver regra em `CLAUDE.md`, seção "Integração com o Veredata".

## Publicar o relatório (opcional, pra compartilhar com quem revisa/imprime)

Mesmo script já usado pras peças — `_tools/publicar_peca.py` — com `--tipo-peca "Relatório de Análise Forense"`. Gera link de compartilhamento sem login, só pra aquele arquivo.
