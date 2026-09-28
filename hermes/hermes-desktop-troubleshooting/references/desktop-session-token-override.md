# Desktop session token overridden by ~/.hermes/.env

## Symptom (2026-07 Mac Mini / Leonardo)

- Hermes Desktop appeared broken after `hermes update`
- App process alive; backend repeatedly respawned
- `~/.hermes/logs/desktop.log` pattern:
  1. `HERMES_BACKEND_READY port=...`
  2. `could not read served dashboard token ... web UI disabled` (benign for headless serve)
  3. `Hermes backend is ready. Finalizing desktop startup`
  4. Electron main: `Error occurred in handler for 'hermes:api': Error: 401: {"detail":"Unauthorized"}`
  5. `[bootstrap] reset requested by renderer; clearing latched failure`
  6. `Restarting desktop connection` → loop

## Root cause

1. Desktop Electron mints a fresh `HERMES_DASHBOARD_SESSION_TOKEN` and spawns:
   `python -m hermes_cli.main serve --host 127.0.0.1 --port 0`
   with that token in the child environment.
2. Early in CLI startup, `load_hermes_dotenv()` loads `~/.hermes/.env` with **`override=True`**
   (see `hermes_cli/env_loader.py`: user env overrides shell/spawn env).
3. A stale line existed in `.env`:
   `HERMES_DASHBOARD_SESSION_TOKEN=<old value>`
4. After dotenv load, both `os.environ[...]` and `web_server._SESSION_TOKEN` matched the **.env** value,
   not the Desktop-minted spawn token.
5. Desktop kept calling APIs with the spawn token → middleware 401 → boot failure overlay/retry loop.

### How we proved it

Sitecustomize preload on a manual `hermes serve`:

- t=0 env token = Desktop-style minted value
- t=+3s after startup: env **and** `web_server._SESSION_TOKEN` equaled the `.env` value

Public endpoints still returned 200 without auth (`/api/status`, `/api/model/info` is public),
which can falsely suggest “backend is fine” while protected routes fail.

## Fix

```bash
# confirm
rg -n 'HERMES_DASHBOARD_SESSION_TOKEN' ~/.hermes/.env

# backup + remove the line (do not leave empty assignment)
cp ~/.hermes/.env ~/.hermes/.env.bak.desktop-token-$(date +%Y%m%d%H%M%S)
# delete HERMES_DASHBOARD_SESSION_TOKEN=... from the file

pkill -f 'Hermes.app/Contents/MacOS/Hermes' || true
pkill -f 'hermes_cli.main serve' || true
hermes desktop --skip-build   # or --force-build after large agent updates
```

### Post-fix probes

```bash
# with token from: ps eww -p <serve_pid> | tr ' ' '\n' | sed -n 's/^HERMES_DASHBOARD_SESSION_TOKEN=//p'
curl -sS -H "X-Hermes-Session-Token: $TOKEN" http://127.0.0.1:$PORT/api/config | head -c 120
# expect JSON config, HTTP 200

# WS should accept ?token= in loopback mode
```

Success criteria:

- No new `reset requested by renderer` after `Finalizing desktop startup`
- Serve PID stable >30s
- WS connect OK

## Do not do

- Do **not** re-add `HERMES_DASHBOARD_SESSION_TOKEN` to `.env` “to fix auth”
- Do **not** treat headless “web UI disabled” as the failure
- Do **not** start with long desktop rebuilds before checking `.env` override

## Related code

- `hermes_cli/env_loader.py` — `load_hermes_dotenv`, user env `override=True`
- `hermes_cli/web_server.py` — `_SESSION_TOKEN`, `_SESSION_HEADER_NAME = X-Hermes-Session-Token`
- `apps/desktop/electron/main.ts` — spawn env mint of `HERMES_DASHBOARD_SESSION_TOKEN`
- `apps/desktop/electron/dashboard-token.ts` — served-token adoption (404 on headless is expected)
