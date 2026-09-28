---
name: tailscale-vpn
description: "Remote access to devices via Tailscale VPN — SSH, HTTPS, and tunnel setup. Access devices by hostname from anywhere without exposing ports to the internet."
category: devops
---

# Tailscale VPN — Remote Device Access

## When to Use

Use when the user wants to:
- Access a device (SSH, HTTPS, file transfer) remotely without exposing it to the internet
- Set up a personal VPN using Tailscale's relay network
- Access a Home Assistant instance, NAS, or server remotely
- Create a tailnet with SSH access across devices
- Diagnose Mini "vai e volta" (Tailscale / SSH / painéis / Claude Code / Orca caindo juntos)

Host Mini: `mac-mini-de-leonardo.tail57f54b.ts.net` (`100.122.80.53`). Ports: `references/this-mini-ports.md`. Sono/keepawake: `references/mini-keepawake.md`.

**Flap offline neste Mini não é Tailscale.** É sono do macOS (`sleep 1` na tomada → Deep Idle → DarkWake Wi‑Fi → Maintenance Sleep). SSH, Funnel, painéis e agentes caem no mesmo ciclo. Diagnosticar com `pmset -g` + `pmset -g log | grep 'Entering Sleep'` **antes** de mexer em Tailscale.

Quando o usuário pedir o que fazer no Mini: **checklist colável** (comandos), não ensaio. Senha admin só no Terminal.app — o gateway bloqueia `launchctl bootstrap` KeepAlive.

## Key Concepts

- **Tailnet**: Your private network on Tailscale
- **MagicDNS**: Devices reachable by name (e.g. `pinephone`) within the tailnet
- **Exit nodes**: Route all traffic through a specific device (for censorship bypass, accessing home IP)
- **Subnet routers**: Access devices on the LAN that aren't running Tailscale directly

## Core Commands

```bash
# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Login / authenticate
tailscale up --login

# SSH access (requires SSH server on remote device)
tailscale ssh user@hostname

# Access web UI (e.g. Home Assistant at port 8123)
tailscale --browser=browser ssh user@hostname

# Connect as exit node (route all traffic)
tailscale up --exit-node=hostname

# Share a local subnet (access LAN devices not running Tailscale)
tailscale up --advertise-routes=192.168.1.0/24

# Check status
tailscale status

# Log out / disconnect
tailscale down
```

## Tailscale Funnel — Expose Local Services to the Internet

Funnel shares a local port publicly via HTTPS using your Tailscale domain. On macOS with the **macsys system extension** (the default install), `sudo` is NOT required — the CLI runs as the user and the network extension handles port binding as root.

```bash
# Reset any conflicting config first
tailscale funnel reset

# Expose a local HTTP service to the internet (background — works from terminal)
tailscale funnel 8642
# Or from Hermes terminal tool (background=true):
tailscale funnel 8642

# Result: https://<hostname>.tail<tailnet>.ts.net/ → http://127.0.0.1:8642
```

### Funnel vs Serve

| Command | Access | Require sudo (macOS macsys) |
|---------|--------|------------------------------|
| `tailscale serve <port>` | Tailnet only (Tailscale devices) | No |
| `tailscale funnel <port>` | Public internet via HTTPS | No (macsys extension handles as root) |

### How to verify funnel is ACTUALLY working

**Wrong command:** `tailscale serve status` — shows "No serve config" when using funnel (different subsystem, misleading).

**Correct commands:**
```bash
# Check funnel config — this is the authoritative status
tailscale funnel status --json

# Test external connectivity
curl -s --connect-timeout 8 https://<hostname>.tail<tailnet>.ts.net/health
# Expected: {"status": "ok", "platform": "hermes-agent"}

# Check what process is listening on the gateway port
lsof -i :8642 -P -n | grep LISTEN
```

### Hermes Workspace vs Gateway — Different Ports, Different Verifications

Two distinct services run on the Mac Mini, often confused:
- **Hermes Gateway** (port 8642): API server for AI completions, token-auth required, serves `/v1/*` endpoints. Exposed via Funnel for the Atomic mobile app bridge.
- **Hermes Workspace** (port 3000): Vite dev server serving the web UI, no Bearer token needed for the HTML page, serves `/api/*` endpoints. Exposed via Funnel for browser access.

When the user wants to "open Hermes remotely in the browser", they mean **Workspace (port 3000)**. When they say "connect the Atomic mobile app", they mean **Gateway (port 8642)**.

**Verification commands — which port for which check:**

```bash
# Workspace (port 3000) — browser-accessible web UI
curl -s https://mac-mini-de-leonardo.tail57f54b.ts.net/api/connection-status
# Expected: {"status": "enhanced", "activeModel": "minimax-m2.7", "chatReady": true}

# Gateway (port 8642) — API bridge
curl -s https://mac-mini-de-leonardo.tail57f54b.ts.net/v1/models
# Expected: {"object": "list", "data": [{"id": "hermes-agent", ...}]}
```

### Funnel config structure (from `tailscale funnel status --json`)

```json
{
  "Foreground": {
    "<id>": {
      "TCP": { "443": { "HTTPS": true } },
      "Web": {
        "<hostname>.tail<tailnet>.ts.net:443": {
          "Handlers": { "/": { "Proxy": "http://127.0.0.1:<port>" } }
        }
      },
      "AllowFunnel": { "<hostname>.tail<tailnet>.ts.net:443": true }
    }
  }
}
```

### Common issues
- **"foreground listener already exists for port 443"**: Run `tailscale funnel reset` first, then retry. The port is held by a previous funnel process.
- **`tailscale serve status` shows "No serve config"**: This is NORMAL when using funnel. Use `tailscale funnel status --json` instead.
- **Funnel appears configured but connection is refused**: The funnel CLI may be running but the network extension may not have bound the port. Check with `curl -s https://<hostname>.tail<tailnet>.ts.net/api/connection-status` from an external network.
- **Workspace API calls return HTML instead of JSON**: The Workspace (port 3000) returns Vite SPA HTML when the backend is unreachable or misconfigured — not the same problem as gateway token auth. Check: `curl -s http://localhost:3000/api/connection-status` should return JSON.
- **OLLAMA_API_KEY missing**: When the Hermes Workspace uses a provider like `ollama-cloud` that resolves credentials from env vars, the `.env` must contain `OLLAMA_API_KEY=<token>`. Without it, the Workspace status shows `"chatReady": false` and AI completions fail silently.
- **Hermes Workspace API calls return HTML / silent failures**: The gateway requires Bearer token authentication. When `API_SERVER_KEY` is set in `config.yaml`, the Workspace must also have `HERMES_API_TOKEN=<same-key>` in its `.env` — otherwise `/api/gateway-status` etc. return the Vite SPA HTML instead of JSON.

## Pitfalls

- MagicDNS only works when devices are on the same tailnet and authenticated
### Starting the Tailscale Daemon on macOS (macsys GUI Install)

When Tailscale is installed via the official macOS app (`.app` bundle) rather than Homebrew or CLI-only, the daemon is managed by the macsys network extension — **not by running `tailscaled` manually**.

**Symptom:** `tailscale status` → "Tailscale is stopped" even after `sudo tailscaled`

**Fix — open the GUI app:**
```bash
open -a Tailscale
```
This starts the network extension and the daemon becomes responsive. The CLI then works normally.

**Check:** `/Applications/Tailscale.app/Contents/MacOS/Tailscale status` returns peer list when running.

---

### Tailscale SSH — Important Limitation

`tailscale ssh` is a **wrapper** around system SSH, not a separate protocol. It:
- Resolves hostnames via MagicDNS
- Uses a ProxyCommand through tailscaled
- But still invokes the system's SSH binary with all its config (StrictHostKeyChecking, known_hosts, etc.)

This means `tailscale ssh` **does NOT bypass SSH server problems** — if the remote SSH server rejects connections, `tailscale ssh` fails too.

### SSH Troubleshooting Path (via Tailscale)

**Symptom: "Connection closed by port 22"**
The TCP connection reaches the remote port but the SSH server closes it immediately. This means:
- The SSH port is open and reachable ✓
- The SSH server is rejecting the connection ✗

**Diagnostic steps:**
1. On the target device, verify Remote Login is enabled: `sudo systemsetup -getremotelogin`
2. If off: `sudo systemsetup -setremotelogin on`
3. Check that the user is an allowed admin: `sudo grep leonardo /etc/ssh/sshd_config`
4. Check SSH logs: `sudo log show --predicate 'process == "sshd"' --last 5m`

**Symptom: "Permission denied (publickey,password,keyboard-interactive)"**
The TCP connection succeeds (port 22 reachable) but the SSH server rejects the authentication. This means the local machine's public key is not in the remote's `~/.ssh/authorized_keys`.

**Two fixes:**
1. **Quick / one-time** — add local pubkey to remote authorized_keys:
   ```bash
   ssh user@remote-ip 'cat >> ~/.ssh/authorized_keys' < ~/.ssh/id_ed25519.pub
   ```
2. **Enable Tailscale SSH** (no key management needed) — on the remote device:
   ```bash
   sudo tailscale set --ssh
   ```
   Then `tailscale ssh user@hostname` works without keys.

**Diagnostic on remote:**
```bash
# Verify the key is in authorized_keys
grep "$(cat ~/.ssh/id_ed25519.pub)" ~/.ssh/authorized_keys

# Check SSH logs for auth failure reason
sudo log show --predicate 'process == "sshd"' --last 5m
```

**Symptom: "Host key verification failed"**
Even `tailscale ssh` falls back to system SSH strict host checking. Workaround:
```bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null user@hostname
```
But if the server closes the connection after this, the problem is server-side (not the host key).

- SSH access requires the remote device to have an SSH server running
- Exit nodes require a device with sufficient bandwidth; free tier has limits
- Subnet router advertisement requires accepting the route on the admin console

## Hermes Gateway — Token Auth with Workspace

When `API_SERVER_KEY` is set in `~/.hermes/config.yaml` (under `platforms.api_server.secret`), the Hermes gateway requires a Bearer token on every `/v1/*` request. This affects two consumers:

**1. External clients (Atomic mobile app, etc.)**
```bash
curl https://mac-mini-de-leonardo.tail57f54b.ts.net/v1/models \
  -H "Authorization: Bearer <API_SERVER_KEY>"
```

**2. Hermes Workspace (Vite dev server on port 3000)**
The Workspace's `.env` must contain the matching token:
```
HERMES_API_TOKEN=<mesmo valor de API_SERVER_KEY>
HERMES_API_URL=http://127.0.0.1:8642
HERMES_DASHBOARD_URL=http://127.0.0.1:9119
```
Without it, `/api/gateway-status` returns HTML (Vite SPA fallback) instead of JSON — the UI renders but all backend calls silently fail. Debug: `curl -s http://localhost:3000/api/gateway-status` should return JSON, not HTML.

## Related Skills

| Skill | Relationship |
|-------|--------------|
| `maestri` | Maestro agent orchestration across tailnet devices |