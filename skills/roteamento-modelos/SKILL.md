---
name: roteamento-modelos
description: "Fonte única de modelos: qual modelo usar em cada tipo de tarefa, cadeias de fallback quando a cota acaba ou o provedor cai, regras de API × assinatura, modelos locais (Mac mini + GTX 1070 via PAIR), Jev e Laya. Ler antes de escolher modelo, disparar worker ou subagente, ou trocar de modelo. As outras skills apontam para as cadeias daqui e não citam modelo."
---

# Roteamento de modelos — fonte única

> v1.4 · 10/11/2026. IDs conferidos no Claude CLI 2.1.319, no Orca e no Ollama `claude-fable-5-2` conferido no Claude CLI 2.1.322 (Air, 10/11/2026).
> **Trocar modelo = editar só este arquivo** (§3 e §4). Skills, agentes e lentes apontam para a **cadeia** (L, P, A…), nunca para o modelo.
> Mapa das skills da Fitobrasil → cadeias: `fito-skills/docs/modelos-por-skill.md`.

## 1. Modo de cobrança decide a régua

| Modo | Onde | Régua |
|---|---|---|
| **API** | Tarefa que roda **direto no Hermes** · qualquer chamada à **API Anthropic** | Menor modelo capaz. **Opus e Fable só quando realmente necessário.** Cadeias da §4 como estão |
| **Assinatura** | **Orca** ou **CLI** com Claude por login/auth | Sem custo por token: o primário Claude é o **melhor para a tarefa** (§4, coluna "Assinatura"). Cota acabou → segue a cadeia |

Valem nos dois modos: regras de dado (§2), revisor de outra família, rascunho ⏳ em fallback das cadeias A/X/PL, e **GPT-6 Astra só quando realmente necessário**. No **Orca**, qualquer GPT (Codex) só quando realmente necessário — lista fechada na regra 11.

**Grok Bot** é outra plataforma (bots na nuvem, navegador com login, cofre de senhas). O **Grok CFO** roda nela com o **modelo próprio** da plataforma: não chama outro modelo por CLI e não segue cadeia. "Grok" neste arquivo = modelos da xAI chamados pelo Orca, pela API ou pelo Cursor.

## 2. Regras

1. **Comece no primário da cadeia.** Antes de descer por qualidade, suba o `effort` do mesmo modelo.
2. **Dois motivos de troca, duas regras:**
   - **Cota esgotada ou provedor fora** → próximo item **de outra conta**. Nunca troque para modelo da mesma conta esgotada (Luna não salva Sol; Sonnet não salva Opus). As cadeias já alternam conta.
   - **Saída falhou no contrato** → falha 1: mesmo modelo corrige com a evidência; falha 2: próximo da cadeia ou uma classe acima. Nunca terceira tentativa igual.
3. **Contas:** Claude (Haiku, Sonnet, Opus, Fable — o Fable tem cota semanal própria) · Codex (Luna, Terra, Sol, Astra) · Grok (cota semanal própria) · local · Jev · Laya. Antes de uma leva no Orca: `orca account list --json`.
4. **Revisor = outra família, sessão nova, não reimplementa.** Codex escreveu → `claude-sonnet-5-5` (ou `claude-opus-5-5` se impact ≥ 2). Claude escreveu → Grok (`grok-4.7`) com dado público; `gpt-6-sol` com dado interno ou impact ≥ 2. Grok escreveu → `claude-sonnet-5-5` (`gpt-6-sol` se impact ≥ 2).
5. **Um planejador por tarefa**, e só com complexity ou ambiguity ≥ 2. **No Orca o planejador é o próprio orquestrador** (cadeia O): não suba worker Fable para planejar; Astra só se o desenho da implementação travar. Fora do Orca: Fable se o difícil é duração, ambiguidade ou norma; Astra se é o desenho da implementação. Planejador não escreve código que Opus, Sonnet ou Grok resolvem.
6. **Dado:**
   - Texto público ou sintético → Jev pode receber. **Dado interno nunca vai ao Jev**, nem como fallback.
   - Dado interno (ERP, CRM, e-mail, WhatsApp, PII) → Laya, local ou Claude/Codex. Grok só com dado público.
   - Material marcado **confidencial** (ex.: RAG confidencial) → só local.
7. **Local caiu = para e enfileira.** Não migra para nuvem por queda (regra do Hermes).
8. **Fallback em A, X ou PL** sai como rascunho ⏳: não publicar, não gravar em ERP, não enviar.
9. **Registrar** no resultado: `modelo usado (fallback de <primário> — motivo: cota|queda|contrato)`.
10. **Não usar:** `claude-opus-4-*`, `claude-sonnet-4-6`, `claude-fable-5`, `claude-fable-5-1` (só como reserva se o launch recusar o `claude-fable-5-2`), `gpt-5.4*`, `gpt-reserve`, `codex-auto-review`, `grok-4.6`, `grok-4.5`, `grok-4.7-build-fast` (sem pedido), tags `*:cloud` do Ollama, `qwen3.6:27b` (não cabe em 16 GB). `gpt-6-luna` → `gpt-5.6-luna` e `gpt-5.5` só se o ID atual recusar o launch. Effort `max`/`ultra` só se o Leonardo pedir. Gemini, Kimi, OpenCode e MiniMax: só com login confirmado em `orca account list`.
11. **GPT (Codex) no Orca — lista fechada:** revisão de código Claude com dado interno ou impact ≥ 2 · auditoria da cadeia X · desenho de implementação que travou (PI) · fallback por cota ou queda. Fora disso, worker no Orca é Claude ou Grok.

## 3. Catálogo (IDs desta máquina)

### Claude (conta Claude)

| ID | Melhor em | Observação |
|---|---|---|
| `claude-haiku-5-5` | Volume: localizar, extrair, classificar, resumir fonte única, lançar com trava de script | Sem `--effort`. Tokenizador conta ~30% mais tokens que o 4.5 |
| `claude-sonnet-5-5` | Padrão: rotina, docs, análise, copy, revisão de código Codex, terminal e infraestrutura | Já é o padrão do perfil principal do Hermes |
| `claude-opus-5-5` (alias `opus-5-5`) | Julgamento sustentado, código complexo, regulatório/financeiro de alto risco | Se o launch recusar: `claude-opus-5` |
| `claude-fable-5-2` | **Orquestrador no Orca** (sessão principal); plano longo, ambíguo ou regulatório | Cota semanal própria; gasta mais rápido que Opus. Reserva: `claude-fable-5-1` |

> Conferido no Claude CLI 2.1.319 (Air, 06/11/2026): Opus 5.5, Fable 5.1, Sonnet 5.5 e Haiku 5.5. Fable 5.2 conferido no CLI 2.1.322 (Air, 10/11/2026); falta conferir no Mini. **Reserva** se o launch recusar o ID atual (ex.: CLI mais antigo no Mini): `claude-sonnet-5`, `claude-haiku-4-5-20251001`, `claude-opus-5`.

### Codex (conta Codex — via Orca `--agent codex --model <id>`)

| ID | Melhor em | Effort |
|---|---|---|
| `gpt-6-luna` | Diff pequeno, rename, boilerplate, lint | low |
| `gpt-5.6-terra` | Tarefa direta e isolada | low |
| `gpt-6-sol` | Revisor de código Claude (dado interno ou impact ≥ 2); fallback de código | medium |
| `gpt-6-astra` | Auditoria crítica (X); desenho de implementação que travou; fallback de plano | high (default dele é low) |

Effort Codex: `low`, `medium`, `high`, `xhigh`. A home `~/.codex` pode estar em cache sem GPT-6: disparar Codex pelo Orca.

### Grok (conta Grok)

| Como | Modelo | Melhor em |
|---|---|---|
| Orca `--agent grok` (sem `--model`) | `grok-4.7` — a cota que vale para failover é a do `orca account list`, que pode ser outra conta que a do Hermes | Pesquisa web, contraponto, código que depende de web no mesmo passo |
| API xAI, se configurada | `grok-4.3` · `grok-4.20` multi-agent | Volume barato com contexto grande · pesquisa profunda em paralelo |

### Gemini — bloqueado

Binário instalado, **sem credencial**. Quando `orca account list --json` mostrar `gemini.status` ok: segundo pesquisador e leitura de PDF/imagem longos (`--agent gemini`).

### Local — Mac mini M4 16 GB + PC GTX 1070 8 GB (NVIDIA PAIR)

| Nó | Runtime | Modelos | Uso |
|---|---|---|---|
| **PC GTX 1070** (Windows, 24 h) | Ollama | `qwen3.5:9b` **e nada mais** | Agente local, resumo, RAG. `OLLAMA_MAX_LOADED_MODELS=1`, `NUM_PARALLEL=2`, `KEEP_ALIVE=24h`, contexto 8K. Pascal fora da lista oficial do PAIR — **em teste** |
| **Mac mini** | Ollama `:11434` | `qwen3.5:9b` (só fallback direto, **fora do PAIR**), `qwen3.5:2b` → trocar por `qwen3.5:4b`, `gemma4:e4b` (~9,6 GB, visão+áudio), `gemma4:e2b`, `hermes3`, `llama3.2:3b` | Fallback e triagem |
| **Mac mini** | LM Studio `:1234` | `google/gemma-4-e4b` (~5 GB) | Visão (foto de NF, laudo, etiqueta) |

- Entrada única para o 9B: proxy do PAIR. Fallback: Ollama do Mini direto.
- A aposentar quando o `qwen3.5:9b` estiver estável: `hermes3`, `llama3.2:3b`. `qwen3.5:2b` sai quando o `qwen3.5:4b` for instalado.
- Mini: um modelo grande por vez (~7 GB de teto, a memória é dividida com Hermes, App e CRM).

### Decisão tipada (sem LLM)

| Serviço | Recebe | Como | Regra |
|---|---|---|---|
| **Jev** (TypeSafe, externo) | Texto público ou sintético | `cd ~/Dev/typesafe && python3 -c "from jev import ask; ..."` | `confidence < 0,6` → cadeia DP |
| **Laya** (serviço local próprio) | Dado interno, arquivo | `mcp__laya__classify` com `paths` · CLI `~/.hermes/scripts/laya_decide.py` | `top < 0,7` → descartar o rótulo. Não escolhe ID de modelo. Detalhe: `laya-triagem`, `laya-classificador-modelos`, `jev-system-one` |

## 4. Cadeias

Ordem = primário → fallbacks. **Cada fallback é de outra conta**, para servir também quando a cota acaba.

¹ **Só com dado público.** Com dado interno, pule o Grok e siga para o próximo item da cadeia (na L, o local).

| Cadeia | Uso | API (Hermes / API Anthropic) | Assinatura (Orca / CLI): primário Claude |
|---|---|---|---|
| **O** Orquestrador | Sessão principal: classifica, delega, planeja, decide | Hermes: perfil padrão (`claude-sonnet-5-5`) | Orca: `claude-fable-5-2` → cota Fable acabou: `claude-opus-5-5` (high) |
| **L** Leve | Localizar, extrair, classificar, resumir, lançar | `claude-haiku-5-5` → `gpt-6-luna` → `grok-4.7`¹ → local (`qwen3.5:9b`) | Haiku continua (velocidade) |
| **P** Padrão | Análise, texto, plano curto, copy, revisão | `claude-sonnet-5-5` → `gpt-5.6-terra` → `grok-4.7`¹ | `claude-opus-5-5`; terminal/infra fica `claude-sonnet-5-5` |
| **A** Alto risco | Regulatório, financeiro, estratégia, condição comercial grande | `claude-opus-5-5` → `gpt-6-sol` (high) → **para** ⏳ | `claude-opus-5-5` (high) |
| **X** Crítico | A em esforço alto não bastou | `claude-fable-5-2` → `gpt-6-astra` (high) → **para** ⏳ | Orca: `gpt-6-astra` (high) → **para** ⏳ (o orquestrador já é Fable; auditoria tem de ser de outra família). CLI: `claude-fable-5-2` |
| **PL** Plano longo/regulatório | Plano, DAG, ambiguidade alta, norma | `claude-fable-5-2` (high) → `gpt-6-astra` (high) → orquestrador planeja curto | Orca: o orquestrador planeja, sem worker → `gpt-6-astra` (high) se a cota Fable acabar. CLI: igual à API |
| **PI** Plano de implementação | Arquitetura, desenho de código difícil | `gpt-6-astra` (high) → `claude-fable-5-2` (high) → orquestrador planeja curto | Orca: o orquestrador planeja → `gpt-6-astra` (high) só se o desenho travar. CLI: igual à API |
| **K1** Código pequeno | Diff pequeno, rename, lint | `gpt-6-luna` → `claude-sonnet-5-5` → `grok-4.7`¹ | `claude-sonnet-5-5` → `grok-4.7`¹ → `gpt-6-luna` |
| **KT** Tarefa direta | Isolada, bem especificada | `gpt-5.6-terra` → `claude-sonnet-5-5` → `grok-4.7`¹ | `claude-sonnet-5-5` → `grok-4.7`¹ → `gpt-5.6-terra` |
| **K2** Código do dia | Feature, script, integração comum | `gpt-6-sol` (medium) → `claude-opus-5-5` → `grok-4.7`¹ | `claude-opus-5-5` → `grok-4.7`¹ → `gpt-6-sol` (medium) |
| **K3** Código complexo | Bug difícil, integração complexa | `claude-opus-5-5` (high) → `gpt-6-sol` (high) → `grok-4.7`¹ | `claude-opus-5-5` (high) → `grok-4.7`¹ → `gpt-6-sol` (high) |
| **KW** Código com pesquisa | Depende de web no mesmo passo | `grok-4.7`¹ → `gpt-6-sol` → `claude-opus-5-5` | `grok-4.7`¹ → `claude-opus-5-5` → `gpt-6-sol` |
| **KI** Código interativo | Edição no editor | Cursor (modelo à escolha) | igual |
| **W** Pesquisa | Web com citação, docs de API, contraponto | `grok-4.7`¹ → Gemini (se autenticado) → `claude-sonnet-5-5` + busca → `gpt-6-sol` | igual |
| **N** Navegador com login | Nibo, Vivo, Certel, Gmail do laboratório, Regula | **Grok CFO no Grok Bot**, modelo próprio → caiu: **sem fallback automático**, fila + aviso ao responsável | igual |
| **DP** Decisão — texto público | Escolha fechada | Jev → conf < 0,6: `claude-haiku-5-5` (ou `claude-sonnet-5-5`) com o item | igual |
| **DI** Decisão — dado interno | **Triagem de e-mail e mensagens internas**, roteamento de pedido, rótulo de arquivo — qualquer escolha fechada sobre dado interno | Laya → rótulo fraco: `claude-haiku-5-5` (ou `claude-sonnet-5-5`) · Laya fora: para e enfileira | igual |
| **LT** Local texto | Agente, resumo, RAG com dado interno | `qwen3.5:9b` no PC (PAIR) → `qwen3.5:9b` no Mini (Ollama direto) → para e enfileira | igual |
| **LR** Local rápido | Extração curta de dado interno, **sem** escolha fechada (para escolha fechada, use DI) | `qwen3.5:4b` no Mini (hoje `qwen3.5:2b`) → `qwen3.5:9b` no PC → fila | igual |
| **LV** Local visão | Foto ou print interno, áudio curto | `google/gemma-4-e4b` (LM Studio) → `gemma4:e4b` (Ollama) → fila | igual |

## 5. Como manter

- Modelo novo ou trocado: §3 (catálogo) e §4 (cadeias). Nada mais.
- Modelo saiu de linha: incluir em "Não usar" (§2, item 10).
- Mudou a máquina (RAM, GPU, runtime): §3, "Local".
- Depois de mudar: recopiar esta skill para o Hermes (N2) e conferir com uma tarefa no Orca e um fluxo no Hermes.

## Fontes

IDs e regras de cota: skills `orquestrador-orca`, `orquestracao-hermes` e `laya-classificador-modelos` desta máquina (nov/2026). Capacidades: [AI Career Lab — Claude 5.5](https://theaicareerlab.com/blog/which-claude-model-should-you-use) · [GPT-6 Astra no Codex CLI](https://codex.danielvaughan.com/2026/09/03/gpt-6-astra-codex-cli-configuration-context-notes-safety/) · [AI Toolbox — Grok 2026](https://www.ai-toolbox.co/grok-models/grok-models-explained-2026) · [vdf.ai — local para agentes](https://vdf.ai/blog/best-local-llm-for-agents-tool-calling/) · [NVIDIA PAIR](https://build.nvidia.com/playbooks/pair).
