# Provas recebidas — catálogo por caso

Pasta pra organizar provas que o cliente manda direto (print, PDF, foto, documento escaneado) — fora do fluxo do Veredata (análise forense de celular/disco, que fica em `../Análises Forenses/`).

## Conversa de WhatsApp exportada (não é extração forense)

Quando o cliente (dono do celular) usa o recurso nativo "Exportar conversa" do próprio WhatsApp (`.txt` ou `.zip` com mídia), não precisa de perícia nem de Veredata — o conteúdo já chega legível. Usar `_tools/visualizar_whatsapp.py`:

```
python3 _tools/visualizar_whatsapp.py --arquivo conversa.zip --caso "<caso>" --descricao "<descrição>" [--meu-nome "Nome do cliente, como aparece nas mensagens dele"]
```

Isso cataloga o arquivo original (hash, como qualquer prova — ver acima) e gera `visualizador_conversa.html` na pasta do caso: mensagens em balão (como no WhatsApp de verdade), busca por palavra-chave, estrela pra marcar as relevantes, e um botão "Exportar seleção" que baixa um `.json` com o que foi marcado — pra citar na peça com data/hora/remetente exatos.

**Mensagens de voz buscáveis (opcional)**: adicionar `--transcrever-audio` transcreve cada áudio com `faster-whisper` (local, modelo "small", precisa de `pip3 install faster-whisper` à parte — testado: ~9x mais rápido que o tempo real do áudio, boa qualidade em português coloquial). O texto transcrito entra na busca e aparece sob o player de áudio, sempre marcado como "(transcrição automática)" — é gerado por IA, nunca tratar como o texto literal/garantido do que foi dito.

**Escolher quais áudios transcrever** (em vez de todos): marque com ★ no visualizador os áudios que interessam, clique "Exportar seleção (.json)", e rode de novo com `--arquivo-selecao mensagens_selecionadas.json` — transcreve só esses. `--limite-audios N` (sem seleção) transcreve só as N mensagens mais recentes, útil pra testar qualidade antes de rodar tudo. Transcrições ficam num cache (`transcricoes.json` na pasta do caso) — rodar o script de novo nunca retranscreve o que já foi feito.

**Corrigir erro de transcrição sem mexer no áudio**: clique no ✏️ ao lado de qualquer transcrição no visualizador, edite o texto, salve. No fim, clique "Exportar correções de transcrição (.json)" e rode de novo com `--importar-correcoes correcoes_transcricao.json`. A transcrição automática original fica preservada no cache (nunca sobrescrita) — só a exibição passa a mostrar a corrigida, sempre rotulada "(revisado manualmente)". O arquivo de áudio em si nunca é alterado, continua disponível pra qualquer um reconferir ouvindo.

**Ver a conversa dentro do Veredata** (em vez do HTML avulso): adicionar `--exportar-veredata` (ou `--exportar-veredata /caminho/pro/VisualizadorIPED`, padrão `~/Documents/VisualizadorIPED`) escreve a conversa direto nos dados do Veredata — aparece lá com login, busca, ★ e relatório, no mesmo padrão de uma conversa de celular processada pelo IPED. Reexecutar substitui os itens dessa fonte (nunca duplica).

## Convenção

Cada caso tem sua própria subpasta, dentro da pasta do dia em que a primeira prova chegou:

```
Provas recebidas/
└── DD-MM-2026/
    └── <nome ou nº do caso>/
        ├── catalogo.md
        ├── doc01_print_whatsapp_14-03.jpg
        ├── doc02_comprovante_pagamento.pdf
        └── ...
```

## Regras

1. **Todo arquivo recebido entra no catálogo antes de ser citado em qualquer peça** — nunca citar "o print que o cliente mandou" sem ter salvo o arquivo e dado um ID.
2. **Catalogar com o script, não na mão**: `python3 _tools/catalogar_prova.py --arquivo <caminho> --caso "<caso>" --descricao "<descrição>" [--data-exibida "DD/MM/AAAA HH:MM"]` — copia o arquivo, calcula o hash SHA-256 e já grava a linha no `catalogo.md`, com ID sequencial automático (Doc. 1, Doc. 2, ...), nunca reaproveitado nem pulado.
3. **Distinguir sempre a data que aparece na prova (não verificada) da data real do evento** — usar exatamente a redação `conforme exibido na captura, não verificado tecnicamente` quando citar a peça. Isso é diferente de prova vinda do Veredata (análise forense), que carrega metadado verificado tecnicamente — nunca tratar as duas como equivalentes em força probatória.
4. **O hash SHA-256** prova que o arquivo não foi alterado desde que entrou no catálogo — não prova a autenticidade do conteúdo em si. Se o caso exigir peso probatório maior, reforçar com ata notarial (cartório certifica o que viu na tela, fé pública — mas não é perícia técnica do aparelho) ou carimbo do tempo de autoridade certificadora ICP-Brasil (mais rigoroso tecnicamente, prova existência e integridade num momento específico).
5. As tabelas geradas pela skill `tipografia-juridica` (coluna "Documento/Prova") citam o ID daqui — consistência entre todas as peças do mesmo caso.
6. Pra inserir a imagem de verdade dentro da peça (não só citar), usar o marcador `@IMAGEM caminho/do/arquivo [largura_cm]` do `_tools/gerar_docx.py`.

## Modelo do `catalogo.md`

Ver `_modelo_catalogo.md` nesta pasta — gerado automaticamente pelo `_tools/catalogar_prova.py` na primeira prova de cada caso; só copiar manualmente se precisar catalogar sem o script.
