# Precificação

## Fórmula base — markup divisor

```
Preço de Venda = Custo Direto Unitário ÷ (1 − Σ percentuais sobre preço)
```

Onde Σ percentuais sobre preço reúne tudo que incide sobre a receita:

| Componente | Presumido (indústria/comércio) | Real |
|---|---|---|
| ICMS | Alíquota da operação (por dentro) | Idem |
| PIS | 0,65% | 1,65% |
| COFINS | 3,00% | 7,60% |
| IRPJ efetivo | 1,20% (8% × 15%) | Sobre lucro real |
| Adicional IRPJ | 0% a 0,80% conforme faixa | Sobre lucro real |
| CSLL efetivo | 1,08% (12% × 9%) | Sobre lucro real |
| Comissão de venda | Conforme política | Idem |
| Marketplace / canal | Take rate da plataforma | Idem |
| Frete (se CIF) | % sobre preço | Idem |
| Inadimplência esperada | Histórico por canal | Idem |
| Margem líquida desejada | Objetivo | Idem |

**Trava de sanidade:** se Σ percentuais ≥ 100%, o denominador fica zero ou negativo e não existe preço viável. Isso acontece quando alguém empilha margem alta com take rate de marketplace alto. Reporte como inviabilidade, não como preço absurdo.

No Lucro Real, IRPJ e CSLL não entram no divisor como percentual fixo sobre receita — incidem sobre o lucro. Trate a margem desejada como margem **antes** de IRPJ/CSLL e aplique os tributos depois.

## ICMS é por dentro

A base de cálculo do ICMS inclui o próprio imposto. Alíquota de 17% significa carga efetiva sobre a base líquida maior que 17%.

```
Base ICMS = Preço (o ICMS já está embutido)
Valor ICMS = Preço × alíquota
```

Por isso o ICMS entra direto no divisor como percentual. Quem calcula ICMS "por fora" e soma ao preço subestima a carga.

**IPI é por fora.** Soma-se ao preço depois, não entra no divisor:
```
Preço final ao cliente = Preço de venda + IPI
```

**ICMS-ST quando a indústria é substituta:** o imposto das etapas seguintes é calculado sobre base presumida (preço + MVA do estado de destino) e cobrado do cliente por fora, somado à NF junto com o IPI. Não entra no divisor do fabricante, mas encarece o preço de prateleira e define a competitividade por UF. Antes de fechar tabela, simule o preço final ao consumidor em cada estado relevante — MVA alta pode inviabilizar um mercado mesmo com preço de fábrica competitivo.

## Parâmetros a confirmar, não a assumir

Trate como variáveis de entrada, verificadas antes de cada uso:

- **Alíquota interna de ICMS do estado de origem** — muda por legislação estadual
- **Alíquota interestadual** — 7% ou 12% conforme origem e destino; 4% para produto importado com Resolução Senado 13/2012
- **DIFAL** — venda para consumidor final não contribuinte em outro estado gera diferencial de alíquota, com partilha conforme LC 190/2022
- **ICMS-ST** — se o NCM estiver em substituição tributária no estado de destino, a mecânica muda completamente: o imposto é recolhido antecipadamente com MVA, e o preço precisa considerar isso
- **Enquadramento do NCM** — define IPI, ST e eventual regime monofásico de PIS/COFINS
- **Benefício fiscal estadual** — crédito presumido, redução de base, TTD. Muda a carga real e é frequentemente esquecido no cálculo
- **Regime monofásico de PIS/COFINS** — determinados setores concentram a tributação no fabricante ou importador, com alíquotas próprias; confirme pelo NCM, porque o divisor muda
- **Reforma tributária em transição** — a partir de 2027 a CBS substitui PIS/COFINS e os novos tributos são calculados por fora; ver "Validade temporal do modelo" abaixo

Quando houver acesso a busca, verifique os valores vigentes. Quando não houver, apresente o cálculo com os parâmetros marcados como ⚠️ e liste o que precisa ser confirmado.

## Preço diferenciado por canal

B2B e B2C não têm a mesma estrutura de custo sobre preço. Calcule separado:

| Componente | B2B (distribuidor/atacado) | B2C (loja própria) | Marketplace |
|---|---|---|---|
| Comissão | Baixa ou zero | Zero | Take rate 12% a 20% |
| Frete | Frequentemente FOB | CIF, peso relevante | CIF |
| Inadimplência | Relevante (prazo) | Baixa (pagamento antecipado) | Baixa |
| Custo de aquisição | Comercial | Mídia paga | Mídia + take rate |
| Volume por pedido | Alto | Baixo | Baixo |
| Prazo | 30/60/90 dias | À vista | 15 a 30 dias |

O prazo B2B tem custo financeiro que precisa entrar no preço:
```
Custo financeiro do prazo = Preço × custo de capital mensal × (prazo médio ÷ 30)
```

Vender com 90 dias sem embutir esse custo é conceder desconto invisível.

**Conflito de canal:** preço B2C muito próximo do preço B2B destrói o distribuidor. Regra prática: o distribuidor precisa de margem que remunere o esforço dele. Se o cálculo indicar que não sobra espaço, a conclusão não é "reduza a margem do distribuidor" — é que a estrutura de custo não comporta dois canais no mesmo posicionamento.

## Margem de contribuição e ponto de equilíbrio

```
Margem de Contribuição unitária = Preço − Custo variável unitário − Despesas variáveis unitárias
MC% = MC unitária ÷ Preço

Ponto de Equilíbrio Contábil (unidades) = Custos e Despesas Fixas ÷ MC unitária
Ponto de Equilíbrio Financeiro = (Fixas − Depreciação) ÷ MC unitária
Ponto de Equilíbrio Econômico = (Fixas + Custo de oportunidade do capital) ÷ MC unitária
```

Os três respondem perguntas diferentes:
- **Contábil** — a partir de quanto não dá prejuízo no papel
- **Financeiro** — a partir de quanto o caixa não sangra
- **Econômico** — a partir de quanto o capital investido é remunerado adequadamente

Apresente o econômico quando a decisão envolver capital relevante. O contábil sozinho faz negócio medíocre parecer viável.

Com mix de produtos, use a MC% ponderada pela participação em receita:
```
PE em receita = Fixas ÷ MC% ponderada
```

E declare que o resultado depende do mix se manter. Mudança de mix invalida o ponto de equilíbrio.

## Avaliação de desconto

Pergunta recorrente: "posso dar X% de desconto?"

O desconto não reduz a margem em X pontos — reduz proporcionalmente muito mais, porque sai inteiro da margem de contribuição.

```
Volume adicional necessário = MC% atual ÷ (MC% atual − %desconto) − 1
```

Exemplo: MC de 30%, desconto de 10%.
```
30 ÷ (30 − 10) − 1 = 0,50 → precisa vender 50% a mais só para empatar
```

Sempre apresente esse número quando avaliar desconto ou campanha promocional. Ele muda a conversa.

## Precificação por valor versus por custo

O markup divisor calcula o **preço mínimo viável**, não o preço ótimo. São coisas diferentes.

Custo define o piso. Valor percebido, concorrência e posicionamento definem o teto. Preço fica entre os dois.

Quando o preço de mercado estiver abaixo do piso calculado, a conclusão não é "venda com prejuízo para ganhar share". A conclusão é: o custo precisa cair, o produto precisa se diferenciar, ou esse mercado não é acessível com essa estrutura.

Aponte isso explicitamente. É onde a maioria das empresas erra por otimismo.

## Validade temporal do modelo

Este divisor reflete o sistema vigente até 2026. A partir de 2027, PIS/COFINS deixam de existir (a CBS os substitui) e CBS/IBS são calculados **por fora** — somam-se ao preço em vez de entrar no divisor, como o IPI hoje. ICMS segue no divisor até a transição de 2029–2032.

Consequências práticas:
- Recalibre o modelo na virada 2026→2027 — a estrutura da fórmula muda, não só as alíquotas
- Tabela de preço plurianual precisa de dois blocos de regras
- Em 2026, os documentos fiscais já destacam CBS 0,9% + IBS 0,1%, sem recolhimento para quem cumpre as obrigações acessórias — efeito operacional, não de margem

## Sinais de alerta a reportar sempre

- Precificação existente feita por markup multiplicador
- Tabela de preço projetada para 2027+ com PIS/COFINS no divisor
- Preço único nacional em empresa que vende para múltiplos estados com ST
- Margem de contribuição abaixo de 25% em produto com estrutura fixa relevante
- Preço B2C a menos de 40% acima do preço B2B — risco de conflito de canal
- Desconto recorrente acima de 15% sem contrapartida de volume ou prazo
- Custo unitário calculado apenas com nota de compra, sem rateio de indiretos
- Produto regulado com posicionamento de preço que depende de alegação não autorizada
