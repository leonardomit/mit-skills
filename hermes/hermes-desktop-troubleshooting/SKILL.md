---
name: hermes-desktop-troubleshooting
description: "Diagnose and fix Hermes Desktop boot loops, blank UI, 401/WS auth failures, and backend spawn issues on macOS."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, desktop, electron, troubleshooting, auth, boot]
    related_skills: [debugging-hermes-tui-commands, hermes-s6-container-supervision]
---

# Hermes Desktop Troubleshooting

Use when Desktop fails to start, stays on connecting/boot overlay, chat never opens, API returns 401, WebSocket fails, or the app restarts the backend in a loop after `hermes update`.

## Quick triage (order matters)

1. **Confirm the app is looping, not dead**
   - `pgrep -af 'Hermes.app/Contents/MacOS/Hermes|hermes_cli.main serve'`
   - `tail -n 80 ~/.hermes/logs/desktop.log`
   - Loop signature in log:
     - `Hermes backend is ready. Finalizing desktop startup`
     - then `reset requested by renderer` / `Restarting desktop connection`
     - often preceded by Electron `hermes:api` → `401 Unauthorized`

2. **Check the #1 auth pitfall first (most common after updates)**
   - Search `.env` for a sticky session token:
     ```bash
     rg -n 'HERMES_DASHBOARD_SESSION_TOKEN' ~/.hermes/.env
     ```
   - **If present: remove the line.** This token is ephemeral (per Desktop spawn). It must NOT live in `~/.hermes/.env`.
   - Why it breaks Desktop:
     - Electron mints `HERMES_DASHBOARD_SESSION_TOKEN` and passes it to the child `hermes serve`
     - `load_hermes_dotenv()` loads `~/.hermes/.env` with **`override=True`**
     - The stale `.env` value overwrites the minted token
     - Backend authenticates with `.env` token; Desktop still holds the minted token → **401 on `/api/*` and WS 403**
   - Backup before edit, then strip the key:
     ```bash
     cp ~/.hermes/.env ~/.hermes/.env.bak.desktop-token-$(date +%Y%m%d%H%M%S)
     # remove HERMES_DASHBOARD_SESSION_TOKEN=... line, then relaunch Desktop
     ```

3. **Verify live backend auth after fix**
   - Find serve PID/port/token from process env (`ps eww -p <pid>` → `HERMES_DASHBOARD_SESSION_TOKEN`, `lsof -nP -iTCP -sTCP:LISTEN`)
   - Probe with header `X-Hermes-Session-Token: <token>` (not only `Authorization: Bearer`):
     - Public: `GET /api/status` → 200 even without token
     - Protected: `GET /api/config`, `GET /api/sessions` → 200 with token
     - Note: `/api/model` alone may 404; use `/api/model/info` (public) or `/api/model/options` (protected)
   - WS: `ws://127.0.0.1:<port>/api/ws?token=<token>` should connect in loopback mode

4. **If still broken: rebuild/relaunch Desktop**
   ```bash
   pkill -f 'Hermes.app/Contents/MacOS/Hermes' || true
   pkill -f 'hermes_cli.main serve' || true
   hermes desktop --force-build   # after agent update / asar mismatch
   # or
   hermes desktop --skip-build    # when package is already current
   ```
   - `hermes update` often **skips** desktop packaging (`desktop skipped`). Agent can be 0.19.x while packaged app stays 0.17.x — rebuild when boot/API shapes drift.

## Log & path map

| What | Where |
|------|--------|
| Desktop boot transcript | `~/.hermes/logs/desktop.log` |
| Backend/web server | `~/.hermes/logs/gui.log`, `~/.hermes/logs/agent.log` |
| Packaged app (local build) | `~/.hermes/hermes-agent/apps/desktop/release/mac-arm64/Hermes.app` |
| Electron user data | `~/Library/Application Support/Hermes/` |
| Connection mode | `~/Library/Application Support/Hermes/connection.json` |
| Env secrets | `~/.hermes/.env` |

## Architecture facts that prevent false leads

- Desktop spawns **headless** `hermes serve` (not the browser dashboard). Log line `could not read served dashboard token ... web UI disabled` is **expected** for headless serve; Desktop falls back to the spawn token.
- Separate `hermes dashboard` on port 9119 is optional and **not** required for Desktop chat.
- Correct session header name: **`X-Hermes-Session-Token`**.
- Loopback WS auth uses `?token=<session_token>`. Gated/public binds use tickets — different path.

## Pitfalls

- **Sticky `HERMES_DASHBOARD_SESSION_TOKEN` in `.env`** — causes post-boot 401 loop. Never persist this key. See `references/desktop-session-token-override.md`.
- **Chasing “desktop vs agent version mismatch” first** — version skew can matter after updates, but auth override fails harder and more often; check `.env` before long rebuilds.
- **Probing wrong endpoints** — `/api/model` is not a real route; 401 vs 404 confusion wastes time. Prefer `/api/config` + `/api/sessions`.
- **Assuming process alive means healthy** — serve may be up while renderer is in reset loop; always check `desktop.log` for `reset requested by renderer`.
- **Leaving competing Electron singletons** — if launch fails silently, clear stale `~/Library/Application Support/Hermes/SingletonLock` only after confirming no live Hermes main process.

## Verification checklist

- [ ] No `HERMES_DASHBOARD_SESSION_TOKEN` in `~/.hermes/.env`
- [ ] `desktop.log` ends with `Finalizing desktop startup` **without** immediate `reset requested`
- [ ] `hermes_cli.main serve` PID stable for >30s
- [ ] Authenticated `GET /api/config` returns 200
- [ ] WS `/api/ws?token=...` connects
- [ ] Chat UI leaves connecting overlay

## Related detail

- `references/desktop-session-token-override.md` — full failure chain and reproduction notes from the 2026-07 Desktop loop incident.
