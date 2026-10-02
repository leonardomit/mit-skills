# mit-skills

Skills, agentes e workflows de autoria própria para Claude (Cowork / Claude Code).
Repositório **privado** — critérios pessoais de investimento, produtividade e automações
de infraestrutura. Material específico da empresa (regulatório, comercial, criativos)
vive em repo separado (`fito-skills`), para permitir compartilhar este aqui no futuro.

> **Escopo:** só entra aqui o que foi escrito por mim. Skills de terceiros instaladas na
> conta (ui-ux-pro-max, gpt-taste, emil-design-eng, karpathy-guidelines, llm-council,
> pre-mortem, ckm*, ponytail*, apple-design, animate etc.) **não** fazem parte deste repo —
> redistribuí-las seria uso de obra alheia sem licença.

---

## skills/

Formato Claude Agent Skill (`SKILL.md` com frontmatter `name` + `description`).

| Skill | O que faz |
|---|---|
| `analise-carteira-lendarios` | Auditoria de carteira e teses pelas lentes de Simons, Druckenmiller, Buffett, Lynch, Verde, Dynamo e Barsi. Score 0–10 por dimensão. Análise de processo, não recomendação. |
| `screener-lendarios` | Shortlist de ativos-candidatos aplicando os filtros quantitativos dos mesmos investidores. Todo número vem de busca feita na conversa, com data. |
| `produtividade-foco` | 7 prompts de função executiva: paralisia de tarefas, brain dump, body doubling, menu de dopamina, estimativa de tempo. |
| `markitdown-to-md` | Converte PDF/DOCX/PPTX/XLSX para Markdown via MarkItDown antes da leitura, para economizar contexto. Inclui `scripts/convert_to_md.py`. |
| `orquestracao-claude-code` | Roteamento multimodelo no Claude Code/Cowork: delegação a subagentes Haiku/Sonnet/Opus por impacto/complexidade, revisor em Agent novo, gate humano via AskUserQuestion. |
| `orquestracao-hermes` | Roteamento para automações do Hermes: modelo local para volume, API para julgamento, fila de exceções, handoff para Claude Code. Hermes nunca executa impacto 3. |
| `orquestracao-orca` | Roteamento no Orca ADE: qual CLI agent por classe, fan-out em worktrees, revisão cruzada por família diferente, merge só humano. |

Também na raiz, empacotadas como `.skill`: `financeiro-decisao` (precificação, viabilidade,
comparativo tributário — empresa brasileira genérica) e `financeiro-rotina` (DRE, fluxo de
caixa, fechamento mensal, SOP financeiro).

## hermes/

Skills de autoria própria do Hermes. Não misturar com `skills/` (Claude). Skill de terceiro não entra.

| Skill | O que faz |
|---|---|
| `laya-triagem` | Classificador local Laya no Mac mini. Prefere caminho de arquivo e devolve só rótulo. |
| `laya-classificador-modelos` | Laya rotula a tarefa. Só pesquisa, leitura de documento e extração local viram provedor. O resto não. |
| `orquestracao-worktree` | Orquestra worktree no Orca: escolhe o modelo real (GPT-6, Claude 5, Grok, Ollama, Laya) e dispara o worker. |
| `orquestracao-multimodelo` | Roteamento fora do Orca. Mantém Haiku/Sonnet/Opus e usa o catálogo desta máquina se o modelo nomeado não existir. |
| `google-sheets-sync-preservar-formulas` | Sync de planilha local para Sheets sem apagar fórmula de total. |
| `instagram-afiliados` | Páginas de afiliados no Instagram, fora da marca empresa. |
| `daily-journal-obsidian-gbrain` | Journal noturno: Obsidian e gbrain. |
| `social-content-ingest` | Ingestão de post Instagram/X/YouTube quando o fetch direto falha. |
| `tailscale-vpn` | Acesso ao Mac mini via Tailscale, portas e keepawake. |
| `apple-silicon-storage` | Expansão de armazenamento neste Mac mini. |
| `self-hosted-apps` | Apps locais em Docker Compose (Nextcloud e outros). |
| `local-llm-runtimes` | Um GGUF compartilhado entre Ollama e LM Studio. |
| `hermes-cron-ops` | Diagnóstico e reparo de cron do Hermes. |
| `hermes-desktop-troubleshooting` | Boot loop, UI em branco e 401 do Hermes Desktop. |

## agents/

Personas e orquestradores (mesmo formato de frontmatter, usados como subagentes).

- `comite-lendarios` — analista que audita decisões de investimento; par do `screener-lendarios`.

## orca-workflow/

Projeto autocontido de orquestração por tickets: `README.md`, `PLAYBOOK.md`, `SETUP.md`,
as skills `plan-tickets` e `orchestrate-tickets`, e os templates de ticket, `CLAUDE.md` de
projeto e bootstrap de repo.

## docs/

- `orca-fluxo.md` — desenho do fluxo Orca.
- `deep-value-investing-graham-greenwald.md` — nota de referência (Graham / Greenwald).
- `manual-claude-metodo-completo.md` — manual completo do método de trabalho com Claude.

---

## Instalação

Copiar a skill desejada para o diretório de skills do agente:

```bash
cp -r skills/analise-carteira-lendarios ~/.claude/skills/
```

Ou empacotar como `.skill` (zip com a pasta na raiz) para subir pela interface:

```bash
cd skills && zip -r ../analise-carteira-lendarios.skill analise-carteira-lendarios
```

## Aviso

As skills de investimento são análise de processo — não são recomendação de compra ou venda.
