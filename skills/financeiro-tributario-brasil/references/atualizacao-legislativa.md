# Checagem de atualização legislativa

A skill não se atualiza sozinha. Este arquivo define como detectar, a cada uso, o que mudou na legislação desde que o conteúdo foi escrito — e como avisar o usuário.

## Data de referência

**Conteúdo consolidado em: 2026-11-10.**

A consolidação reuniu textos anteriores e **não revalidou** cada norma nessa data. Trate a data como limite superior: tudo que foi publicado depois dela é desconhecido da skill, e parte do que veio antes pode já estar defasado.

Ao atualizar a skill, troque a data e registre a mudança em "Histórico de atualizações", no fim deste arquivo.

## Quando rodar

| Situação | O que fazer |
|---|---|
| Pergunta simples (uma alíquota, um CFOP, um prazo) | Confirmar só a norma usada na resposta. Sem varredura. |
| Análise que usa regra ou número das referências | Varredura 1 nas normas que a análise toca |
| Análise de regime, carga, reforma, preço plurianual ou parametrização | Varreduras 1 e 2 |
| Pedido explícito ("confere se mudou algo", "a skill está atualizada?") | Varreduras 1 e 2 completas, em toda a lista |

Uma vez por sessão basta. Não repita a varredura a cada mensagem.

Sem acesso a busca: não rode, e diga isso. Escreva "legislação não reconferida; conteúdo com referência em [data]" no bloco de saída.

## Varredura 1 — o que a skill cita mudou?

Para cada norma tocada pela análise, busque com o ano corrente e vá ao texto compilado ou ao portal do órgão (`tributario-fontes.md`). Pergunta única: **houve alteração, revogação, regulamentação ou adiamento depois da data de referência?**

Normas e parâmetros em que a skill se apoia:

| Tema | Norma ou parâmetro | Onde a skill usa |
|---|---|---|
| Reforma do consumo | EC 132/2023, LC 214/2025, regulamentos e atos conjuntos RFB/CGIBS; alíquotas de referência; cronograma 2026–2033 | `tributario-metodo.md` (Passo 4), `decisao-regime-comparativo.md`, `decisao-precificacao.md`, `rotina-dre.md` |
| Documento fiscal | Notas Técnicas da NF-e/NFC-e (campos de CBS/IBS, CST, cClassTrib, datas de obrigatoriedade) | `rotina-sop-controles.md`, `tributario-metodo.md` (Passo 7) |
| Simples Nacional | LC 123/2006 e resoluções do Comitê Gestor: limites, sublimite, anexos, Fator R | `tributario-metodo.md`, `tributario-armadilhas.md` |
| PIS/COFINS | Leis 10.637/2002 e 10.833/2003; conceito de insumo (REsp 1.221.170); alíquotas cumulativas, não cumulativas e de importação | `decisao-regime-comparativo.md`, `tributario-armadilhas.md` |
| IRPJ/CSLL | Percentuais de presunção, adicional, limite de receita do Presumido, regime de caixa, compensação de prejuízo | `decisao-regime-comparativo.md`, `rotina-dre.md` |
| Lucros e dividendos | Lei 9.249/95 (art. 10) e a regra vigente de IRRF sobre dividendos: limiar, alíquota, transição | `decisao-regime-comparativo.md`, `tributario-armadilhas.md` |
| ICMS | Alíquotas internas por UF, FCP/FECP, convênios e protocolos de ST, MVA, LC 190/2022 (DIFAL), Resolução do Senado 13/2012 | `decisao-precificacao.md`, `tributario-metodo.md` |
| IPI e importação | TIPI e Ex-tarifários, TEC, IN RFB 1.984/2020 (RADAR) | `tributario-armadilhas.md` |
| Depreciação e perdas | IN RFB 1.700/2017 (taxas de depreciação), Lei 9.430/96 (perdas em créditos) | `decisao-viabilidade.md`, `rotina-dre.md` |
| Folha | INSS patronal, RAT×FAP, terceiros, FGTS, desoneração/CPRB | `rotina-sop-controles.md`, `tributario-armadilhas.md` |
| Contábil | Lei 6.404/76 (art. 187), CPC 26, CPC 03, NBC TG 1000, norma da CVM sobre EBITDA | `rotina-dre.md`, `rotina-fluxo-caixa.md` |
| Obrigações | Calendário de vencimentos federais e estaduais | `rotina-fluxo-caixa.md` |
| Contencioso | Art. 138 do CTN (denúncia espontânea); teses do STF/STJ sobre base de cálculo e suas modulações | `tributario-metodo.md` (Passo 8), `tributario-armadilhas.md` |
| Taxas de mercado | Selic/CDI, índices de reajuste (IPCA, IGP-M, INPC) | `decisao-viabilidade.md`, `decisao-planejamento.md` |

## Varredura 2 — surgiu algo que a skill não cobre?

A varredura 1 só acha mudança no que já está escrito. Esta procura o que **não** está.

Faça buscas abertas, com o ano corrente, restritas ao tema do pedido:

- lei, lei complementar ou medida provisória nova sobre o tributo ou o setor em análise
- decreto ou convênio novo da UF de origem e das principais UFs de destino
- ato novo da Receita, do CGIBS ou do Comitê Gestor do Simples sobre o tema
- decisão nova do STF ou STJ em repercussão geral ou repetitivo sobre o tema
- obrigação acessória nova ou com data de início dentro do horizonte da análise

Notícia e blog servem para **achar** a novidade. A confirmação vem do texto oficial. Novidade não confirmada entra como ❌ não verificada, nunca como fato.

Medida provisória tem prazo: confirme se foi convertida, alterada ou perdeu eficácia.

## O que fazer com o que achar

1. **Use a regra vigente na resposta**, não a da referência. Diga que a referência está defasada naquele ponto.
2. **Se a mudança ainda não vigora**, entregue os dois cenários, com a data de início.
3. **Se a mudança invalida um método** da skill (fórmula, ponto de indiferença, estrutura de cálculo), diga isso antes de calcular.
4. **Não edite a skill em silêncio.** Liste a proposta de atualização para o usuário decidir.

## Bloco de saída

Entra no fim da resposta, antes das fontes. Curto.

```
## Atualização legislativa
Conferido em: [data] · Referência da skill: [data de referência]

| Norma / tema | O que mudou | Vigência | Efeito nesta análise | Fonte |
|---|---|---|---|---|

Sem mudança encontrada em: [normas conferidas]
Não conferido: [o que ficou de fora e por quê]

Proposta de atualização da skill:
- [arquivo] — [o que trocar]
```

Sem mudança relevante, o bloco vira uma linha: `Legislação conferida em [data]: sem alteração nas normas usadas.`

Nunca escreva "sem mudanças" sobre o que não foi conferido. Ausência de resultado na busca não é prova de ausência de mudança.

## Fora do escopo da skill

Temas que a skill não cobre. Se o pedido depender deles, avise e pesquise do zero, sem apoiar a resposta nas referências:

- Legislação trabalhista (CLT): jornada, contratos, rescisão, convenção coletiva. A skill só trata o custo e os encargos da folha.
- Tributação de pessoa física, além da regra de dividendos.
- Contencioso tributário e teses judiciais em profundidade.
- Normas regulatórias setoriais (ANVISA, MAPA, ANP e outras), além da coerência com a classificação fiscal.

## Histórico de atualizações

| Data | O que mudou na skill | Motivo |
|---|---|---|
| 2026-11-10 | Consolidação dos módulos de rotina, decisão e tributário; inclusão desta checagem | Unificação |
