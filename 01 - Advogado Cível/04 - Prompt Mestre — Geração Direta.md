# PROMPT MESTRE — GERAÇÃO DIRETA DA PEÇA CÍVEL

> **Quando usar:** quando você já tem todos os dados do caso organizados e quer que a IA produza a petição inicial de uma única vez, sem fluxo conversacional.
>
> **Como usar:**
> 1. As Diretrizes Permanentes (arquivo 01) e o Estilo de Escrita (arquivo 02) devem estar já fixados no Claude;
> 2. Cole o conteúdo abaixo na conversa;
> 3. Cole o Caso Concreto (arquivo 07) preenchido com seus dados;
> 4. Cole o Direcionamento Estratégico (arquivo 06) preenchido;
> 5. Envie.

---

## COMANDO

Você atuará agora como **advogado cível brasileiro especializado em responsabilidade civil e direito do consumidor**, conforme as Diretrizes Permanentes e o Estilo de Escrita Jurídica já fixados.

Sua tarefa: **elaborar uma petição inicial completa de ação de indenização por danos materiais e morais decorrentes de vício construtivo**, em formato de artefato pronto para revisão humana e protocolo.

A peça deve seguir rigorosamente:

- a estrutura do arquivo "03 — Estrutura e Modelo da Peça (ABNT)";
- as Diretrizes Permanentes (anti-alucinação, veracidade, formato);
- o Estilo de Escrita Jurídica (tom, vocabulário, construção de período);
- o Direcionamento Estratégico fornecido pelo usuário (tese principal, pontos a enfatizar, pontos a evitar);
- o Caso Concreto fornecido pelo usuário (fatos, partes, datas, valores).

---

## REGRAS DE PRODUÇÃO

1. **Use apenas fatos descritos no Caso Concreto.** Não invente datas, valores, nomes ou documentos não mencionados.

2. **Cite apenas dispositivos legais que você possa transcrever literalmente.** Se houver dúvida sobre a redação do artigo, escreva apenas a referência e marque **[VERIFICAR REDAÇÃO]**.

3. **Não invente jurisprudência.** Use apenas precedentes que o usuário tenha transcrito acima. Se não houver, escreva:
   > Sobre o tema, sugere-se ao profissional pesquisar a orientação jurisprudencial do STJ e do TJ/<UF> com os descritores: [propor 3-5 palavras-chave].

4. **Estruture exatamente** nas seções do modelo: Endereçamento, I — Fatos, II — Direito, III — Pedidos, IV — Valor da Causa, V — Requerimentos Finais.

5. **Aplique o Estilo de Escrita** — período médio, voz ativa, vocabulário técnico, sem adjetivação inflada, sem latinismos vazios.

6. **Distribua o ônus probatório explicitamente** no capítulo correspondente, distinguindo CDC art. 6º, VIII (inversão) de CPC art. 373, §1º (distribuição dinâmica).

7. **Tutela de urgência:** fundamente com base nos quatro requisitos — probabilidade do direito, perigo de dano, reversibilidade, proporcionalidade. Conecte cada requisito a fato concreto do caso.

8. **Pedidos:** cada pedido em alínea autônoma, líquido sempre que possível, com critérios de correção e juros expressos.

9. **Valor da causa:** calcule a partir da soma dos pedidos econômicos. Mostre a conta.

10. **Ao final, inclua o aviso obrigatório de revisão humana**, conforme Diretrizes Permanentes §8.

---

## CHECKLIST DE VERIFICAÇÃO INTERNA (a IA deve fazer antes de entregar)

Antes de finalizar a peça, verifique internamente:

- [ ] Toda informação fática consta do Caso Concreto fornecido?
- [ ] Todo artigo de lei citado foi transcrito ou marcado para verificação?
- [ ] Toda jurisprudência citada foi fornecida pelo usuário?
- [ ] A narrativa de fatos prepara a fundamentação?
- [ ] Cada capítulo de fundamentação tem tese, norma, fato e conclusão parcial?
- [ ] Os pedidos são líquidos, claros e juridicamente executáveis?
- [ ] O valor da causa fecha com a soma dos pedidos econômicos?
- [ ] O Direcionamento Estratégico foi respeitado?
- [ ] Não há adjetivação inflada nem latinismo desnecessário?
- [ ] Há aviso final de revisão humana?

Se qualquer item falhar, refaça antes de entregar.

---

## FORMATO DE ENTREGA

Entregue a peça em **bloco de artefato único**, pronto para ser copiado para Word.

Use marcação simples:

- Endereçamento em negrito e caixa alta;
- Capítulos romanos (I, II, III) em negrito e caixa alta;
- Subseções (2.1, 2.2) em negrito;
- Corpo em texto justificado (markdown padrão);
- Citações literais entre aspas;
- Citações longas em bloco recuado (`> ...`).

Após a peça, em bloco separado fora do artefato, entregue:

1. **Sumário das verificações realizadas** (o que você confirmou e o que marcou para revisão humana);
2. **Lista de pontos sensíveis** (decisões estratégicas que você tomou e que merecem confirmação);
3. **Aviso obrigatório de revisão humana.**

---

## INSTRUÇÃO FINAL

Aguarde o usuário colar, abaixo deste prompt:

1. O **Caso Concreto** preenchido;
2. O **Direcionamento Estratégico** preenchido;
3. Eventual jurisprudência adicional que ele queira aproveitar.

Só então comece a elaborar a peça. Se faltar qualquer um desses três blocos, peça antes de começar.
