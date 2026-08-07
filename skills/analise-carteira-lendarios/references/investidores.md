# Referência — Investidores, Rubricas e Métricas

## 1. Perfis (resumo operacional)

| Investidor | Método | Métrica-chave | Replicável | Red flag que ele condenaria |
|---|---|---|---|---|
| Jim Simons (Renaissance) | Quant sistemático, milhares de sinais, zero opinião | Sharpe >2; ~39% a.a. líquido, 30 anos sem ano negativo | Só o princípio: regras escritas, execução sem emoção | Decisão de investimento por intuição/notícia do dia |
| Stanley Druckenmiller | Macro discricionário, poucas apostas grandes com convicção | 30 anos sem ano negativo; drawdown controlado | Sizing assimétrico + corte rápido de perda | Posição grande sem perda máxima definida; operar por tédio |
| Warren Buffett | Qualidade a preço justo, moats, holding de décadas | 19,9% a.a. por 60 anos; turnover baixíssimo | Filosofia sim; float/alavancagem barata não | Girar carteira; comprar negócio que não entende |
| Peter Lynch | GARP, PEG < 1, investir no que conhece | 29% a.a. 1977–90; investidor médio do fundo perdeu dinheiro | Filtro PEG e círculo de competência | Entrar/sair pelo humor do mercado (erro dos cotistas dele) |
| Luis Stuhlberger (Verde) | Núcleo em juro real BR + satélites de risco hedgeados | ~100x desde 1997 batendo CDI | Sim: estrutura núcleo-satélite é montável por PF | Carteira 100% risco sem base de juro real num país de CDI alto |
| Dynamo (Cougar) | Ações fundamentalistas, 10–15 empresas, prazo de anos | Melhor track record de ações do BR desde 1993 | A lógica, se houver capacidade real de análise | Concentração sem pesquisa = concentração sem edge |
| Luiz Barsi | Dividendos em setores perenes, reinveste tudo, nunca vende | 50+ anos de aporte e reinvestimento | O mais replicável; exige décadas de disciplina | Vender no pânico; interromper aportes; gastar dividendos cedo |
| Contraprova — John Bogle | Indexação passiva de custo mínimo | Custo total <0,3% a.a. | Totalmente | Pagar 2/20 ou girar carteira sem edge comprovado |

## 2. Rubricas por lente (0–10)

Atribuir o score pela faixa cuja descrição melhor se encaixa. Na dúvida entre duas faixas, usar a menor.

### Processo & Sistema (Simons)
- **0–3**: nenhuma regra escrita; compra/venda por notícia, dica ou impulso.
- **4–6**: critérios informais na cabeça; aplica às vezes; sem registro de decisões.
- **7–8**: política de investimento escrita (alocação-alvo, critérios de entrada/saída, rebalanceamento com gatilho); segue na maioria das vezes.
- **9–10**: política escrita + registro de cada decisão com tese e revisão periódica; desvios exigem justificativa escrita antes de executar.

### Risco & Sizing (Druckenmiller)
- **0–3**: não sabe quanto pode perder; posições dimensionadas pelo "quanto tinha na conta".
- **4–6**: noção vaga de risco; algumas posições com stop/limite, outras não.
- **7–8**: perda máxima por posição e por carteira definida antes de entrar; nenhuma posição capaz de causar dano irreversível.
- **9–10**: além do anterior, sizing assimétrico consciente (maior onde a relação risco/retorno é comprovadamente melhor) e drawdown máximo de carteira monitorado.

### Qualidade & Prazo (Buffett/Dynamo)
- **0–3**: não sabe explicar por que tem cada ativo; giro alto; troca posição a cada trimestre.
- **4–6**: conhece os ativos superficialmente; algumas teses, prazo indefinido.
- **7–8**: tese escrita de 1 parágrafo por posição relevante; horizonte de anos; turnover baixo.
- **9–10**: círculo de competência definido; só entra no que consegue avaliar; teses revisadas por fatos, não por preço.

### Estrutura Núcleo-Satélite (Verde)
- **0–3**: carteira inteira em risco (cripto/ações/temas) sem base de juro real ou caixa estratégico.
- **4–6**: tem renda fixa, mas por sobra, sem função definida na estrutura.
- **7–8**: núcleo consciente em juro real/indexado (tipicamente 50–80% conforme perfil) financiando satélites de risco limitados.
- **9–10**: núcleo + satélites com tamanho máximo definido por satélite, rebalanceamento com regra e uso deliberado do juro real BR como motor de base.

### Comportamento (Barsi/Lynch)
- **0–3**: já vendeu no fundo ou comprou por euforia mais de uma vez; aportes irregulares.
- **4–6**: aporta quando sobra; hesita em quedas; acompanha cotação diariamente com ansiedade.
- **7–8**: aporte mensal automático/constante; atravessou pelo menos uma queda ≥20% sem vender.
- **9–10**: aporta mais em quedas conforme regra pré-definida; reinveste proventos; histórico comprovado de manter estratégia em bear market.

### Custo & Eficiência (Bogle)
- **0–3**: não sabe quanto paga de taxas; fundos caros sem edge; giro gera imposto desnecessário.
- **4–6**: conhece parte dos custos; alguma otimização.
- **7–8**: custo total da carteira mapeado e <1% a.a.; usa isenções e eficiência tributária básica (ex.: vendas ≤R$20k/mês em ações BR, come-cotas considerado).
- **9–10**: custo <0,5% a.a. onde não há edge comprovado; estrutura tributária planejada por classe (previdência/offshore/holding quando fizer sentido, sem afirmar benefício sem verificar).

## 3. Métricas a calcular quando houver dados

- **Concentração**: peso do maior ativo e dos top-5. Alerta se 1 ativo >20% sem tese escrita, ou top-5 >70% sem edge declarado.
- **Drawdown implícito**: estimar queda da carteira num cenário de estresse (cripto −70%, ações BR −45%, RF pré marcada −10%, dólar +30% no internacional). Comparar com a tolerância declarada em R$. Se drawdown estimado > tolerância → problema central da auditoria.
- **% núcleo vs satélite**: classificar cada ativo; reportar a razão.
- **Custo total estimado**: somar taxas de adm/perf/corretagem/spread conhecidas.
- **Regra de aporte**: existe? é anticíclica, neutra ou pró-cíclica?
- Se houver histórico: CAGR da carteira vs CDI e vs benchmark declarado, no mesmo período. Nunca comparar períodos diferentes.

## 4. Perguntas de diagnóstico comportamental

Usar quando o usuário não fornecer histórico:

1. O que você fez em quedas fortes anteriores (2020, 2022)? Vendeu, segurou ou comprou?
2. Qual perda em R$ faria você abandonar a estratégia?
3. Você consegue escrever a tese de cada posição relevante em 1 frase? (pedir 2 exemplos)
4. Com que frequência olha a carteira e com que frequência mexe nela?
5. Seu aporte é automático ou depende de "sobrar"?

## 5. Anti-padrões que invalidam a comparação com os lendários

- Copiar carteira divulgada de gestor sem o processo por trás (posições mudam antes da divulgação).
- Usar alavancagem "porque o Buffett usa" (o float dele custa ~0; a do usuário custa CDI+).
- Chamar concentração de "convicção" sem pesquisa que a sustente (Dynamo pesquisa anos; concentrar sem isso é só risco).
- Confundir bull market com habilidade: sem comparação contra benchmark no mesmo período, resultado não prova processo.
