# Rotina — princípios do módulo

Leia antes de qualquer referência `rotina-`. Módulo para o ciclo recorrente: apurar o que aconteceu, projetar o caixa, fechar o mês com controle.

## Antes de qualquer cálculo: validar a entrada

Número financeiro errado é pior que número ausente, porque gera decisão confiante e equivocada. Rode esta checagem sempre, e reporte o resultado dela antes de apresentar qualquer valor.

1. **Fonte única.** Se os dados vierem de mais de um sistema (ex.: um ERP para B2C e outro para B2B/fiscal), há risco de dupla contagem e de divergência de regime. Pergunte qual é a fonte de verdade para cada dataset. Se não houver resposta, apure separado por canal e **não some** — apresente lado a lado com aviso explícito.
2. **Regime.** Competência ou caixa? DRE é competência. Fluxo de caixa é caixa. Misturar os dois é o erro mais comum e produz "lucro sem dinheiro".
3. **Período fechado.** Confirme que o mês está com notas emitidas e devoluções lançadas. Fechar em D+2 com devolução pendente distorce a receita líquida.
4. **Cobertura.** Confira se o total de receita bate com o faturamento fiscal do período. Divergência acima de 2% é sinal de dado faltando, não de arredondamento.

Leia `rotina-contrato-dados.md` para o schema mínimo de entrada e as regras de deduplicação entre sistemas.

## Princípios de apresentação

**Comece pela conclusão.** Primeira linha responde a pergunta. Depois a tabela, depois a análise.

**Sempre traga a comparação.** Um número sozinho não informa. DRE vem com mês anterior e mesmo mês do ano anterior. Fluxo de caixa vem com o projetado versus realizado.

**Separe o que é estrutural do que é pontual.** Queda de margem por mix de produto é diferente de queda por reajuste de fornecedor. A primeira se corrige com comercial, a segunda com compras. Se não der para distinguir com os dados disponíveis, diga isso em vez de escolher uma narrativa.

**Marque a confiança do número.** Use três níveis:
- ✅ Conciliado — bate com extrato/fiscal
- ⚠️ Estimado — premissa explicitada
- ❌ Não confiável — dado faltando ou fonte divergente

**Não invente rubrica.** Se a despesa não tem centro de custo, ela vai para "Não classificado" e isso aparece no relatório. Distribuir por rateio silencioso destrói a rastreabilidade.

## Estrutura de saída padrão

```
## Conclusão
[1-3 frases. O que aconteceu e o que exige ação.]

## Números
[Tabela. Sempre com período comparativo e coluna de variação %.]

## Análise
[O que explica a variação. Separar estrutural de pontual.]

## Pontos de atenção
[Dados faltando, premissas frágeis, divergências entre fontes.]

## Próxima ação
[No máximo 3 itens, com responsável sugerido por cargo/setor.]
```

## Erros que este módulo existe para evitar

- **Somar B2B e B2C de sistemas diferentes sem deduplicar.** Se a NF aparece nos dois, o faturamento infla.
- **Tratar receita bruta como receita.** No Brasil, deduções (ICMS, PIS, COFINS, devoluções) saem antes da receita líquida. Comparar margem sobre bruta com benchmark de líquida gera conclusão invertida.
- **Projetar caixa por média histórica em negócio sazonal.** Use o padrão do mesmo período do ano anterior ajustado por crescimento, não a média dos últimos 3 meses.
- **Ignorar provisões.** 13º, férias e encargos sobre elas são obrigação que compete ao mês, mesmo sem desembolso. Fluxo de caixa sem provisionamento mensal produz surpresa em novembro e janeiro.
- **Confundir EBITDA com geração de caixa.** EBITDA ignora capital de giro. Em negócio com estoque alto e prazo B2B longo, os dois divergem muito.

## Contexto tributário

Confirme o regime tributário da empresa antes de apurar: os efeitos no DRE mudam com ele — principalmente PIS/COFINS (cumulativo sem crédito versus não-cumulativo com crédito). Não assuma regime. Se a apuração de resultado for usada para avaliar mudança de regime, use `decisao-regime-comparativo.md` e o Passo 6 de `tributario-metodo.md`.

Documentos fiscais de 2026 já destacam CBS/IBS (ano-teste da reforma do consumo); a estrutura de deduções do DRE muda a partir de 2027, quando a CBS substitui PIS/COFINS. Confirme o cronograma vigente (`atualizacao-legislativa.md`).

**Limite de atuação:** o módulo organiza e analisa. Não substitui contador nem produz peça contábil oficial. Qualquer número destinado a obrigação acessória, defesa fiscal ou decisão de regime tributário precisa de validação do contador responsável. Diga isso quando o contexto indicar esse uso.
