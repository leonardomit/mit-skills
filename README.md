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
| `orquestracao-hermes` | Roteamento para automações do Hermes: modelo local para volume, API para julgamento, fila de exceções, handoff para Claude Code. Hermes nunca executa impacto 3. |
| `roteamento-modelos` | **Fonte única de modelos.** IDs desta máquina, cadeias de fallback por conta (cota acabou → outra conta), regra API × assinatura, nós locais (Mac mini + GTX 1070 via PAIR), Jev e Laya. As demais skills apontam para as cadeias e não citam modelo. |
| `orquestracao-multimodelo` | Método fora do Orca (Claude Code, Cowork, Hermes): classificação 0–3, pipeline, executor × revisor de outra família, escalonamento, gate humano. Junta as antigas `orquestracao-claude-code` e `orquestracao-multimodelo` (Hermes). |
| `orquestrador-orca` | **Skill única do Orca.** Claude ou Hermes orquestram; Jev/Laya para decisões fechadas; workers Claude, Codex e Grok em janelas/worktrees; papel → cadeia da `roteamento-modelos`; revisão por outra família; gate humano. Absorveu `orquestracao-worktree`. |
| `jev-system-one` | Jev/System One (TypeSafe) como classificador tipado e consultivo: política de dados, gatilhos de urgência, protocolo de teste. Pacote Hermes (manifesto MCP) em `hermes/jev-system-one/`. |
| `criacao-de-marca-e-manual` | Cria ou revisa identidade de marca: entrevista de voz, paleta, tipografia, logo, kit de marca (.md), manual (Paper/HTML), design system, papelaria e kit web. |
| `financeiro-tributario-brasil` | Finanças e tributos de empresa brasileira genérica, em três módulos: rotina (DRE, fluxo de caixa, fechamento, SOP), decisão (preço, viabilidade, orçamento, Presumido × Real) e tributário (regime, ICMS/ST/DIFAL, PIS/COFINS, reforma CBS/IBS/IS, NCM/CFOP/CST, parametrização de ERP). Substitui `financeiro-decisao` e `financeiro-rotina` (arquivadas em `../arquivados/financeiro-nov2026/`). |

## hermes/

Skills de autoria própria do Hermes. Não misturar com `skills/` (Claude). Skill de terceiro não entra.

| Skill | O que faz |
|---|---|
| `laya-triagem` | Classificador local Laya no Mac mini. Prefere caminho de arquivo e devolve só rótulo. |
| `laya-classificador-modelos` | Laya rotula a tarefa. Só pesquisa, leitura de documento e extração local viram provedor. O resto não. |
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

> Arquivadas em 05/11/2026 (em `Skills/arquivados/orquestracao-nov2026/`, fora do repo): `orquestracao-claude-code`, `orquestracao-worktree`, `orquestracao-multimodelo` (versão Hermes e o `.skill` da raiz) e `docs/orca-fluxo.md`.

## orca-workflow/

Kit de apoio: `README.md`, `PLAYBOOK.md`, `SETUP.md` e templates (ticket, `CLAUDE.md` de projeto,
bootstrap de repo). As skills de execução foram unificadas em `skills/orquestrador-orca`.

## docs/

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
