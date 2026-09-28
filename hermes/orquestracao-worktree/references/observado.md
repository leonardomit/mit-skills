# Observado no Orca, ainda não é regra

Run `run_62602d8da209` no regulatorio, branch main, árvore suja. Hermes coordenou. Três workers em paralelo no mesmo checkout: Claude (auth e sessão), Codex (tenant e laboratório), Grok (MCP, SSRF, e-mail e cron). Os três terminaram `succeeded`. Nada disso muda a tabela de papéis até a skill ser otimizada de propósito.

## O que funcionou

- Partir por arquivo, não por worktree novo. Cada spec tinha lista exclusiva e lista `fora`. Ninguém reverteu mudança alheia. Claude viu a árvore suja e deixou os arquivos dos outros.
- Spec curta que os três obedeceram: linha de impacto, só estes arquivos, fora desta lista pare e diga, sem commit/push/merge/deploy, sem migration de produção, sem imprimir `.env`, rode só o teste que você criou.
- Achado fora da lista fica no relatório. O Grok viu texto de CSV público e `sincronizar_fonte_custo` e não editou.
- Checklist já nomeado não precisou de Fable nem de Astra. O Hermes escreveu as três specs e disparou.
- Depois que o teste passou, um "não altere mais, só `worker_done`" segurou o Codex. Melhor do que abrir um quarto escritor.

## O que a skill ainda erra ou não diz

- O card mente. `worktree ps` marcou o painel do Grok como `agentType: claude`. `terminal list` tinha `agentIdentity: grok`. Família e revisor saem de `agentIdentity`, não do `displayName`.
- "Não aplique migration em produção" não impediu o Claude de criar `prisma/migrations/...` e aplicar no Postgres local. Se a intenção for não criar migration, a spec tem de dizer isso. Produção não foi tocada.
- Implementação paralela não é revisão. Este Run parou no `worker_done`. Revisor de outra família ainda não rodou.
- Suíte inteira no checkout compartilhado é corrida. Os três rodaram só o próprio arquivo de teste.
