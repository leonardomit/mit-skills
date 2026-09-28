---
name: orquestracao-orca
description: Roteamento multimodelo no Orca ADE: qual CLI agent (Claude Code, Codex, Gemini, Grok) recebe cada tarefa, quando fazer fan-out paralelo em worktrees, revisão cruzada por agente diferente e merge só com aprovação humana. Usar ao abrir tarefas no Orca.
---

# Orquestração no Orca ADE

Orca roda vários CLI agents em paralelo, cada um em worktree isolado, e deixa comparar e mesclar o vencedor. O que muda aqui: o isolamento já vem pronto, o revisor independente é **outro agente**, e o gate humano é o merge.

## Classes → agente

| Classe | Agente no Orca | Uso |
|---|---|---|
| `ECONOMY` | Claude Code com Haiku; Gemini CLI flash | localizar, resumir, boilerplate, testes triviais |
| `STANDARD` | Claude Code com Sonnet; Codex | feature isolada, bugfix reproduzível, docs |
| `PREMIUM` | Claude Code com Opus | arquitetura, refactor crítico, segurança, gate |
| `CODE_AGENT` | qualquer um acima, em worktree próprio | toda execução técnica |
| `RESEARCH` | Grok CLI; Gemini com web | docs de API, alternativas, contraponto |
| `HUMAN_GATE` | merge/aprovação no Orca ou GitHub | mudança relevante, produção |

Mantenha o agente da tabela. Se o modelo nomeado não existir nesta máquina, use o fallback da mesma classe. Não suba de classe por isso.

| Classe | Fallback nesta máquina |
|---|---|
| `ECONOMY` | `claude-haiku-4-5-20251001`. Local: `qwen3.5:9b`; extração curta `qwen3.5:2b`. Gemini flash só se autenticado. |
| `STANDARD` | `claude-sonnet-5`; código `gpt-6-sol`. Tarefa direta: `gpt-5.6-terra` ou `gpt-6-luna`. |
| `PREMIUM` | `claude-opus-5-5` (alias `opus-5-5`). Se recusar, `claude-opus-5`. Plano longo: `claude-fable-5-1`. Fronteira de implementação: `gpt-6-astra` `--effort high`. |
| `CODE_AGENT` | `gpt-6-sol`. Complexo: `claude-opus-5-5`. Diff pequeno: `gpt-6-luna`. |
| `RESEARCH` | `grok-4.7`. Cota do Grok acabou: Gemini autenticado; senão Claude; senão Codex. |

Para disparo supervisionado no Orca, prefira `orquestracao-worktree`. Gemini sem login não entra.

Regra de independência: **o revisor é de família diferente do executor**. Claude executa → Codex ou Gemini revisa. Codex executa → Claude revisa. Mesmo modelo em worktree novo não conta como independente.

## Classificação ao abrir a tarefa

Uma linha no título ou primeira linha do prompt:

`[impact 0-3 | complexity 0-3 | ambiguity 0-3 | fanout N | reviewer <agente>]`

`impact`: produção, dados, dinheiro, ANVISA/LGPD. `fanout`: quantos agentes recebem o mesmo prompt.

## Quando usar fan-out

| Situação | fanout | Escolha |
|---|---|---|
| Tarefa clara, baixo impacto | 1 | executor único + revisor |
| Abordagem incerta, médio impacto | 2–3 agentes diferentes | comparar diffs, mesclar melhor, revisor no vencedor |
| Refactor crítico ou bug obscuro | 3–5 | PREMIUM compara e escolhe; revisor cruzado; humano mescla |
| Volume de tarefas pequenas independentes | 1 por tarefa, N tarefas em paralelo | ECONOMY/STANDARD, revisor por amostra |

Fan-out custa N vezes. Só vale quando o custo de escolher errado supera o custo de rodar N. Não use fan-out para tarefa de impact <= 1 e ambiguity <= 1.

## Pipeline por tarefa

```text
1. PLAN      Sonnet/Opus escreve spec curta se complexity >= 2 (pode ser a própria tarefa 0)
2. EXEC      1..N agentes, cada um em worktree; prompt idêntico; sem push/merge
3. VALIDATE  cada worktree roda testes, lint, build; resultado no relatório do agente
4. COMPARE   se fanout > 1: Opus compara diffs e relatórios; escolhe ou combina
5. REVIEW    agente de outra família revisa o diff vencedor; anotações via "Annotate AI Diffs"
6. FIX       executor original recebe as anotações em lote; 1 rodada
7. GATE      impact >= 2: Opus classifica APROVAR / DEVOLVER / BLOQUEAR
8. MERGE     humano mescla no Orca/GitHub. Sempre.
9. LOG       agente, modelo, fanout, vencedor, achados, tentativas
```

## Prompt padrão de execução (idêntico para todos os agentes do fan-out)

```md
[impact X | complexity Y | ambiguity Z]
Objetivo: [observável]
Escopo: [arquivos/módulos]. Fora do escopo: [lista].
Critérios de aceite: [mensuráveis]
Validação: [comandos exatos]
Regras: menor mudança; rode a validação e cole a saída real; sem push, merge, deploy;
regra de negócio ambígua = pare e registre em OPEN_QUESTIONS.md no worktree.
Entrega: resumo, arquivos, decisões, saída dos comandos, critérios atendidos/pendentes, riscos.
```

## Prompt de revisão cruzada

```md
Revisor adversarial de outra família de modelo. Não reimplemente, não elogie.
Compare requisito e diff. Reporte só problemas concretos: erro funcional, dados, segurança,
critério não atendido, teste ausente, compatibilidade, risco regulatório.
Por achado: severidade, arquivo:linha, cenário, correção mínima.
Sem achados: "Nenhum problema concreto encontrado" + o que não pôde validar.
```

## Prompt de comparação (fanout > 1)

```md
Compare os N diffs e relatórios abaixo contra o requisito.
Critérios, nesta ordem: validação passou; critérios de aceite; tamanho do diff; risco; clareza.
Saída: vencedor, motivo em 3 linhas, o que aproveitar dos outros, o que nenhum resolveu.
```

## Escalonamento

- Falha de validação: 1 rodada de correção no mesmo worktree.
- Segunda falha: nova tarefa com agente de classe acima ou fan-out 2–3.
- Todos os agentes do fan-out falharam: o problema é o requisito. Voltar ao PLAN, não subir modelo.
- Regra de negócio ausente: `OPEN_QUESTIONS.md` bloqueia o merge até resposta.

## Gate humano (lista fechada)

Merge em main/produção, migração de banco, mudança em auth/segredos/permissões, integração que escreve em ERP/CRM/e-commerce, exclusão de dados ou infra, deploy. Worktree descartável não exige gate.

## Custo e contexto

- `orca.yaml` e `AGENTS.md` do repo carregam as regras fixas; o prompt da tarefa carrega só o específico.
- Fan-out com Opus só em impact >= 2. Abaixo disso, Sonnet e Codex.
- Acompanhe uso por conta no próprio Orca; se uma conta esgotar, troque de conta, não de classe.
- Registre por tarefa: fanout, vencedor, achados do revisor, rodadas. Fan-out que nunca muda o vencedor é desperdício; reduza.

## Checklist ao abrir tarefa no Orca

- Linha de classificação no prompt?
- Fan-out justificado pelo impacto/ambiguidade?
- Revisor de outra família definido?
- Comandos de validação explícitos?
- Merge reservado ao humano?
