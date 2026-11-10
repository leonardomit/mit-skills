# Armadilhas — 24 erros recorrentes em análise tributária brasileira

Cada entrada tem: **o erro** · **por que acontece** · **como detectar** · **exemplo** (quando houver) · **ação correta**.

Os exemplos são ilustrativos e não trazem dados de nenhuma empresa.

---

# A. Regime e apuração

## 1. Fator R não se aplica a comércio e indústria

**O erro.** Montar tese de recolhimento a maior, ou de restituição, por "Fator R não aplicado" em empresa industrial ou comercial no Simples.

**Por que acontece.** O Fator R (folha ÷ RBT12 ≥ 28%) é muito citado e pouco delimitado. Quem vê folha alta e DAS alto assume que há tese.

**Como detectar.** Olhe o anexo. Fator R só desloca atividade de **serviço** do Anexo V para o Anexo III. Anexos I (comércio) e II (indústria) não são alcançados, qualquer que seja a razão folha/receita.

**Exemplo.** PGDAS-D declarando folha zerada em indústria com empregados ativos. A leitura apressada é "Fator R não aplicado, pode haver recolhimento a maior". Errada: no Anexo II não há tese financeira nenhuma.

**Ação correta.** Em comércio e indústria, a folha omitida no PGDAS-D é **inconsistência declaratória**, não recolhimento a maior. Risco real: malha por cruzamento PGDAS-D × eSocial × DCTFWeb. Avaliar retificação pelo saneamento, não pela restituição.

---

## 2. Lucro Presumido é apuração trimestral

**O erro.** Perguntar ao contador se "a estimativa mensal de IRPJ está sendo recolhida" em empresa no Presumido.

**Por que acontece.** Confusão com o Lucro Real anual, onde a estimativa mensal existe.

**Como detectar.** No Presumido a apuração é **sempre trimestral**. Vencimento no último dia útil do mês seguinte ao fim do trimestre. Quota única ou três quotas com Selic.

**Exemplo.** Dossiê que pergunta ao contador se a estimativa mensal está sendo recolhida. A pergunta certa é: o IRPJ/CSLL do trimestre foi apurado e recolhido no vencimento? A pergunta errada expõe desconhecimento e dá margem ao contador.

**Ação correta.** Pergunte por trimestre, peça DARF e memória de cálculo, confira os códigos (IRPJ e CSLL do Presumido têm códigos próprios — confirme os vigentes).

---

## 3. Adicional de 10% de IRPJ

**O erro.** Projetar IRPJ do Presumido como `base presumida × 15%` e parar aí.

**Por que acontece.** O adicional é fácil de esquecer porque não aparece como alíquota própria.

**Como detectar.** Incide 10% sobre a parcela da base presumida que exceder R$ 60.000 por trimestre (R$ 20.000/mês). Com receita trimestral acima de ~R$ 750K em atividade de presunção 8%, o adicional já existe.

**Exemplo.** Projeção anual que ignora o adicional e ainda aplica alíquota errada sobre a base presumida. Dois erros somados subdimensionam o IRPJ/CSLL de forma material.

**Ação correta.** Rode em código. Fórmula: `IRPJ = base×15% + max(0, base − 60.000)×10%`.

---

## 4. Receitas que entram sem presunção

**O erro.** Aplicar a presunção sobre tudo que entra na conta.

**Por que acontece.** O raciocínio "receita × presunção" vira automático.

**Como detectar.** Receitas financeiras, descontos obtidos, aluguéis e ganhos de capital entram **integralmente** na base do Presumido, sem presunção. Verifique no balancete se existem e se estão sendo somadas.

**Ação correta.** Peça o razão das contas de receita não operacional e confira contra a memória de cálculo do trimestre.

---

## 5. Sublimite não é teto

**O erro.** Tratar os dois limites do Simples como um só, ou acreditar que estourar limite é escolha.

**Por que acontece.** Ambos são "limites do Simples" e os valores são próximos na conversa informal.

**Como detectar.** São efeitos distintos:
- **Sublimite de ICMS/ISS** estourado → no ano seguinte o ICMS/ISS sai do DAS e passa à apuração normal, **mantendo o resto no Simples**
- **Teto geral** estourado em mais de 20% → exclusão **no mês seguinte** ao excesso, com recálculo retroativo

Confirme os valores vigentes na LC 123/2006 atualizada. Não de memória.

**Exemplo.** Empresa fecha o ano acima do sublimite e, no ritmo de faturamento do ano seguinte, cruzaria o teto em poucos meses. A migração para o Presumido em janeiro **não é escolha vantajosa, é saída compulsória bem executada**. Apresentar como "decisão que gerou economia" distorce o histórico e enfraquece a análise.

**Ação correta.** Projete RBT12 mês a mês contra os dois limites. Quando a saída for compulsória, diga isso: o mérito está em ter transicionado de forma planejada, não em economia.

---

# B. Carga efetiva e comparação

## 6. Comparação entre regimes precisa ser like-for-like

**O erro — o mais grave da lista.** Comparar a alíquota efetiva do DAS com os tributos do regime normal e anunciar economia.

**Por que acontece.** O DAS é um número só e parece comparável a uma soma de tributos. Não é.

**Como detectar.** Três assimetrias:
1. O DAS **inclui a CPP patronal**; no regime normal ela migra para GPS e some da conta de "tributos"
2. No regime normal **aparece a contribuição a terceiros** (Sistema S, ~5,8% da folha) que **não existia** no Simples — custo novo, estrutural
3. O ICMS no Simples é percentual da faixa; no normal é débito cheio menos créditos

**Exemplo.** Análise anuncia "economia comprovada" comparando a carga do Presumido — sem IRPJ/CSLL **e** sem encargos patronais — com a alíquota efetiva do DAS, que inclui a CPP. Refeita em base comparável, a carga fica **igual ou levemente superior**. A economia não existia.

**Ação correta.** Monte duas tabelas. A primeira: tributos sobre receita. A segunda: a primeira **mais** encargos patronais (INSS 20% + RAT×FAP + terceiros + FGTS). Só a segunda pode ser comparada com o DAS. Sem ela, a palavra "economia" não aparece no texto.

---

## 7. SPED não mostra IRPJ/CSLL

**O erro.** Somar os tributos que aparecem nos SPEDs e chamar aquilo de carga tributária.

**Por que acontece.** Os SPEDs são os documentos mais completos que chegam às mãos do analista. Parecem exaustivos.

**Como detectar.** SPED Fiscal traz ICMS e IPI. EFD Contribuições traz PIS e COFINS. **IRPJ e CSLL não estão em nenhum dos dois** — estão em DCTF e DARF, porque a apuração é trimestral.

**Exemplo.** Carga calculada somando PIS, COFINS, ICMS e DIFAL dos SPEDs de alguns meses. Falta todo o IRPJ/CSLL — pontos percentuais inteiros da receita.

**Ação correta.** Carga tributária só fecha com DCTF/DARF na mão. Enquanto não chegarem, escreva "parcial — falta IRPJ/CSLL" no título da tabela.

---

## 8. Primeiro mês distorce o run-rate

**O erro.** Tirar média dos meses disponíveis e anualizar.

**Por que acontece.** A média é o gesto mais natural com uma série curta.

**Como detectar.** O primeiro mês de um regime novo carrega: crédito de ICMS sobre estoque de transição, saldos credores herdados, ajustes de abertura. Nenhum se repete.

**Exemplo.** O primeiro mês após a saída do Simples gera saldo credor de ICMS pelo crédito sobre o estoque. A média do período fica bem abaixo do run-rate dos meses seguintes; anualizar pela média subestima o ICMS.

**Ação correta.** Calcule o run-rate a partir do segundo ou terceiro mês e **diga qual base usou**. Reporte os dois números quando a diferença for material.

---

## 9. Apuração que não fecha na conta simples

**O erro.** Aceitar `débitos − créditos = a recolher` sem conferir.

**Por que acontece.** É a conta que todo mundo espera. Quando não bate, é fácil atribuir a arredondamento.

**Como detectar.** Diferença entre o esperado e o apurado aponta para ajustes nos registros **E110/E111**: estornos de crédito ou débito, outros débitos, benefícios, transferências de saldo.

**Exemplo.** Diferença positiva num mês e negativa no seguinte, nenhuma explicada nos resumos. Podem ser crédito a recuperar **ou** passivo oculto — não se sabe sem o detalhe.

**Ação correta.** Peça o detalhe do E110/E111 sempre que a conta não fechar. Nunca arredonde a diferença para dentro da análise.

---

## 10. Encargos de folha: retenção não é custo

**O erro.** Dizer que os encargos somam 47–48% sobre os proventos.

**Por que acontece.** O resumo de folha soma, numa coluna só, o INSS **retido do empregado** (que é dele, não custo da empresa) com o encargo patronal.

**Como detectar.** Separe: patronal 20% + RAT×FAP + terceiros + FGTS 8%. O que é descontado do empregado não entra.

**Ação correta.** Custo marginal real de contratação ≈ salário × **1,47 a 1,55**, já incluindo provisões de 13º e férias. Use esse multiplicador para dimensionar contratação, não o percentual do resumo de folha.

---

## 11. Por dentro × por fora

**O erro.** Comparar a carga atual com a alíquota de referência da reforma e anunciar aumento de vários pontos.

**Por que acontece.** Os dois números aparecem como percentuais e parecem da mesma natureza. Não são: ICMS, PIS e COFINS são **por dentro** (embutidos no preço); IBS e CBS são **por fora**.

**Como detectar.** Converta antes de comparar. Carga por dentro de X% equivale a `X/(1−X)` por fora. Exemplo: 21,7% por dentro ≈ **27,7% por fora** — mesma ordem de grandeza da alíquota de referência estimada do sistema novo (confirmar o número vigente).

**Exemplo.** Concluir "pressão de vários p.p. no preço B2C" por confundir impacto **relativo** (o produto fica caro *em relação a* itens que vão a alíquota zero ou reduzida) com impacto **absoluto** (quase neutro, na mesma base). A correção muda a conclusão do relatório.

**Ação correta.** Toda comparação de carga antes/depois roda em código, com as duas bases explicitadas. E compare carga efetiva sobre **valor agregado**, não sobre receita bruta — porque o crédito muda de limitado para amplo.

---

# C. Operação e enquadramento

## 12. Industrialização por encomenda não é fabricação por contrato

**O erro.** Tratar produção white label como industrialização por encomenda — ou o contrário.

**Por que acontece.** Comercialmente, os dois são "fabricar para terceiro". Fiscalmente, são operações distintas.

**Como detectar.** A pergunta é uma só: **quem compra a matéria-prima?**
- Empresa compra a MP, industrializa e entrega produto acabado com marca do cliente → **venda de produto industrializado**. Presunção 8%/12%, CFOP de venda (5.101/6.101), IPI e ICMS destacados, sem discussão de ISS.
- Cliente **remete** a MP e a empresa só transforma → **industrialização por encomenda**. CFOP 5.124/6.124, remessa e retorno, discussão ISS × ICMS, presunção de 32% em certas leituras.

**Exemplo.** Parte relevante da receita vem de produção com marca do cliente e MP comprada pela própria indústria. Classificar como serviço (presunção 32%) em vez de produto (8%) quadruplica a base presumida de IRPJ sobre essa receita.

**Ação correta.** Confirme no contrato, não na conversa. Blindagem: contrato escrito explicitando que a indústria adquire os insumos por conta própria e vende produto acabado. É a melhor defesa documental contra reclassificação.

---

## 13. NCM com Ex-tarifário

**O erro.** Ler a alíquota geral do NCM na TIPI e parar.

**Por que acontece.** O Ex-tarifário aparece como linha subordinada e é fácil de passar batido.

**Como detectar.** Vários NCMs têm alíquota geral **e** exceção (Ex 01) com alíquota zero, condicionada a critério técnico — diluição, composição, destinação, teor.

**Exemplo.** NCM com alíquota positiva na regra geral e **0% no Ex 01**, condicionado a critério técnico (por exemplo, grau de diluição). Sem ficha técnica por SKU, não dá para afirmar qual se aplica. SPED com IPI zero pode estar correto para parte do portfólio e indeterminado para o restante.

**Ação correta.** Exija ficha técnica ou laudo por SKU. A descrição comercial não resolve. Se houver tributo devido, considere denúncia espontânea antes de qualquer procedimento fiscal.

---

## 14. A descrição manda, não o código

**O erro.** Classificar pelo que o produto é chamado, ou herdar o NCM do fornecedor.

**Por que acontece.** O código parece objetivo. Mas ele é consequência da natureza do produto, não causa.

**Como detectar.** Em alimentos, suplementos, cosméticos e farma, a fronteira entre capítulos muda tudo: ICMS, ST, PIS/COFINS, benefício na reforma. O critério vinculante costuma ser **finalidade declarada e registro regulatório**: registro como medicamento → Capítulo 30; notificação como suplemento alimentar → Capítulo 21.

**Exemplo.** A RFB reclassifica um grupo de produtos para outro código NCM. O benefício estadual redigido para o código antigo vira disputa: acompanha ou não a reclassificação? Há resposta de SEFAZ no sentido de que o benefício segue a **descrição**, não o código — confirme na UF em questão.

**Ação correta.** Garanta coerência entre NCM fiscal, registro sanitário e descrição na NF-e. Divergência entre os três gera retenção na aduana e glosa de benefício. Classificação errada que resulte em recolhimento menor expõe a lançamento de ofício.

---

## 15. DIFAL calculado não é DIFAL recolhido

**O erro.** Ver o DIFAL apurado no SPED e concluir que está sendo pago.

**Por que acontece.** O SPED calcula para todos os destinos. O recolhimento, porém, depende de GNRE emitida estado a estado — processo separado, manual, fácil de furar.

**Como detectar.** Olhe o campo **"valor a recolher"** linha a linha, UF por UF. Zerado em estados com venda significa passivo.

**Exemplo.** O SPED calcula DIFAL para dezenas de UFs; GNRE recolhida, só para duas ou três. O passivo cresce todo mês. Achado mais comum em e-commerce.

**Ação correta.** Levante o passivo por estado. Avalie **denúncia espontânea** (art. 138 CTN) antes de qualquer fiscalização — afasta a multa de ofício de 50–150%, restando principal, mora e Selic. Verifique FECP e estados que exigem inscrição de remetente. Parametrize o ERP para emitir GNRE automática por venda B2C interestadual.

---

## 16. ST sem checar protocolo entre as duas UFs

**O erro.** Afirmar que um NCM "não tem ST" com base na regra de um estado.

**Por que acontece.** A consulta costuma ser feita na UF de origem, e a resposta é tomada como geral.

**Como detectar.** ST interestadual depende de **convênio ou protocolo entre as duas UFs específicas** para aquele NCM/CEST, e a mercadoria precisa se enquadrar cumulativamente na **descrição e** na classificação. Mesmo NCM pode ter ST em uma UF e não em outra.

**Ação correta.** Pesquise por par de UFs, não por produto. Confirme no CONFAZ e no RICMS do destino. Em caso de dúvida, resposta a consulta da SEFAZ de destino é a fonte.

---

## 17. Origem importada muda a alíquota interestadual

**O erro.** Aplicar a alíquota interestadual padrão sem olhar a origem da mercadoria.

**Por que acontece.** O campo de origem no cadastro é preenchido uma vez e esquecido.

**Como detectar.** Mercadoria importada, ou com conteúdo de importação acima do limite, tem alíquota interestadual própria (Resolução do Senado 13/2012). O código de origem no cadastro do produto (0 a 8) governa isso.

**Ação correta.** Audite o campo de origem no cadastro de produtos. Para mercadoria com insumo importado, calcule o Conteúdo de Importação e verifique obrigação de FCI.

---

## 18. Contribuinte × não contribuinte

**O erro.** Aplicar a regra de um ao outro.

**Por que acontece.** Em e-commerce misto, a mesma SKU sai para os dois públicos no mesmo dia.

**Como detectar.** Muda DIFAL (existe para não contribuinte; para contribuinte só em uso, consumo ou ativo), muda ST, muda responsabilidade pelo recolhimento, muda CFOP.

**Ação correta.** Parametrize por **tipo de destinatário × UF × origem**, uma linha por combinação. Não por produto.

---

# D. Fontes e vigência

## 19. Alíquota interna de ICMS de memória

**O erro.** Preencher a alíquota modal das 27 UFs de cabeça.

**Por que acontece.** Parece conhecimento estável. Não é: estados reajustam a modal com frequência, e há adicional de FCP/FECP em vários.

**Como detectar.** Se o número não veio de busca feita nesta sessão, ele é "não verificado".

**Ação correta.** Busque por UF, com o ano corrente, no RICMS ou no portal da SEFAZ. Registre vigência. Numa tabela de 27 linhas, marque cada uma com o rótulo de confiança.

---

## 20. Benefício de outra UF, ou que exige regime especial

**O erro.** Aplicar ao cliente analisado um benefício que existe, mas não para ele.

**Por que acontece.** Benefício encontrado em pesquisa parece disponível a todos.

**Como detectar.** Duas perguntas: (a) o benefício é da UF **do contribuinte**? (b) exige **TTD, regime especial ou habilitação prévia** que ele não tem?

**Exemplo.** Concorrentes de outra UF operam com crédito presumido nas saídas interestaduais, via TTD estadual. A empresa analisada não tem acesso a isso — mas o benefício dos concorrentes **derrete** na transição da reforma, o que é reequilíbrio competitivo a favor de quem nunca dependeu de incentivo. Benefício alheio é informação competitiva, não oportunidade fiscal.

**Ação correta.** Antes de citar benefício, confirme UF, requisito formal e vigência pós-reforma.

---

## 21. Base de um tributo incluindo outro

**O erro.** Montar base de cálculo ignorando teses judiciais vigentes sobre exclusão.

**Por que acontece.** O tema muda com decisões do STF e STJ, e a modulação define quem aproveita e desde quando.

**Como detectar.** Sempre que a base de um tributo contiver outro, verifique se há tema de repercussão geral ou repetitivo decidido, e qual a modulação.

**Ação correta.** Consulte o andamento no STF/STJ antes de afirmar. Se houver tese favorável não aproveitada, é oportunidade a levar ao advogado — não algo a aplicar sozinho na apuração.

---

# E. Comércio exterior e sócios

## 22. RADAR não depende de capital social

**O erro.** Dizer que importação acima de certo valor está bloqueada pelo capital social baixo.

**Por que acontece.** Era assim na regra antiga, e a informação envelhecida circula muito.

**Como detectar.** Desde a **IN RFB 1.984/2020**, as modalidades (Expressa, Limitada, Ilimitada) são definidas pela **capacidade financeira estimada** — calculada a partir dos recolhimentos federais dos últimos anos e consultável no e-CAC.

**Exemplo.** Diagnóstico afirma que o capital social baixo bloqueia a modalidade superior do RADAR. Com histórico relevante de recolhimentos federais, a empresa pode **já se qualificar** para a modalidade acima da Expressa. A recomendação errada atrasaria a importação direta em meses e por nada.

**Ação correta.** Consulte a capacidade financeira no e-CAC **antes** de qualquer recomendação de aumento de capital. Aumentar capital continua útil por outros motivos — crédito bancário, governança, base futura de JCP — nunca por esse.

---

## 23. PIS/COFINS-Importação viram custo no Presumido

**O erro.** Calcular a parcela irrecuperável da importação como II + AFRMM.

**Por que acontece.** Esquece-se que o crédito de PIS/COFINS só existe no regime não cumulativo.

**Como detectar.** No Presumido (cumulativo), PIS/COFINS-Importação (**11,75%** sobre o valor aduaneiro) **não geram crédito** — são custo definitivo.

| Parcela irrecuperável sobre CIF | Presumido (até 2026) | Real |
|---|---|---|
| II + AFRMM | ~10–17% | ~10–17% |
| + PIS/COFINS-Imp sem crédito | **~23–29%** | — |

**Exemplo.** Análise projeta economia relevante na importação direta contando só II + AFRMM como parcela irrecuperável. Com os 11,75% somados, a vantagem encolhe ou desaparece em vários insumos.

**Ação correta.** Refaça a conta de importar × comprar nacional com a parcela certa. **E note o prazo:** em 2027 a CBS-Importação passa a ser creditável em qualquer regime — a restrição some, e a importação direta fica viável no Presumido sem migrar de regime. Pilotar em 2026, escalar em 2027.

---

## 24. Dividendos e capitalização

**O erro.** Repetir "projeto de lei pode tributar dividendos" sem verificar o que foi aprovado — ou aplicar a regra nova sem olhar a transição.

**Por que acontece.** O tema esteve anos em tramitação e a memória guarda o projeto, não a lei.

**Como detectar.** Verifique na sessão: existe IRRF sobre dividendos vigente? Qual o **limiar mensal por beneficiário, por empresa**? Há regra de transição para lucros apurados em exercícios anteriores com distribuição deliberada até a data de corte?

**Exemplo.** Relatório alerta para "projeto que pode tributar dividendos" e estima impacto anual. A regra efetivamente vigente usa limiar mensal por beneficiário, e os sócios recebem abaixo dele: **impacto zero** no padrão de distribuição. O alerta era ruído, não risco.

**Ação correta.** Verifique a lei vigente e o número dela antes de citar. Sobre capitalização de lucros: não é distribuição, não há IR (art. 10 da Lei 9.249/95) — **mas há trava**: redução de capital nos anos seguintes é tratada como distribuição disfarçada. Os sócios precisam saber disso antes de decidir o valor.

---

# Resumo operacional

Antes de fechar qualquer análise, três perguntas eliminam a maior parte dos erros acima:

1. **Esse número veio de onde?** Se não veio de busca nesta sessão ou de documento do cliente, ele é "não verificado".
2. **Estou comparando as mesmas coisas?** Like-for-like entre regimes; por dentro × por fora entre sistemas; carga sobre receita × sobre valor agregado.
3. **Quem compra a matéria-prima, quem é o destinatário, de qual UF para qual UF?** Tributa-se a operação, não a empresa.
