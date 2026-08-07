# mit-skills

Skills, agentes e workflows de autoria própria para Claude (Cowork / Claude Code).
Repositório **privado** — contém material regulatório interno da empresa e critérios
pessoais de investimento.

> **Escopo:** só entra aqui o que foi escrito por mim. Skills de terceiros instaladas na
> conta (ui-ux-pro-max, gpt-taste, emil-design-eng, karpathy-guidelines, llm-council,
> pre-mortem, ckm*, ponytail*, apple-design, animate etc.) **não** fazem parte deste repo —
> redistribuí-las seria uso de obra alheia sem licença.

---

## skills/

Formato Claude Agent Skill (`SKILL.md` com frontmatter `name` + `description`).

| Skill | O que faz |
|---|---|
| `adequacao-anvisa-suplementos-importados` | Análise regulatória de suplementos para o mercado BR: enquadramento, constituintes autorizados, limites da IN 28, riscos de rotulagem, checklist de submissão. Foco em importados e private label. |
| `avaliacao-formula-suplementos-anvisa` | Avaliação de fórmula de suplemento contra os limites e constituintes permitidos pela ANVISA. |
| `conferencia-rotulos-anvisa` | Conferência de rótulos e embalagens de suplementos contra as normas vigentes. |
| `conferencia-marketing-anvisa-suplementos` | Revisão técnico-regulatória de peças de marketing (anúncios, carrosséis, PDPs, scripts) — classifica em conforme / ajuste recomendado / não conforme / depende de validação. |
| `analise-carteira-lendarios` | Auditoria de carteira e teses pelas lentes de Simons, Druckenmiller, Buffett, Lynch, Verde, Dynamo e Barsi. Score 0–10 por dimensão. Análise de processo, não recomendação. |
| `screener-lendarios` | Shortlist de ativos-candidatos aplicando os filtros quantitativos dos mesmos investidores. Todo número vem de busca feita na conversa, com data. |
| `produtividade-foco` | 7 prompts de função executiva: paralisia de tarefas, brain dump, body doubling, menu de dopamina, estimativa de tempo. |
| `markitdown-to-md` | Converte PDF/DOCX/PPTX/XLSX para Markdown via MarkItDown antes da leitura, para economizar contexto. Inclui `scripts/convert_to_md.py`. |

## agents/

Personas e orquestradores (mesmo formato de frontmatter, usados como subagentes).

- `comite-lendarios` — analista que audita decisões de investimento; par do `screener-lendarios`.
- `claude-orquestrador-empresa` — orquestrador lite: separa contexto fixo de variável e roteia tarefas.
- `empresa-loop-orchestrator` — orquestrador avançado com intake estruturado e loop de execução.
- `empresa/` — quadro de agentes da empresa: `ceo`, `cto`, `chief-of-staff`, `comercial-b2b`, `comercial-digital`, `criativos-publicidade`.

## orca-workflow/

Projeto autocontido de orquestração por tickets: `README.md`, `PLAYBOOK.md`, `SETUP.md`,
as skills `plan-tickets` e `orchestrate-tickets`, e os templates de ticket, `CLAUDE.md` de
projeto e bootstrap de repo.

## docs/

- `orca-fluxo.md` — desenho do fluxo Orca.
- `CLAUDE-exemplo.md` — `CLAUDE.md` de referência com o contexto da empresa.
- `deep-value-investing-graham-greenwald.md` — nota de referência (Graham / Greenwald).
- `manual-claude-metodo-completo.md` — manual completo do método de trabalho com Claude.
- `manual-claude-orchestrador-empresa.md` — manual de implementação do orquestrador empresa.

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

## Procedência e versões

As skills de ANVISA são a **v2.1 · Ago/2026**: frontmatter corrigido (só `name` e `description`,
que é o único campo que o Claude usa para disparar a skill) e base regulatória verificada
contra o AnvisaLegis. A versão instalada na conta Claude ainda é a v1 e **está defasada** —
reinstalar a partir daqui.

As demais (`analise-carteira-lendarios`, `screener-lendarios`, `produtividade-foco`,
`markitdown-to-md`) estão idênticas entre conta e vault.

## Aviso

As skills regulatórias reduzem erro operacional e padronizam triagem, mas **não substituem**
a leitura da norma vigente nem parecer jurídico-regulatório. As skills de investimento são
análise de processo — não são recomendação de compra ou venda.

## Base regulatória — verificada em ago/2026

- **IN 28/2018** — *vigente com alterações*. 12 alterações: IN 76/2020, 102/2021, 275/2024,
  284/2024, 304/2024, 318/2024, 336/2024, 373/2025, 418/2025, **431/2026**, **438/2026**,
  **450/2026**. Sempre usar o texto consolidado do AnvisaLegis.
- **IN 431/2026** — óleos, polifenóis de açaí e probióticos; novas alegações de vitaminas do complexo B e probióticos.
- **IN 438/2026** — cúrcuma: extrato e tetraidrocurcuminoides, associação simultânea proibida, limites e advertência obrigatória. Adequação em 6 meses (≈ out/2026).
- **RDC 990/2025** — altera o art. 32 da RDC 843/2024: notificação de suplementos e alimentos
  para controle de peso com comunicado anterior à RDC 843/2024 vai **até 1º/09/2026**.
