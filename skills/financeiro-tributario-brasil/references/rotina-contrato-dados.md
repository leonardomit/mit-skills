# Contrato de Dados

Define o que a skill precisa receber, independente de qual sistema origina. Isso desacopla a lógica financeira da decisão de ERP — trocar a fonte não exige reescrever nada.

## Por que existe

Empresa que roda mais de um sistema (ex.: um ERP para varejo/B2C, outro para atacado/fiscal) não tem acurácia de estoque nem de receita por construção. O mesmo pedido pode existir nos dois, com numeração diferente. Sem chave de deduplicação, todo relatório consolidado está errado.

O contrato resolve isso exigindo que a origem seja declarada em cada linha e que exista chave única fiscal.

## Datasets

### 1. `vendas`

Uma linha por item de nota fiscal (não por nota).

| Campo | Tipo | Obrigatório | Nota |
|---|---|---|---|
| `data_emissao` | date | sim | AAAA-MM-DD |
| `data_competencia` | date | sim | Normalmente = emissão |
| `numero_nf` | string | sim | Chave de dedup |
| `serie_nf` | string | sim | Chave de dedup |
| `cnpj_emitente` | string | sim | Chave de dedup |
| `cliente_id` | string | sim | |
| `cliente_doc` | string | não | CPF/CNPJ |
| `uf_destino` | string | sim | Define alíquota e ST |
| `canal` | enum | sim | `B2B` \| `B2C` \| `MARKETPLACE` |
| `sku` | string | sim | |
| `ncm` | string | sim | Define tributação |
| `quantidade` | decimal | sim | |
| `valor_bruto` | decimal | sim | Antes de desconto |
| `desconto` | decimal | sim | 0 se não houver |
| `valor_icms` | decimal | sim | 0 se isento/ST |
| `valor_icms_st` | decimal | sim | |
| `valor_pis` | decimal | sim | |
| `valor_cofins` | decimal | sim | |
| `valor_ipi` | decimal | sim | Por fora, não integra receita bruta |
| `cfop` | string | sim | Distingue venda de remessa/bonificação |
| `sistema_origem` | string | sim | Nome do ERP que exportou |

**Chave de deduplicação:** `cnpj_emitente + serie_nf + numero_nf + sku`.
Se a mesma chave vier de dois `sistema_origem`, mantenha um e registre o conflito. Nunca some.

**Filtro obrigatório:** excluir CFOP que não é venda — remessa, bonificação, demonstração, retorno, transferência entre filiais. Incluir esses infla receita sem contrapartida de caixa. Se a base não trouxer CFOP, sinalize como ❌ não confiável.

**Validação de exportação — total repetido por linha:** alguns exportadores de ERP repetem o **total da NF** em cada linha de item. Somar essa coluna multiplica o faturamento pelo número de itens da nota. Validação obrigatória antes de qualquer soma: para cada NF, comparar Σ(valor dos itens) com o total do documento. Se cada linha carregar o total, usar a coluna de valor unitário do item; na ausência dela, marcar ❌ e não consolidar.

### 2. `compras`

| Campo | Tipo | Obrigatório | Nota |
|---|---|---|---|
| `data_entrada` | date | sim | |
| `numero_nf` | string | sim | |
| `fornecedor_id` | string | sim | |
| `item` | string | sim | |
| `tipo_item` | enum | sim | `MATERIA_PRIMA` \| `EMBALAGEM` \| `REVENDA` \| `USO_CONSUMO` \| `IMOBILIZADO` |
| `quantidade` | decimal | sim | |
| `valor_total` | decimal | sim | |
| `credito_icms` | decimal | sim | |
| `credito_pis` | decimal | sim | Só existe no Lucro Real |
| `credito_cofins` | decimal | sim | Só existe no Lucro Real |
| `centro_custo` | string | não | |

`tipo_item` é crítico para o comparativo Presumido versus Real: apenas matéria-prima, embalagem, revenda e alguns itens de uso na produção geram crédito de PIS/COFINS no regime não-cumulativo. Uso e consumo administrativo não gera.

### 3. `despesas`

| Campo | Tipo | Obrigatório | Nota |
|---|---|---|---|
| `data_competencia` | date | sim | Regime de competência |
| `data_pagamento` | date | não | Vazio = não pago |
| `categoria` | string | sim | |
| `grupo_dre` | enum | sim | `VENDAS` \| `ADMINISTRATIVA` \| `FINANCEIRA` \| `OUTRAS` |
| `natureza` | enum | sim | `FIXA` \| `VARIAVEL` |
| `fornecedor` | string | não | |
| `valor` | decimal | sim | |
| `centro_custo` | string | não | Vazio vira "Não classificado" |

`natureza` alimenta o cálculo de ponto de equilíbrio no módulo de decisão (`decisao-precificacao.md`). Sem essa coluna, ponto de equilíbrio é chute.

### 4. `caixa`

Movimentação bancária realizada — base da conciliação.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `data` | date | sim |
| `conta` | string | sim |
| `tipo` | enum `ENTRADA`/`SAIDA` | sim |
| `valor` | decimal | sim |
| `contraparte` | string | não |
| `categoria` | string | não |
| `documento_vinculado` | string | não |

`documento_vinculado` (número da NF ou do título) é o que permite conciliar caixa com competência. Sem ele, a conciliação é manual.

### 5. `titulos`

Contas a receber e a pagar em aberto — base da projeção.

| Campo | Tipo | Obrigatório |
|---|---|---|
| `tipo` | enum `RECEBER`/`PAGAR` | sim |
| `documento` | string | sim |
| `contraparte` | string | sim |
| `data_emissao` | date | sim |
| `data_vencimento` | date | sim |
| `valor` | decimal | sim |
| `status` | enum `ABERTO`/`LIQUIDADO`/`ATRASADO` | sim |

### 6. `recebiveis` (cartão, PIX, gateway, marketplace)

Necessário para conciliar B2C: a NF sai pelo valor cheio, o banco recebe o líquido.

| Campo | Tipo | Obrigatório | Nota |
|---|---|---|---|
| `data_venda` | date | sim | |
| `meio` | enum | sim | `CREDITO` \| `DEBITO` \| `PIX` \| `BOLETO` \| `MARKETPLACE` |
| `plataforma` | string | sim | Adquirente, gateway ou marketplace |
| `parcelas` | int | sim | 1 se à vista |
| `valor_bruto` | decimal | sim | |
| `taxa` | decimal | sim | Valor retido |
| `valor_liquido` | decimal | sim | |
| `data_repasse_prevista` | date | sim | |
| `antecipado` | bool | sim | |
| `custo_antecipacao` | decimal | condicional | Se antecipado |
| `pedido_ou_nf` | string | sim | Vínculo com `vendas` |

Sem este dataset, a projeção de caixa B2C usa prazo nominal e o custo dos meios de pagamento fica invisível — dois erros relevantes em operação de e-commerce.

### 7. `estoque` (opcional, mas necessário para CPV preciso)

| Campo | Tipo |
|---|---|
| `sku` | string |
| `data_referencia` | date |
| `quantidade` | decimal |
| `custo_medio_unitario` | decimal |

Sem estoque inicial e final, o CPV vira estimativa. Marque como ⚠️.

## Formato de entrega

CSV UTF-8 com cabeçalho, ou abas de um XLSX com os nomes acima. Decimal com ponto. Datas ISO.

## Roteiro quando faltar dado

Não bloqueie a análise. Degrade com transparência:

| Falta | Consequência | Como reportar |
|---|---|---|
| `estoque` | CPV estimado por compras do período | ⚠️ em Lucro Bruto |
| `cfop` | Risco de contar remessa como venda | ❌ em Receita Bruta |
| `natureza` da despesa | Sem ponto de equilíbrio | Omitir a métrica, avisar |
| `centro_custo` | Sem análise por área | Agrupar em "Não classificado" |
| `sistema_origem` | Sem controle de dedup | ❌ no consolidado; apurar por canal separado |
| `recebiveis` | Caixa B2C projetado por prazo nominal; custo de meios de pagamento estimado | ⚠️ em recebimentos e em despesas com vendas |

## Migração futura

Quando a fonte única for definida, o único artefato novo é um exportador que produza estes datasets. A lógica dos módulos não muda. Se a escolha for um ERP que não expõe algum campo (comum: `natureza` da despesa e `tipo_item` da compra), a lacuna precisa ser preenchida por cadastro manual — planeje isso antes da migração, não depois.
