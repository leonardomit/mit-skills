---
name: orquestracao-hermes
description: Roteamento multimodelo para automações no Hermes: modelo local (Ollama/MLX) para volume, API para julgamento, fila de exceções para humano, e quando entregar a tarefa ao Claude Code. Usar ao desenhar ou ajustar fluxos e agentes do Hermes.
---

# Orquestração no Hermes

Hermes roda em produção, sem humano olhando. Por isso a regra muda: **nada de alto impacto termina no Hermes**. Ele classifica, processa volume, prepara e enfileira. Julgamento vai para API; código vai para o Claude Code; decisão vai para a fila de exceções.

## Classes → provedor

| Classe | Provedor no Hermes | Uso |
|---|---|---|
| `ECONOMY` | Ollama/MLX local (Qwen3-30B-A3B) | classificar, extrair, resumir, rotear, formatar |
| `STANDARD` | API Sonnet (ou equivalente configurado) | síntese, resposta a cliente em rascunho, validação de amostra |
| `PREMIUM` | API Opus | só revisão de exceção com impact = 2; nunca executor |
| `CODE_AGENT` | **fora do Hermes** | abrir tarefa para Claude Code (Notion/Linear) com pacote de contexto |
| `RESEARCH` | Perplexity em cadência fixa; SuperGrok para sentimento | nunca em tempo real dentro de fluxo crítico |
| `HUMAN_GATE` | fila de exceções (Notion) + notificação | tudo com impact = 3 ou ação externa |

Mantenha o provedor da tabela. Se o modelo nomeado não existir nesta máquina, use o fallback da mesma classe. Runtime local caiu: o fluxo para e enfileira. Não migra para API por queda. O fallback local abaixo é troca de tag instalada, não é API.

| Classe | Fallback nesta máquina |
|---|---|
| `ECONOMY` | `qwen3.5:9b`. Extração curta: `qwen3.5:2b`. Qwen3-30B-A3B não está instalado. Arquivo longo: Laya. Não suba `qwen3.6:27b` em 16 GB. |
| `STANDARD` | `claude-sonnet-5`, se a API Sonnet nomeada não existir. |
| `PREMIUM` | `claude-opus-5-5`. Se recusar, `claude-opus-5`. Continua só revisão de exceção, nunca executor. |
| `RESEARCH` | `grok-4.7`, se Perplexity ou SuperGrok não estiverem nesta máquina. |

Modelo local caiu: o fluxo para e enfileira. Não migra silenciosamente para API.

## Classificação por fluxo (feita uma vez, no desenho)

Cada fluxo do Hermes recebe classificação fixa, não por item:

```yaml
flow: <nome>
impact: 0-3          # financeiro, ANVISA/LGPD, cliente, ERP produtivo
ambiguity: 0-3
volume: 0-3
external_change: bool   # escreve em ERP/Bling/Reportana, envia mensagem
sensitive_data_export: bool
autonomy_max: 0-3       # Hermes nunca opera em nível 4
```

Regra de desenho:
- `impact <= 1` e `ambiguity <= 1` → ECONOMY executa, validação por schema, amostra de 2–5% para STANDARD.
- `impact = 2` → ECONOMY prepara, STANDARD decide, log obrigatório. Ação externa só se `external_change` estiver aprovado no desenho do fluxo.
- `impact = 3` → Hermes só coleta e enfileira. Humano decide.
- `ambiguity >= 2` em qualquer impacto → fila de exceções.

## Pipeline por item

```text
intake → ECONOMY classifica (JSON com schema rígido)
      → validação determinística (schema, faixas, duplicidade, idempotência)
      → passou?  sim: executa no nível autorizado pelo fluxo
                 não: 1 retry local com o erro anexado
      → falhou de novo ou fora de faixa → fila de exceções com contexto completo
      → log: flow, item_id, modelo, tentativas, resultado, motivo
```

Sem segunda escala automática dentro do Hermes. Segunda falha = humano ou Claude Code.

## Contrato de saída do ECONOMY

```json
{"item_id":"","class":"","fields":{},"out_of_range":[],
 "needs_human":false,"reason":""}
```

Sem campo de confiança. Modelo local não se autoavalia; a validação determinística decide.

## Handoff para Claude Code

Quando o fluxo precisa de código, correção de integração ou análise de incidente, Hermes cria um item com:

```md
Título: [flow] — [problema]
Evidência: logs resumidos por ECONOMY (max 300 tokens), item_ids afetados, horário
Hipótese: [ou "nenhuma"]
Impacto: [0-3] · Ação externa envolvida: sim/não
Contexto: endpoints, contratos, últimas mudanças
```

Hermes não edita código nem config em produção. Nem por retry.

## Fila de exceções

Vai para a fila: dado ausente ou contraditório, valor fora de faixa, divergência entre ERP/Bling/Reportana, regra de negócio não documentada, ação irreversível, segunda falha, suspeita de problema ANVISA/LGPD.

Cada item da fila traz: o que foi feito, o que está bloqueado, opções (máximo três), recomendação do STANDARD se impact <= 2.

## Gate humano (lista fechada)

Envio externo a cliente (WhatsApp, e-mail), escrita em pedido/preço/estoque/NF, pagamento ou cobrança, exportação ou exclusão de dados pessoais, alteração de credenciais, qualquer decisão regulatória. Leitura e classificação interna não exigem gate.

## Custo e contexto

- Local é grátis mas lento: limite prompts a 2k tokens de entrada e JSON curto na saída.
- API só recebe o pacote montado pelo local: item + campos + motivo. Nunca o histórico do fluxo.
- Métricas por fluxo: taxa de exceção, taxa de retry, custo API/dia, itens por hora. Exceção acima de 10% = fluxo mal classificado ou prompt fraco; revisar o desenho, não subir o modelo.

## Checklist ao criar ou alterar um fluxo

- Classificação e `autonomy_max` declarados no YAML?
- Schema de saída e validação determinística definidos?
- Idempotência garantida (item_id, dedup)?
- Integração começa em modo leitura?
- Fila de exceções conectada e notificação ativa?
- Log com modelo, tentativas e motivo?
- Hermes não toca código, credencial ou ação de impact 3?
