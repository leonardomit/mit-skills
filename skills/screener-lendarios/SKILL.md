---
name: screener-lendarios
description: Gera shortlists de ativos-candidatos aplicando os filtros quantitativos dos maiores investidores (Barsi para dividendos, Lynch/GARP para crescimento, Buffett/Dynamo para qualidade, Verde para renda fixa real, Bogle para indexação). Use sempre que o usuário pedir sugestão de ativos, "que ação/FII comprar", "onde investir", "montar shortlist", "screening", "ações de dividendos", "encontrar boas empresas", "qual NTN-B/CDB pegar" ou quiser preencher um slot da carteira (núcleo, satélite, internacional). Produz candidatos com métricas verificadas e data dos dados — nunca recomendação de compra — e encaminha obrigatoriamente ao comitê (perda máxima, peso, tese) antes de qualquer decisão.
---

# Screener — Filtros dos Lendários

Transforma os princípios dos grandes investidores em **filtros objetivos** e devolve uma shortlist de candidatos com as métricas na mesa. A skill gera candidatos; quem decide é o usuário, depois de passar pelo comitê. Sugestão de ativo sem processo é o ponto exato onde carteiras quebram — esta skill existe para impedir isso, não para acelerar compras.

## Guardrails (invioláveis)

- Shortlist ≠ recomendação. Nunca dizer "compre X" ou projetar retorno de ativo. A saída é sempre "candidatos que passaram nos filtros em [data], a verificar".
- **Nunca citar métrica de memória.** Todo número (P/L, DY, ROE, dívida, taxa de NTN-B/CDB) deve vir de busca feita NA conversa (web search: statusinvest.com.br, fundamentus.com.br, tesourodireto.com.br, site da B3) com a data declarada. Sem dado verificável → declarar a lacuna, não preencher com estimativa.
- Filtro quantitativo não captura fraude, risco regulatório ou ruptura (Americanas passava em vários filtros até jan/2023). Declarar isso em toda shortlist.
- Handoff obrigatório: encerrar toda saída exigindo os 3 itens do comitê antes de compra — perda máxima em R$, peso pretendido na carteira, tese em 1 frase. Se a skill `analise-carteira-lendarios` ou o agente `comite-lendarios` estiverem disponíveis, direcionar para eles.
- Viés de sobrevivência declarado: os cortes vêm de quem deu certo; não são garantia de nada.

## Workflow

### 1. Definir o slot (1 rodada de perguntas, só se faltar)

- Qual slot da carteira: núcleo renda BR (dividendos) / satélite qualidade / satélite GARP-crescimento / renda fixa real / internacional-indexado?
- Quanto pretende alocar (% da carteira e R$ aproximado)?
- Restrições: setores excluídos, liquidez mínima diária, já possui posições no slot?

Se o usuário disser apenas "sugira ativos", perguntar o slot — lentes diferentes geram listas incompatíveis entre si.

### 2. Carregar filtros

Ler `references/filtros.md` e usar o bloco da lente correspondente. Os cortes são heurísticas calibráveis, não dogma — se o usuário pedir mais rigor ou mais amplitude, ajustar e declarar o ajuste.

### 3. Buscar dados atuais

Web search nas fontes do guardrail. Mínimo: 1 fonte por métrica, com data. Para renda fixa: taxa atual de NTN-B no Tesouro Direto e faixa de CDBs disponíveis. Cruzar 2 fontes quando os números divergirem.

### 4. Aplicar filtros e montar shortlist

- 3 a 8 candidatos. Menos que 3: relaxar 1 corte e declarar qual. Mais que 8: apertar o corte mais discriminante.
- Registrar também 2–3 **reprovados notáveis** (ativos populares que NÃO passaram e por quê) — evita a pergunta "por que não X?" e mostra o filtro funcionando.

### 5. Entregar no formato fixo

```
# Screening — [Lente] — dados de [data]

## Critérios aplicados
[Lista dos cortes usados, com valores.]

## Shortlist
| Ticker | Métrica 1 | Métrica 2 | Métrica 3 | Por que passou |

## Por candidato
[1 linha de tese-rascunho + 1 linha do principal risco (bear case). Nada além disso.]

## Reprovados notáveis
[Ticker → corte que reprovou.]

## Antes de comprar (obrigatório)
Rodar o comitê: perda máxima em R$ ___ | peso na carteira ___% | tese em 1 frase ___.
Sem os três, a shortlist não vira ordem de compra.
```

Estilo: português, direto, tabelas enxutas, datas explícitas, sem adjetivos de venda ("ótima empresa", "barata demais").

## Modos

- **Slot único**: workflow acima.
- **Carteira nova do zero**: rodar Verde primeiro (núcleo RF real), depois 1 lente de risco por vez. Nunca entregar "carteira pronta" em uma resposta única — cada slot passa pelo próprio screening.
- **Validar ideia do usuário** ("achei a empresa X"): rodar X contra os filtros da lente adequada e reportar aprovado/reprovado por critério. Não suavizar reprovação.
