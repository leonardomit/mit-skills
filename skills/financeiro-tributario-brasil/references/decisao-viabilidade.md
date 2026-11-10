# Análise de Viabilidade de Investimento

## Taxa Mínima de Atratividade (TMA)

Sem TMA definida, não existe VPL nem payback descontado. É o primeiro parâmetro a estabelecer.

```
TMA = Taxa livre de risco + Prêmio de risco do projeto
```

No Brasil, a taxa livre de risco é a Selic ou o CDI vigente — **não** treasury americano. Usar referência estrangeira sem ajuste de risco-país e de moeda produz TMA irrealisticamente baixa e aprova projeto ruim.

Prêmio de risco por tipo de projeto (ordem de grandeza, a calibrar):

| Tipo | Prêmio sobre a taxa base |
|---|---|
| Substituição de equipamento com demanda conhecida | 2 a 4 p.p. |
| Expansão de capacidade em linha existente | 4 a 8 p.p. |
| Novo produto em mercado conhecido | 8 a 15 p.p. |
| Novo mercado ou novo modelo de negócio | 15 p.p. ou mais |

**Verifique a taxa base vigente antes de calcular.** Ela muda com frequência e a conclusão é sensível a ela. Quando houver acesso a busca, confirme; quando não houver, marque como ⚠️ e explicite a premissa.

Se a empresa tiver dívida relevante, considere o custo médio ponderado de capital em vez da TMA simples. O custo da dívida entra líquido de tributo apenas se a empresa estiver no Lucro Real — no Presumido não há dedutibilidade de juros contra a base tributável.

**Consistência nominal × real:** fluxos nominais (com inflação embutida) exigem taxa nominal; fluxos em moeda constante exigem taxa real — relação de Fisher: (1 + nominal) = (1 + real) × (1 + inflação). O erro clássico é projetar fluxo constante e descontar por TMA nominal cheia: rejeita projeto bom por inconsistência de método, não por mérito. Declare qual convenção está em uso.

## Métricas

### Valor Presente Líquido

```
VPL = Σ [FCt ÷ (1 + TMA)^t] − Investimento inicial
```

Critério: VPL > 0 significa que o projeto remunera o capital acima da TMA. É a métrica principal — decide.

### Taxa Interna de Retorno

Taxa que zera o VPL. Critério: TIR > TMA.

Limitações que precisam ser declaradas quando a TIR for apresentada:
- Fluxos com mais de uma inversão de sinal podem ter múltiplas TIRs
- Assume reinvestimento dos fluxos à própria TIR, o que raramente é realista
- Não distingue tamanho de projeto: 40% sobre R$ 50 mil é menos relevante que 20% sobre R$ 2 milhões

Quando houver inversão de sinal, use TIR Modificada, que assume reinvestimento à TMA.

### Payback

```
Payback simples = período até o fluxo acumulado nominal zerar
Payback descontado = período até o fluxo acumulado descontado zerar
```

Use sempre o descontado. O simples ignora custo do dinheiro e superestima a atratividade.

Payback é métrica de **risco e liquidez**, não de retorno. Não decide sozinho — projeto de payback curto e VPL baixo é pior que o inverso, se houver capital disponível.

### Índice de Lucratividade

```
IL = Valor presente dos fluxos ÷ Investimento inicial
```

Útil quando o capital é restrito e há projetos concorrentes. Ordena por eficiência de capital, coisa que o VPL absoluto não faz.

## Montagem do fluxo de caixa do projeto

Erros que invalidam a análise:

**1. Usar lucro contábil em vez de fluxo de caixa.** Depreciação não é saída de caixa. Variação de capital de giro é saída de caixa e não aparece no DRE.

```
Fluxo de Caixa Livre do projeto
=   EBIT do projeto
(-) Tributos sobre EBIT
(+) Depreciação e amortização
(-) Variação de capital de giro
(-) CAPEX
```

**2. Esquecer o capital de giro.** Projeto que aumenta produção aumenta estoque e contas a receber. Isso consome caixa no início e é recuperado no encerramento. Em negócio com ciclo financeiro longo, o capital de giro pode superar o CAPEX.

```
Variação de NCG = (Ciclo financeiro em dias ÷ 360) × Receita incremental
```

**3. Incluir custo afundado.** Dinheiro já gasto não entra. Estudo já pago, equipamento já comprado — irrelevantes para a decisão de seguir ou parar.

**4. Ignorar custo de oportunidade.** Se o projeto usa espaço, máquina ou pessoa que teria outro uso produtivo, esse valor entra como custo.

**5. Usar fluxo incremental errado.** O fluxo relevante é a diferença entre "com projeto" e "sem projeto", não o fluxo total da operação.

## Efeito tributário da depreciação

Só existe no **Lucro Real**. No Presumido, a base é presumida sobre a receita — depreciação não reduz tributo.

Isso muda materialmente a viabilidade de projeto intensivo em CAPEX. Empresa no Presumido avaliando compra de equipamento não tem o benefício fiscal da depreciação, e a análise precisa refletir isso. Se a mesma empresa estiver considerando migrar de regime, os dois efeitos interagem — trate conjuntamente com `decisao-regime-comparativo.md`.

Taxas de depreciação fiscal (IN RFB 1700/2017, Anexo III — confirmar vigência):

| Bem | Taxa anual | Vida útil fiscal |
|---|---|---|
| Edificações | 4% | 25 anos |
| Máquinas e equipamentos | 10% | 10 anos |
| Instalações | 10% | 10 anos |
| Móveis e utensílios | 10% | 10 anos |
| Veículos | 20% | 5 anos |
| Computadores e periféricos | 20% | 5 anos |

Depreciação acelerada é possível em operação com mais de um turno, conforme condições da legislação.

**Reforma do consumo:** a partir de 2027, a LC 214/2025 prevê crédito amplo de CBS/IBS na aquisição de bens de capital — independentemente do regime de IR. Projeto de CAPEX cujo horizonte cruza 2027 deve modelar os dois mundos tributários; confirmar as regras vigentes no momento da análise.

## Horizonte e valor terminal

Horizonte igual à vida útil econômica do ativo, não à vida útil fiscal. Máquina que se torna obsoleta em 5 anos não deve ser avaliada em 10, mesmo que deprecie em 10.

Valor residual entra como entrada no último período, líquido de tributo sobre eventual ganho de capital.

Para projeto sem prazo definido, evite perpetuidade em análise de PME — a sensibilidade da perpetuidade à taxa de crescimento é alta demais e a conclusão vira artefato da premissa. Prefira horizonte finito de 5 a 10 anos com valor residual conservador.

## Teste de ruptura

Obrigatório em toda análise. Não apresente VPL sem ele.

Para cada variável de maior alavancagem, encontre o valor que zera o VPL:

| Variável | Pergunta |
|---|---|
| Volume | Quanto abaixo do previsto o volume pode ficar antes do VPL zerar? |
| Preço | Quanto de queda de preço o projeto suporta? |
| CAPEX | Quanto o investimento pode estourar? |
| Custo de insumo | Quanto de alta o projeto absorve? |
| Prazo de implantação | Quantos meses de atraso o projeto suporta? |

Depois avalie a plausibilidade: "o VPL zera se o volume ficar 12% abaixo do previsto" é um alerta forte se a previsão veio de otimismo comercial sem contrato assinado.

## Estrutura de saída

```
## Conclusão
[Aprovar, rejeitar ou condicionar. Primeira frase.]

## Premissas
[TMA e sua origem, horizonte, volume, preço, custos. Cada uma marcada como confirmada ou estimada.]

## Fluxo de caixa do projeto
[Tabela por período]

## Métricas
[VPL, TIR, payback descontado, IL]

## Teste de ruptura
[Ponto de inversão de cada variável relevante + plausibilidade]

## Onde isso falha
[Cenário concreto de fracasso]

## Próxima ação
```

## Sinais de alerta a reportar sempre

- TMA não definida ou ancorada em referência estrangeira
- Fluxo montado sobre lucro contábil, sem ajuste de depreciação e capital de giro
- Capital de giro ausente em projeto de expansão de produção
- Benefício fiscal de depreciação considerado em empresa no Lucro Presumido
- Volume projetado sem lastro em contrato, pipeline ou histórico
- Payback usado como critério único de decisão
- Custo afundado incluído no fluxo
- Projeto que só fica viável no cenário otimista
