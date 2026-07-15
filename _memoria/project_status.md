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

### 14-15/07/2026 — Skill tipografia-juridica + curso Tipografia Jurídica
- [x] Skill global `tipografia-juridica` criada (`~/.claude/skills/tipografia-juridica/SKILL.md`) a partir do prompt "Organização Visual de Peças Jurídicas.pdf" — padrão obrigatório de elementos visuais (tabelas, linhas do tempo, listas) em toda peça, nova ou reformatada
- [x] Regra registrada em `CLAUDE.md` e template AE x NPJ_BASE (contextos A/B/C) confirmado e documentado na memória do usuário
- [x] Segundo prompt do mesmo curso ("Assistente de Síntese Estratégica de Peças Jurídicas.pdf") analisado — vira skill `sintese-estrategica` (resumo de 1ª página p/ leitura do juiz) — **ainda não construída**, aguardando decisão do Angelo
- [x] 59 arquivos .docx do curso "Tipografia Jurídica Associados" (ChatGPT) movidos para `Modelos jus/Curso Tipografia Jurídica/` e analisados por amostragem — são exemplos trabalhados (não templates plugáveis; estilos inconsistentes entre arquivos), cobrindo praticamente todo tipo de documento do escritório
- [x] `tipografia-juridica` ampliada para v1.1.0 com 2 modelos novos extraídos do curso: Modelo 11 (linha do tempo horizontal de tempestividade) e Modelo 12 (card de jurisprudência/precedente — com regra explícita de nunca usar citação fictícia)

### 15/07/2026 — Pendências resolvidas: sintese-estrategica, procuração tabular, docs fora de peça
- [x] Skill global `sintese-estrategica` criada (`~/.claude/skills/sintese-estrategica/SKILL.md`) a partir do prompt "Assistente de Síntese Estratégica de Peças Jurídicas.pdf" — quadro-resumo de 1ª página, padrão obrigatório junto com a `tipografia-juridica`. Formato "Quadro jurídico" (MODO A, automático) validado contra `1. RECURSO ESPECIAL.docx` e `1. MEMORIAL.docx` do curso, com linhas específicas por tipo de peça (inicial/contestação/réplica/recurso/peça objetiva). MODO B mantém o fluxo original do prompt (propor 2-4 formatos, usuário escolhe).
- [x] `tipografia-juridica` v1.2.0: Modelo 13 (procuração tabular — 4 blocos Outorgante/Outorgado/Poderes/Finalidade, validado contra `1. PROCURAÇÃO (1).docx`, reaproveitando o marcador `@TABELA_URGENCIA` já existente no `gerar_docx.py`, sem código novo).
- [x] `bravy-procuracao.md` (agente pré-empacotado) ganhou seção 2.1 apontando para o Modelo 13 quando a procuração for gerada dentro do pipeline `gerar_docx.py` — mesmo padrão de "exceção pontual" já usado no agente de usucapião (12/07).
- [x] `bravy-minuta-contrato-servicos.md` ganhou nota pontual sobre quadros-resumo (dados de imóvel/pagamento em tabela) referenciando `2. CONTRATO (1).docx` / `3. CONTRATO (2).docx` do curso.
- [x] Notificação extrajudicial: **já estava coberta** — `ae-notificacao-extrajudicial.md` já usa `@TABELA_SUMARIO`/`@TABELA_URGENCIA`, nenhuma mudança necessária.
- [x] Decisão sobre currículo/proposta comercial/acompanhamento processual (docs fora de peça, sem agente próprio hoje): **não construir agente dedicado agora** — não são peças jurídicas, e nada na prática atual do escritório (defesa criminal, VD, injúria racial, XKOO, TCC) indica necessidade imediata. Ficam arquivados como referência em `Modelos jus/Curso Tipografia Jurídica/` para quando (se) surgir demanda real.
- [x] `CLAUDE.md` atualizado com a regra permanente da `sintese-estrategica` ao lado da `tipografia-juridica`.

### 15/07/2026 (continuação) — teste end-to-end + correção de rótulo
- [x] `sintese-estrategica` testada pela primeira vez: peça simulada completa (petição inicial fictícia, "Roberto Carlos Almeida Santos x Banco Fictício Nacional S.A.", negativação indevida), com todos os elementos — quadro-resumo, linha do tempo, tutela de urgência, card de jurisprudência (Súmula 548/STJ, verificada de verdade), danos e valores — gerada em DOCX e convertida em PDF pronto (`docx2pdf`, via Microsoft Word instalado na máquina). Auditoria de citações: **aprovado** (após 1 ressalva textual corrigida — ver abaixo).
- [x] Mesma peça gerada também no contexto NPJ (`NPJ_BASE.docx`, assinatura Núcleo de Prática Jurídica/Faculdade Vanguarda) — confirma que a tipografia jurídica e a síntese estratégica funcionam igual nos dois templates.
- [x] Angelo notou que o rótulo impresso "SÍNTESE ESTRATÉGICA" soava como sinalização de tentativa de persuadir o juiz — corrigido para "QUADRO-RESUMO" (termo neutro, validado no curso). Regra travada na skill `sintese-estrategica` (v1.0.1): "estratégica" nunca aparece no texto impresso da peça, só na conversa com o usuário.
- [x] Arquivos de teste em `Pecas geradas/Inicial_Roberto_Santos_SIMULACAO_15-07-2026.*` (AE) e `Inicial_Roberto_Santos_SIMULACAO_NPJ_15-07-2026.*` (NPJ).

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
