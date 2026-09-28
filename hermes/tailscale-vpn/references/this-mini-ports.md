# This Mini — Tailscale serve / Funnel

Hostname: `mac-mini-de-leonardo.tail57f54b.ts.net`

## Public Funnel ports

Only **443, 8443, 10000**. `funnel --https=8085` looks on (even `curl` from the Mini) but a PC **without Tailscale cannot open it**.

Nextcloud public: `https://mac-mini-de-leonardo.tail57f54b.ts.net:8443` → `http://127.0.0.1:8085`.

Do not Funnel empresa 5051–5055.

## Tailnet serve (not Funnel)

Match **app ports**, not 805x:

| App | Local | Serve HTTPS |
|---|---|---|
| relatorio-a | 5053 | `:443` and `:5053` |
| Lotes v2 | 5051 | `:5051` |
| OPs | 5052 | `:5052` |
| Rótulo fácil | 5054 | `:5054` |
| CRM | 5055 | `:5055` |
| Nextcloud | 127.0.0.1:8085 | Funnel `:8443` only |

`tailscale serve --https=N off` or `funnel --https=N off` can **drop sibling mappings**. Restore 5051–5055 after any off.

Do not `funnel reset` on this Mini without putting those back.

Offline flaps (SSH / painéis / Claude / Orca): sono do Mini, não Tailscale. See `references/mini-keepawake.md`. Prefer Ethernet `en0`; Wi‑Fi 5 GHz SSID **Starlink** (not `Starlink 2,4 GHz`).
