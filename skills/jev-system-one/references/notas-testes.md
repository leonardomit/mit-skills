# Jev (TypeSafe System One) — notas de teste
Última atualização: 2026-09-30 · Testes em `testes/` (rodar*.py, resultado*.json)

## O que é
Modelo de "decisão rápida" com saída estruturada. POST https://api.typesafe.ai/v1/systemone,
Bearer TYPESAFE_API_KEY, model "jev-latest" (testado: jev-1.13.0). Três tipos de pergunta:
- choice (criteria = {opção: descrição}) → choice, probabilities, confidence
- score (criteria = [nível0, nível1, ...]) → score contínuo, legend, confidence
- noul (sem criteria) → noul 0–1 (sem confidence)
Várias perguntas por chamada, avaliadas em paralelo sobre o mesmo "state".

## Números medidos
- Latência: 35 chamadas paralelas em ~2,6 s. ~700–900 tokens/chamada (3 perguntas).
- Determinismo: 5 execuções iguais variam ±0,02. Estável.
- PT vs EN nas instruções: sem diferença relevante.

## Resultados por uso (55 e-mails reais+simulados, 15 clientes CRM)
| Uso | Resultado | Veredito |
|---|---|---|
| Categoria de e-mail (choice) | 33/35 e 20/20; erros com conf < 0,5 | USAR |
| Urgência abstrata (noul "requer ação em 48h?") | pegou 7/15 urgentes | NÃO USAR |
| Urgência por gatilhos concretos (choice) | pegou 13/15, 4 alarmes falsos (defensáveis) | USAR |
| Nível de ação (score 0–3) | ordem ok, escala muda com o prompt | Só ranking, nunca faixa fixa |
| Priorizar clientes com dados numéricos | Spearman 0,94, mas fórmula faz igual | NÃO USAR (use fórmula) |
| Abordagem comercial (choice) | 8/15; nunca escolhe "baixa"; conf 0,93 errado | NÃO USAR |
| Golpe/phishing | 2/2 simulados, conf ≥0,82 | USAR |

## Regras aprendidas
1. Perguntas concretas > abstratas. Trocar "é urgente?" por choice de gatilhos específicos dobrou o recall.
2. Descrição dos critérios muda o resultado. Escrever cada opção com exemplos do negócio.
3. Contexto importa: corpo completo > snippet (Nibo: noul 0,18→0,80; gatilho correto 0,99).
4. Confidence baixa (<0,6) = mandar p/ humano. Mas há erros com conf alta (webinar "É HOJE" → agir hoje 0,92; abordagem "reativação" 0,93).
5. Palavras de tempo ("hoje", "últimas horas") enganam score/noul de urgência.
6. Score não é calibrado entre prompts: não usar limiares fixos; recalibrar a cada mudança.
7. Opção "incerto" no choice não é usada pelo modelo. Usar confidence.
8. Não conhece listas regulatórias normativas. Não usar como decisão regulatória.
9. Dados numéricos/tabelas: não agrega. Regra determinística é melhor e grátis.
10. Decisão final por regra de negócio sobre a categoria, não pelo score do Jev.

## Desenho recomendado (e-mail)
- newsletter/sistema com conf ≥0,8 → arquivar
- cliente, regulatório, interno, golpe → sempre humano
- gatilho != nenhum → alerta
- financeiro/fornecedor → fila diária; conf <0,6 → revisão
