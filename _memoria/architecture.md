# ARQUITETURA TÉCNICA — SISTEMA WEB (Fase 1+)

## Stack

- **Backend:** PHP 8+ 
- **Banco:** MySQL (mesmo servidor que XKOO em afrontar.com.br ou VPS dedicado)
- **IA:** Claude API (Anthropic) — modelo `claude-opus-4-8` para peças, `claude-sonnet-4-6` para buscas
- **Frontend:** HTML/CSS/JS (sem framework pesado — padrão XKOO)
- **Exportação Word:** PHPWord ou python-docx via script auxiliar

## Chamada à API Claude

```php
function callClaude(string $system, array $messages, string $model = 'claude-opus-4-8'): string {
    $payload = json_encode([
        'model'      => $model,
        'max_tokens' => 8192,
        'system'     => $system,
        'messages'   => $messages,
    ]);
    $ch = curl_init('https://api.anthropic.com/v1/messages');
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => $payload,
        CURLOPT_HTTPHEADER     => [
            'Content-Type: application/json',
            'x-api-key: ' . ANTHROPIC_API_KEY,
            'anthropic-version: 2023-06-01',
        ],
    ]);
    $resp = curl_exec($ch);
    curl_close($ch);
    $data = json_decode($resp, true);
    return $data['content'][0]['text'] ?? '';
}
```

## Estrutura do prompt por especialidade

```
SYSTEM PROMPT (fixo no projeto):
├── Diretrizes Permanentes (arquivo 01)
└── Estilo de Escrita Jurídica (arquivo 02)

USER PROMPT (montado por caso):
├── Prompt Mestre OU Fluxo Guiado (arquivo 04 ou 05)
├── Caso Concreto preenchido (arquivo 07)
├── Direcionamento Estratégico preenchido (arquivo 06)
└── Jurisprudência fornecida pelo usuário (opcional)

CONHECIMENTO INJETADO (context injection):
├── Estrutura e Modelo da Peça (arquivo 03)
└── Precedentes buscados (Fase 3+)
```

## Banco de dados (Fase 2+)

```sql
CREATE TABLE especialidades (
    id INT PRIMARY KEY AUTO_INCREMENT,
    slug VARCHAR(50) UNIQUE,   -- 'civel', 'trabalhista', etc.
    nome VARCHAR(100),
    diretrizes TEXT,           -- conteúdo arquivo 01
    estilo TEXT,               -- conteúdo arquivo 02
    estrutura TEXT,            -- conteúdo arquivo 03
    prompt_mestre TEXT,        -- conteúdo arquivo 04
    prompt_guiado TEXT         -- conteúdo arquivo 05
);

CREATE TABLE casos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT,
    especialidade_id INT,
    cliente VARCHAR(200),
    tipo_acao VARCHAR(200),
    status ENUM('ativo','concluido','arquivado') DEFAULT 'ativo',
    dados_caso JSON,           -- campos do Caso Concreto preenchidos
    direcionamento JSON,       -- campos do Direcionamento Estratégico
    criado_em DATETIME DEFAULT NOW()
);

CREATE TABLE pecas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    caso_id INT,
    tipo VARCHAR(100),         -- 'inicial','contestacao','recurso'...
    conteudo_md TEXT,          -- minuta gerada pela IA
    conteudo_docx BLOB,        -- arquivo Word gerado
    revisada TINYINT DEFAULT 0,
    criado_em DATETIME DEFAULT NOW()
);

CREATE TABLE conversas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    caso_id INT,
    role ENUM('user','assistant'),
    conteudo TEXT,
    etapa INT,                 -- etapa do Fluxo Guiado (1-10)
    criado_em DATETIME DEFAULT NOW()
);
```

## Fluxo de dados — Geração Direta

```
Usuário preenche formulário (caso + direcionamento)
    ↓
api.php monta system prompt (diretrizes + estilo)
    ↓
api.php monta user prompt (prompt_mestre + caso + direcionamento)
    ↓
Chama Claude API (claude-opus-4-8, max_tokens: 8192)
    ↓
Recebe minuta em Markdown
    ↓
Salva no banco (pecas) + exibe no painel de entrega
    ↓
Usuário copia / baixa .docx / revisa / protocola
```

## Fluxo de dados — Fluxo Guiado (10 etapas)

```
Etapa 1: usuário responde perguntas iniciais → IA valida
    ↓
Etapas 2-8: coleta e validação progressiva (cada etapa = 1 turno de conversa)
    ↓
Etapa 9: IA gera minuta completa (sem entrar antes desta etapa)
    ↓
Etapa 10: revisão técnica final + lista de pontos sensíveis
    ↓
Salvar conversa completa + minuta final no banco
```
