---
name: hermes-cron-ops
description: "Use when diagnosing or repairing Hermes cron jobs."
category: devops
tags: [cron, hermes, drift_skip, wiki-llm]
version: 1.0.0
---

# Hermes cron — diagnóstico e reparo

Classe: jobs Hermes que falharam no ticker (`last_status: error`, alerta no Telegram, journal/intel que não gravou).

## Diagnóstico

1. `cronjob action=list` — `job_id`, `last_status`, skills, toolsets.
2. `~/.hermes/cron/executions.db` tabela `executions` — campo `error`.
3. Output: `~/.hermes/cron/output/<job_id>/` (mais recente).
4. Prompt real: `~/.hermes/cron/jobs.json`.

## drift_skip (modelo/provider global mudou)

Sintoma: `RuntimeError: [drift_skip] ... model 'X' -> 'Y' ... job is unpinned`. Nenhum inference. O job **continua pulando** até pin.

O tool `cronjob` **não** seta `--model` / `--provider`. No host:

```bash
hermes cron edit <job_id> --model <model.default> --provider <model.provider>
```

Valores atuais em `config.yaml`: `model.default` + `model.provider`. Depois `cronjob action=run` se a janela já passou.

Jobs com snapshot vistos: intel `cffeb772f91e`; relatórios B2C+B2B `3a0da579e544`.

## Idle timeout 600s

Sintoma: `TimeoutError: Cron job '...' idle for Ns (limit 600s)` — last activity `receiving stream response`, `executing tool: terminal`, ou `search_files`.

Causa 1 — skill anexada demais: `chief-of-staff-workflows` injeta os 9 fluxos (~20k tokens). O prompt do job já é auto-contido. Radar `7ac04296fad6` e Resumo `4fd78ade6710` não devem carregar essa skill (Wiki LLM tampouco). Journals 14–17/08/2026 se perderam assim.

Causa 2 — job LLM fazendo trabalho de script. Meta Ads Daily KPIs `6a6eee03c621` estoura 600s no `terminal` (Graph + Sheets). Caminho que funciona: `python3 ~/meta_ads_to_sheets.py` (conta `act_237609954257064`, aba `Meta Ads B2C`). Depois do append, preencher colunas M–O (Valor Vendido / Ticket / ROAS) — o script deixa vazias. Não relançar o cron LLM para "consertar" KPI; rodar o script.

Causa 3 — relançar 2–3 jobs LLM em paralelo no mesmo gateway. Competem pelo stream e caem no mesmo timeout. Relançar **um** por vez (ou só o que não tem script).

Pin de jobs ativos (evitar drift_skip): `hermes cron edit <id> --model grok-4.6 --provider xai-oauth`. Relatórios B2C+B2B `3a0da579e544` é segunda 9:15 — pin, não disparar no meio da semana.

## Wiki LLM / Cérebro Secundário

Job `7be746ab9ee2` — `0 23 * * *`.

| Campo | Valor |
|-------|--------|
| skills | **somente** `daily-journal-obsidian-gbrain` |
| enabled_toolsets | `terminal`, `file` |
| Prompt | data de HOJE; `extract_journal_day.py` + `write_obsidian_journal.py`; nunca MCP `put_page` |

Ops: skill `daily-journal-obsidian-gbrain`. Não anexar `chief-of-staff-workflows` neste job. Não disparar o journal 23h no meio do dia.

## Intel mercado suplementos

Job `cffeb772f91e` — `0 7 * * 1`. Vault: `empresa/Inteligência de Mercado/YYYY-MM-DD.md`. Toolsets: `web`, `terminal`, `file`. Se drift_skip: pin + run.

## Verificação

`jobs.json` deve ter `model` e `provider` preenchidos (não null). Após run: `executions.status=completed` e arquivo no vault.
