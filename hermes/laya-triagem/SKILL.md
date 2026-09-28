---
name: laya-triagem
description: "Use when Laya classifica ou pula arquivo longo."
version: 1.0.0
---

# Laya — triagem local

Classificador no Mac mini (M4, MLX). Não é chat e não substitui o modelo da conversa. Escolher provedor da tarefa é outra skill: `laya-classificador-modelos`.

## Ferramenta

`mcp__laya__classify` — só aparece em sessão nova, com o MCP `laya` no config. Resources e prompts do servidor ficam desligados para não gastar schema à toa.

- Prefira `paths`. O corpo do arquivo não volta; só rótulos.
- Não chame `read_file` antes. Leia o arquivo só se `labels.proxima` for `precisa_ler`.
- `ignorar`: não leia e não encaminhe.
- `so_rotulo`: use os rótulos; não leia o arquivo.
- Texto já colado na mensagem não economiza token. A economia é não puxar o arquivo para o contexto.
- `top` não é probabilidade calibrada. `proxima_ajustada` significa que o modelo quis pular e a regra manteve a leitura porque a intenção era pergunta, pedido ou reclamação.
- Canal e área erram. Não roteie cliente só por `canal`. Reclamação e pedido de revenda foram medidos certo em intenção; “farmácia + atacado” saiu `b2c`.
- Primeira chamada depois que o processo sobe leva ~30 s. Timeout: 180 s.
- Presets: `triagem` (canal, intencao, area, proxima) e `acao`. `questions_json` substitui o preset; no máximo 6 perguntas.

## Onde roda

- Processo: `~/.hermes/venvs/laya/bin/python ~/.hermes/scripts/laya_mcp.py`
- Pesos: `aac6fef/laya-multilingual-mlx`
- CLI sem o Hermes: `~/.hermes/scripts/laya_decide.py`
