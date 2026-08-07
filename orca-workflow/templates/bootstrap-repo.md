# Bootstrap — plugar o fluxo num repo (5–10 min por repo)

Checklist antes do primeiro `/plan-tickets`:

- [ ] Repo git limpo, branch principal definida, sem trabalho não commitado
- [ ] `gh auth status` OK (workers abrem PR com `gh pr create`)
- [ ] **Testes:** existe runner + pelo menos 1 teste real rodando?
      - Não → o primeiro ticket é obrigatoriamente `T-000-bootstrap-testes` (runner + smoke tests + pre-commit). Sem isso não há paralelismo.
- [ ] Lint/pre-commit configurado (ou entra no T-000)
- [ ] Criar pasta `tickets/` na raiz (modo markdown) — ou board no Linear (modo híbrido)
- [ ] Copiar `templates/ticket.md` para `tickets/_template.md`
- [ ] **Segredos fora do repo:** `.env` no `.gitignore`, nenhuma credencial versionada (worktrees herdam tudo)
- [ ] Copiar `templates/CLAUDE-projeto.md` para a raiz do repo como `CLAUDE.md`, preencher os `<campos>` e criar o symlink para os demais agentes:

```bash
ln -s CLAUDE.md AGENTS.md   # Codex/Grok leem AGENTS.md
```

- [ ] Se o projeto NÃO for da empresa: apagar a seção "Conformidade empresa" do CLAUDE.md

- [ ] Definir permissão do repo no Orca: Yolo (isolado, sem segredos) ou Manual (integrações reais) — ver SETUP §3

Pronto: `/plan-tickets "sua ideia"`.
