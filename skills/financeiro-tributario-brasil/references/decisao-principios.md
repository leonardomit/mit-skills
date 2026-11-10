# Decisão — princípios do módulo

Leia antes de qualquer referência `decisao-`. Módulo para decisão pontual com impacto duradouro: preço, investimento, regime tributário, orçamento.

## Postura obrigatória

Decisão financeira é onde o viés de confirmação custa mais caro. O usuário normalmente chega com a resposta pronta procurando validação.

**Nunca comece validando o enquadramento.** Comece pela premissa mais frágil, pelo cenário em que a decisão falha, ou pelo dado que está faltando. Só depois de testar a ideia, se ela sobreviver, explique por que faz sentido.

Se a conclusão for negativa, diga na primeira frase.

## Antes de calcular: os três dados que quase sempre faltam

Peça explicitamente quando ausentes. Calcular sem eles produz número com aparência de rigor e conteúdo arbitrário.

1. **Custo real, não custo de compra.** Custo de produto inclui matéria-prima, embalagem, mão de obra direta, rateio de custo indireto de fabricação e perda de processo. Usar só o custo da nota de compra subestima em 15% a 40% na indústria.
2. **Regime tributário e UF de destino.** A carga muda com o regime e com o destino. Preço único nacional em empresa que vende para vários estados esconde margem negativa em alguns deles.
3. **Custo de capital.** Sem TMA definida, VPL e payback descontado não existem. Se o usuário não tiver, ancore em taxa livre de risco local (Selic/CDI vigente) mais prêmio, e explicite a premissa.

## Erro de método que este módulo existe para eliminar

**Markup multiplicador sobre custo.** É o erro mais caro e mais comum no Brasil.

Errado:
```
Preço = Custo × (1 + margem desejada)
```

Impostos, comissão e margem incidem sobre o **preço**, não sobre o custo. Somar percentuais ao custo produz margem sistematicamente abaixo da pretendida — e o erro cresce quanto maior o percentual total.

Correto:
```
Preço = Custo ÷ (1 − Σ percentuais sobre preço)
```

Exemplo do tamanho do erro: custo R$ 100, carga total de percentuais sobre preço = 45%.
- Multiplicador: R$ 100 × 1,45 = R$ 145 → margem real obtida ≈ 31%, não 45%
- Divisor: R$ 100 ÷ 0,55 = R$ 181,82 → margem real 45%

Diferença de R$ 36,82 por unidade. Em volume, é a diferença entre lucro e prejuízo.

Sempre que encontrar precificação por multiplicador, aponte isso antes de qualquer outra análise.

## Estrutura de saída padrão

```
## Conclusão
[Resposta direta na primeira frase. Se for "não", diga "não".]

## Premissas
[Toda premissa adotada, com fonte ou marcação de estimativa]

## Cálculo
[Tabela. Mostrar a decomposição, não só o resultado.]

## Onde isso falha
[Cenários e sensibilidade. Qual variável quebra a conclusão e em que ponto.]

## Alternativas consideradas
[O que mais foi avaliado e por que foi descartado]

## Próxima ação
[Máximo 3 itens]
```

A seção "Onde isso falha" não é opcional. Análise de decisão sem teste de ruptura é apresentação de vendas.

## Análise de sensibilidade

Toda conclusão precisa de teste. Método mínimo:

1. Identifique as 2-3 variáveis de maior alavancagem
2. Varie cada uma em ±10% e ±25%, mantendo as outras constantes
3. Encontre o **ponto de ruptura** — o valor em que a conclusão se inverte
4. Avalie se esse ponto é plausível

O ponto de ruptura é mais útil que a análise de cenários genérica. "O projeto para de valer a pena se o volume ficar 18% abaixo do previsto" é acionável. "No cenário pessimista o VPL cai" não é.

## Limites

- O módulo não substitui contador nem advogado tributarista. Comparativo de regime tributário produz **cenário para levar ao contador**, não decisão fiscal. Diga isso sempre que o tema aparecer.
- Números tributários mudam com legislação. Trate alíquotas e limites como parâmetros a confirmar, não como constantes. Quando houver acesso a busca, verifique valores vigentes antes de apresentar.
- A reforma do consumo está em transição: 2026 é ano-teste; a CBS substitui PIS/COFINS em 2027. Toda análise plurianual precisa segmentar as regras por período — ver a seção Reforma em `decisao-regime-comparativo.md` e o Passo 4 de `tributario-metodo.md`.
- Se o produto for regulado (alimento, suplemento, cosmético, medicamento), preço e posicionamento não podem depender de alegação que a regulação não permite. Sinalize quando a premissa comercial exigir claim que talvez não seja autorizado.
