# Criminal Lab — Kit 73 Skills Execução Penal — instalado em 21/09/2026

**Status:** as 73 skills foram copiadas para `~/.claude/skills/` (prefixo `ep-*`) em 21/09/2026, após análise das 9 sobreposições abaixo. Nenhuma skill existente foi removida ou sobrescrita — convivem lado a lado. `~/.claude/skills/` não é versionado em git (fica só neste projeto o registro de proveniência).

**Achado da análise das 9 sobreposições:** não são duplicatas reais — são duas arquiteturas diferentes. As skills `execucao-*` já instaladas são referência narrativa autocontida (lei + tabela + template de petição pronto pra preencher + citações de julgados específicos embutidas). As novas `ep-*` são um par diagnóstico→peça, com saída em JSON, integração de orquestrador (`case_id`/`task_id`), pontuação de risco/confiança, e regra explícita de **nunca** embutir número de julgado não verificado — desenho mais rígido contra alucinação, mas sem tabela/template prontos. Mantidas as duas por serem complementares (rascunho rápido × pipeline rigoroso), sem colisão de nome (`ep-` prefixo vs. nome simples).

**Correção aplicada nas 6 skills `execucao-*`/`agravo-em-execucao` que citavam julgados específicos (HC/REsp/AgRg/Informativo/Tema) sem nenhuma ressalva:** adicionada a mesma cautela de vigência já usada em outras skills do projeto — tratar cada julgado citado por número como `[NÃO VERIFICADO]` até confirmação via `jurisprudencia-stj-stf` + `verificador-citacoes`. Afetadas: `execucao-indulto-comutacao` (não tinha ressalva alguma, era a mais exposta), `execucao-progressao-regime` (tinha ressalva fraca, reforçada), `execucao-remicao`, `execucao-saida-temporaria`, `execucao-unificacao-penas`, `agravo-em-execucao`. `execucao-livramento-condicional` e `execucao-provisoria-pena` já tinham a ressalva completa — não mexidas.

**Origem:** zip `d59caf80-3995-41fe-9488-c12fe08dadc0.zip` (nome de download genérico), encontrado solto na raiz do projeto em 21/09/2026 — apareceu **durante** esta sessão (timestamp 12:31, no meio do trabalho de reorganização), não fazia parte do levantamento inicial. Mesmo vendor ("Criminal Lab") dos agentes `clabs-*` já instalados em `~/.claude/agents/`.

**O que é:** kit comercial com 73 skills especializadas em **Execução Penal**, namespace `ep-*` (prefixo próprio, sem colisão de nome com as skills já instaladas). Contém manual em PDF/DOCX, o pacote completo, 73 zips individuais (`criminal-lab-73-skills-execucao-penal-zips-individuais.zip`) para upload avulso, e um fallback para Custom GPT/Projeto ChatGPT.

**Por que não foi instalado nesta sessão:** ao contrário do CriminalRadar (plugin auto-namespaced, sem risco de colisão), este kit **tem sobreposição funcional real** com skills já existentes neste projeto — a regra de memória do usuário ("checar duplicidade funcional, não só nome, antes de instalar pacote novo") exige comparação item a item antes de qualquer instalação em massa. Decisão de instalar (tudo, parte, ou nada) cabe ao Angelo/Vanildo.

## Sobreposição identificada com skills já instaladas (`~/.claude/skills/`)

| Skill já existente | Equivalente(s) no kit novo |
|---|---|
| `agravo-em-execucao` | `ep-peca-agravo-execucao` |
| `execucao-indulto-comutacao` | `ep-indulto-comutacao`, `ep-peca-indulto-comutacao` |
| `execucao-livramento-condicional` | `ep-livramento-condicional`, `ep-peca-livramento-condicional` |
| `execucao-progressao-regime` | `ep-progressao-regime`, `ep-peca-progressao-regime` |
| `execucao-provisoria-pena` | `ep-execucao-provisoria` |
| `execucao-remicao` | `ep-remicao-calculator`, `ep-peca-remicao` |
| `execucao-saida-temporaria` | `ep-saida-temporaria-trabalho-estudo` |
| `execucao-unificacao-penas` | `ep-detracao-unificacao-nova-condenacao` (parcial) |
| skill/agente `habeas-corpus` (genérico) | `ep-peca-habeas-corpus-execucao` (especializado em execução) |

Nesses casos caberia **decidir por skill** — manter a existente, substituir pela nova (mais especializada em execução penal), ou mesclar o melhor de cada uma — não uma escolha única para o pacote inteiro.

## Sem equivalente hoje (maioria do kit — ~64 das 73)

Cobertura nova real: auditoria de cálculo de pena, detector de benefícios vencidos, leitor de SEEU, extrator de dados executórios, linha do tempo executória, triagem de família/atendimento, exame criminológico, PAD/falta grave, medida de segurança, monitoração eletrônica, harmonização de domiciliar, LGPD/sigilo penal, simuladores (julgador/MP), banco de teses, revisores (jurídico/cálculo/jurisprudência/probatório), editor persuasivo, memoriais para sustentação oral, entre outras — lista completa no `CATALOGO.json` dentro do zip.

## Passos para decidir (quando o Angelo quiser)

1. Extrair `criminal-lab-kit-73-skills-execucao-penal.zip`.
2. Ler `Manual_Criminal_Lab_73_Skills_Execucao_Penal_ChatGPT_Claude.pdf` (visão geral do vendor sobre cada skill).
3. Para os 9 itens da tabela de sobreposição: decidir manter/substituir/mesclar, um a um.
4. Para o restante: instalar em lote (copiar os `.md` para `~/.claude/skills/<nome>/SKILL.md`, como já feito com os pacotes Bravy/Clabs anteriores) ou seletivamente.

**Não instalado nem parcialmente processado nesta sessão** — fica só arquivado, aguardando decisão.
