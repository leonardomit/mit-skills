Aqui está o passo a passo completo e detalhado dos dois fluxos do Packer, escrito especialmente para quem nunca usou o Orca.

Vou unir a Parte 1 (planejamento + execução manual) com a Parte 2 (automação com waves) em um único fluxo prático que você pode seguir hoje.

  

Pré-requisitos (faça só uma vez)

1. Instale o Orca ([onorca.dev](https://www.onorca.dev/) ou via Homebrew/AppImage/exe).
2. Instale os CLIs:

- Claude Code
- Codex (GPT)
- Grok CLI (xAI)

4. No Orca: Settings → Agents → configure Claude, Codex e Grok (deixe em modo Yolo).
5. Settings → Experimental → CLI → ative o CLI.
6. Settings → Integrations → Linear → cole seu token de API.
7. Instale as skills (no terminal de um agente Claude ou Codex):  
    npx skills add https://github.com/stablyai/orca --skill orca-cli
8. npx skills add https://github.com/stablyai/orca --skill orca-linear
9. npx skills add https://github.com/stablyai/orca --skill orchestration
10.   
    

  

Fluxo Completo (do zero até produção)

Fase 0 – Você tem uma ideia nova

1. Abra o Orca.
2. Crie um worktree chamado planejamento-ideia-xyz (parte de origin/main).
3. Lance dois agentes em paralelo nesse mesmo worktree (ou em worktrees separados):

- PM Agent → use Claude (ou Grok)
- Design Agent → use Claude ou Grok

Fase 1 – Planejamento (PM + Design)

Prompt para o PM Agent:

Você é o Product Manager sênior.

Ideia: [cole a ideia aqui]

  

Faça comigo:

1. Avalie impacto × esforço

2. Defina o MVP mínimo

3. Defina escopo (o que entra e o que fica explicitamente fora)

4. Quebre em tickets que possam rodar em paralelo

5. Defina dependências explícitas (blockedBy)

  

No final, gere os tickets no formato completo pronto para o Linear.

Prompt para o Design Agent:

Você é o Design Specialist.

Mesma ideia do PM.

Foque em:

- Fluxos de UI mobile e desktop

- Componentes principais

- Estados (loading, erro, vazio, sucesso)

- Como a feature deve ser apresentada

  

Entregue recomendações claras para os tickets.

Depois que os dois terminarem, você (ou o próprio PM via skill) cria o projeto no Linear e cola todos os tickets.

Formato obrigatório de cada ticket (copie isso):

- Título imperativo e específico
- Context / problema
- Scope (dentro e fora)
- Technical Details
- Files afetados
- Acceptance Criteria (checkboxes)
- Cenários de teste
- Dependências (blockedBy)
- Rollout / kill-switch / métricas (quando necessário)

Fase 2 – Orquestração (as Waves)

Agora você tem duas opções:

Opção A – Manual (melhor para aprender)

1. No Linear, olhe quais tickets não têm blockers → esses são a Wave 1.
2. Para cada ticket da Wave 1:  
    orca worktree create \
3.   --name eng-123-titulo-curto \
4.   --base-branch origin/main \
5.   --linear-issue  \
6.   --agent codex \          # ou claude ou grok
7.   --prompt "$(cat prompt-do-ticket.md)" \
8.   --json
9.   
    
10. Deixe os agentes trabalharem em paralelo.
11. Quando terminarem, revise o PR, faça merge.
12. Rode git fetch origin main.
13. Agora os tickets que dependiam da Wave 1 ficam liberados → crie a Wave 2.
14. Repita.

Opção B – Automatizada (recomendado depois de 1-2 vezes)

1. Cole a skill completa orchestrate-project (a que o Packer postou) no seu agente principal.
2. Rode:  
    /orchestrate-project  --agent sol
3.   
    (você pode mudar para --agent sonnet ou adaptar para Grok)

O orquestrador:

- Lê todos os tickets
- Monta o grafo de dependências
- Cria as waves
- Dispara worktrees em paralelo
- Monitora CI e reviews
- Só libera a próxima wave depois do seu merge

Fase 3 – Dentro de cada worktree (o que o agente faz)

O prompt do ticket já contém o workflow. O agente deve:

1. Mover o ticket para “In Progress” no Linear
2. Ler os arquivos relevantes
3. Implementar somente o escopo do ticket
4. Escrever/atualizar testes
5. Rodar pre-commit + testes afetados
6. Commit + push
7. Abrir PR contra main
8. Vincular o PR no Linear e mover para “In Review”
9. Parar (você revisa)

Fase 4 – QA e Review

1. Depois que o PR está aberto, você pode lançar um QA Agent no mesmo worktree:Abra o Chrome com DevTools, teste o fluxo completo, encontre bugs e corrija.
2.   
    
3. CI roda automaticamente.
4. Reviews (CodeRabbit, etc.) são triados.
5. Você faz o review humano final e dá merge.

Fase 5 – Deploy e Observação

1. Merge → CD joga para produção.
2. Teste manual em produção.
3. Observe AppSignal (métricas, logs, traces).
4. Acompanhe PostHog (adoção e erros).
5. Se algo der errado → cria novo ticket e volta para a Fase 1.
6. Se deu certo → novas ideias surgem e o ciclo recomeça.

  

Como misturar Grok + Claude + GPT na prática

|   |   |   |
|---|---|---|
|Fase|Modelo ideal|Por quê|
|PM + Design|Claude ou Grok|Contexto longo e raciocínio|
|Orquestrador|Claude ou Grok|Monta o grafo e monitora|
|Implementação|Codex (GPT-Sol)|Rápido e bom em código|
|Testes / QA|Claude ou Grok|Boa em encontrar edge cases|
|Tickets exploratórios|Grok|Pensamento diferente|

Você pode abrir 5–8 worktrees ao mesmo tempo sem problema.

  

Resumo visual do ciclo diário

Ideia nova

  → PM + Design (Claude/Grok)

  → Tickets bem escritos no Linear

  → Orquestrador cria Waves no Orca

  → Agentes implementam em paralelo (Codex/Claude/Grok)

  → QA + CI + Review humano

  → Merge → Prod

  → AppSignal + PostHog

  → Novas ideias

  

Quer que eu te mande agora, em mensagens separadas:

1. O texto completo da skill orchestrate-project já adaptada para Grok/Claude/Codex?
2. Os prompts prontos de PM e Design?
3. Um exemplo real de 3 tickets com dependências?
4. Ou um checklist diário para você imprimir?

Aqui vai tudo que prometi, pronto para copiar e usar.

  

1. Prompts prontos de PM e Design

Prompt do PM Agent (cole no Claude ou Grok):

Você é o Product Manager sênior de um produto SaaS.

  

Ideia atual:

[COLE A IDEIA AQUI]

  

Faça o seguinte comigo, de forma clara e estruturada:

  

1. Avalie Impacto × Esforço (escala 1-5)

2. Defina o MVP mínimo absoluto

3. Defina o escopo:

   - O que ENTRA

   - O que fica EXPLICITAMENTE fora

4. Quebre a feature em tickets que possam rodar o máximo possível em paralelo

5. Defina as dependências explícitas (blockedBy) entre os tickets

  

No final, gere TODOS os tickets no formato completo abaixo (um por um):

  

## Título

[imperativo e específico]

  

## Context

[problema e por que precisa ser resolvido]

  

## Scope

[o que está dentro e o que está fora]

  

## Technical Details

- ...

  

## Files

- caminho/do/arquivo.ex

- ...

  

## Acceptance Criteria

- [ ] ...

- [ ] ...

  

## Test Scenarios

- ...

  

## Dependencies

blockedBy: ENG-XXX, ENG-YYY

  

## Rollout / Observability

[se houver risco]

Prompt do Design Agent:

Você é o Design Specialist.

  

Mesma ideia do PM:

[COLE A IDEIA AQUI]

  

Foque exclusivamente em:

- Fluxos principais de UI (mobile e desktop)

- Componentes e estados (loading, empty, error, success)

- Como a feature deve ser apresentada visualmente

- Pontos de atenção de UX

  

Entregue recomendações claras e objetivas que possam ser usadas nos tickets técnicos.

Não escreva código.

  

2. Exemplo real de 3 tickets com dependências

(Exemplo baseado no estilo do Packer – Elixir/LiveView)

Ticket 1 – Wave 1

## Título

Criar ManualTransactionCreationService centralizado

  

## Context

Hoje usuários conseguem criar a mesma transação por LiveView, GraphQL e ferramentas de IA, mas cada entrada executa uma parte diferente do fluxo.

  

## Scope

Centralizar validação, idempotência e regras de domínio em um serviço compartilhado.

Fora de escopo: analytics e formatação de erros nas entradas.

  

## Technical Details

- Criar ManualTransactionCreationService

- Criar Request DTO tipado

- Normalizar chaves string e atom

- Preservar compatibilidade com consumidores atuais

  

## Files

- lib/visor/finance/manual_transaction_creation_service.ex

- lib/visor/finance/manual_transaction_creation_service/request.ex

- test/visor/finance/manual_transaction_creation_service_test.exs

  

## Acceptance Criteria

- [ ] LiveView, GraphQL e MCP usam o mesmo serviço

- [ ] Chaves string e atom são normalizadas

- [ ] Opções conflitantes retornam erro de domínio

- [ ] Testes cobrem cada branch do serviço

- [ ] pre-commit e testes afetados passam

  

## Dependencies

Nenhuma

Ticket 2 – Wave 1 (pode rodar em paralelo com o 1)

## Título

Adicionar factories e fixtures para ManualTransaction

  

## Context

Precisamos de factories consistentes para os novos testes do serviço de criação de transações.

  

## Scope

Criar factories ExMachina para ManualTransaction e Request.

Fora de escopo: qualquer lógica de negócio.

  

## Files

- test/support/factories/manual_transaction_factory.ex

- ...

  

## Acceptance Criteria

- [ ] Factory gera dados válidos

- [ ] Factory gera dados inválidos para testes de erro

- [ ] Testes de factory passam

Ticket 3 – Wave 2 (depende dos dois anteriores)

## Título

Integrar ManualTransactionCreationService no LiveView de criação

  

## Context

O LiveView ainda usa lógica antiga. Precisa passar a usar o novo serviço centralizado.

  

## Scope

Substituir a lógica atual pelo serviço. Manter a UI igual.

Fora de escopo: mudanças visuais.

  

## Dependencies

blockedBy: ENG-123 (serviço), ENG-124 (factories)

  

## Acceptance Criteria

- [ ] LiveView usa o novo serviço

- [ ] Testes de integração passam

- [ ] Comportamento do usuário permanece idêntico

  

3. Skill completa `orchestrate-project` (adaptada para Grok + Claude + Codex)

Cole isso como uma skill no seu agente principal (Claude ou Grok):

---

name: orchestrate-project

description: |

  Orchestrate an entire Linear project into merge-gated waves of Orca child

  worktrees, each driven by an autonomous implementation agent.

  Accept optional worker selector: --agent sol | --agent sonnet | --agent grok | --agent claude

  Use when: "orchestrate this Linear project", "run the whole project", or when a Linear project URL is pasted.

---

  

# Orchestrate a Linear Project

  

You are the **orchestrator**, not the implementer. 

Your job is mechanical: read Linear, compute the wave order, spawn Orca child worktrees with an autonomous agent per ticket, monitor PRs, and advance waves as merges land. 

You never write ticket code yourself. You never merge.

  

Arguments: `$ARGUMENTS` must contain a Linear project URL or name and may include one worker selector: `--agent sol`, `--agent sonnet`, `--agent grok` or `--agent claude`.

  

## Baked-in defaults

- Merge-gated waves (ticket só começa depois que TODOS os blockers estão mergeados em main)

- Every PR targets main

- Human review is the final quality gate (você nunca faz merge)

- Children of the current worktree

  

## Implementation agent selection

- Default: Claude

- `--agent sol` ou "use Sol" → Codex com gpt-5.6-sol

- `--agent sonnet` → Claude Sonnet

- `--agent grok` → Grok

- `--agent claude` → Claude (default)

  

## Phase 0 - Read the project

1. Resolve the project with Linear tools

2. List every issue

3. For each issue get full relations (blocks / blockedBy)

  

## Phase 1 - Build the wave order

- Tickets with no open blockers = Wave 1

- Wave number = max(wave of blockers) + 1

- Print a clear wave table

  

## Phase 2 - Clarify only genuine ambiguities

Ask only project-specific questions (scope, in-flight tickets, etc.)

  

## Phase 3 - Spawn a wave

For each ticket in the current wave (in parallel):

1. Write a self-contained prompt file with the FULL ticket + standing workflow

2. Create worktree with the chosen agent

3. Record the task

  

Standing workflow to embed in every prompt:

> 1. Move ticket to "In Progress"

> 2. Implement only the scope

> 3. Run tests and pre-commit, fix everything

> 4. Commit + push + open PR against main

> 5. Move ticket to "In Review" and comment the PR URL

> 6. Do NOT merge. Stop.

  

## Phase 4 - Babysit CI and reviews

Monitor PRs, CI and review feedback.

Only intervene on real failures.

Never merge.

  

## Phase 5 - Advance waves

When a PR is merged by the human:

- Fetch origin/main

- Launch the next wave of unblocked tickets

  

4. Checklist diário (pode imprimir)

[ ] Ideia nova capturada

[ ] PM + Design rodaram e geraram tickets

[ ] Tickets criados no Linear com formato completo + dependências

[ ] Orquestrador rodou (manual ou skill)

[ ] Wave 1 criada e agentes trabalhando

[ ] PRs revisados e mergeados

[ ] Próximas waves liberadas

[ ] Teste manual em staging/prod

[ ] AppSignal e PostHog verificados

[ ] Novas ideias anotadas

  

Pronto. Agora você tem tudo para rodar o fluxo completo.

Quer que eu monte também a versão da skill já com os comandos exatos de orca worktree create para Grok/Claude/Codex, ou prefere começar testando com 1-2 tickets primeiro?

Aqui está a versão completa e pronta para usar da skill orchestrate-project, já com os comandos exatos de orca worktree create para Grok, Claude e Codex (Sol).

É só copiar e colar como uma skill no seu agente principal (Claude ou Grok).

---

name: orchestrate-project

description: |

  Orchestrate an entire Linear project into merge-gated waves of Orca child

  worktrees. Supports --agent sol | --agent sonnet | --agent grok | --agent claude

  Use when the user pastes a Linear project URL or says "orchestrate this project".

---

  

# Orchestrate a Linear Project

  

You are the **orchestrator**, never the implementer.

Your job is purely mechanical:

- Read the Linear project

- Build the dependency graph (waves)

- Spawn Orca child worktrees

- Dispatch the correct agent

- Monitor PRs, CI and reviews

- Advance waves only after human merge

  

You never write application code. You never merge.

  

### Arguments

`$ARGUMENTS` must contain a Linear project URL (or name) and optionally one of:

- `--agent sol`      → Codex (GPT-Sol)

- `--agent sonnet`   → Claude Sonnet

- `--agent grok`     → Grok

- `--agent claude`   → Claude (default)

  

---

  

## Phase 0 – Read the project

  

1. Resolve the Linear project

2. List all issues

3. For every issue fetch full relations (`blocks` / `blockedBy`)

4. Treat already Done/merged tickets as satisfied blockers

  

## Phase 1 – Build the wave order

  

- Tickets with no open blockers = Wave 1

- Wave number of a ticket = max(wave of its blockers) + 1

- Print a clear table:

  

| Wave | Tickets | Unblocks after |

|------|---------|----------------|

  

## Phase 2 – Clarify only real ambiguities

  

Ask the human only about:

- Whether to include low-priority independent tickets

- How to handle tickets already In Progress

- Missing critical decisions in a ticket description

  

Do **not** ask about branching strategy or who implements.

  

## Phase 3 – Spawn a wave

  

Resolve context once:

  

```bash

REPO_ID=$(orca worktree current --json | jq -r .repoId)

PARENT=$(orca worktree current --json | jq -r .path)

git fetch origin main

For each ticket in the current wave (run in parallel):

1. Write the self-contained prompt file

Create a temporary file (e.g. /tmp/ticket-ENG-123.md) containing:

- The full ticket content (Context, Scope, Technical Details, Files, Acceptance Criteria, etc.)
- Plus this standing workflow:

1. Move the ticket to "In Progress" in Linear.

2. Read the relevant files before editing.

3. Implement ONLY the scope of this ticket.

4. Treat implementation and tests as separate workstreams.

5. Run the affected tests + pre-commit. Fix ALL failures.

6. Commit with conventional message.

7. Push and open a PR against main (`gh pr create`).

8. Link the PR to the Linear ticket and move it to "In Review".

9. Comment the PR URL on the ticket.

10. Do NOT merge. Stop when the PR is open and checks are green (or fixes are pushed).

11. Create the worktree + agent

If agent is Claude (default):

orca worktree create \

  --repo id:$REPO_ID \

  --name  \

  --base-branch origin/main \

  --parent-worktree path:$PARENT \

  --linear-issue  \

  --agent claude \

  --prompt "$(cat /tmp/ticket-ENG-123.md)" \

  --json

If agent is Sol / Codex:

create_json=$(orca worktree create \

  --repo id:$REPO_ID \

  --name  \

  --base-branch origin/main \

  --parent-worktree path:$PARENT \

  --linear-issue  \

  --json)

  

worktree_id=$(echo $create_json | jq -r .id)

  

terminal_json=$(orca terminal create \

  --worktree id:$worktree_id \

  --title "-sol" \

  --command 'codex --model gpt-5.6-sol -c model_reasoning_effort="medium"' \

  --json)

  

terminal_handle=$(echo $terminal_json | jq -r .handle)

  

orca terminal wait --terminal $terminal_handle --for tui-idle --timeout-ms 60000 --json

orca terminal send --terminal $terminal_handle --text "$(cat /tmp/ticket-ENG-123.md)" --enter --json

If agent is Grok:

create_json=$(orca worktree create \

  --repo id:$REPO_ID \

  --name  \

  --base-branch origin/main \

  --parent-worktree path:$PARENT \

  --linear-issue  \

  --json)

  

worktree_id=$(echo $create_json | jq -r .id)

  

terminal_json=$(orca terminal create \

  --worktree id:$worktree_id \

  --title "-grok" \

  --command 'grok' \

  --json)

  

terminal_handle=$(echo $terminal_json | jq -r .handle)

  

orca terminal wait --terminal $terminal_handle --for tui-idle --timeout-ms 60000 --json

orca terminal send --terminal $terminal_handle --text "$(cat /tmp/ticket-ENG-123.md)" --enter --json

If agent is Claude Sonnet:

# same pattern as Sol, but command:

--command 'claude --model sonnet'

Record the worktree id and terminal handle.

Phase 4 – Monitor

Keep a persistent monitor watching:

- PR opened
- CI status (keyed by branch + SHA)
- Review comments (from humans, CodeRabbit, etc.)
- PR merged

Rules:

- On real CI failure → go into the worktree and fix (or re-dispatch the agent)
- On review comments → triage carefully before asking the agent to change code
- Never merge

Phase 5 – Advance

When a PR is merged by the human:

1. git fetch origin main
2. Find every ticket whose blockers are now all merged
3. Launch the next wave from fresh origin/main

Repeat until the project is done.

  

Done when: every ticket has a merged PR, no open actionable feedback remains, and you have surfaced any human-only follow-ups (feature flags, backfills, etc.).

---

  

Agora você tem a skill completa e funcional.

  

**Como usar:**

1. Cole a skill acima no seu agente principal.

2. Rode:

/orchestrate-project https://linear.app/seu-time/project/nome-do-projeto –agent sol

(ou `--agent grok`, `--agent claude`, etc.)

  

Quer que eu mande também a versão ainda mais curta (só o essencial) ou prefere um exemplo de como o orquestrador deve responder na prática quando você cola a URL do Linear?