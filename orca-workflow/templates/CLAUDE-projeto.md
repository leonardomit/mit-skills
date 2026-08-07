# CLAUDE.md — <NOME_DO_PROJETO>

> **Template do fluxo Orca.** Uso: copiar para a raiz do repo como `CLAUDE.md`, preencher os `<campos>`, rodar `ln -s CLAUDE.md AGENTS.md` (Codex/Grok leem `AGENTS.md`) e apagar esta linha.
> Lido por TODOS os agentes: planejador, orquestrador, workers e QA. Mantenha curto — cada linha custa contexto em toda sessão.

---

## Projeto

- **O que é:** <1 frase — objetivo do repo>
- **Stack:** <linguagens, frameworks, versões>
- **Branch principal:** `<main>` — todo PR aponta para ela
- **Tickets:** <`tickets/*.md` (padrão) | Linear: projeto `<X>`>
- **Permissão Orca:** <Yolo — repo isolado, sem segredos | Manual — toca integrações reais>

## Comandos (fonte da verdade)

```bash
<comando de testes>            # testes
<comando de lint/pre-commit>   # lint
<comando para rodar local>     # run
<comando de setup>             # setup (worktree novo roda isso)
```

## Método (inegociável)

1. **Nenhum código sem ticket** com Acceptance Criteria (`tickets/_template.md`). Pedido fora de ticket → parar e avisar.
2. **Só o escopo do ticket.** Dúvida de arquitetura → perguntar ao coordenador/humano. Não decidir sozinho, não "aproveitar para melhorar" código vizinho.
3. **Testes acompanham a implementação.** Refactor só em código com testes.
4. **PRONTO =** testes afetados passando + lint ok + PR aberto contra `<main>` com: o que mudou, como testar, link do ticket.
5. **Merge é do humano. Sempre.** Nenhum agente faz merge, nem com aprovação verbal no meio da sessão.
6. **Gate humano obrigatório antes de:** migração/schema, deletar dados, deploy, gastar dinheiro, escrever em integração de produção (ERP, NF-e, pagamento, e-mail real).
7. **Commits:** conventional commits (`feat:` `fix:` `test:` `chore:` `docs:`), mensagem curta.
8. **Worker orquestrado:** encerrar com exatamente 1 `worker_done` (`--outcome succeeded|failed`) com a URL do PR. Falhou → `failed` com o erro real; nunca mascarar falha como sucesso.

## Estilo de trabalho (Leonardo)

- Comunicação em **PT-BR**. Direto ao resultado, sem narração. Raciocínio breve → conclusão.
- **Pense antes de codar. Simplicidade primeiro. Mudanças cirúrgicas. Objetivo do ticket guia tudo.** (princípios Karpathy)
- Questione premissas: se o ticket pede algo que quebra outra coisa, avise ANTES de implementar.
- Extras (riscos, atalhos, follow-ups) vão como **nota no PR** — nunca como código não pedido ou arquivo extra.
- Ações simples e reversíveis: execute sem pedir confirmação. Irreversíveis: gate (regra 6).
- **Nunca invente dados** de negócio, API, SKU, NCM ou regulatórios. Não achou → pergunte ou marque `TODO(humano)`.

## Segurança

- **Nunca versionar segredos.** `.env` no `.gitignore`. Worktrees herdam tudo que está no repo.
- **Não tocar sem gate:** <pastas/arquivos proibidos — ex.: `migrations/`, `dados/`, `.github/workflows/`>
- Dados reais (clientes, fiscal, produção): **somente leitura**, e apenas se o ticket exigir explicitamente.
- Este repo **não acessa o vault pessoal do Leonardo.** Memória do projeto = este arquivo + `docs/DECISIONS.md` + tickets. Nada de ler/escrever fora do repo.

## Decisões do projeto

Decisão técnica tomada durante um ticket → registrar em `docs/DECISIONS.md` (3 linhas: data, decisão, motivo + alternativa rejeitada). Decisão de **negócio** é do Leonardo — vira gate, não registro automático.

## ❌ Nunca fazer

> Cresce a cada erro real. Adicionar linha aqui faz parte do conserto.

- Nunca mergear PR nem deletar branch de outro worker
- Nunca mudar arquitetura ou adicionar dependência sem ticket próprio
- Nunca desabilitar/skipar teste para "passar" — falhou, reporte
- Nunca commitar código morto, `print`/`console.log` de debug ou credenciais
- Nunca editar este arquivo ou tickets de outros workers (só o coordenador/humano)
- <novos erros entram aqui via PR>

---

## Conformidade empresa — APAGAR esta seção se o projeto não for da empresa

- Todo texto de produto/comunicação (rotulagem, copy, e-mail, UI) passa pelo filtro **ANVISA**: sem alegação de cura/prevenção/tratamento; alegação funcional só da lista autorizada; na dúvida → `TODO(humano: revisão compliance/RT)`. Nunca validar alegação fora da lista.
- Integrações fiscais/ERP (ERP, Bling, NF-e, loja virtual): **escrita = gate humano**; leitura livre conforme o ticket. ERP tem rate limit agressivo (`MISUSE_API_PROCESS` bloqueia 30 min) — usar backoff.
- Identidade visual (kit v2): cor primária `#XXXXXX` · cor secundária `#XXXXXX` · Amarelo Sol `#XXXXXX` · fundos Areia/Verde Névoa · tipografia Serif + Sans.
