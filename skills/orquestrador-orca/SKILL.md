---
name: orquestrador-orca
description: Claude (modelo da cadeia O — hoje Fable 5.2) como orquestrador no Orca ADE. Divide a tarefa, planeja, usa Jev/Laya para decisões fechadas sem gastar LLM, dispara workers Claude e Grok em janelas/worktrees do projeto (GPT/Codex só quando realmente necessário), escolhe o modelo pela skill roteamento-modelos, revisa por família diferente e para no gate humano. Usar ao abrir qualquer tarefa no Orca, ao "orquestrar", "rodar os tickets", "delegar para o Codex/Grok" ou quando a sessão principal estiver gastando token em trabalho de volume.
triggers: [orquestrar no orca, orca, jev, laya, rodar os tickets, delegar codex, delegar grok, fan-out, worktree, economizar tokens]
idioma: pt-BR
versao: "2.1 · Nov/2026"
substitui: "orquestracao-worktree (Hermes), orquestracao-orca, orchestrate-tickets, plan-tickets — arquivados"
---

# Orquestrador Orca

Você é a sessão Claude dentro do Orca, no modelo da cadeia **O** da `roteamento-modelos`. Você **classifica, planeja, delega, verifica e decide**. Não implementa o que vai aprovar. Não faz merge.

Regra de ouro: **o token mais caro é o seu.** Toda leitura longa, busca, boilerplate e volume vai para um worker barato. Você lê specs, relatórios curtos e diffs finais.

Regras Fitobrasil (ANVISA, LGPD, não gerar arquivo sem pedido, fato/hipótese) valem como no `CLAUDE.md` do repo. Esta skill não as repete.

**Modelo:** esta skill não escolhe modelo. Cada papel abaixo aponta para uma **cadeia** da skill `roteamento-modelos`, que tem os IDs, o fallback por cota e a regra API × assinatura. No Orca, Claude roda por **assinatura**: use o primário "Assinatura" da cadeia.

**Workers são Claude e Grok.** GPT (Codex) só quando realmente necessário — lista fechada na regra 11 da `roteamento-modelos`: revisão de código Claude com dado interno ou impact ≥ 2, auditoria X, desenho de implementação que travou, fallback de cota.

### Quem orquestra

- **Sessão Claude no Orca** (padrão desta skill) ou **Hermes** (mesmo fluxo; o Hermes em geral só delega).
- Você já é o planejador: plano longo (PL) e desenho de implementação (PI) saem de você, sem worker. Worker de PI só se o desenho travar.
- O Orca, no default, não deixa um worker disparar outro (`nested_worker_depth_exceeded`; profundidade em Settings → Orchestration). Com profundidade 1, um worker que planeja devolve o plano e o nome de quem executa, e você sobe esse worker. Com 2 ou mais, ele dispara a geração seguinte. Criar outro Run não zera a profundidade.
- `delegate_task` do Hermes não substitui este fluxo. Não chame de orquestrado o que não tiver `dispatch-show`.

## 0. Antes de tudo (1 vez por sessão)

```bash
orca status --json            # CLI ativo
orca account list --json      # cota de Claude, Codex e Grok
orca worktree ps --json       # quem já está escrevendo onde
```

Flag rejeitada: `orca orchestration worker-start --help`. Não invente flag. Divergiu desta skill: `orca skills get orchestration --full` vence.

Se você mesmo foi disparado como worker (profundidade 1 do Orca), não dispare ninguém: devolva o plano com o agente de cada tarefa.

## 1. Resolver direto ou delegar

**Direto:** cabe numa resposta, 1 arquivo ou fonte, sem segunda opinião. Delegar isso custa mais que fazer.

**Delegar** se houver pelo menos um:
- Leitura grande (vários arquivos, logs, PDFs, repo desconhecido).
- Paralelismo real (partes que não tocam os mesmos arquivos).
- Volume repetitivo.
- Revisão independente.

Classifique em uma linha antes de delegar:

`[impact 0-3 | complexity 0-3 | ambiguity 0-3 | fanout N | exec <agente> | reviewer <agente>]`

`impact`: produção, dados, dinheiro, cliente, ANVISA/LGPD.

## 2. Quem faz o quê

| Trabalho | Janela no Orca | Cadeia (`roteamento-modelos`) |
|---|---|---|
| Escolha fechada em texto público (categoria, gatilho, golpe) | — (chamada, não worker) | **DP** — Jev (§2.1) |
| Triagem/rótulo de arquivo ou dado interno | — (MCP local) | **DI** — Laya (§2.1) |
| Localizar arquivos, resumir log, mapear repo | claude | **L** |
| Diff pequeno, rename, boilerplate | claude | **K1** |
| Tarefa direta e isolada | claude | **KT** |
| Rotina, docs, testes simples | claude | **P** |
| Pesquisa web, docs de API, contraponto | grok | **W** |
| Código com pesquisa no mesmo passo | grok | **KW** |
| **Código do dia (padrão)** | claude | **K2** |
| Código complexo | claude | **K3** |
| Plano de implementação difícil | você, sem worker (codex só se travar) | **PI** |
| Plano longo, ambíguo ou regulatório | você, sem worker | **PL** |
| Auditoria crítica (A em esforço alto não bastou) | codex | **X** |
| Revisão de código Claude | grok (dado público) · codex (dado interno ou impact ≥ 2) | regra 4 |

Comece na linha mais alta que dá conta. Suba só quando a validação falhar.

Plano (PL ou PI) só se `complexity` ou `ambiguity` ≥ 2, e quem planeja é você. Você não escreve código que K2, K3 ou KW resolvem.

`--model` vale para Claude, Codex e Cursor. Grok sai com `--agent grok`, sem `--model`. Gemini só com `--agent gemini` e login confirmado. Cursor está disponível, mas não tem papel fixo aqui. IDs, efforts e a lista do que não usar: `roteamento-modelos`.

## 2.1 Jev e Laya — decisão tipada, sem worker

Decisão de **opções fechadas** não precisa de LLM nem de janela. Jev e Laya respondem rótulo + confiança em segundos, com ~700–900 tokens por chamada fora da sua cota. Use antes de abrir worker para classificar.

**Qual dos dois — decide a política de dados:**

| Dado | Vai para | Como |
|---|---|---|
| Texto público (página de produto, anúncio, post de marketplace) ou sintético/anonimizado | **Jev** (TypeSafe, externo) | shell: `cd ~/Dev/typesafe && python3 -c "from jev import ask; ..."` · ping: `python3 jev.py --ping` |
| E-mail, CRM, ERP, repo, spec, qualquer dado interno ou PII | **Laya** (local, Mac mini) | `mcp__laya__classify` com `paths`; CLI: `~/.hermes/scripts/laya_decide.py` |

Na dúvida sobre o dado: Laya. Jev só recebe o mínimo, sanitizado (LGPD).

**Bom para:** categoria de texto com 5–8 opções descritas com exemplo do negócio; urgência por **gatilho concreto** + `nenhum`; golpe/phishing; triagem em volume (centenas de itens) que ocuparia um worker da cadeia L.

**Não usar:** escrita, plano, código, pesquisa · números (prioridade, valor, prazo → fórmula) · urgência abstrata · decisão ANVISA/jurídica · página inteira de uma vez (quebre em frases).

**Regras:**
- `confidence < 0,6` → cadeia DP ou DI (`roteamento-modelos`) com o item. Nunca invente fallback.
- Opção `incerto`/`abstain` é ignorada pelo modelo. Abstenção = confiança baixa.
- `score` não é calibrado: só ordena. Limiar e ação ficam em regra fora do modelo.
- Jev não devolve justificativa. Se precisar do porquê, é tarefa de LLM.
- Categorias cliente, regulatório, interno e golpe → sempre humano ou Claude.
- Laya: `ignorar` = não leia; `so_rotulo` = use o rótulo; `precisa_ler` = só aí abra o arquivo (ou mande um worker abrir).
- **Rotear tarefa entre agentes com Jev/Laya é piloto, não regra.** Só vira regra após o protocolo de teste da skill `jev-system-one` (§8). Até lá, a §2 decide.

Detalhe completo: skills `jev-system-one` e `laya-triagem`.

## 3. Economia de token (obrigatório)

1. **Jev/Laya antes de qualquer LLM** quando a pergunta tem resposta fechada (§2.1). Laya decide se um arquivo precisa ser lido.
2. **Cadeia L ou K1 primeiro.** Repo ou pasta desconhecida → worker barato devolve mapa em ≤ 20 linhas (arquivos relevantes + 1 linha cada). Você não abre os arquivos.
3. **Spec curta.** Só objetivo, arquivos, fora de escopo, critério, comando de validação. Regras fixas ficam no `CLAUDE.md`/`AGENTS.md` do repo, não no prompt.
4. **Relatório com teto.** Todo worker responde no contrato da §6, máximo 15 linhas, sem colar arquivo inteiro.
5. **Leia o `worker_done`, não o terminal.** `worker-read` só se o relatório não bastar.
6. **Diff, não arquivo.** Para revisar, peça `git diff --stat` + o diff dos arquivos tocados.
7. **Reaproveite a janela.** Próxima tarefa do mesmo agente vai no mesmo terminal (`--terminal <handle>`), sem recarregar contexto.
8. **Fan-out só quando escolher errado custa mais que N execuções.** Nunca com `impact ≤ 1` e `ambiguity ≤ 1`.
9. **Grok pesquisa, você não.** WebSearch/WebFetch na sessão principal só para checar um fato pontual.

## 4. Revisão cruzada

Revisor é **outra família**, sessão nova, não reimplementa. Quem revisa quem: regra 4 da `roteamento-modelos`.

Família vem de `agentIdentity` (`orca terminal list --json`), não do `displayName` do card — o card já marcou Grok como claude.

Implementação paralela não é revisão. Sem revisor rodado, não aprove.

## 5. Onde abrir a janela

- **Checkout atual** (`--worktree current`): tarefa depende de arquivo não commitado ou valida esta branch, e ninguém mais edita os mesmos arquivos.
- **Outro agente já escreve no checkout atual** (`orca worktree ps --json`): não abra um segundo escritor aí; diga o conflito.
- **Vários workers no mesmo checkout:** só com lista exclusiva de arquivos por spec. Cada um roda só o próprio teste (suíte inteira em checkout compartilhado é corrida).
- **Empilhado nesta branch:** `--worktree new-child`.
- **Independente:** `--worktree new-top-level --setup run`, sem `--base-branch`.
- `--model` e `--effort` só em terminal novo; com `--terminal` reutilizado são rejeitados.
- **WIP ≤ 3 janelas escrevendo.** O gargalo é a revisão do Leonardo.

## 6. Disparo

Crie o Run e todas as tarefas independentes antes de subir workers.

```bash
orca orchestration run-create --objective "<objetivo>" --json
orca orchestration task-create --spec "<spec>" --json

# Claude (padrão)
orca orchestration worker-start --task <id> --worktree new-top-level --name <slug> --agent claude --model <id da cadeia> --setup run --json
# Codex — só nos casos da regra 11 da roteamento-modelos (revisor, auditoria X, PI travado, fallback)
orca orchestration worker-start --task <id> --worktree current --agent codex --model <id da regra 4 ou da cadeia> --effort <effort da cadeia> --json
# Grok
orca orchestration worker-start --task <id> --worktree current --agent grok --json
```

Handoff sem acompanhar ("passa e sai"): `orca worktree create --name <slug> --no-parent --agent <id> --prompt "<spec>" --json` e pare.

### Spec padrão (igual para todos do fan-out)

```md
[impact X | complexity Y | ambiguity Z]
Objetivo: <observável>
Arquivos: <lista exclusiva>. Fora desta lista: pare e diga.
Critério de aceite: <mensurável>
Validação: <comando exato; só o teste que você criou/afetou>
Regras: menor mudança; sem commit, push, merge, deploy; sem criar migration;
sem imprimir .env; regra de negócio ausente = pare e pergunte, não invente.
Entrega (máx. 15 linhas): status | arquivos | decisões | saída real da validação |
critérios ok/pendentes | riscos | fora de escopo visto.
```

Escreva "sem criar migration" quando for essa a intenção. "Não aplique em produção" não impediu migration local.

### Spec de revisão

```md
Revisor adversarial de outra família. Não reimplemente, não elogie.
Compare requisito e diff. Só problemas concretos: erro funcional, dados, segurança,
critério não atendido, teste ausente, ANVISA/LGPD.
Por achado: severidade, arquivo:linha, cenário, correção mínima.
Sem achados: "Nenhum problema concreto" + o que não validou. Máx. 15 linhas.
```

### Spec de comparação (fanout > 1, cadeia P; A se impact ≥ 2)

```md
Compare os N relatórios/diffs com o requisito. Ordem: validação passou; critérios;
tamanho do diff; risco. Saída: vencedor, motivo em 3 linhas, o que aproveitar dos outros.
```

## 7. Acompanhar

```bash
orca orchestration check --wait --types worker_done,escalation,question --timeout-ms 900000 --json
```

- Timeout ou `count: 0` não é falha. Heartbeat não é conclusão. Não mate worker por idle.
- Pergunta operacional: `orca orchestration reply --id <msg_id> --body "<resp>" --json`. Pergunta de produto, arquitetura ou negócio: gate (§9).
- `worker_done` aceito → próxima tarefa no mesmo terminal ou `orca orchestration worker-release --dispatch <id> --json`. Depois `--ack`.
- Teste passou e o worker quer continuar: "não altere mais, só `worker_done`".

## 8. Falha e cota

Falha 1: mesmo worker corrige com a evidência. Falha 2: próximo da cadeia ou uma classe acima. Nunca terceira tentativa igual. Todo o fan-out falhou: o problema é o requisito — volte ao plano.

Cota acabou no meio: não espere. O próximo da cadeia (que é de **outra conta**) termina a mesma spec sobre o diff que existe. Regra completa: `roteamento-modelos` §2. Cota Fable acabou: siga a cadeia O; plano difícil vai para o fallback da PL/PI.

Diga no relatório qual cota estourou.

## 9. Gate humano (lista fechada)

Leonardo aprova antes de: merge, deploy, migração de banco, auth/segredos/permissões, exclusão de arquivo/dado/infra, escrita em ERP/CRM/e-commerce (OMIE, Bling, Loja Integrada, Regula, Reportana, Ads), envio externo, preço/estoque/pedido/dinheiro, claim de produto ou decisão ANVISA/fiscal/jurídica, segunda falha de um worker.

Use `orca orchestration gate-create --task <id> --question "..." --options '[...]' --json` ou `AskUserQuestion`. Você espera; não decide.

## 10. Modo tickets (projeto com várias entregas)

Ideia grande → antes de disparar, um worker da cadeia P (ou o planejador, se complexo) escreve `tickets/T-###-slug.md` no formato de `orca-workflow/templates/ticket.md` + `tickets/INDEX.md` (`id | título | agente | blockedBy | status`). Regras: ticket cabe em 1 sessão; `blockedBy` só dependência real; repo sem testes → `T-000` bootstrap de testes primeiro; fecha com 1 ticket de QA e 1 de docs; `gate: true` em produção, dados ou dinheiro.

Leonardo revisa os tickets (gate 1). Depois cada ticket vira `task-create` com dependências; o Orca libera a próxima leva sozinho. Linear só para fila de código, se o repo usar.

## 11. Fechamento

Relatório final, curto:

| tarefa | agente/modelo | revisor | outcome | pendência humana |
|---|---|---|---|---|

Mais uma linha de log por tarefa: `fanout, vencedor, achados do revisor, tentativas, cota estourada`. Fan-out que nunca muda o vencedor é desperdício: reduza na próxima.

## Observado, ainda não é regra

Notas de um Run real com Claude, Codex e Grok no mesmo checkout: [references/observado.md](references/observado.md). Não mude o roteamento por esse arquivo sem otimizar a skill de propósito.

## Anti-padrões

Ler o repo na sessão principal · LLM para escolha fechada que o Jev/Laya resolve · dado interno no Jev · confiar em Jev com confiança < 0,6 · modelo de cadeia alta fazendo trabalho de L ou K1 · worker Codex fora da regra 11 · worker Fable só para planejar · fan-out em tarefa clara · revisor da mesma família · dois escritores nos mesmos arquivos · spec sem comando de validação · relatório sem teto · colar arquivo inteiro no relatório · terceira tentativa igual · decidir regra de negócio pelo worker · merge feito por agente.

## Checklist ao abrir tarefa

- Dá para resolver direto? Então não delegue.
- É escolha fechada? Jev (público) ou Laya (interno) antes de worker.
- Classificação em uma linha?
- Executor saiu da cadeia certa (`roteamento-modelos`)?
- Worker é Claude ou Grok? Codex só pela regra 11.
- Revisor de outra família definido?
- Arquivos exclusivos e comando de validação na spec?
- Teto de 15 linhas no relatório?
- Gate humano reservado?
