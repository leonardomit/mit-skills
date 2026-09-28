# Supply Chain Attack Verification — Shai-Hulud (2026-05-12)

**Attack:** Mini Shai-Hulud — 84 malicious @tanstack packages published 2026-05-11. Worm persists in `~/.claude/settings.json`, `~/.claude/setup.mjs`, installs `gh-token-monitor` daemon via LaunchAgent/systemd.

## Verification Results — mac-mini-de-leonardo (2026-05-12)

All checks: CLEAN ✅

| Check | File/Path | Result |
|-------|-----------|--------|
| Worm persistence file | `~/.claude/setup.mjs` | ✅ Not present |
| Worm persistence file | `~/.claude/settings.json` | ✅ Not present |
| Worm daemon (macOS) | `~/Library/LaunchAgents/com.gh-token-monitor.plist` | ✅ Not present |
| Worm daemon (Linux) | `systemctl list-units --all` (gh-token-monitor) | ✅ Not present |
| npm global packages | `npm list -g --depth=0` | ✅ Clean |
| TanStack packages | `@tanstack/*` in node_modules | ✅ Not installed |
| Malicious SDKs | `mistralai`, `guardrails-ai` | ✅ Not installed |
| Git hooks | `git config --global --list` | ✅ Clean |
| DNS blocklist | `/etc/hosts` (git-tanstack.com, *.getsession.org) | ✅ Not blocked (clean) |
| Crontab | `crontab -l` | ✅ Clean |
| MiroFish backend | `~/MiroFish/package-lock.json` | ✅ Clean |
| MiroFish frontend | `~/MiroFish/frontend/package-lock.json` | ✅ Clean |
| ComfyUI | `~/Documents/comfy/package-lock.json` | ✅ Clean |
| Homebrew | `brew list` | ✅ Clean |

## Recommended Ongoing Check

For any Node.js project:
```bash
grep -r "tanstack\|mistralai\|guardrails" ~/ --include="package-lock.json"
```

## If Infection Suspected

1. **Do NOT revoke tokens yet** — isolate machine first
2. Check for `mistralai==2.4.6` or `guardrails-ai==0.10.1` in lockfiles
3. Block domains: `git-tanstack.com`, `*.getsession.org`
4. Rotate all credentials: GitHub token, cloud keys, npm tokens, SSH keys
5. Safe TanStack packages (not affected): `@tanstack/query*`, `@tanstack/table*`, `@tanstack/form*`, `@tanstack/virtual*`, `@tanstack/store`