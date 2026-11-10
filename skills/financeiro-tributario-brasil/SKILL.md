---
name: financeiro-tributario-brasil
description: "Finanças e tributos de empresa brasileira em uma skill: rotina (DRE Lei 6.404, fluxo de caixa, fechamento mensal, conciliação, provisões, SOP e controles internos), decisão (precificação por markup divisor, margem, desconto, ponto de equilíbrio, viabilidade com VPL/TIR/payback, orçamento e cenários) e análise tributária (regime Simples/Presumido/Real, ICMS, ST, DIFAL, ISS, PIS/COFINS, IPI, IRPJ/CSLL, reforma CBS/IBS/IS, carga efetiva, NCM, CFOP, CST, parametrização fiscal de ERP e marketplace). Use SEMPRE que o pedido envolver fechar o mês, resultado, caixa, runway, quanto cobrar, se um preço ou desconto cabe, se um investimento vale a pena, imposto, alíquota, nota fiscal, mudança de regime ou efeito da reforma tributária, mesmo sem a palavra 'análise'."
---

# Financeiro e Tributário — Brasil

Três módulos, um método. Leia só as referências que o pedido exige. Antes da primeira referência de rotina, leia `rotina-principios.md`; antes da primeira de decisão, `decisao-principios.md`. Eles trazem a validação de entrada, os dados a pedir e o formato de saída de cada módulo.

| Módulo | Para quê | Prefixo em `references/` |
|---|---|---|
| Rotina | Apurar o que aconteceu, projetar o caixa, fechar o mês com controle | `rotina-` |
| Decisão | Preço, investimento, orçamento — decisão pontual com efeito duradouro | `decisao-` |
| Tributário | Enquadramento, tributos por operação, regime, reforma, parametrização | `tributario-` |

A skill não carrega dados de nenhuma empresa. Regime, UF, CNAE, NCM, canais e números vêm do usuário, da memória, do ERP ou dos arquivos da sessão. Consulte essas fontes antes de perguntar. Nunca assuma regime tributário: confirme.

## Roteiro por pedido

| O usuário pede | Leia |
|---|---|
| DRE, resultado do mês, margem, "por que o lucro caiu" | `rotina-dre.md` + `rotina-contrato-dados.md` |
| Caixa, projeção, runway, contas a pagar/receber, conciliação | `rotina-fluxo-caixa.md` + `rotina-contrato-dados.md` |
| Fechamento, calendário de close, alçadas, segregação, fraude | `rotina-sop-controles.md` |
| Preço, margem, desconto, tabela B2B × B2C, ponto de equilíbrio | `decisao-precificacao.md` |
| Investimento, máquina, expansão, payback, retorno | `decisao-viabilidade.md` |
| Orçamento, metas, cenários, projeção anual | `decisao-planejamento.md` |
| Presumido × Real (conta rápida, ponto de indiferença) | `decisao-regime-comparativo.md` |
| Qual regime, quanto pago, Simples na comparação, carga efetiva | `tributario-metodo.md` (Passo 6) + `decisao-regime-comparativo.md` + `tributario-armadilhas.md` |
| Imposto, alíquota, NCM, CFOP, CST, ST, DIFAL, nota fiscal | `tributario-metodo.md` + `tributario-fontes.md` |
| Regra fiscal de ERP, emissor ou marketplace | `tributario-metodo.md` (Passo 7) |
| Efeito da reforma (CBS, IBS, IS) em preço, carga ou contrato | `tributario-metodo.md` (Passo 4) + referência do módulo afetado |
| Particularidade de setor | `tributario-setores.md` |
| "Mudou alguma coisa?", "a skill está atualizada?", novidade legislativa | `atualizacao-legislativa.md` |

Pedidos cruzam com frequência. "Vale a pena essa máquina?" exige viabilidade **e** efeito no custo unitário. "Fecha o mês e me diz como está o caixa" exige DRE **e** fluxo. Preço com tributo exige precificação **e** o mapa de tributos da operação. Leia os dois.

Toda análise tributária termina percorrendo `tributario-armadilhas.md`.

## Checagem de atualização

O conteúdo tem data de referência e a legislação muda depois dela. Em toda análise que use regra ou número das referências, rode a checagem de `atualizacao-legislativa.md`: primeiro se as normas citadas mudaram, depois se surgiu norma nova que a skill não cobre. Feche a resposta com o bloco "Atualização legislativa" e, se houver defasagem, com a proposta de atualização da skill. Pergunta simples confere só a norma usada. Sem acesso a busca, declare que a legislação não foi reconferida.

## Regras comuns aos três módulos

1. **Crítica antes de validação.** Comece pela premissa mais frágil, pelo dado que falta ou pelo cenário em que a conclusão falha. Se a resposta for "não", diga na primeira frase.
2. **Conclusão primeiro.** Primeira linha responde a pergunta. Depois tabela, depois análise.
3. **Nenhum número tributário de memória.** As alíquotas, limites, presunções e datas escritas nas referências são parâmetros de partida, não constantes. Com acesso a busca, confirme o valor vigente com fonte e data antes de apresentar (`tributario-fontes.md`). Sem acesso, marque como não verificado.
4. **Comece pela data.** A reforma do consumo está em transição (2026–2033). Toda análise que cruza virada de ano entrega as regras por período.
5. **Conta em código.** Aritmética com fórmulas e premissas visíveis, nunca de cabeça.
6. **Validar a entrada antes de calcular.** Fonte única ou apuração separada por canal; competência × caixa; período fechado; receita batendo com o faturamento fiscal (`rotina-contrato-dados.md`).
7. **Estimativa é marcada como estimativa**, com a premissa ao lado. Rubrica sem classificação vai para "Não classificado", nunca para rateio silencioso.
8. **Teste de ruptura obrigatório em decisão.** Varie as 2–3 variáveis de maior alavancagem e informe o ponto em que a conclusão se inverte, e se esse ponto é plausível.
9. **Proporcionalidade.** Pergunta simples recebe resposta direta com fonte. Não transforme consulta de CFOP em relatório.
10. **Limite do papel.** A skill organiza, analisa e prepara a conversa com contador ou advogado. Não substitui parecer, peça contábil oficial nem consulta ao fisco. A opção de regime é anual e irretratável: comparativo é cenário para o contador, não decisão fiscal. Diga isso uma vez, no fim.

## Rótulos de confiança

Use um rótulo em cada número relevante.

| Rótulo | Dado financeiro | Dado tributário |
|---|---|---|
| ✅ Confirmado | Conciliado com extrato ou fiscal | Norma localizada e lida na sessão |
| ⚠️ Estimado | Premissa explicitada | Regra geral; número específico não conferido |
| ❌ Não confiável | Dado faltando ou fonte divergente | Não verificado; exige validação |

## Erros que a skill existe para eliminar

- **Markup multiplicador.** Impostos, comissão e margem incidem sobre o preço. `Preço = Custo ÷ (1 − Σ percentuais sobre preço)`, nunca `Custo × (1 + margem)`. Aponte antes de qualquer outra análise.
- **Somar sistemas diferentes sem deduplicar.** A mesma NF em dois ERPs infla o faturamento.
- **Tratar receita bruta como receita.** Margem se mede sobre a líquida.
- **Misturar competência e caixa.** DRE é competência; fluxo é caixa.
- **Projetar caixa por média em negócio sazonal** e ignorar provisões de 13º e férias.
- **Confundir EBITDA com geração de caixa.** EBITDA ignora capital de giro.
- **Comparar regimes sem base like-for-like.** O DAS inclui a CPP patronal; fora do Simples aparecem encargos que não existiam. Sem as duas tabelas, a palavra "economia" não aparece.
- **Comparar carga por dentro com alíquota por fora.** Converta antes: X% por dentro equivale a X/(1−X) por fora.
- **Tributar a empresa em vez da operação.** Quem vende, para quem, de onde para onde, o quê e com que origem.

## Estrutura de saída

Rotina e decisão:

```
## Conclusão
[Resposta direta. Se for "não", diga "não".]

## Premissas
[Cada premissa com fonte ou marcação de estimativa]

## Números
[Tabela com decomposição, período comparativo e variação %]

## Análise
[O que explica o número. Separar estrutural de pontual.]

## Onde isso falha
[Sensibilidade e ponto de ruptura. Obrigatório em decisão.]

## Pontos de atenção
[Dados faltando, premissas frágeis, divergência entre fontes]

## Próxima ação
[Máximo 3 itens, com responsável sugerido por cargo ou setor]
```

Análise tributária completa segue a estrutura de dez seções de `tributario-metodo.md`. Cada referência traz a variação de saída do seu tema.

Ao documentar controles e responsabilidades, identifique por cargo ou setor, nunca por nome próprio. Em produto regulado, sinalize quando a premissa comercial depender de alegação que a regulação talvez não autorize.
