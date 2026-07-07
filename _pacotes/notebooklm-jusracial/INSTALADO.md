# Instalação — Agente JusRacial (fonte NotebookLM)

**Data:** 08/07/2026

## Origem

`agente-claude-jusracial.md` — prompt de sistema gerado via NotebookLM, especificando um agente "Defensor JusRacial" para defesa de terreiros e religiões de matriz africana. Formato original: instruções para colar em "Custom Instructions" de um Claude Project (chat), não um agente do Claude Code.

## O que foi feito

1. Conteúdo adaptado e expandido para o formato de agente do Claude Code (frontmatter `name`/`description`/`tools`/`model` + estrutura padrão dos agentes `ae-*`), instalado em `~/.claude/agents/ae-jusracial.md`.
2. Preservadas todas as teses jurídicas do original (tutela constitucional/convencional, inviolabilidade de domicílio, descaracterização do flagrante em contravenção, consequências penais/cíveis do abuso estatal), reorganizadas nas seções A–D do agente.
3. Adicionada seção de precedentes **verificados** (RE 494.601/STF, Resolução CNJ 440/2022, caso Ilê Asé Surú/Campinas) separada dos precedentes citados na literatura da causa mas **ainda não confirmados neste projeto** (Babá Eriberto Sena, HC TJ-PA, Iturama/MG) — estes últimos marcados `[VERIFICAR]` no agente.
4. Adicionadas seções que o original não tinha, para alinhar ao padrão dos demais agentes AE: estrutura de peça em marcadores (@TITULO etc.), pipeline `gerar_docx.py`, delegação para `ae-habeas-corpus`/`ae-notificacao-extrajudicial`, checklist pré-entrega, anti-padrões.

## Arquivos de apoio trazidos junto (5 PDFs, também em 08/07/2026)

Movidos para `_analises/religiao/` e convertidos para `.md` via `_tools/pdf_para_md.py` (nova área `religiao` → "Liberdade Religiosa" adicionada ao dicionário `AREAS` do script):

| Arquivo | Status |
|---|---|
| `STF_RE_494601_47f7f.pdf` | ✓ texto extraído (78 págs., acórdão completo) |
| `RESOLUÇÃO No 440, DE 7 DE JANEIRO DE 2022.pdf` | ✓ texto extraído (Resolução CNJ completa) |
| `Suru Decisão Mandado 24-09-25.pdf` | ✓ texto extraído (decisão TJSP Campinas) |
| `MemorialSTF26Jul18 com assinatura e timbrado.pdf` | ✗ PDF escaneado, 0 caracteres extraídos — **precisa de OCR** |
| `Parecer e decisão 20181005_172230.pdf` | ✗ PDF escaneado, 0 caracteres extraídos — **precisa de OCR** (possivelmente o precedente de Iturama/MG citado na literatura — data bate) |

**Pendente:** máquina não tem `tesseract` instalado — os 2 PDFs escaneados não puderam ser convertidos. Rodar OCR (`brew install tesseract` + reprocessar) ou ler manualmente, se Angelo quiser que esse conteúdo fique disponível para o agente.

## Por que arquivar assim

Mesmo padrão usado para o pacote Clabs (`_pacotes/clabs-139-skills-criminal/INSTALADO.md`) — preserva a fonte original e documenta o que foi transformado/instalado, para rastreabilidade futura.
