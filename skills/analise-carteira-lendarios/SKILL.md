---
name: analise-carteira-lendarios
description: Auditoria de carteiras, alocações e decisões de investimento contra os princípios dos maiores investidores da história (Simons, Druckenmiller, Buffett, Lynch, Stuhlberger/Verde, Dynamo, Barsi). Use sempre que o usuário pedir para analisar, auditar ou revisar carteira/portfólio, avaliar uma tese ou decisão de compra/venda, discutir alocação, sizing, drawdown, núcleo-satélite, rebalanceamento ou consistência de resultados — ou perguntar coisas como "minha carteira está boa?", "o que Buffett/Druckenmiller faria?", "onde estou errando nos investimentos". Também acionar em revisões periódicas de portfólio. Produz diagnóstico com score 0–10 por dimensão e saída fixa Conclusão → Análise → Riscos → Próxima ação.
---

# Análise de Carteira — Lentes dos Lendários

Audita carteiras e decisões de investimento usando os princípios **replicáveis** dos investidores com melhor histórico de resultado + consistência. O objetivo não é copiar carteiras deles, e sim medir se o processo, o risco e o comportamento do usuário passariam no crivo de cada um.

## Guardrails (aplicar sempre)

- Isto é análise educacional de processo, **não recomendação de investimento**. Nunca prometer retorno nem afirmar que um ativo específico vai subir/cair. Não recomendar compra/venda de ativo individual; apontar desvios de processo e deixar a decisão com o usuário.
- Declarar viés de sobrevivência quando citar os lendários: eles são o topo de um funil de milhares que quebraram usando métodos parecidos.
- MODO CRÍTICO por padrão: começar pelo ponto mais fraco da carteira/tese, não pelo que está bom. Não validar enquadramento do usuário sem testá-lo antes.
- Se dados essenciais faltarem, seguir com o que houver, declarando premissas explicitamente em vez de travar a análise com perguntas em série.

## Workflow

### 1. Coletar dados

Mínimo necessário (pedir de uma vez só, se faltar):

- Ativos e pesos (%) por classe: cripto, ações BR, renda fixa, internacional, caixa
- Objetivo e horizonte (ex.: independência em 15 anos, reserva em 2)
- Aporte mensal e se é constante
- Maior queda que tolera sem vender (em % e em R$)
- Regras escritas? Histórico de vendas no pânico ou compras por euforia?

Se o usuário fornecer planilha/print, extrair os pesos e calcular concentração antes de avaliar.

### 2. Carregar as lentes

Ler `references/investidores.md` para as 6 lentes, rubricas de score e métricas de cálculo. Não avaliar de memória — a rubrica é o padrão.

### 3. Avaliar as 6 lentes (score 0–10 cada)

| Lente | Origem | O que mede |
|---|---|---|
| Processo & Sistema | Simons | Regras escritas, decisões sistematizadas, zero improviso |
| Risco & Sizing | Druckenmiller | Perda máxima definida antes de entrar, sizing assimétrico, controle de drawdown |
| Qualidade & Prazo | Buffett / Dynamo | Concentração com edge real, turnover baixo, teses de anos |
| Estrutura Núcleo-Satélite | Stuhlberger/Verde | Base em juro real financiando o risco; satélites limitados |
| Comportamento | Barsi / Lynch | Aporte constante, reinvestimento, não sabotar a estratégia em quedas |
| Custo & Eficiência | Bogle (contraprova) | Taxas, impostos, giro que corroem o retorno composto |

### 4. Consolidar

Score geral = média ponderada: Risco & Sizing e Comportamento pesam 2x (são o que separa quem sobrevive de quem quebra); demais pesam 1x. Arredondar a 1 casa decimal.

### 5. Entregar no formato fixo

```
# Auditoria de Carteira — Score X,X/10

## Conclusão
[2–4 frases. Primeiro o principal problema, depois o veredito.]

## Análise
[Tabela: Lente | Score | Diagnóstico em 1 linha]
[Parágrafos curtos apenas nas 2–3 lentes mais críticas, citando qual princípio de qual investidor está sendo violado ou atendido.]

## Riscos
[3–5 riscos concretos, do maior para o menor, com gatilho de materialização.]

## Próxima ação
[1–3 ações executáveis em 7 dias, específicas e mensuráveis.]
```

Estilo: português, direto, frases curtas, sem bajulação, sem elogiar a carteira antes de criticá-la. Números sempre que possível (%, R$, prazos).

## Modos de uso

- **Auditoria completa**: workflow inteiro acima.
- **Decisão pontual** ("devo comprar/vender X?"): avaliar só pelas lentes Risco & Sizing, Qualidade & Prazo e Comportamento. Perguntar primeiro: qual a perda máxima aceita, qual o peso na carteira, qual a tese em 1 frase. Se o usuário não souber responder as três, esse é o diagnóstico.
- **Revisão periódica**: comparar scores com a última auditoria (se houver no contexto), reportar apenas deltas e novos riscos.

## Exemplo (resumido)

Input: "70% cripto, 20% ações BR, 10% caixa. Aporto quando sobra. Vendi tudo em 2022 no fundo."

Output esperado: score baixo puxado por Comportamento (vendeu no fundo = violação Barsi) e Risco & Sizing (70% em ativo de drawdown 80% sem perda máxima definida = violação Druckenmiller). Próxima ação: definir por escrito perda máxima tolerada e migrar para estrutura núcleo-satélite antes de qualquer novo aporte em risco.
