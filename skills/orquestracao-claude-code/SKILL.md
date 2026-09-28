---
name: orquestracao-claude-code
description: Roteamento multimodelo dentro do Claude Code/Cowork: quando delegar a subagentes Haiku/Sonnet/Opus, como separar executor e revisor, e quando parar para aprovação humana. Usar ao planejar tarefas com mais de uma etapa ou ao delegar.
---

# Orquestração no Claude Code

A sessão principal é o **router e o gate**. Ela classifica, delega via `Agent`, valida e decide. Não executa trabalho de volume nem revisa o que ela mesma produziu.

## Classes → mecanismo

| Classe | Como acionar | Uso |
|---|---|---|
| `ECONOMY` | `Agent(model: "haiku")` | classificar, extrair, resumir, localizar arquivos, montar pacote de contexto |
| `STANDARD` | `Agent(model: "sonnet")` | planejar, documentar, implementar tarefa isolada, revisar amostra |
| `PREMIUM` | `Agent(model: "opus")` ou a própria sessão | arquitetura, segurança, decisão de alto impacto, gate |
| `CODE_AGENT` | `Agent(subagent_type: "general-purpose", isolation: "worktree")` | qualquer mudança em repositório |
| `RESEARCH` | `Agent` com WebSearch/WebFetch; MCP Perplexity quando citações forem obrigatórias | fatos atuais, docs de API, normas |
| `HUMAN_GATE` | `AskUserQuestion` | lista fechada abaixo |

Mantenha o modelo da tabela. Se o alias (`haiku`, `sonnet`, `opus`) não existir nesta máquina, use o id de fallback da mesma classe.

| Classe | Fallback nesta máquina |
|---|---|
| `ECONOMY` | `claude-haiku-4-5-20251001`. Volume local: `qwen3.5:9b`; extração curta `qwen3.5:2b`. |
| `STANDARD` | `claude-sonnet-5`. Código: `gpt-6-sol`. Tarefa direta: `gpt-5.6-terra` ou `gpt-6-luna`. |
| `PREMIUM` | `claude-opus-5-5` (alias `opus-5-5`). Se recusar, `claude-opus-5`. Plano longo: `claude-fable-5-1`. |
| `CODE_AGENT` | `gpt-6-sol` no Codex. Complexo: `claude-opus-5-5`. Diff pequeno: `gpt-6-luna`. |
| `RESEARCH` | `grok-4.7`. Cota do Grok acabou: Gemini, só autenticado; senão o Claude da sessão. |

Subagentes não herdam o contexto da sessão. Isso é desejado: passe só requisito + pacote de contexto.

## Classificação (0–3)

`impact` (financeiro, ANVISA/LGPD, clientes, produção) · `complexity` · `ambiguity` · `volume` · flags `external_change`, `needs_code`, `needs_research`, `sensitive_data_export`.

Classifique em uma linha antes de delegar. Exemplo: `impact 2, complexity 2, ambiguity 1, volume 0, needs_code` → pipeline abaixo.

## Pipeline

```text
1. RESEARCH             se needs_research (antes de planejar)
2. PLAN                 STANDARD se complexity/ambiguity >= 2 ou impact = 2
                        PREMIUM se impact = 3 ou complexity/ambiguity = 3
3. EXEC                 CODE_AGENT se needs_code; senão classe do passo 2 (ECONOMY se nada disparou)
4. VALIDATE             objetivo: testes, lint, schema, reconciliação, checagem ANVISA
5. REVIEW               Agent novo, modelo >= executor, recebe só requisito + diff/entrega
                        ECONOMY em volume: STANDARD revisa amostra
6. GATE:PREMIUM         se impact >= 2
7. GATE:HUMAN           se external_change, sensitive_data_export ou impact = 3
8. LOG                  modelo, tentativas, resultado, motivo de escalonamento
```

Complexidade e impacto decidem antes de volume. Volume alto nunca rebaixa a classe; só permite ECONOMY nos itens repetidos com amostragem.

Várias tarefas independentes: dispare os `Agent` em paralelo na mesma mensagem. Mais de ~5 agentes ou etapas encadeadas com verificação: use `Workflow` (pipeline review → verify), só quando o usuário autorizar.

## Prompt para executor (Agent)

```md
Tarefa isolada. Escopo: [arquivos/sistemas]. Fora do escopo: [lista].
Critérios de aceite: [mensuráveis].
Regras: menor mudança possível; rode as validações e reporte resultados reais;
sem push, merge, deploy, envio externo ou uso de segredos; regra de negócio ambígua = pare e descreva.
Entregue: resumo, arquivos alterados, comandos executados com saída, critérios atendidos/pendentes, riscos.
```

## Prompt para revisor (Agent novo)

```md
Revisor adversarial. Não reimplemente, não elogie.
Compare requisito e entrega. Reporte só problemas concretos: erro funcional,
perda/duplicação de dados, segurança, critério de aceite não atendido, teste ausente, risco ANVISA/LGPD.
Por achado: severidade, local, cenário, correção mínima.
Sem achados: "Nenhum problema concreto encontrado" + o que não pôde validar.
```

## Escalonamento

- Falha 1: mesmo agente corrige com a evidência da falha.
- Falha 2: novo `Agent` uma classe acima. Nunca terceira tentativa igual.
- Regra de negócio ausente: parar e perguntar. Não inventar.
- Impacto 3, segurança ou arquitetura: PREMIUM + HUMAN_GATE.

## Gate humano (lista fechada)

Deploy, merge em produção, migração de banco; envio externo (e-mail, WhatsApp, publicação, anúncio); dinheiro, preço, estoque, pedido, contrato; **exportação/exclusão/compartilhamento** de dados pessoais (leitura interna de e-mail, CRM e leads não exige gate); permissões e segredos; exclusão de arquivos ou infra; decisão legal, fiscal ou regulatória.

## Contexto e custo

1. Haiku localiza e resume antes de qualquer chamada a Opus.
2. Pacote de contexto = requisito + trechos relevantes + logs + decisões. Nada além.
3. Peça saída no formato da tarefa: JSON, diff, achados, checklist.
4. Registre ao final: `task, modelo, tentativas, validação, escalonamento`.

## Checklist antes de delegar

- Classificação em uma linha feita?
- Escopo e fora-de-escopo definidos?
- Modelo é o mais barato adequado ao impacto?
- Critério de aceite e validação objetiva no prompt?
- Revisor será `Agent` novo?
- Ação externa bloqueada até `AskUserQuestion`?
