# Registro de instalação — Clabs (Criminal Lab)

**Data:** 06/07/2026
**Origem:** `pacote-original.zip` (recebido por Angelo, colocado na raiz do projeto)
**Fornecedor:** Criminal Lab — pacote "139 Skills de Prática Criminal"

## O que foi feito

1. **32 agentes** de `agents/` renomeados com prefixo `clabs-` (o pacote original não prefixa) e o campo `name:` do frontmatter ajustado para casar com o novo nome de arquivo. Instalados em `~/.claude/agents/`.
   - Motivo do prefixo: seguir o mesmo padrão já usado para o fornecedor "Bravy" (`bravy-*`), evitando ambiguidade entre agentes de nomes idênticos e funções sobrepostas (ex.: `habeas-corpus` do pacote novo vs. `bravy-habeas-corpus` já instalado).
   - 8 agentes são exclusivos deste pacote, sem equivalente Bravy/AE: `dosimetria-pena`, `analise-denuncia`, `cadeia-custodia-prova-digital`, `negociacao-penal`, `mapa-nulidades`, `analise-contradicoes`, `secretaria-juridica`, `verificador-citacoes`.
2. **107 skills** de `skills/` instaladas **sem renomear** em `~/.claude/skills/` (não havia colisão com nenhuma skill existente, e não há convenção de prefixo de fornecedor para skills neste ambiente).
3. Catálogos atualizados:
   - `~/.claude/agents/CATALOGO.md` — nova seção "Clabs — 32 Agentes Especialistas"
   - `~/.claude/skills/CATALOGO.md` — criado do zero, lista as 107 skills
4. Este diretório (`_pacotes/clabs-139-skills-criminal/`) guarda o pacote original, o guia de instalação em PDF, a licença de uso e a pasta `zips-claude-web/` (para instalar as mesmas skills em claude.ai / Claude Desktop, se um dia for necessário — ver `LEIA-ME.md`, opção B).

## Licença (resumo — ver LICENCA.md)

Uso pessoal/profissional por 1 usuário licenciado (Angelo). Permite adaptar para uso próprio (foi o que fizemos ao prefixar os agentes). **Proíbe redistribuição/revenda** — não compartilhar os arquivos originais ou renomeados com terceiros.

## Se precisar reinstalar ou atualizar

O script `instalar.mjs` do pacote original não sabe do prefixo `clabs-` — ele instalaria os agentes sem prefixo novamente. Para atualizar no futuro (nova versão do pacote), repita manualmente o processo de renomear + ajustar `name:` antes de copiar para `~/.claude/agents/`, ou peça para o Claude fazer isso de novo.
