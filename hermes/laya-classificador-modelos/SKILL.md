---
name: laya-classificador-modelos
description: "Use when Laya classifica o provedor da tarefa."
version: 1.0.0
---

# Laya — classificador de provedor

Classificador local. Não é chat e não escolhe o id do modelo. Devolve rótulo de função e provedor. O mapa abaixo decide se o rótulo vale. O resto vai para `orquestracao-worktree`.

Modelo nomeado pelo usuário ganha. Não chame a Laya para trocar o que ele pediu.

## Chamada

`mcp__laya__classify`. Passe `questions_json` com o objeto abaixo. Isso substitui o preset. No máximo 6 perguntas. Arquivo: `paths`, não o corpo. Texto já na conversa não economiza token; a chamada ainda serve para rotular o pedido.

Primeira chamada depois que o processo sobe leva ~30 s. Timeout 180 s. `top` não é probabilidade. Abaixo de 0,7, descarte aquele rótulo.

```json
{"funcao":{"type":"choice","instructions":"What kind of work does this task ask for?","criteria":{"planejar":"design a plan, architecture, or a hard ambiguous spec before anyone writes code","codigo":"implement, fix, or change code in a repository","menor":"a small edit, a short answer, formatting, or a straightforward routine task","pesquisa":"look up facts on the web, cite a source, or give a counterpoint","ler_doc":"read a long document, PDF, image, or lab report"}},"provedor":{"type":"choice","instructions":"Which provider should do this task?","criteria":{"claude":"the hardest long plan, or complex everyday code that is not a quick edit","codex":"everyday coding, a small code diff, or a demanding implementation design","grok":"web research, a counterpoint, or code that needs the web in the same step","gemini":"a second web source, or reading a long PDF or image","local":"extract or summarize text already in hand, with no repository edit"}},"dureza":{"type":"choice","instructions":"How hard is this task?","criteria":{"facil":"obvious, short, or routine","dia":"normal everyday work","dificil":"long, ambiguous, architectural, or the hardest case"}}}
```

Não use `dureza`. No teste, um plano regulatório saiu `facil` com top 0,90.

## O que aceitar

| Rótulo | Condição | Rota |
|---|---|---|
| `funcao=pesquisa` | top ≥ 0,7 | Grok, pesquisa. Foi o acerto limpo. |
| `funcao=ler_doc` | top ≥ 0,7 | Gemini, se autenticado. Ignore `provedor`: o PDF saiu `claude`. Sem login, não dispare Gemini. |
| `provedor=local` | top ≥ 0,7 e a tarefa não edita repo | `qwen3.5:9b`. Extração curta: `qwen3.5:2b`. Ignore `funcao`: extração saiu `codigo`. |
| `funcao=codigo` e `provedor=codex` | top de `funcao` ≥ 0,9 | Só confirma código na família Codex. Quem escolhe Sol, Luna ou Astra é `orquestracao-worktree`. |
| qualquer outro | | Descarte. Use a tabela de `orquestracao-worktree`. |

`provedor` sozinho puxa para Codex. Não mande Fable, Astra, Opus nem Sonnet porque a Laya disse `claude` ou `codex`. Plano ANVISA saiu `codigo` / `codex` / `facil`. Resposta curta saiu `codex` com top 0,31.

## O que não fazer

- Não peça à Laya o slug (`gpt-6-sol`, `claude-opus-5-5`). Ela não viu esses ids.
- Não suba de classe por um rótulo fraco.
- Não leia o arquivo se a outra skill de triagem, `laya-triagem`, disser `ignorar` ou `so_rotulo`. Esta skill não substitui aquela.
