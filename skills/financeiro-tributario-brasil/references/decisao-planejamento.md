# Planejamento Financeiro e Cenários

## Princípio: orçamento por direcionador, não por percentual

O método mais comum é também o pior: pegar o realizado do ano anterior e aplicar um percentual de crescimento. Isso perpetua ineficiência e não permite diagnóstico quando o número não bate.

Método correto: cada linha é derivada de um **direcionador físico ou contratual**.

| Linha | Direcionador | Não use |
|---|---|---|
| Receita | Volume × preço médio, por canal e por família de produto | "+15% sobre o ano passado" |
| CPV | Consumo por unidade × custo de insumo × volume | "% da receita" |
| Comissão | Política vigente × receita por canal | Histórico agregado |
| Folha | Headcount × salário médio × encargos, mês a mês | "+ dissídio sobre a folha atual" |
| Frete | Custo por pedido × número de pedidos | "% da receita" |
| Marketing | Meta de aquisição ÷ eficiência de canal | "% da receita" |
| Fixas | Contrato a contrato, com data de reajuste | Média do ano anterior |

A vantagem prática: quando a receita fica 10% abaixo, o modelo por direcionador mostra se foi volume ou preço, e em qual canal. O modelo por percentual só mostra que errou.

## Reajustes contratuais

Em ambiente inflacionário, contratos reajustam em datas diferentes por índices diferentes. Modelar tudo com um índice único e data única distorce o resultado por trimestre.

Mapeie por contrato: índice (IPCA, IGP-M, INPC), mês-base do reajuste, e periodicidade. Aluguel, seguro, software, plano de saúde e contratos de serviço costumam ter datas espalhadas.

Confirme os índices projetados em fonte corrente — expectativa de mercado muda ao longo do ano. Quando houver acesso a busca, verifique; quando não houver, marque como ⚠️.

## Cenários

Três cenários, com premissas explícitas e distintas. O erro comum é variar só a receita e manter tudo mais constante — isso não é cenário, é sensibilidade de uma variável.

| Cenário | Construção |
|---|---|
| Conservador | Volume abaixo do histórico, preço sob pressão, custo de insumo em alta, prazo de recebimento alongando |
| Base | Direcionadores conforme evidência atual (pipeline, contratos, histórico recente) |
| Otimista | Volume com crescimento lastreado, mix melhorando, ganho de escala em compras |

Regras que fazem cenário ser útil:

1. **Cada cenário precisa de gatilho observável.** "Cenário conservador se ocorrer X" — onde X é algo que a empresa consegue detectar em tempo real. Cenário sem gatilho é exercício de imaginação.
2. **Variáveis correlacionadas se movem juntas.** Volume caindo geralmente vem com pressão de preço e com estoque subindo. Modelar volume baixo com preço cheio produz cenário conservador que não é conservador.
3. **O conservador precisa ser desconfortável.** Se o cenário pessimista ainda dá lucro confortável, ele está mal calibrado. Teste: qual cenário quebra a empresa? Esse é o que importa conhecer.

## O que todo plano precisa conter e quase nunca contém

**Necessidade de capital de giro.** Crescimento consome caixa antes de gerar. Plano de crescimento sem projeção de NCG é o erro que mais mata empresa lucrativa.

```
ΔNCG = (Ciclo financeiro em dias ÷ 360) × Δ Receita
```

Se o plano prevê crescer receita em R$ 2 milhões com ciclo financeiro de 90 dias, o caixa precisa absorver R$ 500 mil de capital de giro adicional. Isso precisa estar no plano, com a fonte de financiamento identificada.

**Ponto de equilíbrio do plano.** Qual faturamento mensal cobre a estrutura planejada. Se o plano adiciona custo fixo, o ponto de equilíbrio sobe — e o mês em que ele sobe precisa estar marcado.

**Calendário de desembolso, não só de competência.** Investimento aprovado em janeiro com pagamento em três parcelas tem efeito de caixa diferente do efeito de resultado.

## Metas e desdobramento

Meta agregada anual não gera ação. Desdobre:

1. **Por período** — respeitando sazonalidade, não dividindo por 12
2. **Por canal** — B2B e B2C têm dinâmica e ciclo de venda distintos
3. **Por responsável** — cargo ou setor, com uma métrica que a pessoa controla

Regra do desdobramento: a métrica atribuída precisa estar sob controle de quem a recebe. Atribuir meta de margem a quem não controla preço nem custo produz frustração, não resultado.

## Acompanhamento

Plano sem ciclo de revisão vira documento morto em 60 dias.

| Frequência | O que revisar |
|---|---|
| Mensal | Realizado versus plano por direcionador; identificar desvio de volume versus preço |
| Trimestral | Recalibrar premissas com evidência nova; decidir se o cenário mudou |
| Anual | Reconstruir o plano |

Regra de revisão: **desvio acima de 10% em qualquer direcionador principal exige explicação documentada e decisão** — manter o plano, ajustar a execução, ou revisar a premissa. Desvio sem decisão é o mecanismo pelo qual planos se tornam ficção.

## Estrutura de saída

```
## Conclusão
[O que o plano exige e onde ele é frágil. Primeira frase.]

## Direcionadores
[Tabela: linha × direcionador × premissa × origem da premissa]

## Cenários
[Tabela comparativa com resultado, caixa e NCG em cada cenário]

## Gatilhos
[Qual evento observável indica mudança de cenário]

## Necessidade de capital
[NCG adicional e fonte de financiamento]

## Onde isso falha
[Qual premissa, se errada, inviabiliza o plano]

## Próxima ação
```

## Sinais de alerta a reportar sempre

- Orçamento construído por percentual sobre o ano anterior
- Crescimento de receita planejado sem NCG correspondente
- Cenário conservador que ainda apresenta resultado confortável
- Meta desdobrada para responsável que não controla a variável
- Premissa de preço acima da inflação sem justificativa de valor ou diferenciação
- Custo fixo crescendo em proporção maior que a receita planejada
- Plano sem gatilho de revisão definido
- Índices de reajuste assumidos sem verificação de projeção corrente
