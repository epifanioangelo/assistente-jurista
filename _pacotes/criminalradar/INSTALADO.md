# CriminalRadar v1.0.0 — pacote arquivado, instalação pendente

**Origem:** zip `dd67940e-c8eb-45d2-9db8-f4450dfd0a4a.zip` (nome de download genérico, sem indicação de proveniência), encontrado solto na raiz do projeto em 21/09/2026.

**O que é:** plugin oficial de Claude Code (não um pacote de agentes soltos como Bravy/Clabs) — `.claude-plugin/plugin.json`, `name: "criminalradar"`. Monitora DJEN (inclusive intimações do SEEU) e DataJud por OAB/processo/parte, classifica publicações por urgência e prazo penal (CPP 798), gera relatório executivo em PDF e envia por e-mail (conector Gmail do claude.ai), com agendamento automático (launchd/cron) fora do Claude. Licença proprietária, uso licenciado, redistribuição não autorizada.

**Comandos previstos:** `/criminalradar:configurar`, `:relatorio`, `:agendar`, `:status`, `:processos`, `:ajuda`.

**Por que não foi instalado nesta sessão:** o instalador (`instalar.command`) roda `claude plugin marketplace add`/`claude plugin install`, que modifica o registro global de plugins do Claude Code — ação sensível, bloqueada pelo classificador de auto-mode ao tentar rodar via Bash. O instalador foi desenhado pra duplo clique manual mesmo (fluxo interativo, pede OAB/e-mails reais, testa conexão, agenda) — não é algo pra automatizar sem supervisão.

**Não há colisão real de nomes** com os agentes `bravy-monitor-dje-djen`/`bravy-andamento-processual` já instalados: os agentes do CriminalRadar (`agents/monitor-dje-djen.md`, `agents/andamento-processual.md`, `agents/execucao-penal-seeu.md`) vivem dentro do namespace do próprio plugin, não em `~/.claude/agents/` solto — não sobrescrevem nem competem com o que já existe.

## Passos pra instalar de verdade (quando o Angelo quiser)

1. Extrair o zip (`_pacotes/criminalradar/criminalradar-v1.0.0.zip`).
2. Dar duplo clique em `instalar.command` (registra o plugin — copia pra `~/CriminalRadar/criminalradar`, chama `claude plugin marketplace add`/`install`).
3. Reiniciar o Claude Code.
4. `/criminalradar:configurar` — pede número da OAB/UF real, e-mails que recebem o relatório, papel predominante (defesa/acusação/misto), horário. Testa conexão com DJEN/DataJud e manda e-mail de teste.
5. `/criminalradar:agendar` — liga o envio automático diário.

**Dado real necessário que eu não tenho e não devo supor:** número da OAB do Angelo (ou de quem for monitorado) e os e-mails que devem receber o relatório — isso só o próprio Angelo fornece na etapa 4.
