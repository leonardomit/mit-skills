# SOP Financeiro e Controles Internos

Processo, rotina e controle. Em empresa pequena e média, o risco não é sofisticação — é acúmulo de função e ausência de rastro.

## Segregação de funções

Princípio: nenhuma pessoa deve controlar mais de uma etapa do ciclo de um recurso. As quatro etapas incompatíveis:

1. **Autorizar** — aprovar a compra ou o pagamento
2. **Executar** — emitir o pedido, fazer a transferência
3. **Custodiar** — guardar o ativo (estoque, dinheiro, senha bancária)
4. **Registrar** — lançar no sistema, conciliar

Combinações críticas quando na mesma pessoa:

| Acúmulo | Risco |
|---|---|
| Compras + Pagamento | Fornecedor fictício, superfaturamento |
| Compras + Faturamento | Manipulação de custo e preço sem detecção cruzada |
| Custódia de estoque + Registro de estoque | Desvio coberto por ajuste de inventário |
| Emissão de NF + Recebimento | Venda não registrada, desvio de recebimento |
| Acesso bancário + Conciliação | Transferência não autorizada sem rastro |

**Realidade de empresa pequena:** segregação completa exige headcount que muitas não têm. Quando o acúmulo for inevitável, aplique **controle compensatório** — não ignore o gap.

Controles compensatórios eficazes:
- Revisão independente periódica por quem não executa (sócio, direção, contador externo)
- Aprovação obrigatória de segundo nível acima de valor de corte
- Conciliação feita por pessoa diferente de quem lança
- Rotação de função ou férias obrigatórias com substituição efetiva — fraude contínua exige presença contínua
- Log de alterações no ERP com revisão amostral

Ao mapear controles, **sempre liste os acúmulos existentes e o controle compensatório correspondente**. Acúmulo sem compensação é achado que precisa aparecer no relatório, independente de quem ocupa o cargo.

## Alçadas de aprovação

Matriz por valor e por tipo. Modelo base para adaptar:

| Faixa | Compra recorrente | Compra nova / CAPEX | Pagamento |
|---|---|---|---|
| Até 1% da receita mensal | Responsável da área | Responsável + gestor | Financeiro |
| 1% a 5% | Responsável + gestor | Gestor + direção | Financeiro + gestor |
| Acima de 5% | Direção | Direção | Dupla assinatura |

Percentuais da receita mensal em vez de valores fixos — evita que a matriz fique obsoleta com o crescimento.

Regras que evitam contorno:
- Fracionamento de pedido para escapar de alçada é violação. Controle: agrupar por fornecedor e período de 30 dias na verificação.
- Pagamento a fornecedor não cadastrado exige aprovação de nível acima, independentemente do valor.
- Alteração de dados bancários de fornecedor exige confirmação por canal independente do que solicitou a mudança. Esse é o vetor mais comum de fraude por engenharia social.

## Calendário de fechamento

Modelo em dias úteis após o encerramento do mês:

| Dia | Atividade | Responsável (setor) |
|---|---|---|
| D+1 | Corte de faturamento; bloqueio de lançamento retroativo | Faturamento |
| D+1 | Conciliação bancária final do mês | Financeiro |
| D+2 | Lançamento de devoluções e notas de crédito pendentes | Faturamento |
| D+2 | Inventário de estoque (contagem ou ciclo) | Estoque |
| D+3 | Apuração de CPV com estoque final | Custos |
| D+3 | Provisões: 13º, férias, encargos | Financeiro |
| D+4 | Classificação de despesas sem centro de custo | Financeiro |
| D+5 | Apuração de tributos | Contabilidade |
| D+5 | DRE preliminar | Financeiro |
| D+6 | Revisão de variações relevantes | Direção + Financeiro |
| D+7 | DRE final + fluxo de caixa + relatório gerencial | Financeiro |

Regra que faz o calendário funcionar: **bloqueio de lançamento retroativo em D+1**. Sem trava no sistema, o mês nunca fecha de verdade e todo relatório é provisório.

## Provisões mensais obrigatórias

Competência exige reconhecer o que já foi gerado, mesmo sem desembolso:

| Provisão | Cálculo mensal aproximado |
|---|---|
| 13º salário | Folha ÷ 12 |
| Encargos sobre 13º | (Folha ÷ 12) × alíquota de encargos |
| Férias | Folha ÷ 12 |
| 1/3 constitucional sobre férias | (Folha ÷ 12) × 1/3 |
| Encargos sobre férias | (Folha ÷ 12) × 4/3 × alíquota de encargos |

Alíquota de encargos varia com o enquadramento (INSS patronal, RAT, terceiros, FGTS) — parametrize conforme a folha real, confirmada com a contabilidade.

Empresa que não provisiona apresenta lucro inflado durante o ano e leva um choque em novembro. Se as provisões não estiverem lançadas, sinalize ⚠️ no DRE.

## Controles mínimos por ciclo

### Ciclo de receita
- Toda venda tem pedido aprovado antes da emissão
- Limite de crédito por cliente validado no pedido, não depois
- Emissão de NF conferida contra pedido (preço, quantidade, condição)
- Recebimento conciliado contra título em até 2 dias úteis
- Relatório mensal de títulos vencidos por faixa de atraso
- Conferência de exportação: Σ dos itens = total da NF (exportadores que repetem o total por linha inflam o faturamento)
- Emissão fiscal com os campos de CBS/IBS do ano-teste da reforma (NT 2025.002) — nota sem os campos pode ser rejeitada a partir da obrigatoriedade

### Ciclo de despesa
- Toda compra tem requisição com centro de custo
- Cotação mínima obrigatória acima de valor de corte
- Recebimento físico conferido contra pedido antes do aceite fiscal
- Pagamento apenas com os três documentos: pedido, nota, comprovante de recebimento
- Cadastro de fornecedor com CNPJ validado

### Ciclo de estoque
- Contagem cíclica por curva ABC — itens A com frequência maior
- Divergência acima de tolerância exige investigação documentada, não ajuste direto
- Ajuste de inventário requer aprovação de nível acima de quem custodia

## Estrutura de saída ao mapear controles

```
## Conclusão
[Nível de risco geral e o achado mais crítico]

## Matriz de segregação
[Tabela: função × pessoa (por cargo/setor) × conflito identificado]

## Achados
[Ordenados por criticidade. Cada um com: o que é, por que importa, exposição estimada]

## Controles compensatórios propostos
[Para cada achado sem solução estrutural viável]

## Próxima ação
[Máximo 3, com prazo sugerido]
```

Ao documentar, **identifique por cargo ou setor, nunca por nome próprio**. Documento de controle interno circula e pode ser lido como acusação pessoal quando na verdade descreve desenho de processo.

## Sinais de alerta a reportar sempre

- Mesma pessoa com acesso bancário e responsabilidade de conciliação
- Fornecedor com pagamento acima da média e sem cotação registrada
- Alteração de dados bancários de fornecedor nos últimos 90 dias
- Ajustes de inventário recorrentes no mesmo SKU
- Lançamentos retroativos após o fechamento
- Colaborador de função crítica sem férias há mais de 12 meses
