# DECISÕES DO PROJETO — ASSISTENTE JURISTA

## 28/06/2026

### Começar pela Fase 0 (Claude.ai Projects, sem código)
**Motivo:** Permite validar o fluxo completo (diretrizes → prompt → peça → revisão) com zero infraestrutura e zero custo adicional. Só avança para desenvolvimento web quando o modelo estiver comprovado em uso real.

### Stack web futura: PHP + MySQL + Claude API
**Motivo:** Consistência com o stack do XKOO já dominado. Hospedagem já disponível em afrontar.com.br. Não adicionar nova linguagem sem necessidade.

### Modelo Opus (mais capaz) para geração de peças
**Motivo:** Trabalho jurídico exige máxima qualidade e raciocínio complexo. O risco de um erro em uma peça processual (dado inventado, artigo errado) é alto demais para economizar no modelo. Sonnet pode ser usado para tarefas auxiliares (busca, classificação, resumo).

### Anti-alucinação como regra número 1 das Diretrizes
**Motivo:** Peça com jurisprudência inventada pode causar nulidade processual, dano ao cliente e processo disciplinar perante a OAB. Esta regra é inegociável e deve estar no topo de todo system prompt.

### Estrutura com 5 especialidades separadas
**Motivo:** Cada área do Direito tem vocabulário, bases legais, estratégias e tipos de peça muito diferentes. Um único assistente genérico produziria resultado medíocre. A especialização garante qualidade técnica.

### Project Instructions = Diretrizes + Estilo de Escrita
**Motivo:** São os arquivos permanentes — o "DNA" da IA. Devem estar fixos no contexto de cada sessão. Os Prompts de uso (Mestre e Guiado) são operacionais e mudam por caso, portanto ficam fora do projeto e são colados na conversa.

### Gerador DOCX usa templates existentes como base (não cria do zero)
**Motivo:** Os modelos em `Modelos jus/` já têm fontes (Manuale, Alegreya Sans), estilos, margens e numeração configurados corretamente. Recriar do zero perderia essa tipografia. A abordagem correta é abrir o template, limpar o conteúdo e popular com os estilos já definidos.

### Peças geradas em DOCX (não PDF) como formato de trabalho
**Motivo:** O advogado precisa editar a peça (preencher placeholders, ajustar estratégia, fazer revisão colaborativa). DOCX permite isso. PDF é para o arquivo final após assinatura — pode ser gerado com `gerar_pdf.py`.

### Nunca incluir aviso de IA nas peças processuais
**Motivo:** Documento protocolado em juízo é documento profissional. Aviso de IA no corpo da peça é inadequado e pode prejudicar a credibilidade do profissional. Regra propagada para todas as Diretrizes e ignorada pelo gerador.

### Documentos do caso vão na conversa, não no Project Knowledge
**Motivo:** Project Knowledge é compartilhado por todas as conversas do projeto. Colocar documentos de casos lá mistura dados de clientes distintos. A separação correta: Project Knowledge = arquivos permanentes (03, 06, 07, 08); conversa = documentos do caso específico (PDF, Word, laudo, contrato, qualificação das partes). Claude lê esses formatos diretamente na conversa. Cada peça = uma conversa nova com os documentos do caso em anexo.
