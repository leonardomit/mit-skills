# DRE — Demonstração do Resultado do Exercício

Base normativa: Lei 6.404/76 art. 187, com apresentação conforme CPC 26 (R1). Para PME, NBC TG 1000 (R1) simplifica divulgação mas mantém a mesma cascata.

## Estrutura obrigatória (em cascata)

```
   RECEITA BRUTA DE VENDAS E SERVIÇOS
(-) Devoluções e vendas canceladas
(-) Descontos incondicionais concedidos
(-) Impostos incidentes sobre vendas (ICMS, PIS, COFINS, ISS)
=   RECEITA LÍQUIDA
(-) Custo dos Produtos Vendidos (CPV) ou das Mercadorias (CMV)
=   LUCRO BRUTO
(-) Despesas com Vendas
(-) Despesas Administrativas e Gerais
(+/-) Outras receitas e despesas operacionais
=   RESULTADO ANTES DO RESULTADO FINANCEIRO  [EBIT]
(+) Receitas financeiras
(-) Despesas financeiras
=   RESULTADO ANTES DOS TRIBUTOS  [LAIR]
(-) Provisão para IRPJ
(-) Provisão para CSLL
=   RESULTADO LÍQUIDO DO EXERCÍCIO
```

**IPI não integra a receita bruta.** É imposto por fora, cobrado do adquirente e repassado ao fisco. Incluí-lo infla o faturamento e distorce toda margem percentual.

**ICMS-ST retido também não é receita.** Quando a empresa é substituta tributária, o valor retido é obrigação de terceiro, não venda.

**Marketplace e meios de pagamento:** a receita bruta é o valor da NF emitida — a comissão retida pelo marketplace é despesa com vendas, não redutor de receita. Taxas de cartão/gateway: escolha um critério (despesa com vendas ou financeira), declare-o e mantenha. Mudar o critério entre meses quebra a comparabilidade.

**PECLD (perdas estimadas em créditos de liquidação duvidosa):** com prazo B2B relevante, constitua provisão por faixa de atraso com base no histórico de perda, em despesas com vendas. Provisão contábil ≠ dedução fiscal — no Lucro Real, a dedução segue as condições de perdas efetivas da Lei 9.430/96, não a estimativa.

## EBITDA

Não é exigência da Lei 6.404/76. Para uso gerencial:

```
EBITDA = EBIT + Depreciação + Amortização
```

A CVM 156/2022 disciplina a divulgação para companhias abertas — a regra útil mesmo para empresa fechada é: se divulgar EBITDA, reconcilie explicitamente com o resultado líquido. EBITDA "ajustado" com exclusões arbitrárias vira instrumento de autoengano.

**Limite do EBITDA:** ignora variação de capital de giro. Negócio com estoque relevante e prazo de recebimento B2B longo pode ter EBITDA positivo e queimar caixa todo mês. Nunca apresente EBITDA sem apresentar o fluxo de caixa ao lado.

## Composição do CPV (indústria)

```
   Estoque Inicial de Produtos Acabados
(+) Custo de Produção do Período
(-) Estoque Final de Produtos Acabados
=   CPV
```

Onde o Custo de Produção inclui:
- Matéria-prima consumida
- Embalagem
- Mão de obra direta + encargos
- Custos indiretos de fabricação (energia da fábrica, depreciação de máquinas, manutenção, controle de qualidade)

**Erro frequente:** jogar mão de obra de produção em Despesas Administrativas. Isso infla o Lucro Bruto e faz a margem bruta parecer saudável enquanto o resultado operacional não fecha. Se a folha não estiver segregada entre produção e administrativo, sinalize ⚠️ e proponha o rateio por critério declarado (headcount ou horas), nunca silencioso.

## Tributos sobre o resultado

### Lucro Presumido

Incidem sobre base presumida, não sobre lucro real. Para venda de produtos (indústria e comércio):

| Tributo | Presunção sobre receita bruta | Alíquota | Efetivo sobre receita |
|---|---|---|---|
| IRPJ | 8% | 15% | 1,20% |
| CSLL | 12% | 9% | 1,08% |

**Adicional de IRPJ:** 10% sobre a parcela da base presumida que exceder R$ 20.000/mês (R$ 60.000/trimestre).

```
Adicional = max(0; (Receita × 8%) − 20.000/mês) × 10%
```

Convertido em percentual da receita, o adicional cresce e tende assintoticamente a 0,8%. Exemplo: receita mensal de R$ 500.000 → base R$ 40.000 → excedente R$ 20.000 → adicional R$ 2.000 = 0,4% da receita. IRPJ efetivo total = 1,60%.

PIS e COFINS no Presumido são cumulativos: 0,65% e 3,00%, sem crédito.

**Consequência para o DRE:** no Presumido, tributo sobre resultado independe do resultado. Mês com prejuízo ainda paga IRPJ e CSLL. Isso precisa aparecer explicitamente na análise, porque contraria a intuição.

**Regime de caixa opcional:** no Presumido é permitido apurar IRPJ, CSLL, PIS e COFINS pelo regime de caixa. O DRE permanece por competência — divergência entre o tributo efetivamente apurado e o teórico sobre a receita do mês é efeito de regime, não erro de cálculo. Registre qual regime a empresa adotou.

**Transição da reforma do consumo:** PIS/COFINS serão extintos em 2027 e substituídos pela CBS (LC 214/2025). Com os novos tributos calculados por fora, as deduções sobre vendas encolhem e a receita bruta converge para a líquida. Em 2026 o efeito é só de destaque em documento fiscal. Referência completa em `decisao-regime-comparativo.md`.

### Lucro Real

IRPJ 15% + adicional 10% sobre o lucro real que exceder R$ 20.000/mês. CSLL 9% sobre o lucro real ajustado. PIS 1,65% e COFINS 7,60%, não-cumulativos, com crédito sobre insumos.

O lucro real parte do lucro contábil e aplica adições e exclusões do LALUR. Despesa não dedutível (multa fiscal, brinde, parte de doação) aumenta a base.

Para o comparativo entre regimes, use `decisao-regime-comparativo.md`.

## Análises que acompanham o DRE

### Análise vertical

Todo item como percentual da **Receita Líquida** (não da bruta). Padrão de mercado. Comparar margem calculada sobre bruta com benchmark calculado sobre líquida inverte conclusões.

### Análise horizontal

Variação percentual contra:
1. Mês anterior — captura movimento recente
2. Mesmo mês do ano anterior — neutraliza sazonalidade

Em negócio sazonal, apenas a comparação contra mês anterior produz leitura errada. Traga as duas.

### Decomposição de variação de margem

Quando a margem bruta cai, existem quatro causas possíveis. Separe-as, porque cada uma tem dono diferente:

| Causa | Como identificar | Área responsável |
|---|---|---|
| Preço médio caiu | Receita líquida por unidade vendida caiu | Comercial |
| Custo de insumo subiu | CPV unitário subiu com volume estável | Compras |
| Mix mudou | Participação de SKU de margem baixa cresceu | Comercial |
| Ineficiência produtiva | Consumo de matéria-prima por unidade subiu | Produção |

Cálculo do efeito mix isolado:
```
Efeito Mix = Σ (participação_atual − participação_anterior) × margem_unitária_anterior
```

Sem essa decomposição, o diagnóstico vira opinião.

## Formato de apresentação

Tabela com quatro colunas mínimas: valor do período, % sobre receita líquida (AV), variação contra período comparativo (AH), e marcador de confiança.

Rubricas com valor zero podem ser omitidas, exceto quando o zero for informação relevante (ex.: devoluções zeradas em mês com volume alto é suspeito, não é boa notícia — sinalize).

## Sinais de alerta a reportar sempre

- Devoluções acima de 3% da receita bruta
- Margem bruta variando mais de 5 pontos percentuais contra o mesmo mês do ano anterior
- Despesa administrativa crescendo acima da receita por dois períodos consecutivos
- Resultado financeiro negativo relevante — indica dependência de capital de giro caro
- Inadimplência B2B crescendo sem PECLD constituída
- "Não classificado" acima de 5% das despesas — indica cadastro deficiente, e qualquer análise por área fica comprometida
