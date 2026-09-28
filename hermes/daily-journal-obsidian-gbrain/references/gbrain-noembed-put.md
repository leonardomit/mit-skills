# gbrain journal put sem embed (PGLite)

Verificado 2026-07-29 e 2026-07-31 no cron Fluxo 5.

## PATH no cron
```bash
export PATH="$HOME/.bun/bin:$PATH"
# ~/.bun/bin/gbrain  (v0.35+)
```

## Lock stale
```bash
LOCK=~/.gbrain/brain.pglite/.gbrain-lock/lock
# JSON: {pid, acquired_at, command}
# se kill -0 $pid falhar → rm -rf ~/.gbrain/brain.pglite/.gbrain-lock
```

Só mate `gbrain serve` com **ppid=1** (órfão). Deixe watchdogs MCP
(`mcp_stdio_watchdog` → bun gbrain serve). Vários serves vivos sob watchdog é normal.

## Bun putPage — cwd = ~/gbrain (obrigatório)

Imports `./src/core/...` resolvem a partir do **cwd do script**, não do PATH.
Rodar o `.js` de `~/.hermes/cache/` falha com:
```text
Cannot find module './src/core/config.ts' from '.../cache/gbrain_put_journal.js'
```

Preferir o script empacotado (sem `bun -e` — cron bloqueia inline scripts):
```bash
export PATH="$HOME/.bun/bin:$PATH"
STAGE_JS=~/.hermes/skills/note-taking/daily-journal-obsidian-gbrain/scripts/gbrain_put_journal.js
cp "$STAGE_JS" ~/gbrain/_put_journal_tmp.js
cd ~/gbrain && bun ./_put_journal_tmp.js YYYY-MM-DD
rm -f ~/gbrain/_put_journal_tmp.js
# sucesso: PAGE journal/YYYY-MM-DD Registro do Dia — …
```

O script lê o stage:
`~/.hermes/cache/gbrain-journal-stage/journal/YYYY-MM-DD.md`

## Alternativa CLI
```bash
gbrain import ~/.hermes/cache/gbrain-journal-stage --no-embed
```
Se hang em `[import.files] start` > 30s → abortar e usar bun.

## Disco cheio
Se write falhar com `No space left on device`:
```bash
df -h /
: > /tmp/hermes-workspace.err.log   # truncate seguro (rm pode ser blocked no cron)
```
Depois reescrever stage + Obsidian + put.

## Não fazer
- Confiar só em MCP `put_page` no cron (timeout 300s comum)
- `gbrain put` sem timeout de subprocess
- Steal de lock enquanto serve MCP escreve (deadlock WASM)
- Afirmar “gbrain não é CLI” — é (`gbrain` v0.35+)
- Rodar bun put a partir de `~/.hermes/cache` (module path errado)
- Matar todos os `gbrain serve` (quebra MCP)
- Depender de `bun -e '...'` no cron (pode ser blocked como script inline)
