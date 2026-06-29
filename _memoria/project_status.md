# STATUS DO PROJETO — ASSISTENTE JURISTA

## Fase atual: FASE 0 — Configuração Claude.ai Projects

**Iniciado em:** 28/06/2026
**Última sessão:** 28/06/2026

---

## O que foi feito (28/06/2026)

- [x] Estrutura de arquivos completa para 5 especialidades (01 a 05)
- [x] Modelos .docx das peças em `Modelos jus/` (7 documentos)
- [x] Git inicializado no projeto
- [x] CLAUDE.md criado (instruções para sessões Claude Code)
- [x] ROADMAP.md criado (algoritmo completo Fase 0 → Fase 5)
- [x] Sistema de memória criado (`_memoria/`)
- [x] Pasta `_setup/` criada — 5 arquivos "PROJECT INSTRUCTIONS" prontos para colar no claude.ai (Diretrizes + Estilo de cada especialidade já combinados)
- [x] Diretrizes das 5 especialidades atualizadas: aviso de IA **removido** das peças
- [x] Gerador DOCX (`_tools/gerar_docx.py`) criado:
  - Usa os templates existentes em `Modelos jus/` como base (preserva fontes Manuale/Alegreya Sans, estilos, margens)
  - Suporta: @LINHA_DO_TEMPO, @TABELA_QUESTOES, @TABELA_PROVAS, @TABELA_URGENCIA, @TABELA_LIVRE, @LISTA_ALFA, @BULLETS, @CITACAO, @IMAGEM, @TITULO, @SUBTITULO, @CENTRO, @ASSINATURA
- [x] Gerador PDF (`_tools/gerar_pdf.py`) criado (para arquivo final após assinatura)
- [x] Primeira peça de teste gerada: Representação Criminal com Medidas Protetivas (Maria da Penha) em `Pecas geradas/`
- [x] Fluxo validado: IA gera texto → gerador converte para DOCX → advogado revisa/edita no Word → imprime/arquiva como PDF

## O que está pendente (próxima sessão)

- [x] Repositório remoto criado e push feito — github.com/epifanioangelo/assistente-jurista (29/06/2026)
- [ ] Configurar os 5 projetos no claude.ai
  - Usar os arquivos prontos em `_setup/` para Project Instructions
  - Fazer upload dos arquivos 03, 06, 07, 08 de cada especialidade como Project Knowledge
  - Começar pelo Cível
- [ ] Fazer primeiro teste real com caso concreto no claude.ai
- [ ] Criar especialidade 06: Violência Doméstica e Penal (identificada como lacuna na sessão de hoje)

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
