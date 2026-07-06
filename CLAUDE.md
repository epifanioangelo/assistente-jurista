# ASSISTENTE JURISTA — Instruções para Sessões Claude Code

## O que é este projeto

Sistema de IA jurídica para elaboração de peças processuais, análise de casos, pesquisa de jurisprudência e estratégia contenciosa. Estruturado em 6 especialidades, cada uma com seu próprio conjunto de diretrizes, prompts e modelos.

## Estrutura de pastas

```
Assistente Jurista/
├── 01 - Advogado Cível/              ← diretrizes + prompts área cível
├── 02 - Advogado Trabalhista/        ← diretrizes + prompts área trabalhista
├── 03 - Advogado Público e Adm./     ← diretrizes + prompts área pública
├── 04 - Judiciário e Gabinetes/      ← diretrizes + prompts gabinetes
├── 05 - Advogado Empresarial/        ← diretrizes + prompts área empresarial
├── 06 - Violência Doméstica e Penal/ ← diretrizes + prompts criminal/VD (criado 30/06/2026)
├── Modelos jus/                       ← templates .docx das peças
├── _memoria/                          ← memória do projeto (ler sempre ao iniciar)
├── ROADMAP.md                         ← algoritmo completo de desenvolvimento
└── CLAUDE.md                          ← este arquivo
```

## Arquivos por especialidade (padrão em todas as 5 pastas)

| Arquivo | Papel |
|---------|-------|
| 01 - Diretrizes Permanentes | "DNA" da IA — fixa no Claude como system prompt |
| 02 - Estilo de Escrita Jurídica | Como escrever (tom, período, vocabulário) |
| 03 - Estrutura e Modelo (ABNT) | Esqueleto literal da peça + formatação Word |
| 04 - Prompt Mestre — Geração Direta | Usuário tem tudo; IA entrega de uma vez |
| 05 - Prompt Fluxo Guiado | IA conduz 10 etapas antes de entregar a peça |
| 06 - Direcionamento Estratégico | Tese principal, pontos a enfatizar/evitar |
| 07 - Caso Concreto para Simulação | Template de dados do caso (preencher por caso) |
| 08 - Checklist de Revisão Humana | Lista de conferência antes do protocolo |

## Ao iniciar qualquer sessão neste projeto

1. Ler `_memoria/MEMORY.md` para contexto atual
2. Ler `ROADMAP.md` para saber fase atual de desenvolvimento
3. Verificar se há tarefas pendentes em `_memoria/project_status.md`

## Regras permanentes deste projeto

- Todo conteúdo gerado é minuta — nunca protocolar sem revisão humana
- Nunca inventar jurisprudência, artigos de lei ou fatos não fornecidos
- Usar sempre DADOS INSUFICIENTES quando faltar informação essencial
- Ao criar novos arquivos de diretrizes: seguir o padrão dos existentes em `01 - Advogado Cível/`
- Commits frequentes — nada se perde

## Antes de redigir qualquer peça ou dar parecer sobre um caso concreto

Skills e agentes disparam sozinhos pela descrição do caso, mas o material de referência em `_analises/` (manuais, teses, ementários, checklists — convertidos de PDF para `.md`) é passivo: só é usado se alguém procurar por ele. Portanto, **antes de redigir a peça ou fundamentar a análise**, sempre:

1. Identificar a área do caso (penal, vd, familia, previdencia, canabico, geral, ou outra pasta que exista em `_analises/`).
2. Rodar `grep -ril 'palavra-chave' _analises/<área>/` (ou consultar `_analises/INDICE.md`) buscando pelo tipo penal, instituto ou tema específico do caso — não só em Penal, em **qualquer área** que tenha material salvo (cível, trabalhista, tributário, etc., conforme forem sendo adicionados).
3. Se houver tese, súmula ou estratégia relevante no material encontrado, incorporar à análise/peça (citando a fonte), em vez de redigir só com conhecimento genérico.
4. Se nada relevante for encontrado, seguir normalmente — mas não pular esta etapa silenciosamente.

Isso vale tanto para peças penais quanto cíveis, trabalhistas, previdenciárias etc. — qualquer área em que exista (ou venha a existir) material salvo em `_analises/`.
