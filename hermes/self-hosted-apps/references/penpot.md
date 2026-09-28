# Penpot on this Mac

Two installs coexist. Do not replace one with the other unless asked.

## Desktop client

- App: `/Applications/Penpot Desktop.app` (v0.23.2, Apple Silicon)
- Source: unofficial community wrapper `author-more/penpot-desktop` (no Homebrew cask)
- Default target: https://design.penpot.app
- To use the local stack: Settings → instance → `http://localhost:9001`
- DMG SLA: `printf 'Y\n' | hdiutil attach -nobrowse -readonly -noverify penpot-desktop-arm64.dmg`

## Self-host

- Dir: `~/Apps/penpot`
- Official compose: https://raw.githubusercontent.com/penpot/penpot/main/docker/images/docker-compose.yaml
- Pinned: `PENPOT_VERSION=2.16` (running 2.16.2)
- UI: http://localhost:9001 (`127.0.0.1:9001→8080`)
- Mailcatcher: http://localhost:1080
- Project name: `penpot` (`docker compose -p penpot`)
- Flags in use: `disable-email-verification enable-smtp enable-prepl-server disable-secure-session-cookies`
- Telemetry off. Secret in `.env` as `PENPOT_SECRET_KEY`.
- First user: sign up in the UI (registration left on).

### MCP disabled (2.16 arm64)

`penpotapp/mcp:2.16` inspects as `linux/arm64` but `/opt/node/bin/node` is **0 bytes** → `exec format error`. Frontend nginx then fails with `host not found in upstream "penpot-mcp"` while the flag `enable-mcp` is set.

Working state:

- `enable-mcp` removed from `PENPOT_FLAGS`
- frontend `depends_on` no longer lists `penpot-mcp`
- `docker compose … up -d --scale penpot-mcp=0`

Revisit MCP only after a newer image has a non-empty `node` binary.

### Commands

```bash
cd ~/Apps/penpot
docker compose -p penpot --env-file .env -f docker-compose.yaml up -d --pull never
docker compose -p penpot --env-file .env -f docker-compose.yaml down
curl -sS -o /dev/null -w '%{http_code}\n' http://127.0.0.1:9001/
```
