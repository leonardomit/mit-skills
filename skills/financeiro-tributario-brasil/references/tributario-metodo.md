# Análise tributária — método

Módulo de método, não de tabela. A legislação muda todo mês e o país está em transição de sistema (2026–2033). Uma alíquota lembrada de memória é o erro mais provável e mais caro. Este módulo ensina o raciocínio e obriga a buscar o número vigente com fonte e data.

**Arquivos de apoio:**
- `tributario-armadilhas.md` — 24 erros recorrentes, como detectar cada um e exemplo. **Leia antes de concluir qualquer análise.**
- `tributario-fontes.md` — onde verificar cada tipo de número, com links oficiais.
- `tributario-setores.md` — perguntas a pesquisar por setor.
- `decisao-regime-comparativo.md` — fórmulas do ponto de indiferença Presumido × Real.

## Princípios

1. **Nenhum número sem fonte.** Toda alíquota, limite, MVA, percentual de presunção ou prazo sai de uma busca feita na sessão, com link e data de vigência. Se não foi possível confirmar, escreva "não verificado" em vez de preencher. Um campo vazio custa uma pergunta; um campo errado custa um auto de infração.
2. **Comece pela data.** Confirme a data atual antes de tudo. A resposta certa em 2026 é errada em 2027.
3. **A descrição do produto manda, não o código.** NCM, NBS e CNAE são consequência da natureza da mercadoria ou do serviço. Benefícios seguem a descrição legal. Classificação fiscal é responsabilidade do contribuinte; aponte quando for duvidosa.
4. **Operação, não empresa.** Tributa-se cada operação: quem vende, para quem (contribuinte ou não, consumo final ou revenda), de onde para onde, o quê, e com que origem (nacional ou importado). Uma empresa tem várias respostas.
5. **Crítica antes de validação.** Abra pela premissa mais fraca ou pelo maior risco — inclusive os seus, de análises anteriores. Conclusão errada em análise passada se corrige de forma nominal, não silenciosa.
6. **Conta em código, nunca de cabeça.** Toda aritmética roda em código, com fórmulas e premissas visíveis. Erro de multiplicação em base presumida já custou análise inteira.
7. **Proporcionalidade.** Pergunta simples = uma busca e resposta direta. Análise completa = buscas dirigidas ao que move o número. Não transforme consulta de CFOP em relatório de nove seções.
8. **Limite do papel.** A análise orienta decisão e prepara a conversa com contador ou advogado. Não substitui parecer formal nem consulta à SEFAZ ou à Receita. Diga isso uma vez, no fim.

## Passo 1 — Coleta mínima

Antes de analisar, tenha em mãos (pergunte só o que faltar; consulte memória, ERP e arquivos antes de perguntar):

- Regime atual: Simples Nacional (anexo), Lucro Presumido, Lucro Real, MEI
- CNAE principal e secundários; **atividade real exercida**
- UF e município do estabelecimento; filiais
- O que vende: NCM (mercadoria) ou NBS / item da LC 116 (serviço)
- Para quem: B2B, B2C, governo, exterior; contribuinte de ICMS ou não
- Para onde: interno, interestadual (quais UFs), exportação
- Origem da mercadoria: nacional, importada, conteúdo de importação
- Faturamento dos últimos 12 meses (e RBT12) e folha de pagamento
- Margem aproximada e principais insumos (decide Presumido × Real e créditos)
- Benefícios fiscais, regimes especiais, TTD, inscrições de substituto em outras UFs
- Canal: loja própria, marketplace, full/fulfillment, representante

**Pergunta de triagem obrigatória:** o modelo operacional declarado bate com o modelo real? (armadilha 12).

Se faltar dado essencial, pare e pergunte em uma mensagem só. Se for acessório, siga com premissa explícita.

### Documentos a pedir quando houver análise de carga ou de regime

Dado solto não sustenta conclusão sobre carga. Peça o documento.

**Sempre:** contrato social consolidado · demonstrativos de faturamento mensal (3 anos) · DRE e Balanço (2–3 exercícios) · balancete analítico do último exercício.

**Simples:** PGDAS-D de todos os meses · DEFIS do último ano-calendário · extrato do Simples no e-CAC.

**Presumido / Real:** SPED Fiscal (EFD ICMS/IPI) mensal · EFD Contribuições mensal · DCTF/DCTFWeb + DARFs (IRPJ, CSLL, PIS, COFINS) · ECD e ECF · guias de ICMS e GNRE de DIFAL/ST por estado.

**Folha:** resumos mensais · GPS/FGTS · eSocial.
**Comércio exterior:** DIs, faturas, consulta de capacidade financeira no e-CAC.
**Setorial:** registros ou notificações do órgão regulador (ANVISA, MAPA, ANP, ANS, ANTT).

Documento que o cliente diz ter mas não enviou é pendência bloqueante, não premissa. Liste em tabela de dados faltantes dizendo o que cada um destrava.

## Passo 2 — Mapa de tributos por operação

Percorra na ordem. Para cada tributo: incide? base? alíquota? código (CST/CSOSN/CFOP/cClassTrib)? quem recolhe e quando? fonte?

**Consumo — sistema em extinção**
- ICMS: alíquota interna da UF de origem; interestadual por destino **e por origem da mercadoria**; redução de base; isenção; diferimento; crédito presumido; FCP/FECP
- ICMS-ST: há convênio ou protocolo entre as duas UFs para aquele NCM/CEST? MVA original e ajustada; quem é o substituto; antecipação na entrada
- DIFAL: venda a não contribuinte em outra UF; venda a contribuinte para uso, consumo ou ativo; base única ou dupla conforme a UF; forma de recolhimento
- IPI: produto industrializado ou equiparado? alíquota na TIPI vigente, **inclusive Ex-tarifário**; situação pós-reforma
- ISS: item da LC 116, município competente, alíquota municipal, retenção pelo tomador
- PIS/COFINS: cumulativo ou não cumulativo, monofásico, alíquota zero, ST, créditos admitidos; conferir vigência na data

**Consumo — sistema novo**
- CBS, IBS e Imposto Seletivo: CST e cClassTrib corretos, regime diferenciado ou específico do setor, redução de alíquota, crédito, split payment

**Renda e folha**
- IRPJ e CSLL: presunção da atividade ou lucro real; **adicional de 10%**; receitas que entram sem presunção
- Distribuição de lucros: regra de IRRF vigente, limiar, transição, capitalização
- INSS patronal, RAT×FAP, terceiros, CPRB/desoneração, Fator R no Simples (só para serviço)

**Comércio exterior**
- Importação: II, IPI, PIS/COFINS-importação ou CBS/IBS, ICMS-importação, AFRMM, regimes especiais, habilitação no RADAR
- Exportação: imunidades, manutenção de créditos, ressarcimento

## Passo 3 — Pesquisa obrigatória

Ordem de confiança (detalhe e links em `tributario-fontes.md`):

1. **Texto legal** — Planalto (leis e LCs), CONFAZ (convênios, protocolos, ajustes SINIEF), RICMS da UF, lei municipal do ISS
2. **Órgão** — Receita Federal (INs, ADEs, Soluções de Consulta COSIT), SEFAZ estadual (respostas a consultas), CGIBS, Comitê Gestor do Simples, Portal da NF-e (notas técnicas)
3. **Jurisprudência vinculante** — STF e STJ (repercussão geral e repetitivos)
4. **Consultorias e blogs** — só como pista para achar a norma. Nunca como fonte final.

Busque sempre com o ano corrente. Faça buscas separadas por UF em operação interestadual. Quando duas fontes divergirem, vá ao texto legal e diga qual prevaleceu. Para cada número registre: norma, artigo, vigência, link.

**Rótulos de confiança**, usados em cada linha da análise:
- **Confirmado** — norma localizada e lida na sessão
- **Regra geral** — princípio estável, número específico não conferido
- **Não verificado** — não foi possível confirmar; exige validação

Estimativa é marcada como estimativa, com a premissa ao lado. Certo: `~R$ 62K (estimado: receita do 2º tri × presunção 8%/12%)`. Errado: `R$ 62K`.

## Passo 4 — Reforma tributária (checagem obrigatória)

Toda análise informa em que fase da transição a operação está. Marcos da EC 132/2023 e LC 214/2025, **a reconfirmar na data** porque regulamentos e prazos vêm sendo ajustados:

- **2026** — fase de teste; CBS e IBS destacados em alíquota simbólica; apuração informativa; dispensa de recolhimento **condicionada** ao cumprimento das obrigações acessórias; tributos antigos integrais
- **2027** — CBS em cobrança efetiva; PIS e COFINS extintos; IPI zerado na maior parte dos produtos (exceto ZFM); Imposto Seletivo; IBS ainda em teste; Simples passa a destacar
- **2029–2032** — ICMS e ISS caem em degraus; IBS sobe; benefícios estaduais encolhem na mesma proporção
- **2033** — ICMS e ISS extintos

Responda sempre:
- A análise vale para qual período? Se cruza virada de ano, entregue os dois cenários.
- O setor tem regime diferenciado, específico ou alíquota reduzida no sistema novo? Mapa formal NCM/NBS × Anexo da LC 214.
- Benefício de ICMS em uso sobrevive até quando? Há compensação prevista?
- Simples: recolher CBS/IBS por dentro ou por fora (híbrido)? Impacto no crédito do cliente B2B.
- Preço e contratos de longo prazo têm cláusula de repasse?
- Saldos credores de PIS/COFINS e ICMS: como serão aproveitados até 2032?
- Split payment: efeito no capital de giro.
- **Fornecedores do Simples** geram crédito limitado ao efetivamente cobrado. Mapear e renegociar.
- **Risco comercial no B2B:** o cliente vai perceber que o crédito dele aumentou e pedir desconto. A reforma é neutra na cadeia, não na mesa de negociação.

> Converter antes de comparar: tributo atual é por dentro, IBS/CBS é por fora. Carga por dentro de X% equivale a X/(1−X) por fora (armadilha 11).

## Passo 5 — Módulos setoriais

Leia o módulo do setor em `tributario-setores.md` e some ao mapa do Passo 2.

## Passo 6 — Comparação de regimes e carga efetiva

Quando a pergunta for "qual regime" ou "quanto pago":

- Simule Simples (anexo e faixa efetiva), Presumido e Real com os dados do Passo 1.
- **Toda conta em código.** Mostre fórmulas e premissas.
- **Comparação like-for-like obrigatória** (armadilha 6): o DAS do Simples inclui a CPP patronal; no regime normal a CPP migra para GPS e aparece a contribuição a terceiros, que não existia. Compare tributos sobre receita **mais** encargos patronais nos dois lados. Sem isso, não escreva "economia".
- Inclua créditos ganhos ou perdidos e o efeito no preço do cliente B2B.
- Verifique limites, vedações, **sublimite × teto** (armadilha 5) e prazo de opção na data.
- Mostre o **ponto de virada** — faturamento ou margem em que o regime troca de vencedor.
- Entregue **matriz de sensibilidade**: margem (3 cenários) × volume de importação (2–3 cenários). Não um número único.
- Rode o cenário do ano seguinte com as regras da reforma.

> **Presumido × Real muda de natureza em 2027.** A CBS é não cumulativa para todos os regimes: o eixo PIS/COFINS some da comparação, créditos de importação deixam de ser exclusivos do Real, e a decisão passa a ser quase só IRPJ/CSLL (break-even na margem real pré-IR). Refaça qualquer comparação feita antes disso.

## Passo 7 — Parametrização (quando pedido)

Para ERP, emissor de NF-e ou planilha de regras de marketplace:

- Leia o layout ou a documentação do sistema antes de preencher. Respeite formato, listas fechadas e separador decimal.
- Uma linha por combinação: tipo de destinatário × UF × origem da mercadoria.
- Campos de benefício, alíquota efetiva, MVA e desoneração ficam vazios ou zerados se não houver norma que os justifique. Cite a norma quando preencher.
- Preencha os campos da reforma (CST e cClassTrib de IBS/CBS) conforme a tabela oficial vigente.
- Entregue junto a lista "validar com o contador" e a data de validade da regra.

## Passo 8 — Riscos e regularização

Classifique em 🔴 Alta / 🟡 Média / 🟢 Baixa por **exposição × iminência**, não por gravidade teórica.

| # | Risco | Exposição estimada | Prazo | Ação |
|---|---|---|---|---|

Para todo passivo já constituído, avalie **denúncia espontânea** (art. 138 do CTN): recolher antes de qualquer procedimento fiscal afasta a multa de ofício, restando principal, multa de mora e juros. Quantifique regularizar agora × risco de autuação.

Separe sempre:
- **Erros de execução** (contabilidade/escritório) — tom de correção
- **Decisões pendentes dos sócios** — tom de encaminhamento

Isso muda a reunião de cobrança para construção e preserva o contador como aliado.

## Estrutura da entrega

Frases curtas. Tabela onde houver comparação.

```
# Análise tributária — [empresa/operação] — [data]

## 1. Veredito
Três frases: maior risco, conclusão, ação imediata.

## 2. Premissas e lacunas
O que foi assumido. O que falta. Premissa mais fraca primeiro.
Correções a análises anteriores, se houver.

## 3. Enquadramento
Regime, CNAE, NCM/NBS, UF/município, fase da reforma.

## 4. Tributos por operação
Tabela: operação | tributo | base | alíquota | código | confiança | fonte

## 5. Carga efetiva e comparação de regimes
Só quando aplicável. Com fórmulas. Like-for-like.

## 6. Reforma tributária
O que muda, quando, e o que fazer agora.

## 7. Riscos e pontos cegos
Ordenados por impacto financeiro. Inclui o que a análise não cobre.

## 8. Próximos passos
Ações, responsável sugerido, o que levar ao contador ou advogado.

## 9. Dados faltantes
O que falta e o que cada item destrava.

## 10. Fontes
Norma, artigo, vigência, link. Data da consulta.
```

Pergunta simples (uma alíquota, um CFOP) recebe resposta direta com fonte e rótulo de confiança, sem o relatório inteiro.

## Checklist antes de entregar

- [ ] Toda alíquota tem rótulo de confiança e fonte
- [ ] `tributario-armadilhas.md` percorrido
- [ ] Comparação entre regimes é like-for-like
- [ ] Aritmética rodada em código, não de cabeça
- [ ] Estimativas marcadas como estimativa, com premissa
- [ ] Erros de análises anteriores corrigidos nominalmente
- [ ] Prazos citados confirmados como vigentes
- [ ] Dados faltantes listados com o que destravam
- [ ] Validade da análise declarada
- [ ] Ressalva: não substitui parecer de profissional habilitado

## Frases proibidas

| Não escreva | Porque |
|---|---|
| "Economia comprovada de X%" | Só com base like-for-like |
| "A carga é de X%" a partir dos SPEDs | Falta IRPJ/CSLL |
| "O regime X é favorável, confirmado" | Depende de margem real e base creditável |
| "Aumentar capital para habilitar RADAR" | Critério é capacidade financeira |
| "Estimativa mensal de IRPJ no Presumido" | No Presumido a apuração é trimestral |
| "A reforma aumenta a carga em X p.p." | Sem converter por dentro/por fora e sem créditos |
| "Esse NCM não tem ST" | Sem checar protocolo entre as duas UFs |
