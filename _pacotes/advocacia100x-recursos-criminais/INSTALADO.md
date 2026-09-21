# Advocacia 100X — 4 skills de recursos criminais aos tribunais superiores — instalado em 21/09/2026

**Origem:** 4 zips (`acusacao-recurso-especial-extraordinario-mp.zip`, `agravo-em-resp-re.zip`, `recurso-especial-criminal.zip`, `revisao-e-validacao-de-recurso-especial-criminal.zip`) colocados pelo Angelo na raiz do projeto em 21/09/2026, pedido explícito de instalação. Vendor: **Advocacia 100X** (`alunos.advocacia100x.com.br`), repositório declarado `github.com/bbpropulse/skills-enriquecimento.git` — curso/produto licenciado, mesmo padrão de proveniência já usado para Criminal Lab, Fernanda Dornellas (usucapião) e Tipografia Jurídica Associados.

**O que são:**
- `agravo-em-resp-re` — **já existia** (Criminal Lab). Sobreposição de nome real.
- `recurso-especial-criminal` — **já existia** (Criminal Lab). Sobreposição de nome real.
- `acusacao-recurso-especial-extraordinario-mp` — novo. REsp/RE pelo polo acusatório (MP/assistente) — sem equivalente local.
- `revisao-e-validacao-de-recurso-especial-criminal` — novo. Auditoria de REsp já redigido, 8 blocos de admissibilidade, veredito estruturado — sem equivalente local.

## Decisão sobre as 2 sobreposições — não foi substituição cega

As duas skills já instaladas (Criminal Lab) eram boas e já seguiam a convenção do projeto (`type: prompt`, `description` com "Aciona com" completo). O conteúdo novo trazia uma coisa que elas não tinham: uma reforma processual real e recente — **Lei 15.484/2026** (filtro de relevância para REsp no STJ, sancionada 04/08/2026, em vigor desde 03/09/2026) e a **Emenda Regimental STJ 55/2026** — **confirmada via WebSearch em 21/09/2026** (Migalhas, Senado Notícias, STJ, TJRJ) antes de aceitar qualquer coisa.

Em vez de sobrescrever os arquivos inteiros (ação bloqueada pelo classificador de segurança como "Irreversible Local Destruction" na primeira tentativa, e also arriscava perder conteúdo já bom), apliquei **edições cirúrgicas** nos dois arquivos existentes:
- Corrigida a única informação desatualizada (diziam que o filtro estava "em estágio de regulamentação"; hoje está em vigor).
- Inserida a seção "Adendo — regime de relevância" com o texto verificado, no mesmo ponto em que o pacote novo a colocava.
- Versão bump para `1.1.0`.
- Todo o resto do conteúdo original (que já era bom) foi preservado.

As outras 2 skills (`acusacao-recurso-especial-extraordinario-mp`, `revisao-e-validacao-de-recurso-especial-criminal`) não tinham equivalente — instaladas por completo, com frontmatter normalizado para o padrão do projeto (`type: prompt`, `description` com gatilhos completos em vez do formato truncado "…" do pacote original) e citações específicas ainda não conferidas marcadas `[NÃO VERIFICADO]` (ex.: HC 120.275/STF, HC 482.549/STJ, REsp 1.595.636/RN — citadas pelo pacote sem essa ressalva).

## Arquivos de referência mantidos

Cada skill ganhou uma pasta `references/` com o material de apoio do próprio pacote:
- `high-performance-contract.md` (as 4) — protocolo operacional condensado, já embutido no corpo do SKILL.md também.
- `fontes-oficiais-transcritas.md` (só em `revisao-e-validacao-de-recurso-especial-criminal`) — transcrição literal de CF art. 105, Lei 15.484/2026 (texto integral do art. 1.035-A) e outras fontes, com data de leitura. Conferi um trecho contra o texto oficial via WebSearch e bateu.

## Pendências

- Citações `[NÃO VERIFICADO]` nas 2 skills novas ainda não foram conferidas uma a uma (a maior parte do pacote já vem com essa disciplina; um punhado ficou sem, e eu marquei ao instalar).
- `~/.claude/skills/` não é versionado em git — este arquivo é o único registro de proveniência que sobrevive no repositório do projeto.
