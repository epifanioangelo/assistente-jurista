# ROADMAP — ASSISTENTE JURISTA IA
> Algoritmo completo de desenvolvimento — da configuração inicial ao sistema web completo.
> Atualizar este arquivo a cada sessão que avance uma fase ou adicione funcionalidade.

---

## VISÃO GERAL DO PROJETO

**Objetivo final:** Plataforma web de IA jurídica para elaboração de peças processuais, pesquisa de jurisprudência e gestão de casos — para uso individual do advogado ou compartilhado em escritório.

**Princípio central:** A IA nunca substitui o advogado. Ela é a ferramenta dele. Toda saída é minuta, sujeita à revisão humana obrigatória antes do protocolo.

**Stack prevista (Fase 3+):** PHP + MySQL + Claude API (Anthropic) + interface web responsiva.

---

## FASE 0 — CONFIGURAÇÃO NO CLAUDE.AI PROJECTS
**Status: EM ANDAMENTO (iniciado 28/06/2026)**

### O que é
Usar o Claude.ai (interface web) com o recurso Projects para criar um ambiente persistente por especialidade. Sem código — funciona hoje, imediatamente.

### Como configurar cada projeto (passo a passo)

**Para cada uma das 5 especialidades:**

1. Acessar **claude.ai → Projects → New Project**
2. Nomear o projeto: `Assistente Jurídico — [Especialidade]`
3. Em **Project Instructions** (Custom Instructions), colar o conteúdo de:
   - `01 - Diretrizes Permanentes da IA.md`
   - `02 - Estilo de Escrita Jurídica.md`
   (colar os dois em sequência no mesmo campo)
4. Em **Project Knowledge** (arquivos do projeto), fazer upload de:
   - `03 - Estrutura e Modelo da Peça (ABNT).md`
   - `06 - Direcionamento Estratégico.md`
   - `07 - Caso Concreto para Simulação.md`
   - `08 - Checklist de Revisão Humana.md`
5. Os prompts de uso (`04` e `05`) NÃO vão no projeto — o usuário cola na conversa quando for usar.

### 5 Projetos a criar

| Projeto | Pasta de origem |
|---------|----------------|
| Assistente Jurídico — Cível | `01 - Advogado Cível/` |
| Assistente Jurídico — Trabalhista | `02 - Advogado Trabalhista/` |
| Assistente Jurídico — Público e Adm. | `03 - Advogado Público e Administrativo/` |
| Assistente Jurídico — Judiciário | `04 - Judiciário e Gabinetes/` |
| Assistente Jurídico — Empresarial | `05 - Advogado Empresarial e Contratos/` |

### Fluxo de uso diário (Fase 0)

```
1. Abrir o projeto da especialidade no claude.ai
2. Para peça direta:  colar Prompt Mestre (arquivo 04) + Caso Concreto preenchido + Direcionamento
3. Para fluxo guiado: colar Prompt Fluxo Guiado (arquivo 05) e responder as 10 etapas
4. Receber minuta → revisar → formatar no Word com as instruções ABNT do arquivo 03
5. Protocolal após revisão humana obrigatória
```

### Entregáveis desta fase
- [x] Estrutura de arquivos criada (28/06/2026)
- [x] Git inicializado
- [x] CLAUDE.md e ROADMAP criados
- [ ] Projeto Cível criado no claude.ai
- [ ] Projeto Trabalhista criado no claude.ai
- [ ] Projeto Público e Adm. criado no claude.ai
- [ ] Projeto Judiciário criado no claude.ai
- [ ] Projeto Empresarial criado no claude.ai
- [ ] Primeiro teste real com caso concreto

---

## FASE 1 — SISTEMA WEB BÁSICO (MVP)
**Status: PLANEJADO**

### O que é
Interface web própria que encapsula o fluxo da Fase 0 em uma aplicação simples. O usuário não precisa mais colar prompts manualmente — a aplicação monta o prompt e chama a API Claude.

### Funcionalidades do MVP

1. **Seletor de especialidade** — dropdown com as 5 áreas
2. **Seletor de modo** — Geração Direta ou Fluxo Guiado
3. **Formulário de Caso Concreto** — campos estruturados (partes, fatos, documentos, valores)
4. **Formulário de Direcionamento Estratégico** — tese principal, pontos a enfatizar/evitar
5. **Chat com a IA** — interface de conversa para o Fluxo Guiado
6. **Painel de entrega** — área de artefato para copiar/exportar a peça gerada
7. **Aviso de revisão humana** — sempre visível ao receber a minuta

### Arquitetura técnica

```
assistente-jurista/
├── index.php              ← seletor de especialidade + modo
├── caso.php               ← formulário do caso concreto
├── chat.php               ← interface de conversa (fluxo guiado)
├── api.php                ← backend: monta prompt + chama Claude API
├── config.php             ← ANTHROPIC_API_KEY (nunca no git)
├── prompts/               ← versões PHP dos arquivos .md de cada área
│   ├── civel.php
│   ├── trabalhista.php
│   ├── publico.php
│   ├── judiciario.php
│   └── empresarial.php
└── assets/                ← CSS/JS da interface
```

### Chamada à API Claude (exemplo)

```php
// api.php
$systemPrompt = getDiretrizes($especialidade) . "\n\n" . getEstiloEscrita($especialidade);
$userPrompt   = montarPromptMestre($caso, $direcionamento, $especialidade);

$response = callClaudeAPI([
    'model'      => 'claude-opus-4-8',  // modelo mais capaz para trabalho jurídico
    'max_tokens' => 8000,
    'system'     => $systemPrompt,
    'messages'   => [['role' => 'user', 'content' => $userPrompt]]
]);
```

### Entregáveis desta fase
- [ ] Estrutura de pastas do projeto web
- [ ] Configuração da Claude API (Anthropic)
- [ ] Conversão dos arquivos .md para prompts PHP
- [ ] Formulário de Caso Concreto funcional
- [ ] Integração com Claude API (Geração Direta)
- [ ] Interface de Chat (Fluxo Guiado)
- [ ] Painel de entrega com botão "Copiar peça"
- [ ] Deploy em servidor (afrontar.com.br ou VPS dedicado)

---

## FASE 2 — GESTÃO DE CASOS E HISTÓRICO
**Status: PLANEJADO**

### Funcionalidades

1. **Login e autenticação** — acesso protegido por senha
2. **Banco de casos** — salvar casos com cliente, tipo, status, data
3. **Histórico de peças** — todas as minutas geradas, por caso
4. **Rascunhos** — salvar progresso do Fluxo Guiado e retomar depois
5. **Modelos personalizados** — o advogado pode customizar os templates base
6. **Exportação Word** — gerar .docx com a formatação ABNT correta automaticamente

### Banco de dados (MySQL)

```sql
casos (id, cliente, tipo_acao, especialidade, status, criado_em)
pecas (id, caso_id, tipo_peca, conteudo_md, conteudo_docx, criado_em)
conversas (id, caso_id, role, conteudo, criado_em)
modelos (id, especialidade, tipo, nome, conteudo, padrao)
```

### Entregáveis desta fase
- [ ] Sistema de autenticação (login/senha)
- [ ] CRUD de casos
- [ ] Histórico de peças por caso
- [ ] Salvamento automático de rascunhos
- [ ] Exportação .docx com python-docx ou PHPWord

---

## FASE 3 — BUSCA DE JURISPRUDÊNCIA INTEGRADA
**Status: PLANEJADO**

### O problema atual
O Princípio da Veracidade das Diretrizes proíbe a IA de inventar jurisprudência. O advogado precisa fornecer os acórdãos manualmente. Isso limita a produtividade.

### Solução

Integrar fontes públicas de jurisprudência para que o sistema busque acórdãos reais e os injete no contexto da peça:

| Fonte | API/Método | Dados disponíveis |
|-------|-----------|-------------------|
| STJ | API pública (jurisprudencia.stj.jus.br) | acórdãos, súmulas |
| STF | API pública (portal.stf.jus.br) | acórdãos, súmulas vinculantes |
| TJs | Scraping ou APIs onde disponíveis | acórdãos estaduais |
| JusBrasil | API (plano pago) | busca unificada |

### Fluxo com jurisprudência integrada

```
1. Usuário descreve o tema da peça
2. Sistema extrai termos-chave automaticamente
3. Busca acórdãos relevantes nas fontes configuradas
4. Apresenta os resultados ao advogado para seleção
5. O advogado seleciona os que quer usar
6. Sistema injeta os acórdãos selecionados no contexto da IA
7. IA gera a peça com jurisprudência real, não inventada
```

### Entregáveis desta fase
- [ ] Integração STJ API
- [ ] Integração STF API
- [ ] Interface de busca e seleção de precedentes
- [ ] Injeção de precedentes selecionados no prompt
- [ ] Cache de jurisprudência para não repetir buscas

---

## FASE 4 — MULTIUSUÁRIO E ESCRITÓRIO
**Status: PLANEJADO**

### Funcionalidades

1. **Múltiplos usuários** — advogados, estagiários, secretária com permissões diferentes
2. **Clientes** — cadastro de clientes com histórico de casos
3. **Dashboard** — visão geral de casos ativos, prazos, peças pendentes
4. **Prazos processuais** — calendário com alertas
5. **Notificações** — email/WhatsApp quando peça estiver pronta para revisão
6. **Modo estagiário** — fluxo guiado obrigatório, revisão do advogado antes de finalizar

### Estrutura de permissões

```
admin (sócio)    → tudo
advogado         → seus casos + modelos + histórico completo
estagiário       → apenas fluxo guiado + submeter para revisão
secretária       → visualizar casos + clientes + agenda
```

---

## FASE 5 — RECURSOS AVANÇADOS
**Status: VISÃO FUTURA**

- **Análise de documentos** — upload de contrato/sentença → IA extrai fatos relevantes
- **Geração de minutas a partir de áudio** — advogado narra o caso, IA transcreve e gera a peça
- **Comparador de teses** — dada uma situação, IA apresenta 3 abordagens estratégicas distintas
- **Modo simulação adversarial** — IA gera a peça E a contra-argumentação da ré
- **Integração com PJe/e-SAJ** — preenchimento automático de formulários dos sistemas judiciais

---

## DECISÕES TOMADAS

| Data | Decisão | Motivo |
|------|---------|--------|
| 28/06/2026 | Fase 0 via Claude.ai Projects (sem código) | Início imediato, zero infraestrutura, valida o fluxo antes de investir em desenvolvimento |
| 28/06/2026 | Stack web: PHP + MySQL + Claude API | Consistência com XKOO; hospedagem já disponível em afrontar.com.br |
| 28/06/2026 | Modelo Claude Opus (mais capaz) para produção de peças | Trabalho jurídico exige máxima qualidade; Sonnet para buscas e tarefas auxiliares |
| 28/06/2026 | Anti-alucinação como regra número 1 | Peça com jurisprudência inventada pode causar dano ao cliente e processo disciplinar OAB |

---

## PRÓXIMA SESSÃO

**Prioridade imediata:** Configurar os 5 projetos no Claude.ai (Fase 0).

**Passos:**
1. Abrir claude.ai → Projects
2. Começar pelo Cível (mais usado)
3. Testar com um caso concreto real
4. Registrar resultado em `_memoria/project_status.md`
