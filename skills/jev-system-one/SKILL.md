---
name: jev-system-one
description: "Use ao classificar, rotear, pontuar ou escolher entre opções fechadas com Jev/System One (TypeSafe): triagem de e-mail por gatilhos, detecção de golpe. Decisão tipada e consultiva; não usar para geração aberta, estratégia ou dados numéricos."
triggers: [jev, system one, typesafe, classificar, triagem, roteamento, gatilho de urgência]
idioma: pt-BR
versao: 2.0
author: Leonardo Mitsuo + Claude + Hermes Agent
license: Proprietary
metadata:
  hermes:
    tags: [jev, system-one, typesafe, classification, routing, scoring]
    related_skills: [hermes-agent, laya-triagem, orquestracao-hermes]
---

# Jev / System One — decisões tipadas

Skill única para Claude e Hermes. Unifica o contrato do Hermes (v1.0) com os testes reais de 30/09/2026 (`references/notas-testes.md`).

O Jev recebe um texto (`state`) e perguntas tipadas. Devolve escolha, probabilidades e confiança. É consultivo: filtra e roteia; não decide nem executa.

## 1. Política de dados (regra principal)

- Jev é serviço externo. Não enviar dado confidencial, PII, CRM, ERP ou e-mail real sem aprovação explícita do responsável (LGPD).
- **Texto público** (páginas de produto, anúncios, posts de marketplace) → pode ir ao Jev.
- **E-mail, CRM, ERP, dados internos** → classificador local (Laya/Ollama/MLX) com as mesmas regras desta skill. No Jev, só dado sintético ou anonimizado.
- Retenção de dados da TypeSafe não está documentada. Confirmar nos termos antes de produção.
- Enviar o mínimo necessário. Logar entrada sanitizada.

## 2. Quando usar

| Uso | Como | Evidência |
|---|---|---|
| Categoria de texto/e-mail | `choice` com 5–8 categorias descritas com exemplos do negócio | 53/55 corretos; erros com conf < 0,5 |
| Urgência | `choice` de **gatilhos concretos** + `nenhum`. Urgente = gatilho ≠ nenhum | 13/15 urgentes pegos (vs 7/15 abstrato) |
| Golpe/phishing | categoria `spam_golpe` ou gatilho `golpe_verificar` | 2/2, conf ≥ 0,82 |
| Roteamento por área | `choice` fechado | — piloto |

## 3. Não usar

- Escrita, pesquisa, explicação, planejamento, estratégia → Claude.
- Dados numéricos (priorizar cliente, lead por campos, valores, prazos) → fórmula determinística. Jev empatou com fórmula (Spearman 0,94) e errou abordagem 7/15.
- Urgência abstrata ("requer ação em 48h?") → falha (7/15).
- Decisão regulatória ou jurídica final → responsável humano. O modelo não conhece listas normativas.
- Página inteira de uma vez → frase ruim no meio passou. Quebrar em frases.
- Compra/venda, trade, preço, publicação, envio de mensagem, escrita em CRM/ERP → nunca automático.
- Vigilância de rede/incidente sem evidência verificável.

## 4. Contrato da decisão

Entrada: `task` (instrução), `options` (rótulos fechados com descrição), `context` (mínimo, sanitizado).

Saída real da API:
- `choice` → `choice`, `probabilities`, `confidence`
- `score` → `score` contínuo, `legend`, `probabilities`, `confidence`
- `noul` → `noul` 0–1, **sem confidence**

Ajustes ao contrato v1.0 (comprovados em teste):
- A API **não devolve justificativa**. Não exigir `reason_short`.
- O modelo **ignora** opção `abstain`/`incerto`. Abstenção = `confidence < 0,6`.
- Quando a decisão depende de confiança, usar `choice`, não `noul`.

Validar o schema localmente. Limiar, custo e qualquer ação ficam em regra determinística fora do modelo.

## 5. Regras de desenho

1. Concreto vence abstrato. Gatilho específico dobrou o recall de urgência.
2. A descrição de cada opção muda o resultado. Escrever com exemplos do negócio.
3. Contexto completo > trecho (Nibo: 0,18 → 0,80). Respeitar a política de dados.
4. `confidence < 0,6` → humano. Existe erro com confiança alta (webinar "É HOJE" → "agir hoje", 0,92; "reativação" 0,93 em conta pequena).
5. Palavras de tempo ("hoje", "últimas horas") enganam score/noul de urgência.
6. `score` não é calibrado entre prompts: só ordenar; nunca limiar fixo sem recalibrar.
7. Decisão final por regra sobre a categoria, não pelo score.
8. Quase determinístico (±0,02). Instrução em PT ou EN: indiferente.
9. Limiar ajustado num lote só vale depois de validado em outro lote.

## 6. Política de execução

- Baixa confiança → fila humana. Nunca inventar fallback.
- Categorias cliente, regulatório, interno, golpe → sempre humano/Claude.
- Execução externa (e-mail, WhatsApp, preço, publicação, trade, CRM/ERP) → só recomendação; exige regra explícita + aprovação humana.
- Impacto regulatório, financeiro alto ou jurídico → responsável humano valida.

### Roteamento recomendado (e-mail, via classificador local)

- newsletter/sistema com conf ≥ 0,8 → arquivar
- cliente, regulatório, interno, golpe → humano
- gatilho ≠ nenhum → alerta
- financeiro/fornecedor → fila diária
- conf < 0,6 → revisão

### Gatilhos de urgência validados

```python
"criteria": {
  "pedido_cliente_pendente": "A customer order, complaint, cancellation or contract change waiting for our response or invoicing",
  "prazo_hoje_ou_vencido": "A specific payment, tax or document deadline that is today or already passed (not a future due date)",
  "risco_regulatorio_operacional": "Health inspection, failed lab result, retained cargo, marketplace listing suspended, legal notice",
  "pedido_direto_equipe": "A colleague or family member/owner of the company directly asking to talk or act",
  "golpe_verificar": "Suspicious request to pay, change bank details or confirm passwords",
  "nenhum": "Informational, marketing, routine notification, future due date, or event/webinar invitation"}
```

## 7. Setup

**Claude (Cowork):**
- Chave em `~/Dev/typesafe/.env` → `TYPESAFE_API_KEY=`. Nunca no chat, nunca versionada.
- Conectar `~/Dev`; rodar via shell do Mac em `$HOME/mnt/Dev/typesafe`.
- Cliente `jev.py` (stdlib): `from jev import ask; ask(state, questions)`. Teste: `python3 jev.py --ping`.
- `POST https://api.typesafe.ai/v1/systemone`, `Authorization: Bearer`, `model: jev-latest` (testado jev-1.13.0).
- Paralelo `ThreadPoolExecutor(8)`: ~35 chamadas em ~3 s; ~700–900 tokens/chamada.

**Hermes:**
- Plugin comunitário `ourines/hermes-jev` (MIT, v0.1.2 prerelease, 2 estrelas) expõe `jev_evaluate` e `jev_route`. **Não instalado.**
- Antes de instalar: revisar código; ativar só backend TypeSafe (desligar Cloudflare/OpenRouter = menos egress); lembrar que o transcript do Hermes guarda argumentos.
- Não usar como gate automático de ferramentas sem desenho e teste próprios.
- Manifesto de referência: `hermes/jev-system-one/mcp/jev-system-one.mcp.json`.

## 8. Protocolo para testar um uso novo

1. 20+ casos; preferir sintéticos/anonimizados. Marcar fonte (REAL/SIM).
2. Gabarito registrado **antes** de rodar.
3. Rodar em paralelo; salvar `testes/resultadoN.json`.
4. Medir acerto, recall dos críticos, alarmes falsos, erros com confiança alta.
5. Validar limiar em outro lote.
6. Atualizar `references/notas-testes.md`.
7. Reportar: uso, resultado, veredito, limites (amostra, gabarito do próprio Claude, simulado mais fácil). Separar fato / hipótese / recomendação.

## 9. Referências

- `references/notas-testes.md` — resultados e números.
- `references/implementation-links.md` — plugin Hermes e notas IMP do Vault.
- Scripts e dados brutos: `~/Dev/typesafe/testes/`.
