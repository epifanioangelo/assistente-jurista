# ⚖️ 139 Skills de Prática Criminal para o Claude Code

**Criminal Lab** — o arsenal completo do criminalista dentro do Claude Code: 107 skills de peças e institutos + 32 agentes especialistas, cobrindo da porta do inquérito ao Supremo Tribunal Federal.

## O que você recebe

**Skills de peças e institutos (107)** — cada uma ensina o Claude a metodologia, a base legal, a estrutura forense, as teses típicas e as pegadinhas de prazo/preclusão:

- **Investigação e fase pré-processual:** defesa no inquérito, plantão pós-flagrante (primeiras 24h), audiência de custódia, acesso a autos de investigação (SV 14), habilitação/acesso aos autos, pedido de diligências, produção antecipada de provas, arquivamento de inquérito, acompanhamento de depoimento em CPI/PIC, investigação defensiva corporativa
- **Prisão e cautelares:** habeas corpus, liberdade provisória/relaxamento, prisão domiciliar, levantamento de medidas assecuratórias, liberação de bens na lavagem, restituição de coisas apreendidas
- **Instrução, incidentes e audiências:** resposta à acusação, resposta preliminar, exceções processuais, inquirição de testemunhas, quesitos de perícia, incidente de insanidade mental, incidente de falsidade documental, resposta a *mutatio/emendatio*, preparação de interrogatório do cliente, memoriais, alegações finais orais, preparação e transcrição de audiência
- **Provas e nulidades:** impugnação de interceptação/sigilo, de infiltração e ação controlada, de cadeia de custódia, de prova de embriaguez, preservação de prova digital, matriz de contradições da prova oral
- **Recursos (do 2º grau ao STF):** apelação, RESE, embargos de declaração/infringentes, contrarrazões (×3), revisão criminal, REsp criminal, RE criminal, AREsp/agravo em RE, agravo regimental, ED-prequestionamento, HC em STJ/STF, Recurso Ordinário em HC, reclamação constitucional, carta testemunhável, sustentação oral nos tribunais
- **Execução penal e institutos pós-condenatórios:** progressão, livramento, remição, saída temporária, unificação, indulto/comutação, agravo em execução, execução provisória, medida de segurança, sursis da pena, reabilitação criminal, retificação de antecedentes, transferência de direitos do preso
- **Tribunal do Júri:** defesa na pronúncia, quesitação, plenário e debates, mapa completo do júri
- **Justiça negocial:** ANPP, transação penal, suspensão condicional do processo, colaboração premiada, composição civil dos danos (JECRIM)
- **Defesa por matéria (nichos):** armas (posse/porte), violência doméstica (protetivas de urgência, revogação/flexibilização, descumprimento — art. 24-A, Lei Henry Borel), crimes sexuais e depoimento especial, ECA (defesa em ato infracional e execução de medida socioeducativa), lavagem de capitais, organização criminosa, crimes tributários (extinção pelo pagamento) e apropriação indébita previdenciária, fraude eletrônica, crimes ambientais, contravenções penais, crimes contra a pessoa idosa, suspensão do direito de dirigir
- **Querelante e vítima:** queixa-crime, representação, requerimento de investigação, retratação, assistente de acusação, interpelação judicial (pedido de explicações), perdão/perempção na ação privada
- **Ministério Público e consultivo:** denúncia, parecer jurídico criminal
- **Escritório e incidentes transversais:** habilitação/procuração com poderes especiais, extinção da punibilidade/prescrição, justiça gratuita e isenção de custas, DJEN (API oficial do CNJ)
- **Redação (transversal):** `redacao-persuasiva-criminal` — a régua de obra-prima (teoria do caso, subsunção explícita, coesão e persuasão) que eleva TODAS as peças

**Agentes especialistas (32)** — subagentes que o Claude aciona automaticamente: pesquisa de jurisprudência STJ/STF, lei e súmula, doutrina, ementário, tese repetitiva, **verificador de citações** (anti-jurisprudência inventada), mapa de nulidades, dosimetria da pena, análise de denúncia e de contradições, resumo de processo, cadeia de custódia de prova digital, e a rotina do escritório (triagem, onboarding, honorários, contratos, procuração, parecer, prazos, intimações, agenda, follow-up, secretária jurídica).

## Requisitos

- **Claude Code** instalado (CLI, app desktop ou extensão da IDE)
- **Node.js 18+** (o mesmo que o Claude Code já usa)

## Instalação — escolha o seu caminho

📖 **Guia completo com imagens:** abra o `Guia-de-Instalacao-139-Skills.pdf` (incluído neste pacote) — passo a passo ilustrado para os três ambientes.

**A) Claude Code (pacote completo — skills + agentes):**

1. Extraia este ZIP em qualquer pasta.
2. No terminal, dentro da pasta extraída, rode:

```bash
node instalar.mjs
```

3. Feche e reabra o Claude Code. Pronto — as skills valem para **todas** as suas conversas.

O instalador **nunca sobrescreve** skills ou agentes que você já tenha com o mesmo nome.
*(Manual: copie `skills/` para `~/.claude/skills/` e `agents/` para `~/.claude/agents/`.)*

**B) Claude Web (claude.ai) e Claude Desktop (skills):**

1. Habilite **Code execution** e **File creation** em Settings → Capabilities.
2. Em Settings → **Customize → Skills**, clique em "+" e envie os ZIPs da pasta **`zips-claude-web/`** (um por skill — já no formato que o site exige).
3. Instalou uma vez, vale no site, no desktop e no celular — é a mesma conta.

⚠️ Use sempre a pasta `zips-claude-web/` no site (a pasta `skills/` é a versão Claude Code — o site rejeita a descrição longa). Os agentes são um recurso exclusivo do Claude Code.

## Como usar

Peça em linguagem natural — a skill certa é acionada pelo contexto:

- *"Cliente preso em flagrante ontem — prepara a audiência de custódia"*
- *"Monta a apelação contra essa sentença"* (anexe a sentença)
- *"O prazo do agravo regimental no STJ é de quantos dias? Redige a peça"*
- *"Calcula a prescrição deste caso"* · *"Cabe ANPP aqui?"*
- *"O delegado negou acesso ao inquérito — o que faço?"*
- *"Impugna a quebra da cadeia de custódia dessa prova digital"*

## ⚠️ Aviso importante (leia)

Todo conteúdo gerado é **rascunho técnico de apoio**. A conferência de cada citação, a adequação ao caso concreto e a responsabilidade profissional final são **sempre do(a) advogado(a)** (Provimento 205/2021-OAB). As skills instruem o Claude a **verificar jurisprudência antes de citar** e a marcar `[NÃO VERIFICADO]` o que não confirmar — não protocole nada sem revisar.

## Suporte

Dúvidas e atualizações: entre em contato com a **Criminal Lab**.

---
© Criminal Lab — uso licenciado. Proibida a reprodução ou redistribuição sem autorização. Ver `LICENCA.md`.
