---
name: orquestracao-worktree
description: "Use when orquestrar worktree no Orca."
version: 1.3.0
---

# Orquestração de worktree

Prefira esta skill para orquestrar worktree, escolher modelo e disparar worker. As outras continuam válidas: carregue `orca-cli`, `orchestration`, `laya-triagem` ou `orquestracao-multimodelo` quando o detalhe delas for necessário. Se um flag do `orca` for rejeitado, leia `orca orchestration worker-start --help`. Não invente flag e não troque de binário. O catálogo de modelo desta máquina é o daqui, não o de `orquestracao-multimodelo` nem o de `orquestracao-orca`.

Binário: `orca`. Confirme `orca status --json` antes de disparar. Prefira `--json`.

Isto é supervisão: criar Run, criar Task, `worker-start`, esperar `worker_done`. Handoff puro ("passa e sai", sem pedir para esperar resultado) não entra aqui: `orca worktree create --name <nome> --no-parent --agent <id> --prompt "<brief>" --json` e pare. Sem `task-create`, sem `check --wait`.

`delegate_task` não substitui este fluxo. Não chame de orquestrado o que não tiver `dispatch-show`.

## Papéis

Quem orquestra: Hermes, por padrão. Fable e Astra também podem orquestrar, quando a competência for deles. Hermes em geral só delega. Não execute a mudança que vai aprovar.

O Orca, no default, não deixa um worker disparar outro (`nested_worker_depth_exceeded`; profundidade em Settings → Orchestration). Enquanto estiver em 1, Fable ou Astra devolvem o plano e o nome de quem executa; o Hermes sobe esse worker. Se a profundidade for 2 ou mais, Fable ou Astra disparam a geração seguinte eles mesmos. Criar outro Run não zera a profundidade.

| Papel | Quem | Competência |
|---|---|---|
| Planejar o mais longo e o mais difícil | `claude-fable-5-1` `--effort high` | Plano, DAG, ambiguidade alta, regulação. Gasta cota mais rápido que Opus. |
| Planejar o mais exigente de implementação | `gpt-6-astra` `--effort high` | Fronteira de código e arquitetura. O default de effort é `low`; passe `high`. |
| Gerar código do dia | `gpt-6-sol` `--effort medium` | Workhorse. Padrão de código. |
| Gerar código complexo do dia | `claude-opus-5-5` `--effort high` | Opus 5.5. Complexo, não o mais longo. Alias `opus-5-5`. Se o launch recusar, `claude-opus-5`. |
| Gerar código com pesquisa no mesmo passo | `--agent grok` | Quando o código depende de web. Não é o gerador padrão. |
| Tarefa menor | `claude-sonnet-5`, `claude-haiku-4-5-20251001`, `gpt-5.6-terra`, `gpt-6-luna`, grok | Rotina, resposta curta, tarefa direta, diff pequeno, consulta. |
| Pesquisar | `--agent grok` | Web e contraponto. Padrão. |
| Pesquisar em segundo, ou ler documento longo / imagem / PDF | `--agent gemini` | Só depois de autenticado. Contraponto com fonte Google, ou leitura que a Laya marcou `precisa_ler`. Não planeja e não é o gerador de código. |

Escolha um planejador, não os dois. Fable se o duro é duração, ambiguidade ou norma. Astra se o duro é o desenho da implementação. Tarefa pequena não ganha planejador.

Código: Sol, salvo se for complexo do dia (Opus) ou precisar de web no mesmo passo (Grok). O planejador nomeia qual dos três, com esse critério. Não mande Fable nem Astra escrever o código se Sol, Opus ou Grok derem conta.

Tarefa menor, nesta ordem: Sonnet para rotina e docs; Haiku para resposta curta (sem `--effort`); Luna (`gpt-6-luna`) para diff pequeno; Terra (`gpt-5.6-terra`) para tarefa direta no Codex; Grok se for consulta. `gpt-5.6-luna` e `gpt-5.5` só se o slug atual recusar o launch.

## Catálogo

Codex via Orca (`--agent codex --model <slug>`). A home `~/.codex` pode estar num cache antigo sem GPT-6; não dispare Codex solto nessa home. Não disparar: `gpt-reserve`, `codex-auto-review`.

Effort Codex: `low`, `medium`, `high`, `xhigh`. `max` e `ultra` só se o usuário pedir.

Claude neste Mac: 2.1.281. Opus do dia é `claude-opus-5-5` (alias `opus-5-5`). `claude-opus-5` fica de reserva se o 5.5 recusar o launch. Não use os ids de overflow (`claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `claude-fable-5`, `claude-sonnet-4-6`). Effort Claude, exceto Haiku: `low`, `medium`, `high`, `xhigh`, `max`. `max` só se o usuário pedir.

Grok não aceita `--model` no `worker-start` (só Claude, Codex e Cursor). `--agent grok` sai em `grok-4.7`. Não use `grok-4.6`, `grok-4.5` nem `grok-4.7-build-fast` sem pedido. Esta sessão Hermes e o Grok do Orca podem ser contas diferentes; a cota que manda para failover é a do `orca account list`.

Gemini: binário existe, credencial não. Antes de disparar, `orca account list --json` tem de mostrar `gemini.status` ok. Sem isso, não escolha Gemini e diga que falta login. `--model` não vale para Gemini; use `--agent gemini`. Se o Orca rejeitar o agent, `terminal create --command gemini` e não invente slug de modelo.

Kimi, OpenCode e MiniMax estão sem credencial. Não os escolha.

## Roteamento

Classifique de 0 a 3: `impact` (produção, dinheiro, ANVISA, cliente), `complexity`, `ambiguity`.

1. Arquivo longo só para classificar: Laya. Não é worker.
2. Texto já na conversa, volume, sem editar repo: Ollama `qwen3.5:9b`. Extração curta: `qwen3.5:2b`. Não suba `qwen3.6:27b-q4_K_M` (17 GB em 16 GB) nem tags `*:cloud`.
3. `complexity` ou `ambiguity` ≥ 2: um planejador (Fable ou Astra). Ele devolve plano, arquivos, critério de aceite e qual gerador de código.
4. Código: Sol, Opus ou Grok, como na tabela. Tarefa menor: Sonnet, Haiku, Terra, Luna ou Grok.
5. Pesquisa: Grok. Gemini só como segundo pesquisador, ou para PDF/imagem, e só autenticado.
6. Revisor é outra família, sessão nova, e não reimplementa. Codex escreveu → Sonnet, ou Opus se impact ≥ 2. Claude escreveu → Sol. Grok escreveu → Sol ou Sonnet.
7. Impacto 3 ou mudança externa: worker faz o local; gate humano antes de deploy, merge, migração, exclusão, auth, envio externo ou decisão ANVISA.

## Cota da sessão

Antes de uma leva, `orca account list --json`. Sol, Luna, Terra e Astra dividem a sessão Codex. Sonnet, Haiku, Opus e Fable dividem a sessão Claude; Fable tem cota semanal própria. Grok tem a semanal dele.

Se a sessão de quem está no meio do trabalho acabar, não espere: mande outro modelo terminar a mesma spec, em cima do diff que já existe. Diga qual cota estourou.

| Acabou | Termina com |
|---|---|
| Fable ou sessão Claude no plano | Astra |
| Astra ou sessão Codex no plano | Fable |
| Os dois no plano | Hermes planeja aqui. Sem terceiro planejador. |
| Sol ou sessão Codex no código | Opus, depois Grok |
| Opus ou sessão Claude no código | Sol, depois Grok |
| Grok no código | Sol, depois Opus |
| Sonnet ou Haiku | Luna, depois Terra, depois Grok |
| Luna ou Terra | Sonnet, depois Haiku, depois Grok |
| Grok na pesquisa | Gemini, se autenticado; senão Claude; senão Codex |

Não troque para um modelo da mesma conta esgotada. Luna não salva Sol.

## Onde colocar o worker

`orca worktree ps --json` antes de escrever no checkout atual.

- Fica no checkout atual se a tarefa depende de arquivo não commitado ou tem de validar esta branch, e nenhum outro agente está editando os mesmos arquivos.
- Outro agente trabalhando no mesmo checkout: não abra um segundo escritor aí. Diga o conflito. Worktree novo só se o usuário pedir isolamento ou o conflito for real.
- Empilhado nesta branch: `--worktree new-child`. Independente: `--worktree new-top-level` e não passe `--base-branch` (Orca usa a base do repo). Não baseie na branch atual sem pedido.
- Worktree novo: `--setup run`. Checkout atual: não reroda setup.
- `--model` e `--effort` só em terminal novo. Com `--terminal` reutilizado, os dois são rejeitados.

## Disparo

Crie o Run e todas as tarefas independentes antes de subir workers.

```bash
orca orchestration run-create --objective "<objetivo>" --json
orca orchestration task-create --spec "<spec>" --json
orca orchestration worker-start --task <task_id> --worktree current --agent codex --model gpt-6-sol --effort medium --json
```

Claude no checkout atual:

```bash
orca orchestration worker-start --task <task_id> --worktree current --agent claude --model claude-fable-5-1 --effort high --json
```

Worktree novo independente:

```bash
orca orchestration worker-start --task <task_id> --worktree new-top-level --name <nome> --agent codex --model gpt-6-sol --effort medium --setup run --json
```

A spec do worker leva objetivo observável, arquivos, fora de escopo, critério de aceite e o comando de verificação. Sem push, merge ou deploy. Regra de negócio ausente: parar e perguntar, não inventar.

Espere com rolagem, não com sleep:

```bash
orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json
```

Timeout ou `count: 0` não é falha. Heartbeat não é conclusão. Não mate o worker por idle. Pergunta de worker: `orca orchestration reply --id <msg_id> --body "<resposta>" --json`.

Depois de cada `worker_done` aceito: se houver tarefa seguinte no mesmo agente, `worker-start --task <next> --terminal <handle>` com o handle de `worker-show`. Senão `orca orchestration worker-release --dispatch <dispatch_id> --json`. Só então `--ack`. Não dê `worker-release` por timeout.

Falha 1: corrigir no mesmo nível. Falha 2: subir de papel ou trocar de família, pela tabela de cota. Não repita a terceira igual. Worker aninhado só se a profundidade do Orca for 2 ou mais; senão o Hermes dispara quem o planejador nomeou.

## Laya

Antes de ler arquivo longo só para classificar, `laya-triagem`. Para rotular provedor da tarefa, `laya-classificador-modelos`. A Laya não escolhe slug. Pesquisa, leitura de documento e extração local são os únicos rótulos que viram provedor. Plano, dificuldade e `provedor=claude` não entram no roteamento.

- `ignorar`: não leia e não encaminhe.
- `so_rotulo`: use o rótulo; não leia.
- `precisa_ler`: aí leia.
- `top` não é probabilidade. Canal e área erram; não roteie cliente só por `canal`.
- Primeira chamada depois que o processo sobe leva ~30 s. Timeout 180 s.
- Texto já colado na mensagem não economiza token.

## Local

Ollama em `127.0.0.1:11434`. Tags locais: `qwen3.5:2b`, `qwen3.5:9b`, `llama3.2:3b`, `hermes3:latest`, `gemma4:e2b`, `gemma4:e4b`. `google/gemma-4-e4b` é outro arquivo, no LM Studio (`:1234`), não o `gemma4:e4b` do Ollama. Local não edita o repo no lugar de um worker. M4 16 GB: um modelo grande por vez.

## Observado, ainda não é regra

Notas de um Run real com Claude, Codex e Grok no mesmo checkout: [references/observado.md](references/observado.md). Não mude o roteamento por esse arquivo até a skill ser otimizada de propósito.
