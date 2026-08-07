---
name: produtividade-foco
description: >
  7 prompts prontos para produtividade, foco e gestão de tarefas usando IA como copiloto executivo.
  Use este skill quando o usuário mencionar paralisia de tarefas, dificuldade de começar, distração,
  falta de estímulo, travar entre tarefas, subestimar tempo, ou pontoas soltas na cabeça.
  Também acionar quando o usuário pedir "prompt para produtividade", "como usar IA para foco",
  "me ajuda a organizar minha cabeça", ou qualquer variação de TDAH, procrastinação, body doubling,
  menu de dopamina, brain dump, ou gestão de energia cognitiva.
---

# Skill: Produtividade & Foco — 7 Prompts Executivos

Conjunto de 7 prompts prontos para usar com IA (Claude, ChatGPT, etc.) como copiloto de função executiva.
Cada prompt resolve um problema cognitivo específico. Entregue ao usuário o(s) prompt(s) relevante(s)
com as variáveis preenchidas conforme o contexto da conversa.

---

## Como usar este skill

1. Identifique qual dos 7 problemas o usuário está enfrentando (veja tabela abaixo).
2. Entregue o prompt correspondente, substituindo `[variáveis]` pelo contexto real do usuário.
3. Se o usuário não especificou o problema, apresente todos os 7 com descrição curta e pergunte qual aplicar.

### Mapa rápido: problema → prompt

| Problema do usuário | Prompt |
|---|---|
| Não consegue começar uma tarefa | #1 Destruidor da paralisia |
| Sem energia, baixo estímulo | #2 Menu de dopamina |
| Precisa de companhia para focar | #3 Body doubling virtual |
| Travou ao mudar de uma tarefa para outra | #4 Guia de mudança de contexto |
| Tarefa chata / sem motivação | #5 Filtro de interesse |
| Subestima quanto tempo algo vai levar | #6 Auditor de cegueira temporal |
| Cabeça cheia de pontas soltas | #7 Externalizador da função executiva |

---

## Os 7 Prompts

---

### 1. O Destruidor da Paralisia de Tarefas

**Problema:** Está olhando para uma tarefa e não consegue começar.

**Prompt:**
```
Estou olhando para [TAREFA] e não consigo começar.
Divida isso em passos ridiculamente pequenos que levem menos de 1 minuto cada.
Me dê o primeiro passo e diga exatamente onde colocar minhas mãos para começar.
```

**Exemplo preenchido:**
```
Estou olhando para "responder os e-mails da semana" e não consigo começar.
Divida isso em passos ridiculamente pequenos que levem menos de 1 minuto cada.
Me dê o primeiro passo e diga exatamente onde colocar minhas mãos para começar.
```

---

### 2. O Arquiteto do Menu de Dopamina

**Problema:** Pouco estímulo, sem energia para trabalhar.

**Prompt:**
```
Estou me sentindo pouco estimulado.
Crie um "Menu de Dopamina" para mim com:
- "Entradas" de 5 minutos (movimentos rápidos)
- "Pratos principais" de 20 minutos (trabalho profundo)
- "Sobremesas" de 10 minutos (atividades criativas)
para manter meu cérebro engajado ao longo do dia.
```

**Variação contextual:** Se o usuário mencionou área de trabalho (ex: operações, vendas), instrua a IA a criar o menu com tarefas reais dessa área.

---

### 3. O Simulador de Body Doubling

**Problema:** Precisa de presença/companhia para manter foco.

**Prompt:**
```
Aja como meu parceiro virtual de produtividade pelos próximos [TEMPO, ex: 30 minutos].
Vou te dizer no que estou trabalhando, e quero que você faça check-ins a cada 10 minutos
para pedir atualizações e manter meu foco firme.
```

**Como funciona:** O usuário inicia a sessão declarando a tarefa. A IA responde com encorajamento e cobra atualização a cada 10 min.

---

### 4. O Guia de Mudança de Contexto

**Problema:** Acabou uma tarefa e o cérebro travou ao tentar iniciar outra de natureza diferente.

**Prompt:**
```
Acabei de terminar [TAREFA A] e preciso começar [TAREFA B],
mas meu cérebro travou.
Crie uma rotina de 3 minutos de "limpeza mental" para me ajudar
a fazer a transição entre esses dois tipos diferentes de energia.
```

**Exemplo:**
```
Acabei de terminar uma reunião de alinhamento comercial e preciso começar a revisar
planilhas financeiras, mas meu cérebro travou.
Crie uma rotina de 3 minutos de "limpeza mental"...
```

---

### 5. O Filtro Baseado em Interesse

**Problema:** Tarefa administrativa chata que o usuário está evitando.

**Prompt:**
```
Tenho uma tarefa administrativa chata: [TAREFA].
Me ajude a transformar isso em um jogo conectando com minha hiperfixação atual: [INTERESSE].
Crie uma estrutura de "missão" onde concluir a tarefa desbloqueia uma recompensa.
```

**Exemplo:**
```
Tenho uma tarefa administrativa chata: preencher relatório de gastos.
Me ajude a transformar isso em um jogo conectando com minha hiperfixação atual: estratégia de negócios.
Crie uma estrutura de "missão" onde concluir a tarefa desbloqueia uma recompensa.
```

---

### 6. O Auditor da Cegueira Temporal

**Problema:** Sempre subestima o tempo real que uma tarefa leva.

**Prompt:**
```
Acho que [PROJETO/TAREFA] vai levar [ESTIMATIVA DO USUÁRIO], mas normalmente leva mais.
Me ajude a "mapear o tempo" identificando as 3 subtarefas escondidas que eu sempre
esqueço de considerar, para que eu consiga definir um prazo realista.
```

**Exemplo:**
```
Acho que criar o deck de apresentação vai levar 20 minutos, mas normalmente leva 2 horas.
Me ajude a "mapear o tempo" identificando as 3 subtarefas escondidas...
```

---

### 7. O Externalizador da Função Executiva

**Problema:** Cabeça cheia de pontas soltas, difícil priorizar.

**Prompt:**
```
Meu cérebro está cheio de "pontas soltas". Vou despejar abaixo tudo com o que estou preocupado.
Categorize isso em "Agora", "Depois" e "Descartar",
e depois escreva uma "Próxima ação prática" de apenas 1 frase para os itens da categoria "Agora".

[BRAIN DUMP — cole aqui tudo que está na sua cabeça, sem filtro]
```

**Dica de uso:** Pedir ao usuário para fazer um brain dump sem editar antes de colar. Quanto mais bruto, melhor o resultado.

---

## Notas de entrega

- **Sempre substitua as variáveis** `[entre colchetes]` pelo contexto real antes de entregar o prompt ao usuário.
- Se o usuário não tem contexto claro, entregue o prompt com as variáveis explicadas e peça que ele preencha.
- Prompts #3 (body doubling) e #7 (brain dump) são os mais impactantes para uso imediato — priorize-os quando o usuário estiver em crise de foco aguda.
- Estes prompts funcionam com qualquer LLM (Claude, ChatGPT, Gemini).
