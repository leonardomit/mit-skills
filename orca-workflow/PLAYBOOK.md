# PLAYBOOK — Como o fluxo funciona no dia a dia

## Papéis (fases, não pessoas)

| Papel | Quem executa | Faz | Nunca faz |
|---|---|---|---|
| **Planejador** (PM+Design) | Claude (`/plan-tickets`) | Ideia → MVP → escopo → tickets com dependências | Código |
| **Orquestrador** | Claude (`/orchestrate-tickets`) | Cria tasks, despacha workers, monitora, escala gates | Código de ticket, merge |
| **Worker** (implementação) | Claude / Codex / Grok (por ticket) | Implementa SÓ o escopo do ticket + testes + PR | Mudar arquitetura, mergear |
| **QA** | Claude (ticket próprio de QA) | Testa, encontra bugs, reporta | Corrigir (vira ticket novo) |
| **Você** | — | Aprova tickets, responde gates, revisa diffs, **merge** | Escrever código que agente faz melhor |

Regras entre papéis (herdadas do método original):

- Toda tarefa **começa no Planejador**. Worker não trabalha sem ticket com critério de aceite.
- Refactor só em código com testes. Sem testes → primeiro vem o ticket de testes.
- QA tem poder de veto: bug crítico devolve o ticket mesmo que "pareça funcionar".
- Todo ciclo fecha com um ticket de documentação (README/SOP) — é isso que torna o trabalho delegável depois.

## O ciclo

```text
ideia
  → /plan-tickets            (Planejador gera tickets/*.md + INDEX.md)
  → VOCÊ revisa os tickets                                  ← GATE 1
  → /orchestrate-tickets     (run + tasks + workers em worktrees)
  → gates de decisão no meio do caminho                     ← GATE 2
  → PRs abertos → diffs no Orca → VOCÊ faz merge            ← GATE 3
  → dependências liberam a próxima leva automaticamente
  → ticket de docs fecha o ciclo
```

O mecanismo por baixo: `orca orchestration` nativo — tasks com `blockedBy` ficam `blocked` até as dependências completarem; workers reportam `worker_done --outcome succeeded|failed`; decisões param num `gate` até você responder. As "waves" do material original acontecem sozinhas.

## Guardrails (não negociáveis no início)

1. **WIP ≤ 3 worktrees simultâneos.** Só suba depois de 2–3 ciclos redondos. O gargalo é a SUA revisão, não a produção de código.
2. **Ticket pequeno:** cabe em 1 sessão de agente. Maior que isso → o Planejador quebra.
3. **Repo sem testes → T-000 (bootstrap de testes) é sempre o primeiro ticket.** Sem exceção.
4. **Gate humano obrigatório** para: merge, mudança de schema/dados, deploy, deletar qualquer coisa, gasto de dinheiro, qualquer integração de produção (ERP/NF-e/financeiro).
5. **Orçamento de revisão:** não abra mais worktrees do que você consegue revisar no mesmo dia. PR parado 3+ dias apodrece (conflitos).
6. **Segurança:** Yolo só em repo isolado sem segredos (ver SETUP §3). Segredos nunca versionados.

## Matriz de agentes (fleet completo)

| Tipo de tarefa | Agente | Nota |
|---|---|---|
| Planejamento / orquestração | Claude | sempre |
| Implementação padrão | Claude | default do kit |
| Implementação em volume / boilerplate | Codex | quando autenticado |
| QA / edge cases | Claude | |
| Exploratório / 2ª opinião | Grok | quando autenticado |

O agente vai no frontmatter do ticket (`agent: claude|codex|grok`). Sem CLI autenticado → orquestrador usa Claude e avisa no relatório.

## Modo híbrido de tickets

- **Padrão (qualquer repo):** `tickets/*.md` + `INDEX.md`, versionados no próprio repo.
- **Repo com Linear configurado:** o Planejador cria as issues no Linear (skill `orca-linear`), o Orquestrador lê de lá, workers movem status (In Progress → In Review) e comentam o PR. Criar worktree a partir da issue injeta descrição/comentários/imagens no contexto.
- O formato do ticket é o mesmo nos dois modos (`templates/ticket.md`).

## Quando escalar

| Sinal | Ação |
|---|---|
| 2–3 ciclos redondos, revisão sobrando | Subir WIP para 4–5 |
| Muitos tickets de boilerplate | Ativar Codex (contratar ChatGPT) |
| Projeto com board/equipe | Ativar modo Linear |
| Ciclos travando na SUA revisão | **Não** abrir mais worktrees — melhorar testes/CI para revisar mais rápido |

## Diferenças vs o material original (por quê)

| Material (Perplexity) | Este kit | Motivo |
|---|---|---|
| Waves via script + `terminal send` manual | `orca orchestration` nativo | Existe na doc oficial, com estados, retries e gates prontos |
| `--base-branch`, `--linear-issue` | Removidos | Flags não existem na doc oficial (06/08/2026) |
| Linear obrigatório | Opcional (híbrido) | Zero dependência externa por padrão |
| Yolo em tudo | Yolo condicionado (SETUP §3) | Segurança de credenciais |
| 5–8 worktrees | WIP ≤ 3 inicial | Gargalo real é a revisão humana |
