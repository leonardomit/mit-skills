# Filtros por Lente — cortes quantitativos

Todos os cortes são heurísticas derivadas do método de cada investidor, calibráveis por perfil. Na dúvida, aplicar o corte mais restritivo. Nenhum filtro dispensa leitura de release/RI antes de decisão.

## 1. Barsi — Núcleo de renda BR (ações de dividendos)

**Universo**: bancos, energia elétrica (geração/transmissão), saneamento, seguros, telecom. Fora do universo = reprovado direto (perenidade setorial é o 1º filtro do método).

| Métrica | Corte | Observação |
|---|---|---|
| DY médio 5 anos | ≥ 6% a.a. | Régua clássica; não comparar com CDI nominal — o jogo é yield on cost crescente |
| Payout | ≤ 80% | Exceto transmissoras/reguladas com capex baixo |
| Lucro líquido | Positivo em ≥ 8 dos últimos 10 anos | Perenidade > pico |
| Dívida líq./EBITDA | < 3,0x | Bancos: usar Basileia ≥ 11% no lugar |
| ROE | ≥ 10% | Consistente, não pontual |
| Histórico de proventos | Ininterrupto ≥ 5 anos | Corte de disciplina do pagador |
| Liquidez | ≥ R$ 1 mi/dia | Ajustável ao tamanho do aporte |

Red flags que anulam aprovação: dividendo extraordinário inflando o DY médio; estatal com risco de intervenção explícito no ciclo político atual; payout > lucro (pagando com dívida).

## 2. Lynch — GARP (crescimento a preço razoável)

| Métrica | Corte | Observação |
|---|---|---|
| PEG | < 1,0 | P/L ÷ crescimento anual de lucros (média 3–5 anos). PEG < 0,5 = checar se o crescimento é real |
| Crescimento de lucros | 10–25% a.a. | > 25% = desconfiar de sustentabilidade, não celebrar |
| Dívida líq./EBITDA | < 2,0x | Crescimento alavancado quebra em ciclo de juro alto |
| Margem líquida | Estável ou crescente 3 anos | Crescimento com margem caindo = comprar receita, não lucro |
| Círculo de competência | Usuário explica o produto em 1 frase | Se não explica, reprovado independente dos números |

## 3. Buffett / Dynamo — Qualidade

| Métrica | Corte | Observação |
|---|---|---|
| ROE | ≥ 15% em ≥ 4 dos últimos 5 anos | Ou ROIC > custo de capital estimado |
| Margem bruta | Estável/crescente 5 anos | Proxy de poder de preço |
| FCF | Positivo e recorrente | Lucro sem caixa é contabilidade |
| Dívida líq./EBITDA | < 2,5x | |
| Moat (qualitativo) | Responder: "por que o cliente não troca?" | Sem resposta concreta (marca, custo de troca, rede, escala, licença) = reprovado |
| Preço | Earnings yield (1/PL) comparado ao juro real da NTN-B longa | Se a empresa rende menos que o título público real, o prêmio de risco é negativo — exige justificativa forte |

## 4. Verde / Stuhlberger — Núcleo de renda fixa real

| Instrumento | Corte | Observação |
|---|---|---|
| NTN-B (IPCA+) | Juro real ≥ 5,5% a.a. = zona historicamente atrativa | Buscar taxa do dia no Tesouro Direto; escalonar vencimentos (curto/médio/longo), não concentrar num único |
| CDB/LCI/LCA | ≥ 100% CDI (CDB) dentro do limite FGC por instituição | Acima de ~115% CDI: verificar rating e saúde do emissor — prêmio alto é sinal de risco, não presente |
| Marcação | Pré e IPCA+ longos oscilam; segurar até o vencimento neutraliza | Declarar isso sempre que sugerir vencimento longo |
| Caixa tático | Selic/DI pós-fixado para liquidez e oportunidade | Função: financiar compras em queda, não render |

Proporção núcleo: tipicamente 50–80% da carteira conforme perfil — o juro real BR é o motor que financia os satélites de risco.

## 5. Bogle — Internacional / indexado (satélite ou núcleo global)

| Métrica | Corte | Observação |
|---|---|---|
| Custo total (TER) | < 0,25% a.a. | Acima disso, exigir edge comprovado do gestor |
| Diversificação | Índice amplo (mundo ou S&P 500) antes de temático | Temático = satélite pequeno, nunca base |
| Estrutura | ETF/BDR de índice ou conta internacional | Comparar custo cambial + tributação antes de escolher o veículo |
| Sobreposição | Checar duplicidade com posições BR existentes | |

## 6. Druckenmiller e Simons — não geram screening

Estes dois entram **depois** da shortlist, nunca antes:

- **Druckenmiller** define o tamanho: perda máxima em R$ por posição → tamanho da posição = perda máxima ÷ queda de estresse do ativo. Sem perda máxima definida, nenhum candidato vira compra.
- **Simons** define a regra: entrada escalonada ou única, gatilho de rebalanceamento, critério de saída — por escrito, antes da primeira ordem.

## Quedas de estresse por classe (para sizing pós-shortlist)

| Classe | Estresse |
|---|---|
| Ações BR individuais | −50% |
| FIIs | −35% |
| NTN-B longa (marcação) | −20% |
| Internacional (índice, em R$) | −35% |
| Cripto | −70% |

## Fontes de dados (buscar sempre, nunca citar de memória)

- Ações/FIIs B3: statusinvest.com.br, fundamentus.com.br (cruzar quando divergirem)
- Tesouro Direto: tesourodireto.com.br (taxas do dia)
- CDB/LCI/LCA: plataformas das corretoras do usuário
- Internacional: página oficial do ETF (TER e composição)

Declarar a data de coleta em toda shortlist. Dados de fechamento ≠ dados intraday — não misturar sem avisar.
