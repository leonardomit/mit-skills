# Fluxo Orca — Método de Trabalho com Fleet de Agentes

> Genérico: funciona em **qualquer projeto ou repositório**.
> Baseado no método "Packer" (tickets formais + waves + revisão humana), adaptado e **validado contra a doc oficial do Orca em 06/08/2026**.
> Mudança principal vs o material original: usa o subsistema **nativo** `orca orchestration` (tasks + dependências + gates) em vez de scripts manuais de waves — e as flags `--base-branch`/`--linear-issue` do material **não existem** na doc oficial.

---

## A ideia em 3 linhas

1. **Especificação formal antes de código** — toda tarefa vira um ticket com escopo, critérios de aceite e dependências.
2. **Orquestração nativa** — um agente coordenador cria tasks no Orca, despacha workers em worktrees isolados e monitora; dependências liberam a próxima leva sozinhas.
3. **Você é o único gate** — nenhum agente faz merge. Você revisa diffs e decide.

## Mapa do kit

| Arquivo | O que é |
|---|---|
| `SETUP.md` | Instalação única (Orca + agentes + CLI + skills). Fazer 1 vez. |
| `PLAYBOOK.md` | O método: papéis, ciclo diário, guardrails, matriz de agentes. |
| `skills/plan-tickets/` | Skill do **Planejador** (PM+Design): ideia → tickets prontos. |
| `skills/orchestrate-tickets/` | Skill do **Orquestrador**: tickets → workers paralelos → relatório. |
| `templates/ticket.md` | Formato padrão de ticket (copiar para cada repo). |
| `templates/bootstrap-repo.md` | Checklist para plugar o fluxo num repo novo. |

## Quickstart (depois do SETUP.md)

```text
1. No repo: seguir templates/bootstrap-repo.md (5 min)
2. No Claude Code (dentro do Orca): /plan-tickets "sua ideia"
3. VOCÊ revisa/ajusta os tickets gerados            ← gate 1
4. /orchestrate-tickets
5. Responder gates de decisão quando surgirem       ← gate 2
6. Revisar diffs no Orca (diff viewer) e dar merge  ← gate 3
7. Dependências liberam a próxima leva sozinhas
```

## Fleet configurado

| Agente | Papel padrão | Custo |
|---|---|---|
| **Claude Code** | Planejador, Orquestrador, Implementador, QA | Já coberto pelo Claude Max |
| **Codex** | Implementador alternativo | ⚠️ Requer assinatura ChatGPT ou API OpenAI — **pendente contratar** |
| **Grok** | Exploratório / 2ª perspectiva | Conferir em x.ai/cli se o CLI vem com SuperGrok; senão API xAI |

Enquanto Codex/Grok não estiverem autenticados, o orquestrador cai automaticamente para Claude — o fluxo funciona 100% só com Claude.

## Fontes (validação 06/08/2026)

- Doc oficial: [onorca.dev/docs](https://www.onorca.dev/docs) · [CLI reference](https://www.onorca.dev/docs/cli/reference) · [Orchestration](https://www.onorca.dev/docs/cli/orchestration) · [Skills registry](https://www.onorca.dev/docs/cli/skills) · [Agentes suportados](https://www.onorca.dev/docs/agents/supported) · [Linear](https://www.onorca.dev/docs/review/linear)
- Código: [github.com/stablyai/orca](https://github.com/stablyai/orca) (MIT, gratuito)
