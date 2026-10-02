---
name: self-hosted-apps
description: "Use when self-hosting an app via Docker Compose."
version: 1.0.0
author: Hermes Agent
license: MIT
category: devops
metadata:
  hermes:
    tags: [docker, compose, self-host, apps]
    related_skills: [devops]
---

# Self-hosted apps (Docker on this Mac)

Install third-party self-hosted tools the same way: official Compose, isolated folder under `~/Apps`, ports bound to loopback, secrets out of the YAML.

## When to use

- User says "instalar o X" and X is a self-hosted product (Penpot, Plausible, etc.)
- Need to start/stop/upgrade an existing stack in `~/Apps/`
- Distinguish **desktop client** vs **self-host** (ask only if the two paths are truly different)

## Default layout

```
~/Apps/<app>/
  docker-compose.yaml   # official file, small local edits only
  .env                  # secrets + pinned version (gitignored)
  .gitignore
  README.md             # start/stop + URLs
```

Other production apps already occupy **5051–5055**. Pick a free port; never reuse those.

Bind published ports to loopback:

```yaml
ports:
  - "127.0.0.1:9001:8080"
```

Generate secrets; never leave vendor placeholders:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

## Sequence

1. `df -h /System/Volumes/Data` — these stacks are multi-GB. If free space is under ~8 GB, free cache (`brew cleanup -s`) **before** pull.
2. Confirm Docker is up: `docker info`.
3. Confirm the target port is free: `lsof -nP -iTCP:<port> -sTCP:LISTEN`.
4. Download the **official** compose file (do not invent a stack).
5. Pin the image tag in `.env` (`FOO_VERSION=…`). Replace hardcoded insecure keys with `${FOO_SECRET_KEY}`.
6. Pull, then `docker compose -p <app> --env-file .env up -d --pull never`.
7. Verify with curl (HTTP 200 + expected title/API), not just `ps`.
8. Registration: leave it on for first-run local tools unless the user asked for invite-only.

## Docker pull when `credsStore: desktop` hangs

Public Hub pulls can stall with `error getting credentials`. Isolated config (no compose plugin):

```bash
mkdir -p /tmp/docker-nopass
printf '%s\n' '{"auths":{}}' > /tmp/docker-nopass/config.json
DOCKER_CONFIG=/tmp/docker-nopass docker pull <image>:<tag>
```

Pull images one-by-one that way, then `unset DOCKER_CONFIG` (or `export DOCKER_CONFIG="$HOME/.docker"`) before `docker compose` — a temp `DOCKER_CONFIG` **hides** the compose CLI plugin (`unknown shorthand flag: 'p'`).

Do **not** `docker image prune` after a pull: unused-looking images are the ones you just fetched.

## Docker Desktop died after disk pressure

Engine error `Docker Desktop is unable to start` / `no space left on device` in backend logs:

1. Free host space first (Homebrew cache is safe).
2. Hard-restart: `killall -9 "Docker Desktop" Docker com.docker.backend` then `open -a Docker`.
3. Wait until `docker info` works, then `up` again.

`Docker.raw` listed size is often sparse (`ls -lh` vs `du -h`).

## Pitfalls

- `hdiutil attach` on a licensed DMG prints the whole SLA and waits; `printf 'Y\n' | hdiutil attach -nobrowse -readonly -noverify file.dmg`.
- A `depends_on` service that crash-loops can take down nginx frontends (`host not found in upstream`). Scale that service to 0 **and** drop the flag that injects its location block.
- Inspect a crash-loop binary before blaming arch: `docker image inspect` can say `arm64` while the payload is a 0-byte file (`exec format error`).

## References

- `references/penpot.md` — Penpot Desktop + self-host on this machine
