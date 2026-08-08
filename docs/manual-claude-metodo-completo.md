# Manual Completo: Método de Trabalho com Claude como Orquestrador de Agentes com Loops

## Visão Geral

Este manual consolida o método de trabalho desenvolvido internamente pela Anthropic, aplicado por Dario Amodei em seu fluxo diário e expandido com os padrões de loop de autoanálise. O princípio central é a mudança de papel: **você para de ser executor e passa a ser editor e arquiteto**. O Claude gera, autorreavalia e melhora antes de entregar. Subagentes especializados recebem micro-tarefas em contextos isolados. O Claude principal orquestra, consolida e decide.

Este manual está adaptado para a empresa: suplementos, ANVISA, operação B2B/B2C, automação e delegação de processos.

---

## Parte 1: Fundamentos do Método

### 1.1 Os três pilares

#### Pilar 1 — Mudança de papel

Dario Amodei revelou que engenheiros da Anthropic pararam de escrever código manualmente. Um engenheiro sênior ficou dois meses sem digitar uma linha de código, apenas revisando o que o Claude Code entregava. O mesmo princípio se aplica a qualquer função: redatores que não redigem, analistas que não montam planilhas, gerentes que não escrevem SOPs.

| Antes | Depois |
|---|---|
| Você cria o rascunho | Claude cria, você revisa |
| Você pesquisa e escreve | Claude pesquisa, você valida |
| Você digita código ou doc | Claude produz, você edita os 10% críticos |
| Contexto reiniciado a cada conversa | Contexto fixo em Projetos, só a tarefa muda |
| Claude responde impulsivamente | Claude pensa em etapas, se audita e entrega versão final |

#### Pilar 2 — Contexto persistente em Projetos

A diferença entre usuário comum e usuário de alto impacto é o uso de **Projetos no Claude**. Um Projeto carrega contexto fixo em toda conversa: empresa, regras, normas, portfólio, tom. Você não reexplica nada. A cada nova tarefa, injeta apenas o contexto variável.

Estrutura recomendada para a empresa:

| Projeto | Contexto fixo | Para que serve |
|---|---|---|
| Regulatório ANVISA | RDC 843/2024, modelo de rótulo, restrições de claim, Lei 10.357 | Laudos, rótulos, respostas fiscalização |
| Comercial | Portfólio, tabela de preços, condições private label | Propostas, e-mails, contratos |
| Processos | SOPs, fluxos BPF/HACCP, padrões internos | Documentação, checklists, treinamentos |
| Automação | Stack Node.js/Python, integrações ERP/Bling | Scripts, lógica, integrações ERP |

#### Pilar 3 — Modelo certo para a tarefa certa

| Tarefa | Modelo ideal |
|---|---|
| Análise regulatória, estratégia, documentos críticos | Claude Sonnet / Opus |
| Rascunhos, resumos, triagem, respostas rápidas | Claude Haiku |
| Geração de código, automações, scripts | Claude Sonnet + Claude Code |
| Orquestração de subagentes com longa cadeia | Claude Sonnet (contexto 200k tokens) |

---

### 1.2 Regra de delegação

Antes de criar um subagente, responda três perguntas:

1. **A tarefa vai poluir o contexto principal?** → Delegar.
2. **A tarefa é repetível com o mesmo escopo?** → Delegar.
3. **A tarefa é trivial e pode ser resolvida com uma instrução simples?** → Não delegar.

---

## Parte 2: Arquitetura de Orquestração

### 2.1 Fluxo completo

```
Você (humano)
   ↓ objetivo + restrições
Claude Orquestrador
   ↓ intake estruturado
   ↓ planejamento de subtarefas
   ├── Subagente A: Pesquisa/contexto
   ├── Subagente B: Execução do artefato
   └── Subagente C: Revisão/validação
   ↓ consolida
   ↓ self-reflection (autoanálise)
   ↓ reflexion loop (reescrita se necessário)
Entrega final revisada e validada
```

### 2.2 O intake estruturado

Antes de qualquer delegação ou loop, o orquestrador reformula a tarefa em formato canônico:

```
Objetivo:
Entradas disponíveis:
Restrições:
Formato de saída:
Critérios de sucesso:
Riscos potenciais:
Pontos que exigem validação humana:
```

### 2.3 Template de prompt para subagente

```xml
<role>
Você é um subagente especializado em [papel].
Trabalhe exclusivamente no seu escopo.
</role>

<context>
[Contexto mínimo suficiente para a tarefa. Não inclua informação irrelevante.]
</context>

<task>
[Uma única tarefa, com começo e fim claros.]
</task>

<constraints>
- Não inventar fatos.
- Não sair do escopo.
- Sinalizar incerteza quando faltar evidência.
- [Restrição específica do caso]
</constraints>

<output>
[Estrutura exata da resposta esperada.]
</output>

<quality>
- Clareza.
- Separação entre fato, hipótese e recomendação.
- Rastreabilidade do raciocínio.
</quality>
```

### 2.4 Papéis padrão dos subagentes

| Subagente | Missão | Entrega |
|---|---|---|
| Pesquisador | Coleta fatos, normas e referências sem executar | Lista estruturada de fatos e fontes |
| Executor | Produz o artefato principal | Rascunho completo |
| Revisor | Audita risco, lacuna, inconsistência e exagero | Correções priorizadas com justificativa |
| Consolidador | Integra tudo, produz versão final | Entrega pronta com checklist de confiança |

---

## Parte 3: Os Loops de Autoanálise

Esta é a camada que transforma o Claude de um respondedor em um sistema que **pensa, revisa e melhora antes de entregar**. São quatro padrões distintos, combinados em sequência.

### 3.1 Self-Reflection (autocrítica interna)

O Claude gera uma primeira resposta e depois audita o próprio output com critérios definidos antes de entregar. Você nunca vê o rascunho ruim.

**Quando usar:** em qualquer tarefa onde a primeira versão costuma ter lacunas ou excesso.

**Prompt que ativa:**

```xml
<task>Execute a tarefa.</task>
<reflection>
Após gerar a resposta inicial, audite internamente:
- O objetivo foi atingido?
- Há fato inventado?
- Há imprecisão ou omissão crítica?
- A resposta está no formato pedido?
Aplique as correções.
</reflection>
<output>Entregue apenas a versão final revisada. Não mostre o processo.</output>
```

---

### 3.2 Reflexion Loop (tentativa → avaliação → reescrita)

O modelo gera → avalia se satisfez o critério → se não, reflete sobre o erro e tenta novamente com o aprendizado no contexto. Repete até satisfazer o critério ou atingir o limite de ciclos.

**Quando usar:** tarefas difíceis com critério objetivo e claro.

**Estrutura canônica:**

```
Ciclo 1: Tentativa inicial
Ciclo 2: Avaliação — critério foi atingido? Não → Reflexão: o que errei e por quê?
Ciclo 3: Nova tentativa com a reflexão no contexto
Para quando o critério for satisfeito ou ao atingir 3 ciclos.
```

**Prompt que ativa:**

```xml
<task>[Tarefa]</task>
<loop>
Execute a tarefa.
Avalie: o resultado atinge o critério de sucesso?
Se não, gere uma reflexão sobre o que falhou e execute novamente.
Repita por até 3 ciclos. Entregue apenas a versão final.
</loop>
<success_criteria>[Critério objetivo de qualidade]</success_criteria>
```

---

### 3.3 ReAct Loop (Raciocinar → Agir → Observar → Repetir)

Padrão usado internamente na Anthropic para agentes. O modelo alterna entre **pensamento** (o que eu sei, o que preciso descobrir) e **ação** (executar algo e observar o resultado). Não entrega até ter certeza.

**Quando usar:** pesquisa + decisão + execução encadeadas.

**Estrutura:**

```
THOUGHT: O que eu sei? O que falta? Qual minha hipótese?
ACTION: Executo uma única subtarefa para testar a hipótese.
OBSERVATION: O que aprendi? Confirma ou refuta?
→ Repete até completar.
```

**Prompt que ativa:**

```xml
Para cada etapa desta tarefa, siga este ciclo:

THOUGHT: O que eu sei agora? O que falta? Qual a melhor hipótese?
ACTION: Execute uma única análise ou passo objetivo.
OBSERVATION: O que foi aprendido? Isso muda a direção?

Repita até completar ou precisar de input humano.
Entregue apenas a resposta consolidada.
```

---

### 3.4 Self-Rewriting Loop (a IA reescreve suas próprias instruções)

O padrão mais avançado. Após cada execução, o Claude reflete sobre o que poderia ser melhorado nas **próprias instruções**, propõe uma versão nova do prompt para a próxima rodada.

**Quando usar:** para evoluir skills e prompts ao longo do tempo.

**Prompt que ativa:**

```xml
<task>Execute a tarefa.</task>
<meta_reflection>
Após entregar o resultado, reflita sobre as próprias instruções:
- Houve ambiguidade que causou hesitação?
- Alguma regra foi redundante?
- Alguma regra importante estava faltando?
Proponha uma versão melhorada destas instruções para a próxima rodada.
</meta_reflection>
```

---

### 3.5 Qual padrão usar em cada situação

| Situação | Padrão ideal |
|---|---|
| Documento crítico, rótulo, proposta | Self-Reflection |
| Tarefa difícil com critério objetivo | Reflexion Loop |
| Pesquisa + decisão + execução encadeadas | ReAct Loop |
| Skill que você quer melhorar com o tempo | Self-Rewriting Loop |
| Tarefa simples | Nenhum loop — resposta direta |
| Tarefa longa e complexa | Combinação dos três primeiros |

---

### 3.6 A combinação recomendada para empresa

Para tarefas críticas (rótulo, SOP, proposta, regulatório, automação), use o fluxo combinado:

```
Intake estruturado
↓
ReAct: raciocina e age em etapas
↓
Self-Reflection: audita o próprio resultado
↓
Reflexion: se não passou na auditoria, refaz com aprendizado
↓
Entrega final
```

---

## Parte 4: Prompt Único — Loop Completo

Cole este bloco em Project Instructions, System Prompt ou CLAUDE.md.

```text
Atue como meu Claude orquestrador para tarefas complexas da empresa.

Seu papel é receber uma solicitação, estruturar a tarefa, decidir o que precisa ser analisado em etapas, executar ciclos internos de raciocínio e revisão, melhorar a própria resposta antes de entregar e me mostrar apenas a versão final consolidada.

## Contexto fixo
Empresa: empresa.
Setor: fabricação e distribuição de suplementos.
Prioridades: clareza, objetividade, delegação, execução rápida, aderência regulatória com ANVISA quando aplicável, separação entre fato, hipótese e recomendação.
Tom: direto, sem enrolação.

## Regra principal
Antes de entregar qualquer resposta final, passe por este fluxo interno obrigatório:
1. Intake estruturado.
2. Planejamento.
3. Execução em etapas (ReAct).
4. Autoanálise crítica (Self-Reflection).
5. Reescrita da resposta se necessário (Reflexion).
6. Entrega final consolidada.

## Intake obrigatório
Antes de responder, reestruture mentalmente a solicitação:
- Objetivo
- Entradas disponíveis
- Restrições
- Formato de saída
- Critérios de sucesso
- Riscos potenciais
- Pontos que exigem validação humana

## Loop de execução

### Etapa 1 — Planejar
- O que já está claro
- O que precisa ser inferido com cautela
- O que depende de validação
- Quais subtarefas existem

### Etapa 2 — ReAct interno
Para cada subtarefa:
- THOUGHT: o que eu sei, o que falta, qual minha hipótese
- ACTION: executar uma única análise ou passo objetivo
- OBSERVATION: o que aprendi e se isso muda a direção
Repita até a subtarefa estar madura.

### Etapa 3 — Self-reflection
Após montar a primeira versão, audite internamente:
- O objetivo foi realmente atendido?
- Existe fato inventado, fraco ou assumido sem sinalização?
- Há conflito interno, redundância ou excesso de texto?
- O formato solicitado foi seguido?
- Existe risco regulatório, jurídico, operacional ou técnico não destacado?
- A resposta está útil para decisão?

### Etapa 4 — Reflexion loop
Se a auditoria falhar em qualquer ponto:
- gere internamente uma crítica objetiva da sua resposta
- identifique o erro principal
- reescreva com base nessa crítica
- repita por até 3 ciclos
- pare quando estiver sólido o suficiente para uso prático

## Regras de qualidade
- Não inventar fatos.
- Não mascarar incerteza.
- Separar fato, hipótese e recomendação.
- Em temas regulatórios, aplicar lógica conservadora.
- Em temas de suplementos, claims, rotulagem ou ANVISA, sinalizar necessidade de validação humana.
- Preferir resposta utilizável a resposta bonita.
- Evitar repetir o mesmo ponto.

## Regras por tema

Se regulatório:
- verificar claims, linguagem terapêutica, aderência à RDC 843/2024
- sinalizar o que depende de revisão humana

Se comercial:
- transformar complexidade em clareza
- separar argumento comercial de afirmação regulatória

Se processos:
- sequência lógica e checklist
- reduzir ambiguidade

Se automação:
- separar análise, arquitetura, implementação e risco
- sinalizar dependências e o que precisa de teste

## Formato da resposta final
Entregue apenas a versão final consolidada.
Não exponha o processo interno.
Use esta estrutura quando fizer sentido:
1. Conclusão direta
2. Análise objetiva
3. Riscos e lacunas
4. Próxima ação recomendada

## Regra de parada
Se faltar informação crítica, não invente. Explique o que falta e avance até onde for seguro.

## Solicitação do usuário
[COLE AQUI A SUA TAREFA]
```

---

## Parte 5: Implementação Prática na empresa

### 5.1 Plano de implementação em 3 fases

#### Fase 1 — Hoje

- [ ] Criar Projeto "Regulatório ANVISA" no Claude.ai
- [ ] Subir RDC 843/2024, modelo de rótulo padrão, lista dos principais produtos
- [ ] Testar gerando um texto de rótulo completo com o prompt único acima
- [ ] Comparar com a versão atual e anotar o que precisou de ajuste

#### Fase 2 — Esta semana

- [ ] Identificar as 3 tarefas mais repetidas na empresa
- [ ] Criar um Projeto separado para cada com contexto fixo
- [ ] Usar o metaprompt para gerar o system prompt de cada Projeto
- [ ] Delegar 5 tarefas reais e medir tempo economizado

#### Fase 3 — Este mês

- [ ] Para qualquer tarefa que você delegaria a um colaborador, testar com Claude primeiro
- [ ] Documentar onde o Claude tem alavancagem real
- [ ] Criar o Projeto "Automação" com stack técnico
- [ ] Usar Claude Code para automatizar a primeira tarefa operacional recorrente

### 5.2 Exemplo completo: revisão de rótulo

**Você digita:**

```text
Revisar o rótulo do produto X para conformidade com RDC 843/2024.
[cole o rótulo atual]
Formato: análise item a item, versão corrigida, checklist final.
```

**O orquestrador executa:**
1. Intake estruturado
2. ReAct: analisa cada item do rótulo em etapas
3. Self-reflection: audita o diagnóstico e a versão revisada
4. Reflexion: corrige se necessário
5. Entrega: rótulo revisado + checklist + riscos

**Você recebe:** versão utilizável, validada internamente, com checklist pronto para aprovação.

### 5.3 Casos de uso por área

| Área | Tarefa delegável | Loop recomendado |
|---|---|---|
| Regulatório | Revisar rótulo, analisar claim, responder fiscalização | ReAct + Self-Reflection + Reflexion |
| Comercial | Proposta private label, e-mail de negociação | Self-Reflection |
| Processos | SOP de fabricação, checklist BPF | ReAct + Self-Reflection |
| Automação | Script de integração, lógica de pedidos | ReAct + Self-Reflection |
| Estratégia | Análise de mercado, briefing de decisão | ReAct + Reflexion |

---

## Parte 6: Gestão de Contexto e Qualidade

### 6.1 Gerenciar a janela de contexto

- Inicie nova conversa para novos tópicos
- Não recarregue arquivos na mesma conversa
- Use subagentes para pesquisa pesada
- Se o Claude começar a contradizer o que estava no início da conversa, inicie nova sessão

### 6.2 Checklist de validação final

Antes de aceitar qualquer entrega:

- [ ] O objetivo foi entendido corretamente?
- [ ] Há fatos inventados ou sem base?
- [ ] Existe risco não sinalizado?
- [ ] O formato solicitado foi seguido?
- [ ] O que precisa de validação humana está marcado?
- [ ] Existe uma próxima ação clara?

### 6.3 Regras de ouro

1. **Claude executa, você decide.** Nunca publique ou aplique sem revisar.
2. **Contexto persistente > prompt artesanal.** Invista uma vez no Projeto.
3. **Loop aumenta qualidade, não velocidade.** Use para o que importa.
4. **Um subagente = uma tarefa.**
5. **Delegue o que você delegaria a um colaborador.**
6. **Self-rewriting para prompts que você usa toda semana.**

---

## Parte 7: Ferramentas e Recursos

### 7.1 Stack recomendada

| Ferramenta | Uso |
|---|---|
| Claude.ai (Pro) | Projetos com contexto persistente, conversas longas |
| Claude Code | Automações, scripts, integrações |
| console.anthropic.com | Geração de prompts e testes de system prompt |
| CLAUDE.md | Arquivo de contexto para Claude Code por repositório |

### 7.2 Formato CLAUDE.md para repositórios

```markdown
# Contexto do repositório

## Empresa
empresa — fabricante e distribuidora de suplementos.

## Stack
Node.js / Python, integrações ERP e Bling.

## Regras de execução
- Não alterar arquivos de produção sem confirmação.
- Sinalizar qualquer mudança que afete integrações externas.
- Código e comentários em português.
- Aplicar ReAct e self-reflection antes de entregar código final.

## Delegação de modelos
- Tarefas de análise longa: usar Sonnet.
- Buscas simples e geração de texto curto: usar Haiku.
- Geração de código crítico: usar Sonnet com ultrathink.
```

### 7.3 Links oficiais

- Prompting: `platform.claude.com/docs/pt-BR/intro`
- Boas práticas Claude Code: `anthropic.com/engineering/claude-code-best-practices`
- Agentes eficazes: `anthropic.com/research/building-effective-agents`
- Cursos gratuitos: `anthropic.com/learn`

---

## Próximos Passos

O ponto de retorno mais rápido para a empresa está em três frentes: revisão regulatória automatizada, propostas comerciais em escala e automação de processos recorrentes.

**Ação imediata:** colar o prompt único da Parte 4 em um novo chat, substituir `[COLE AQUI A SUA TAREFA]` por uma revisão de rótulo real e comparar com sua forma atual de trabalho. O tempo investido é menos de 10 minutos.
