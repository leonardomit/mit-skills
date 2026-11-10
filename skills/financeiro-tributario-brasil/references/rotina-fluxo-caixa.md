# Fluxo de Caixa

Dois objetos distintos, frequentemente confundidos:

- **DFC contábil** (CPC 03 R2) — demonstração obrigatória, estruturada em operacional/investimento/financiamento, com foco em prestação de contas.
- **Fluxo de caixa gerencial** — ferramenta de gestão, com granularidade diária ou semanal e projeção futura.

Para rotina de gestão, use o gerencial. Só produza DFC quando o pedido for explicitamente contábil ou destinado a terceiros (banco, investidor, auditoria).

## Fluxo gerencial realizado

Estrutura mínima:

```
   SALDO INICIAL
(+) Recebimentos de clientes
(-) Pagamentos a fornecedores
(-) Folha e encargos
(-) Impostos
(-) Despesas operacionais
=   FLUXO OPERACIONAL
(-) Investimentos (CAPEX)
(+) Desinvestimentos
=   FLUXO DE INVESTIMENTO
(+) Captações
(-) Amortizações de dívida
(-) Despesas financeiras
(+/-) Distribuição de lucros / aporte
=   FLUXO DE FINANCIAMENTO
=   SALDO FINAL
```

Saldo final calculado precisa bater com o extrato bancário consolidado. Divergência não é arredondamento — é lançamento faltando. Investigue antes de apresentar.

## Projeção

### Contas a receber

Base: títulos em aberto com vencimento no horizonte + previsão de vendas novas.

Não use o vencimento nominal. Use o vencimento ajustado pelo comportamento real de pagamento:

```
Data provável = Vencimento + Atraso médio do cliente
```

Calcule o atraso médio por cliente (ou por faixa de cliente) a partir do histórico de liquidação. Clientes B2B de atacado costumam ter comportamento estável e previsível — isso é o que torna a projeção útil.

Aplique também a expectativa de inadimplência:
```
Recebimento esperado = Σ (título × (1 − taxa_inadimplência_da_faixa))
```

Taxa por faixa de atraso histórico, não taxa única. Título de cliente com histórico limpo e título de cliente já atrasado não têm a mesma probabilidade.

**Recebíveis de cartão e marketplace:** o prazo não é o do cliente, é o do repasse — débito/PIX em D+1, crédito à vista em torno de D+30, parcelado conforme o fluxo das parcelas, marketplace conforme o ciclo da plataforma. Projete pelo **valor líquido** de taxas (dataset `recebiveis` em `rotina-contrato-dados.md`). Antecipar recebíveis é decisão de custo: compare a taxa de antecipação com o custo da alternativa de capital de giro — antecipar pode ser racional; o problema é dependência estrutural de crédito rotativo caro.

### Contas a pagar

Mais previsível que recebimento. Use vencimento nominal, exceto quando houver política deliberada de alongamento.

Não esqueça o que não está em título:
- Folha e encargos (data fixa)
- FGTS e INSS
- Impostos sobre faturamento — no Presumido, PIS/COFINS mensais, IRPJ/CSLL trimestrais
- ICMS mensal
- Provisões que viram desembolso: 13º (novembro/dezembro), férias

Vencimentos típicos para ancorar a projeção (confirmar o calendário vigente — datas mudam):

| Obrigação | Vencimento usual |
|---|---|
| PIS/COFINS | Dia 25 do mês seguinte |
| IRPJ/CSLL (Presumido) | Último dia útil do mês seguinte ao trimestre — à vista ou em até 3 quotas com juros |
| ICMS | Calendário estadual, por categoria de contribuinte |
| FGTS | Dia 20 |
| INSS / DARF DCTFWeb | Dia 20 |

Se a empresa optou pelo **regime de caixa** no Presumido, os tributos sobre receita acompanham o recebimento, não a emissão — alinhe a projeção ao regime adotado.

### Sazonalidade

Em negócio sazonal, **não projete por média móvel dos últimos meses**. Isso suaviza justamente o que importa.

Método correto:
```
Projeção do mês M = Realizado do mês M do ano anterior × (1 + crescimento anual)
```

Ajuste o crescimento por evidência (pipeline comercial, contratos fechados), não por meta.

### Horizonte e granularidade

| Horizonte | Granularidade | Uso |
|---|---|---|
| 4 semanas | Diária | Gestão de liquidez, decisão de pagamento |
| 3 meses | Semanal | Antecipação de aperto, negociação de prazo |
| 12 meses | Mensal | Planejamento, decisão de investimento |

Projeção diária além de 4 semanas é falsa precisão.

## Saldo mínimo de caixa

Toda projeção precisa de uma linha de corte. Sem ela, o gestor vê saldo positivo e acha que está seguro.

```
Saldo mínimo = Desembolso fixo médio mensal × meses de cobertura desejada
```

Cobertura de 1 a 3 meses conforme volatilidade da receita e acesso a crédito. Marque no relatório todo mês em que a projeção cruza essa linha, mesmo que o saldo continue positivo.

## Ciclo financeiro

Métrica que explica por que lucro não vira caixa.

```
PMR = (Contas a receber ÷ Receita bruta) × dias do período
PME = (Estoque ÷ CPV) × dias do período
PMP = (Contas a pagar ÷ Compras) × dias do período

Ciclo Operacional  = PMR + PME
Ciclo Financeiro   = PMR + PME − PMP
```

Ciclo financeiro positivo significa que a empresa financia o cliente. Cada dia de ciclo custa dinheiro:

```
Necessidade de Capital de Giro = (Ciclo Financeiro ÷ 360) × Receita anual
Custo do ciclo = NCG × custo de capital anual
```

Em empresa que vende B2B com 30/60/90 dias e mantém estoque de matéria-prima, o ciclo financeiro costuma passar de 90 dias. Crescer faturamento com esse ciclo consome caixa — crescimento acelerado sem capital de giro é a causa clássica de quebra de empresa lucrativa. Sempre reporte a NCG junto com a projeção quando houver plano de crescimento.

## Conciliação bancária

Rotina diária, não mensal. Mensal descobre o problema tarde demais.

Passos:
1. Importar extrato de cada conta
2. Casar cada lançamento com título ou documento (`documento_vinculado`)
3. Isolar não conciliados
4. Classificar cada não conciliado: lançamento faltando no sistema, lançamento faltando no banco, diferença de valor, ou erro de data

Não conciliados que persistem por mais de 5 dias úteis viram ponto de controle — reporte na saída.

## Sinais de alerta a reportar sempre

- Projeção cruzando o saldo mínimo em qualquer mês do horizonte
- Ciclo financeiro aumentando por dois períodos consecutivos
- Concentração de recebimento: um cliente acima de 20% do contas a receber
- Dependência estrutural de conta garantida ou rotativo, ou antecipação recorrente sem comparação de custo com alternativas — indica NCG não capitalizada, com o custo disfarçado no resultado financeiro
- Divergência entre saldo projetado e realizado acima de 10% — a premissa de projeção está errada e precisa ser recalibrada
