# Hermes Workspace — Access Patterns via Tailscale

## Overview

[Hermes Workspace](https://hermes-workspace.com/) (outsourc-e/hermes-workspace) is a Node.js web app (TanStack Start + Vite) that provides a GUI for Hermes Agent — chat, terminal, memory, skills, kanban. Installed at `~/hermes-workspace` and run with `pnpm dev` (port 3000).

## Access Patterns Compared

| Method | Best for | Limitation |
|--------|----------|------------|
| SSH tunnel: `ssh -L 3000:localhost:3000 user@host` | Terminal-only / quick checks | WebSockets break — Vite HMR fails, page loads but content stays empty |
| `tailscale serve http://localhost:3000` | Web apps with WS (React/Vite dev servers) | Only reachable from Tailscale devices |
| `tailscale funnel 3000` | Public HTTPS access | Exposes to internet — requires sudo |

**For Hermes Workspace**: Use `tailscale serve` — Vite dev server relies heavily on WebSockets for hot module replacement and live reload.

## Setup Steps (already done on mac-mini)

```bash
# 1. Clone repo
git clone https://github.com/outsourc-e/hermes-workspace.git ~/hermes-workspace
cd ~/hermes-workspace

# 2. Install deps
pnpm install

# 3. Configure — point at local Hermes gateway + dashboard
cp .env.example .env
# Edit .env, uncomment:
HERMES_API_URL=http://127.0.0.1:8642
HERMES_DASHBOARD_URL=http://127.0.0.1:9119

# 4. Start dev server
pnpm dev   # runs on port 3000

# 5. Expose via Tailscale (from the host)
tailscale serve http://localhost:3000

# 6. Access from any Tailscale device:
# http://mac-mini-de-leonardo.tail57f54b.ts.net
```

## Key Ports

| Service | Port | Process |
|---------|------|---------|
| Hermes Workspace (dev) | 3000 | `pnpm dev` (Vite) |
| Hermes Gateway (API) | 8642 | `hermes gateway run` |
| Hermes Dashboard | 9119 | `hermes dashboard` |

Verify:
```bash
lsof -i :3000 -i :8642 -i :9119
curl http://localhost:8642/health   # should return ok
curl http://localhost:9119/api/status  # should return JSON
```

## SSH Tunnel (fails for Workspace)

```bash
# This works for terminal, NOT for web apps with WebSockets:
ssh -L 3000:localhost:3000 user@mac-mini-de-leonardo.tail57f54b.ts.net

# Even with tunnel open, Hermes Workspace shows empty content:
# The Vite dev server's WebSocket-based HMR fails over the tunnel.
# The page skeleton loads, but dynamic content (kanban, chat, etc.) stays blank.
# Backend proxy errors: "Dashboard kanban proxy: GET /api/plugins/kanban/board → 500"
```

## Tailscale Serve (correct for web apps)

```bash
# On the host (Mac Mini):
tailscale serve http://localhost:3000

# Verify:
tailscale serve status --json

# Access from any Tailscale device:
# http://mac-mini-de-leonardo.tail57f54b.ts.net
```

## Common Errors

**Empty content / 500 errors on kanban proxy**
- Cause: `HERMES_API_URL` and/or `HERMES_DASHBOARD_URL` not set in `.env`
- Fix: Edit `~/hermes-workspace/.env` and uncomment:
  ```
  HERMES_API_URL=http://127.0.0.1:8642
  HERMES_DASHBOARD_URL=http://127.0.0.1:9119
  ```
- Then restart: `pkill -f "pnpm dev"; cd ~/hermes-workspace && pnpm dev`

**Port 3000 not listening**
- Vite may take 10-20s to start. Wait and retry.
- Check: `lsof -i :3000`

**Tailscale serve fails with "foreground listener already exists"**
```bash
sudo tailscale funnel reset
tailscale serve http://localhost:3000
```

## Reference Links

- Hermes Workspace: https://hermes-workspace.com/
- Repo: https://github.com/outsourc-e/hermes-workspace
- One-line install: `curl -fsSL https://raw.githubusercontent.com/outsourc-e/hermes-workspace/main/install.sh | bash`