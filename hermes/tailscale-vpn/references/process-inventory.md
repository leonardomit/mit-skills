# Process Inventory Reference

Quick commands to snapshot what services are running on the Mac Mini.

## Ports & Processes

```bash
# Single-port checks (reliable — lsof -i with multiple :port args FAILS on macOS)
lsof -i :8642 -P -n | grep LISTEN   # Hermes Gateway (Paperclip)
lsof -i :3005 -P -n | grep LISTEN   # Hermes Workspace (Vite)
lsof -i :3101 -P -n | grep LISTEN   # Paperclip adapter

# All listening ports, cleaned up
lsof -i -P -n | grep LISTEN | awk '{print $9}' | sort -t: -k2 -n | uniq

# All node/python processes (useful to identify services)
ps aux | grep -E 'node|python|python3' | grep -v grep | awk '{print $1,$2,$11}'

# Full process tree for hermes-related
ps aux | grep -E 'hermes|workspace|paperclip|ollama' | grep -v grep
```

## Current Mac Mini Process Map (as of 2025-05-25)

| Port | Process | Service |
|------|---------|---------|
| 8642 | `python3.1` (PID 57515) | Paperclip gateway (legacy) |
| 3005 | `node` (PID 80202) | Hermes Workspace (Vite) |
| 3101 | `python` (PID 49762) | Paperclip adapter |
| 9119 | — | Hermes dashboard |
| 11434 | Ollama.app (PID 1349) | Ollama local |
| 5432 | `postgres` × 18 | PostgreSQL (embedded + homebrew) |
| 3306 | `mysqld` | MySQL homebrew |

## Key lessons from this setup

- Workspace prefers port 3005 — 3003/3004 were held by zombie vite processes
- The Paperclip gateway on 8642 can keep running even when Workspace is active on 3005
- Funnel always proxies to the port specified at `tailscale funnel <port>` time
- Workspace needs both `OLLAMA_API_KEY` AND `HERMES_API_TOKEN` in env to call the gateway successfully
- `lsof -i :port1,:port2` does NOT work on macOS lsof 4.91 — use separate commands
