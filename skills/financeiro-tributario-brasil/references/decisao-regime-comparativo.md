# Comparativo Lucro Presumido versus Lucro Real

Modelo quantitativo rápido. Se o Simples Nacional estiver na comparação, ou se a análise for usada para decidir regime, aplique também o Passo 6 de `tributario-metodo.md` (like-for-like com encargos patronais, sublimite × teto, matriz de sensibilidade).

**Limite desta análise:** produz cenário quantitativo para levar ao contador. Não é decisão fiscal. A opção pelo regime é anual e irretratável para o exercício — erro custa doze meses. Declare isso em toda saída.

## Estrutura da carga em cada regime

### Lucro Presumido

Tributos calculados sobre base presumida da receita bruta, independentemente do lucro efetivo.

| Tributo | Base | Alíquota | Efetivo sobre receita |
|---|---|---|---|
| IRPJ | 8% da receita (venda de produtos) | 15% | 1,20% |
| Adicional IRPJ | Base presumida acima de R$ 20 mil/mês | 10% | 0% a 0,80% |
| CSLL | 12% da receita | 9% | 1,08% |
| PIS cumulativo | Receita bruta | 0,65% | 0,65% |
| COFINS cumulativo | Receita bruta | 3,00% | 3,00% |

Sem crédito de PIS/COFINS sobre insumos.

Presunção de 8% para IRPJ e 12% para CSLL vale para venda de produtos (indústria e comércio). Serviços têm presunções diferentes — 32% é comum. Empresa com receita mista precisa segregar por atividade.

**Limite de receita:** R$ 78 milhões no ano-calendário anterior. Confirmar valor vigente.

### Lucro Real

| Tributo | Base | Alíquota |
|---|---|---|
| IRPJ | Lucro real (contábil ajustado pelo LALUR) | 15% |
| Adicional IRPJ | Lucro real acima de R$ 20 mil/mês | 10% |
| CSLL | Lucro real ajustado | 9% |
| PIS não-cumulativo | Receita bruta | 1,65% |
| COFINS não-cumulativo | Receita bruta | 7,60% |

Com direito a crédito de PIS/COFINS.

## O ponto que decide: crédito de PIS/COFINS

A leitura ingênua compara 3,65% (Presumido) contra 9,25% (Real) e conclui que o Presumido é sempre melhor. Está errado para indústria.

No não-cumulativo, o crédito de 9,25% incide sobre os insumos. A carga líquida é:

```
Carga líquida PIS/COFINS no Real = (Receita − Base creditável) × 9,25%
```

Se a base creditável for alta o suficiente, o Real fica abaixo dos 3,65% do Presumido.

**Ponto de indiferença de PIS/COFINS:**
```
Receita × 3,65% = (Receita − Créditos) × 9,25%
Créditos ÷ Receita = 1 − (3,65 ÷ 9,25) = 60,5%
```

Ou seja: se a base creditável representar mais de aproximadamente 60% da receita, o Real ganha só no PIS/COFINS. Indústria com custo de matéria-prima e embalagem alto pode chegar perto disso.

### O que gera crédito

Base legal: Leis 10.637/2002 e 10.833/2003. O conceito de insumo foi definido pelo STJ no REsp 1.221.170/PR (2018) por **essencialidade e relevância** para a atividade — critério mais amplo que o restritivo adotado antes pela Receita.

Geram crédito, tipicamente:
- Matéria-prima e material de embalagem
- Bens adquiridos para revenda
- Energia elétrica consumida
- Aluguel de prédio, máquina e equipamento pago a pessoa jurídica
- Arrendamento mercantil
- Depreciação de máquinas e equipamentos usados na produção
- Frete na operação de venda quando o ônus é do vendedor
- Serviços aplicados na produção

Não geram crédito, tipicamente:
- Mão de obra própria (folha de pagamento)
- Aquisição de pessoa física
- Aquisição de optante do Simples Nacional (regra específica, confirmar)
- Despesa administrativa não vinculada à produção

**Consequência prática relevante:** empresa que compra insumo de fornecedor do Simples perde crédito. Isso muda a decisão de fornecedor no Lucro Real e não importa no Presumido.

## Ponto de indiferença de IRPJ/CSLL

No Presumido, IRPJ + CSLL efetivos somam 2,28% da receita (sem adicional). No Real, incidem 15% de IRPJ e 9% de CSLL — 24% combinado, chegando a 34% marginal com o adicional de 10%.

```
Indiferença: Receita × 2,28% = Lucro Real × 24%
Margem de indiferença = 2,28 ÷ 24 = 9,5% de margem antes de tributos
```

Com o adicional de 10% no Presumido, a margem de indiferença sobe um pouco.

Leitura: **margem antes de IRPJ/CSLL abaixo de ~9,5% favorece o Real** nessa dimensão. Acima, favorece o Presumido.

## Modelo de comparação completo

Não decida por dimensão isolada. Some tudo.

```
CARGA PRESUMIDO
= Receita × (0,65% + 3,00%)                    [PIS/COFINS]
+ Receita × 8% × 15%                           [IRPJ]
+ max(0; Receita × 8% − 20.000/mês) × 10%      [Adicional]
+ Receita × 12% × 9%                           [CSLL]

CARGA REAL
= (Receita − Base creditável) × 9,25%          [PIS/COFINS líquido]
+ Lucro Real × 15%                             [IRPJ]
+ max(0; Lucro Real − 20.000/mês) × 10%        [Adicional]
+ Lucro Real × 9%                              [CSLL]
```

A apuração do Presumido é **trimestral** — o adicional incide sobre a base presumida que exceder R$ 60.000 no trimestre. A forma mensal acima é aproximação válida para receita estável; com receita concentrada em poucos meses, calcule por trimestre.

ICMS é igual nos dois regimes e não entra na comparação — a menos que exista benefício estadual condicionado ao regime, o que ocorre em alguns estados. Verifique.

## Fatores que a conta não captura

Quantificar carga é só metade da decisão.

**A favor do Presumido:**
- Obrigação acessória mais simples, custo contábil menor
- Previsibilidade — carga conhecida a partir do faturamento
- Não paga mais tributo em ano bom de margem
- Opção pelo regime de caixa: IRPJ, CSLL, PIS e COFINS apurados no recebimento, não na emissão — relevante para quem vende B2B a prazo longo

**A favor do Real:**
- Prejuízo fiscal compensável em exercícios seguintes (limite de 30% do lucro por período)
- Em ano ruim, paga pouco ou nada de IRPJ/CSLL
- Dedutibilidade de despesa financeira — relevante em empresa endividada
- Benefício fiscal da depreciação
- Créditos de PIS/COFINS sobre CAPEX produtivo
- JCP (juros sobre capital próprio) dedutível — reduz a base de IRPJ/CSLL

**Distribuição de lucros:** no Presumido, a distribuição isenta ao sócio se limita à base presumida líquida dos tributos — distribuir acima disso exige escrituração contábil completa comprovando o lucro efetivo maior. E desde 2026 dividendos pagos a pessoa física acima de R$ 50 mil/mês por empresa sofrem retenção de 10% na fonte (tributação mínima das altas rendas) — confirmar regras e limites vigentes antes de planejar retirada.

**Ponto frequentemente decisivo e esquecido:** empresa em prejuízo ou margem baixa no Presumido paga IRPJ e CSLL mesmo assim. Empresa cíclica ou em fase de investimento sofre desproporcionalmente nesse regime.

## Reforma Tributária do Consumo (EC 132/2023 + LC 214/2025)

Este comparativo tem prazo de validade parcial. Cronograma:

| Ano | O que muda |
|---|---|
| 2026 | Ano-teste: CBS 0,9% + IBS 0,1% destacados nos documentos fiscais (NT 2025.002 — campos CST, cClassTrib, vCBS, vIBS). Quem cumpre as obrigações acessórias fica dispensado do recolhimento. Preenchimento obrigatório na NF-e/NFC-e do regime regular a partir de ago/2026. Simples dispensado do destaque até 2027. |
| 2027 | CBS integral substitui PIS/COFINS (extintos). IPI zerado, exceto ZFM. Início do Imposto Seletivo. |
| 2029–2032 | Transição gradual ICMS/ISS → IBS. |
| 2033 | Sistema pleno; tributos antigos extintos. |

Consequências diretas para este comparativo:

1. **O limiar de ~60,5% de base creditável vale só até 31/12/2026.** A partir de 2027, a CBS é não-cumulativa para todos os regimes de IR — o crédito deixa de depender de estar no Real. A vantagem histórica do Presumido em PIS/COFINS desaparece.
2. De 2027 em diante, Presumido × Real se decide essencialmente por IRPJ/CSLL (margem × presunção de 9,5%) e pelos fatores qualitativos.
3. CBS/IBS são calculados **por fora** — não integram a própria base. A arquitetura de precificação muda (ver `decisao-precificacao.md`).
4. Crédito amplo e imediato previsto sobre bens de capital — melhora viabilidade de CAPEX em relação ao modelo atual.
5. Verificar o enquadramento do NCM nos anexos de alíquota reduzida da LC 214 — há hipóteses de alíquota reduzida por categoria; produto fora da lista expressa exige confirmação caso a caso, não presumir.
6. Alíquotas de referência do sistema pleno serão fixadas por resolução do Senado — confirmar valores vigentes antes de simular além de 2026.

Toda simulação plurianual precisa segmentar: regras atuais até 2026, regras novas de 2027 em diante. Estender a lógica de crédito de PIS/COFINS para 2027+ produz conclusão errada sobre regime.

## Estrutura de saída

```
## Conclusão
[Qual regime a simulação indica e por qual margem. Primeira frase.]

## Premissas
[Receita, margem, base creditável, com origem de cada número]

## Comparativo
[Tabela: componente × Presumido × Real × diferença]

## Sensibilidade
[Como a conclusão muda com receita ±20% e margem ±5 p.p.]
[Explicitar o ponto de virada]

## Fatores não quantificados
[Custo de compliance, prejuízo fiscal acumulado, plano de CAPEX, endividamento]

## Ressalva obrigatória
Simulação para discussão com contador responsável. A opção é anual e irretratável.
Confirmar alíquotas, limites e enquadramento de NCM na legislação vigente.

## Próxima ação
```

## Sinais de alerta a reportar sempre

- Comparação feita só por PIS/COFINS, ignorando IRPJ/CSLL — ou o inverso
- Base creditável estimada sem segregar o que efetivamente gera crédito
- Fornecedores do Simples relevantes na cadeia — reduzem crédito no Real
- Receita próxima do limite de R$ 78 milhões — pode haver desenquadramento obrigatório
- Receita mista (produto + serviço) sem segregação de presunção
- Decisão sendo tomada sem contador envolvido
- Alíquotas usadas sem verificação de vigência
- Simulação plurianual estendendo a lógica de crédito de PIS/COFINS além de 2026
