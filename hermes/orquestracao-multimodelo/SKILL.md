---
name: "orquestracao-multimodelo"
description: "Use when rotear ou delegar tarefa entre modelos."
---

# Orquestração Multimodelo

Worktree no Orca, escolha de modelo e disparo de worker: prefira `orquestracao-worktree`. Esta skill continua válida para roteamento fora do Orca.

Objetivo: usar o modelo mais barato capaz de entregar com segurança aceitável. Separar sempre `Planejar → Executar → Validar → Revisar → Aprovar`. Quem executa uma mudança relevante não a aprova.

Esta skill cobre roteamento e governança. Processo de engenharia (branch, PR, testes, idempotência) fica em `dev-workflow`; aplique-a apenas quando `needs_code = true`.

## Mapeamento de classes (ambiente atual)

| Classe | Modelo real | Como acionar |
|---|---|---|
| `ECONOMY` | Haiku; Qwen3-30B local (Ollama/MLX via Hermes) | `Agent(model: "haiku")` ou Hermes |
| `STANDARD` | Sonnet | `Agent(model: "sonnet")` |
| `PREMIUM` | Opus | `Agent(model: "opus")` ou sessão principal |
| `CODE_AGENT` | Codex; ou `Agent` com Sonnet/Opus em sessão nova | subagente com contexto limpo |
| `RESEARCH` | Perplexity (citações obrigatórias); SuperGrok (sentimento X/BTC); WebSearch | flag `citations_required` decide entre eles |
| `HUMAN_GATE` | Leonardo | `AskUserQuestion` ou pausa explícita |

Mantenha o modelo da tabela. Se ele não existir nesta máquina, use o fallback da mesma classe. Só então suba uma classe. Nunca desça.

| Classe | Fallback nesta máquina |
|---|---|
| `ECONOMY` | `claude-haiku-4-5-20251001`. Local: `qwen3.5:9b`; extração curta `qwen3.5:2b`. Qwen3-30B não está instalado. Arquivo longo: Laya, não um chat. |
| `STANDARD` | `claude-sonnet-5`. Código do dia: `gpt-6-sol`. Tarefa direta: `gpt-5.6-terra` ou `gpt-6-luna`. |
| `PREMIUM` | `claude-opus-5-5` (alias `opus-5-5`). Se recusar, `claude-opus-5`. Plano mais longo: `claude-fable-5-1`. Fronteira de implementação: `gpt-6-astra` `--effort high`. |
| `CODE_AGENT` | `gpt-6-sol`. Complexo: `claude-opus-5-5`. Diff pequeno: `gpt-6-luna`. |
| `RESEARCH` | `grok-4.7`. Cota do Grok acabou: Gemini, só se autenticado; senão Claude; senão Codex. |

Gemini está instalado e sem login. Não use até a credencial existir. Não suba `qwen3.6:27b` em 16 GB. Não use overflow antigo do Claude (`claude-opus-4-*`, `claude-sonnet-4-6`, `claude-fable-5`).

No Hermes não existe `Agent(model:)` nem `AskUserQuestion`. Classes continuam as da tabela. Acionamento: ECONOMY local só se Ollama/Qwen estiver no ar; execução isolada com `delegate_task`; pesquisa com busca web e citação; gate humano com `clarify` ou parada explícita. Se o modelo da classe não existir nesta máquina, use o fallback da mesma classe. Só então suba uma classe. Nunca desça.


## Classificação (0–3 cada)

- `impact`: efeito financeiro, regulatório (ANVISA/LGPD), reputacional, sobre clientes ou sistemas produtivos.
- `complexity`: etapas, dependências, profundidade de raciocínio.
- `ambiguity`: regra ausente, fontes em conflito, julgamento necessário.
- `volume`: quantidade de itens repetidos.
- Flags: `external_change`, `needs_code`, `needs_research`, `citations_required`, `sensitive_data_export`.

```json
{"task_id":"","impact":0,"complexity":0,"ambiguity":0,"volume":0,
 "external_change":false,"needs_code":false,"needs_research":false,
 "citations_required":false,"sensitive_data_export":false,
 "pipeline":[],"approval_required":false,"reason":""}
```

O router (ECONOMY ou regra determinística) produz este JSON. Não há campo de confiança: a decisão de executar vem de validação objetiva, não de autodeclaração do modelo.

## Roteamento

O resultado é um **pipeline** (lista ordenada de papéis), não uma classe única. Aplique nesta ordem; regras posteriores acrescentam etapas, não substituem.

```python
def route(t):
    p = []
    t.approval_required = t.external_change or t.sensitive_data_export or t.impact >= 3

    # 1. Pesquisa vem antes de planejar
    if t.needs_research:
        p.append("RESEARCH(citations)" if t.citations_required or t.impact >= 2 else "RESEARCH")

    # 2. Planejamento e nível de execução — complexidade/impacto antes de volume
    if t.impact >= 3 or t.complexity == 3 or t.ambiguity == 3:
        p.append("PLAN:PREMIUM")
        exec_class = "PREMIUM"
    elif t.complexity >= 2 or t.ambiguity >= 2 or t.impact == 2:
        p.append("PLAN:STANDARD")
        exec_class = "STANDARD"
    else:
        exec_class = "ECONOMY"

    # 3. Execução
    if t.needs_code:
        p += ["EXEC:CODE_AGENT", "VALIDATE:auto", "REVIEW:CODE_AGENT(new session)"]
    else:
        p += [f"EXEC:{exec_class}", "VALIDATE:auto"]
        if exec_class == "ECONOMY" and t.volume >= 2:
            p.append("REVIEW:STANDARD(sample)")
        elif exec_class != "ECONOMY":
            p.append("REVIEW:independent")

    # 4. Gates
    if t.impact >= 2:
        p.append("GATE:PREMIUM")
    if t.approval_required:
        p.append("GATE:HUMAN")
    p.append("LOG")
    return p
```

Regras adicionais:
- ECONOMY só conclui sozinho se `impact <= 1`, `external_change = false` e a validação automática passou.
- Volume alto nunca rebaixa a classe. Rebaixa apenas o executor de itens repetidos, com amostragem revisada por STANDARD.
- Impacto 3 exige PREMIUM em análise/revisão **e** CODE_AGENT na execução técnica. Não é ou/ou.

## Escalonamento

- Falha 1: corrigir no mesmo nível, usando a evidência da falha.
- Falha 2: subir uma classe ou trocar de papel. Nunca uma terceira tentativa igual.
- Regra de negócio ausente: parar, registrar a dúvida, não inventar.
- Dependência externa desconhecida: enviar a RESEARCH com data e fonte.
- Arquitetura, segurança ou impacto ≥ 3: PREMIUM + HUMAN_GATE.

## Validação e revisão

Validação objetiva antes de qualquer revisão: schema, testes, lint/build, reconciliação com dado de controle, checagem de segredos, checagem ANVISA quando houver comunicação de produto.

Revisor independente = **sessão nova, sem acesso ao raciocínio do executor**. Recebe só requisito + entrega. Prompt mínimo:

```md
Revisor adversarial. Compare requisito e entrega. Não reimplemente, não elogie.
Reporte só problemas concretos: erro funcional, perda/duplicação de dados,
segurança, quebra de critério de aceite, teste ausente, risco regulatório.
Por achado: severidade (bloqueador/alto/médio/baixo), local, cenário, correção mínima.
Sem achados: escreva "Nenhum problema concreto encontrado" e liste o que não pôde validar.
```

Gate PREMIUM responde com uma de três saídas: `APROVAR PARA HUMANO`, `DEVOLVER AO EXECUTOR`, `BLOQUEAR POR RISCO`, seguida de evidências.

## Gate humano (lista fechada)

Sempre exige aprovação explícita de Leonardo:
- Deploy, merge em produção, migração de banco produtivo.
- Envio de comunicação externa (e-mail, WhatsApp, publicação, anúncio).
- Movimentação financeira, cobrança, compra, alteração de preço/estoque/pedido/contrato.
- **Exportação, exclusão ou compartilhamento externo** de dados pessoais. Leitura interna de e-mail, CRM e leads não exige gate.
- Permissões, autenticação, segredos, tokens.
- Exclusão de arquivos, contas, registros, infraestrutura.
- Decisão legal, fiscal, regulatória (ANVISA, CRN) ou contratual.

## Contexto e custo

1. ECONOMY localiza e resume antes de qualquer chamada a PREMIUM.
2. Pacote de contexto: requisito + arquivos/trechos relevantes + logs + decisões. Nada além.
3. Saída limitada ao formato da tarefa: JSON, checklist, diff, achados. Sem ensaio.
4. Orçamento indicativo de saída: classificação 100–400 tokens; resumo 200–600; spec 800–2.500; código 1.500–6.000; arquitetura/auditoria 2.000–8.000 com escopo fechado.

## Contrato entre etapas

Toda etapa devolve:

```json
{"task_id":"","role":"","model_used":"","attempt":1,
 "status":"completed|blocked|needs_review|failed",
 "output":"","evidence":[],"assumptions":[],"open_questions":[],
 "tokens_in":0,"tokens_out":0,"next_role":""}
```

O registro final (`LOG`) agrega `model_used`, `attempt`, tokens, resultado da validação e motivo de escalonamento. Sem esses campos não há métrica.

## Níveis de autonomia

| Nível | Permissão |
|---|---|
| 0 Consultivo | pesquisar, explicar, recomendar |
| 1 Rascunho | criar plano, documento, código local |
| 2 Proposta | abrir PR/proposta após validação |
| 3 Homologação | rodar em sandbox, simulação ou modo leitura |
| 4 Produção | só com aprovação humana explícita |

O router declara o nível máximo da tarefa. Nenhuma etapa pode subir de nível sozinha.

## Checklist antes de executar

- Objetivo observável e escopo fechado?
- Classificação feita e pipeline gerado?
- Modelo é o mais barato adequado ao impacto?
- Critério de aceite e validação objetiva definidos?
- Revisor é sessão diferente do executor?
- Ação externa bloqueada até gate humano?

## Exemplos

**Extrair campos de 2.000 documentos** — impact 1, complexity 1, ambiguity 1, volume 3 → `EXEC:ECONOMY → VALIDATE:schema → REVIEW:STANDARD(sample) → LOG`. Exceções vão para fila humana.

**Integração com API externa** — impact 2, complexity 2, needs_code, needs_research → `RESEARCH(citations) → PLAN:STANDARD → EXEC:CODE_AGENT (modo leitura) → VALIDATE → REVIEW:CODE_AGENT(nova sessão) → GATE:PREMIUM → GATE:HUMAN (ativar escrita) → LOG`.

**Incidente em automação produtiva** — impact 3 → `EXEC:ECONOMY (resumir logs) → EXEC:CODE_AGENT (reproduzir) → PLAN:PREMIUM (hipótese, mitigação, rollback) → GATE:HUMAN → STANDARD registra post-mortem → LOG`.