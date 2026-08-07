---
name: orchestrate-tickets
description: >
  Orquestrador: lê os tickets do repo (tickets/*.md ou Linear), cria um run com
  tasks e dependências no Orca e despacha workers em worktrees isolados,
  monitorando até o fim. Use quando o usuário disser /orchestrate-tickets,
  "orquestrar o projeto" ou "rodar os tickets". NUNCA implementa tickets nem faz merge.
---

# Orquestrador — tickets → workers → relatório

Você é o **coordenador**, não o implementador. Trabalho mecânico: grafo → tasks → dispatch → monitorar → relatar. Você nunca escreve código de ticket e **nunca faz merge**.

## Passo 0 — Doc viva

Rode `orca skills get orchestration --full` e siga a sintaxe atual. **Se algo aqui divergir da doc viva, a doc viva vence.** Confirme também `orca status --json` (CLI ativo) e quais CLIs de agente estão autenticados (`claude`, `codex`, `grok`).

## Passo 1 — Ler e validar tickets

- Modo markdown: leia `tickets/*.md` com `status: ready`.
- Modo Linear: leia as issues do projeto via skill `orca-linear`.
- Valide: sem ciclos de `blockedBy`; todo ticket com Acceptance Criteria; tickets grandes demais → devolva ao `/plan-tickets`. Pare e avise se falhar.
- Monte a tabela de waves (tasks sem blockers = wave 1) e mostre ao usuário. Argumentos aceitos: `--wip N` (default **3**), `--agent X` (força um agente para tudo).

## Passo 2 — Criar o run

```bash
orca orchestration run-create ... --json          # sintaxe exata: doc viva
# para cada ticket: task-create com título, corpo e dependências (blockedBy)
```

## Passo 3 — Despachar (respeitando WIP ≤ 3)

Para cada task `ready`, até o limite de WIP:

```bash
orca orchestration worker-start --task <taskId> --worktree new-child \
  --name <t-###-slug> --agent <do ticket, senão claude> --setup run --json
```

Prompt do worker = **conteúdo integral do ticket** + este workflow padrão:

> 1. Leia os arquivos relevantes antes de editar. Siga o `CLAUDE.md`/`AGENTS.md` do repo.
> 2. Implemente SOMENTE o escopo do ticket. Dúvida de arquitetura → pergunte ao coordenador, não decida.
> 3. Escreva/atualize testes junto com a implementação.
> 4. Rode testes afetados + lint/pre-commit. Corrija TODAS as falhas.
> 5. Commit convencional → push → `gh pr create` contra a branch principal. **NÃO faça merge.**
> 6. (Linear) mova a issue para In Review e comente a URL do PR.
> 7. Envie exatamente 1 `worker_done`:
>    `orca orchestration send --type worker_done --subject "<resumo>" --task-id <id> --dispatch-id <id> --outcome succeeded|failed --json`
>    Inclua a URL do PR no corpo. Depois pare.

Agente do ticket não autenticado → use `claude` e anote no relatório.

## Passo 4 — Monitorar

```bash
orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json
```

- `succeeded` → `worker-release` (e `worker-read` se precisar do output); despache dependentes que ficaram `ready`.
- `failed` → **1 retry** com o erro no prompt. Falhou de novo → gate para o humano. Nunca 3ª tentativa sozinho.
- `question` → responda se for operacional; se for decisão de produto/arquitetura → gate.
- Não deixe terminais de workers concluídos abertos.

## Passo 5 — Gates humanos (obrigatórios)

```bash
orca orchestration gate-create --task <taskId> --question "..." --options '["..."]' --json
```

Sempre que: ticket com `gate: true`, merge, schema/dados, deploy, deletar algo, gastar dinheiro, 2ª falha de um worker. Você **espera** a resposta; não decide.

## Passo 6 — Encerrar

Relatório final em tabela: `ticket | agente | outcome | PR | pendência humana`. Liste explicitamente: PRs aguardando merge (gate 3 do usuário), follow-ups, tickets devolvidos. Lembre: merge é do humano; após merges, rodar `/orchestrate-tickets` de novo libera a próxima leva.

## Fallback (Orca antigo, sem `orca orchestration`)

Waves manuais com os comandos validados: `orca worktree create --name <slug> --agent <a> --prompt "<ticket+workflow>" --json`, monitorar com `orca worktree list --json` / `orca terminal wait --terminal <handle> --for tui-idle`, avançar wave após merges com `git fetch origin` no worktree pai. (As flags `--base-branch`/`--linear-issue` NÃO existem — não use.)
