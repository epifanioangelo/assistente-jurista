# STATUS DO PROJETO — ASSISTENTE JURISTA

## Fase atual: FASE 0 — Configuração Claude.ai Projects (em andamento, com trabalho adicional considerável fora do escopo original)

**Iniciado em:** 28/06/2026
**Última sessão:** 09/07/2026

---

## O que foi feito

### 28/06/2026 — Estrutura inicial
- [x] Estrutura de arquivos completa para 5 especialidades (01 a 05)
- [x] Modelos .docx das peças em `Modelos jus/` (7 documentos)
- [x] Git inicializado no projeto
- [x] CLAUDE.md criado (instruções para sessões Claude Code)
- [x] ROADMAP.md criado (algoritmo completo Fase 0 → Fase 5)
- [x] Sistema de memória criado (`_memoria/`)
- [x] Pasta `_setup/` criada — 5 arquivos "PROJECT INSTRUCTIONS" prontos para colar no claude.ai
- [x] Diretrizes das 5 especialidades atualizadas: aviso de IA **removido** das peças
- [x] Gerador DOCX (`_tools/gerar_docx.py`) e gerador PDF (`_tools/gerar_pdf.py`) criados
- [x] Primeira peça de teste gerada (Representação Criminal — Maria da Penha)

### 29/06/2026 — Repositório e template base
- [x] Repositório remoto criado e push feito — github.com/epifanioangelo/assistente-jurista
- [x] Template único definido: `Modelos jus/AGRAVO_INSTRUMENTO.docx` (estilos AE, cabeçalho/rodapé navy)

### 30/06/2026 — Agentes AE e especialidade 06
- [x] Agentes `ae-*` criados em `~/.claude/agents/`: `ae-gerador`, `ae-habeas-corpus`, `ae-canabico`, `ae-notificacao-extrajudicial`, `ae-defesa-penal`
- [x] Especialidade 06 criada: **Violência Doméstica e Penal** (lacuna identificada na sessão de 28/06)

### 05/07/2026 — Primeiro caso real
- [x] Token GitHub renovado, push voltou a funcionar
- [x] Confirmado com Angelo: repositório é **privado** — dados de casos reais podem ser versionados
- [x] Primeiro caso real processado: petição de reconsideração de medidas protetivas "Deborah Cunha" (Lei Maria da Penha)
- [x] Bug identificado: marcador `@LISTA_ALFA` não numera automaticamente no template `AGRAVO_INSTRUMENTO.docx` (precisa digitar "a) b) c)" manualmente)
- [x] Base `_analises/` iniciada — manuais/teses convertidos de PDF para `.md`

### 06/07/2026 — Pacote Clabs e hook de citações
- [x] Pacote "Clabs" (Criminal Lab) instalado: 32 agentes + 107 skills de prática criminal
- [x] Hook de verificação de citações corrigido — movido de `Documents/Assistente jurista/.claude/settings.json` (nunca disparava) para `~/.claude/settings.json` (funcionando)
- [x] Regra permanente adicionada ao CLAUDE.md: sempre consultar `_analises/INDICE.md` antes de redigir peça

### 07/07/2026 — Limpeza de duplicidade
- [x] Identificados 22 agentes `clabs-*` redundantes com equivalentes `bravy-*` já instalados — removidos de `~/.claude/agents/` (mantidos arquivados em `_pacotes/`)
- [x] Restam 10 agentes `clabs-*`: 8 exclusivos + 2 duplicatas criminais intencionais (HC e resposta à acusação)

### 08/07/2026 — Agente ae-jusracial
- [x] Novo agente `ae-jusracial` instalado (defesa de terreiros/religiões de matriz africana + injúria racial como racismo)
- [x] 5 PDFs de apoio convertidos para `_analises/religiao/` (3 com texto extraído, 2 via OCR)
- [x] Tesseract instalado — `pdf_para_md.py` ganhou fallback automático de OCR para qualquer PDF futuro sem texto extraível
- [x] Precedentes Iturama/MG e memorial Hédio Silva Jr. (RE 494.601/STF) verificados e movidos para seção de precedentes confirmados no agente

### 09/07/2026 — Tese do TCC incorporada
- [x] `ae-jusracial` enriquecido com a Teoria da Irradiação Coletiva da Ofensa por Classificação Grupal (capítulo 4 do TCC de Angelo — ver [[project-tcc]])
- [x] Marcado explicitamente no agente como "tese em desenvolvimento do próprio subscritor" (TCC ainda não defendido — defesa prevista out/2026)
- [x] `_memoria/project_status.md` atualizado para refletir todas as sessões acima (este arquivo)

---

## O que está pendente

- [ ] Configurar os 6 projetos no claude.ai (Fase 0 original — ainda não feito; usar arquivos prontos em `_setup/`, criar o 06 que falta)
- [ ] Fazer primeiro teste real com caso concreto direto no claude.ai (fora do Claude Code)
- [ ] Substituir texto "AE" do cabeçalho/rodapé do template DOCX por logo em imagem (PNG)
- [ ] `ROADMAP.md` também está desatualizado (ainda descreve só a Fase 0 original de 28/06) — considerar atualização numa próxima sessão

## Observação sobre o ritmo real do projeto

O trabalho de 30/06 a 09/07 foi consideravelmente além do escopo original da Fase 0 (que previa só configurar 5 projetos no claude.ai): instalação e curadoria de pacotes de agentes/skills de terceiros (Bravy, Clabs), criação de agente próprio original (`ae-jusracial`) com pesquisa jurídica substantiva, processamento de caso real, e infraestrutura de base de conhecimento (`_analises/` com OCR). A Fase 0 "on-paper" segue com poucas caixas marcadas, mas o projeto avançou mais do que o roadmap original media.

## Como configurar cada projeto no claude.ai

1. claude.ai → Projects → New Project
2. Nome: `Assistente Jurídico — [Especialidade]`
3. **Project Instructions:** abrir `_setup/0X - Especialidade — PROJECT INSTRUCTIONS.md` → selecionar tudo → colar
4. **Project Knowledge:** fazer upload de `03`, `06`, `07`, `08` da pasta da especialidade
5. Arquivos `04` e `05` → colar na conversa quando for usar

## Fluxo de uso diário

1. Abrir o projeto da especialidade no claude.ai
2. Iniciar **conversa nova** → fazer upload dos documentos do caso (PDF, Word, fotos)
3. Colar Prompt Mestre (arquivo 04) ou Fluxo Guiado (arquivo 05)
4. IA extrai fatos e gera o texto da peça com marcadores de formatação
5. Salvar o texto em `Pecas geradas/nome_do_caso.txt`
6. `python3 _tools/gerar_docx.py entrada.txt saida.docx` → abre no Word
7. Revisar, preencher placeholders, ajustar → imprimir / salvar como PDF

## Fase seguinte (quando ativar)

**Fase 1 — Sistema Web MVP**
Pré-requisito: ter testado e validado o fluxo da Fase 0 com pelo menos 3 casos reais.
Ver detalhes em `ROADMAP.md`.
