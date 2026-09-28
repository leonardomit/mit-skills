# Nextcloud on this Mac

Not running until the user asks to `up`. Compose-only is the default when they say **montar / sem subir**.

## Layout

- Stack: `~/Apps/nextcloud/` (`docker-compose.yaml`, `.env` mode 600, `.gitignore`, `README.md`)
- Official pattern: nextcloud/docker `.examples/docker-compose/insecure/postgres/apache` (app + db + redis + cron)
- Data bind mounts (keep out of `Docker.raw`):
  - `/Volumes/Trabalho/Nextcloud/html` → `/var/www/html`
  - `/Volumes/Trabalho/Nextcloud/db` → `/var/lib/postgresql`
- Images pinned in `.env`: `NEXTCLOUD_VERSION=31-apache`, `POSTGRES_VERSION=16-alpine`, `REDIS_VERSION=7-alpine`
- Port: `127.0.0.1:8085:80` (5051–5055 and 5070 are empresa; 9001 is Penpot)
- Admin: `NEXTCLOUD_ADMIN_*` in `.env`. Trusted domains include Tailscale hostname.
- `restart: unless-stopped` so it does not appear until the first `up`.

## Do not

- Snap / PHP tarball / native Apache on macOS
- Nextcloud AIO (wants 80/443; fights Docker Desktop on this Mini)
- Desktop client as a substitute for the server
- Funnel / public 80/443
- `docker compose up` when they only asked to montar

## When they ask to start

```bash
cd ~/Apps/nextcloud
docker compose -p nextcloud --env-file .env pull
docker compose -p nextcloud --env-file .env up -d --pull never
# http://127.0.0.1:8085
```

Validate without starting: `docker compose -p nextcloud --env-file .env config --quiet`.
