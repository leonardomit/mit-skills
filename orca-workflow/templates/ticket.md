---
id: T-001
title: Título imperativo e específico
status: draft          # draft | ready | in-progress | review | done
agent: claude          # claude | codex | grok
blockedBy: []          # ex.: [T-000]  — só dependência REAL
gate: false            # true = exige decisão humana antes de executar
---

## Context

Problema e por que precisa ser resolvido. 2–4 frases. Links/paths relevantes.

## Scope

**Dentro:**
- ...

**Fora (explícito):**
- ...

## Technical Details

- Abordagem esperada, contratos, restrições
- Decisões já tomadas (não rediscutir)

## Files

- `caminho/do/arquivo.py`
- ...

## Acceptance Criteria

- [ ] Critério objetivo e verificável
- [ ] Testes novos/afetados passando
- [ ] Lint/pre-commit passando

## Test Scenarios

- Caso feliz: ...
- Caso de erro: ...
- Edge case: ...

## Rollout / Risco

- Reversível? Como desfazer?
- Toca produção/dados/dinheiro? → `gate: true` + revisão redobrada
